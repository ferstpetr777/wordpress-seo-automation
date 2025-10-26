#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт инициализации базы данных для BizFin Pro SEO Pipeline
"""

import os
import sys
import mysql.connector
from mysql.connector import Error
import logging

# Добавляем путь к модулям проекта
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.database import DatabaseConfig

def setup_logging():
    """Настройка логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def create_database():
    """Создание базы данных"""
    logger = setup_logging()
    
    try:
        # Подключаемся к MySQL без указания базы данных
        config = DatabaseConfig.get_config_dict()
        config.pop('database')  # Убираем database из конфигурации
        
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Создаем базу данных
        database_name = DatabaseConfig.DATABASE
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        logger.info(f"✅ База данных '{database_name}' создана или уже существует")
        
        # Создаем пользователя
        username = DatabaseConfig.USER
        password = DatabaseConfig.PASSWORD
        
        try:
            cursor.execute(f"CREATE USER IF NOT EXISTS '{username}'@'localhost' IDENTIFIED BY '{password}'")
            logger.info(f"✅ Пользователь '{username}' создан или уже существует")
        except Error as e:
            logger.warning(f"⚠️ Не удалось создать пользователя: {e}")
        
        # Предоставляем права
        try:
            cursor.execute(f"GRANT ALL PRIVILEGES ON {database_name}.* TO '{username}'@'localhost'")
            cursor.execute("FLUSH PRIVILEGES")
            logger.info(f"✅ Права предоставлены пользователю '{username}'")
        except Error as e:
            logger.warning(f"⚠️ Не удалось предоставить права: {e}")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return True
        
    except Error as e:
        logger.error(f"❌ Ошибка создания базы данных: {e}")
        return False

def create_tables():
    """Создание таблиц"""
    logger = setup_logging()
    
    try:
        # Подключаемся к базе данных
        config = DatabaseConfig.get_config_dict()
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Читаем схему из файла
        schema_file = os.path.join(os.path.dirname(__file__), '..', 'db', 'schema.sql')
        
        if not os.path.exists(schema_file):
            logger.error(f"❌ Файл схемы не найден: {schema_file}")
            return False
        
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Выполняем SQL команды
        # Разделяем по ';' и выполняем каждую команду отдельно
        commands = [cmd.strip() for cmd in schema_sql.split(';') if cmd.strip()]
        
        for i, command in enumerate(commands):
            if command.upper().startswith('CREATE DATABASE') or command.upper().startswith('USE '):
                continue  # Пропускаем команды создания БД и USE
            
            try:
                cursor.execute(command)
                logger.info(f"✅ Команда {i+1}/{len(commands)} выполнена успешно")
            except Error as e:
                logger.warning(f"⚠️ Ошибка выполнения команды {i+1}: {e}")
                continue
        
        connection.commit()
        cursor.close()
        connection.close()
        
        logger.info("✅ Все таблицы созданы успешно")
        return True
        
    except Error as e:
        logger.error(f"❌ Ошибка создания таблиц: {e}")
        return False

def verify_database():
    """Проверка базы данных"""
    logger = setup_logging()
    
    try:
        config = DatabaseConfig.get_config_dict()
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Проверяем количество таблиц
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        logger.info(f"✅ База данных содержит {len(tables)} таблиц:")
        for table in tables:
            logger.info(f"   - {table[0]}")
        
        # Проверяем основные таблицы
        required_tables = [
            'keywords', 'analysis', 'articles', 'seo_checks', 
            'articles_final', 'publish_queue', 'published', 
            'publish_status', 'templates', 'company_cards'
        ]
        
        existing_tables = [table[0] for table in tables]
        missing_tables = [table for table in required_tables if table not in existing_tables]
        
        if missing_tables:
            logger.warning(f"⚠️ Отсутствуют таблицы: {missing_tables}")
        else:
            logger.info("✅ Все основные таблицы присутствуют")
        
        # Проверяем начальные данные
        cursor.execute("SELECT COUNT(*) FROM company_cards")
        company_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM templates")
        template_count = cursor.fetchone()[0]
        
        logger.info(f"✅ Начальные данные: {company_count} компаний, {template_count} шаблонов")
        
        cursor.close()
        connection.close()
        
        return len(missing_tables) == 0
        
    except Error as e:
        logger.error(f"❌ Ошибка проверки базы данных: {e}")
        return False

def main():
    """Основная функция"""
    logger = setup_logging()
    
    print("🚀 Инициализация базы данных BizFin Pro SEO Pipeline")
    print("=" * 60)
    
    # Создаем базу данных
    logger.info("📊 Создание базы данных...")
    if not create_database():
        logger.error("❌ Не удалось создать базу данных")
        sys.exit(1)
    
    # Создаем таблицы
    logger.info("📋 Создание таблиц...")
    if not create_tables():
        logger.error("❌ Не удалось создать таблицы")
        sys.exit(1)
    
    # Проверяем результат
    logger.info("🔍 Проверка базы данных...")
    if not verify_database():
        logger.error("❌ База данных не прошла проверку")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 ИНИЦИАЛИЗАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
    print("=" * 60)
    print("✅ База данных создана")
    print("✅ Таблицы созданы")
    print("✅ Начальные данные загружены")
    print("✅ Проверка пройдена")
    print("\n🚀 Готово к запуску пайплайна v2!")

if __name__ == "__main__":
    main()


