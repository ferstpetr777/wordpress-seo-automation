#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для обновления инструкции web_research_standard_2025 в базе данных
"""

import os
import sys
import sqlite3
import json
import logging
from datetime import datetime

# Добавляем путь к модулям проекта
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def setup_logging():
    """Настройка логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def update_instruction_in_db():
    """Обновление инструкции в базе данных"""
    logger = setup_logging()
    
    try:
        # Путь к базе данных SQLite
        db_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'bizfin_pro.db')
        
        # Подключаемся к базе данных
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        logger.info(f"🗄️ Подключение к базе данных: {db_path}")
        
        # Создаем таблицу для инструкций, если её нет
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS research_instructions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                instruction_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                version TEXT NOT NULL,
                instruction_data TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Читаем обновленную инструкцию из JSON файла
        json_file_path = os.path.join(os.path.dirname(__file__), '..', 'web_research_instruction_standard.json')
        
        if not os.path.exists(json_file_path):
            logger.error(f"❌ Файл инструкции не найден: {json_file_path}")
            return False
        
        with open(json_file_path, 'r', encoding='utf-8') as f:
            instruction_data = json.load(f)
        
        # Обновляем версию
        instruction_data['version'] = '1.1'
        instruction_data['updated_at'] = datetime.now().isoformat()
        
        logger.info(f"📝 Загружена инструкция: {instruction_data['title']}")
        logger.info(f"🆔 ID: {instruction_data['id']}")
        logger.info(f"📊 Версия: {instruction_data['version']}")
        
        # Проверяем количество вторичных поисков
        secondary_searches = instruction_data.get('web_search_strategy', {}).get('secondary_searches', [])
        logger.info(f"🔍 Количество вторичных поисков: {len(secondary_searches)}")
        
        for i, search in enumerate(secondary_searches, 1):
            logger.info(f"   {i}. {search['query']} - {search['purpose']}")
        
        # Сохраняем или обновляем инструкцию в БД
        insert_query = '''
            INSERT OR REPLACE INTO research_instructions 
            (instruction_id, title, version, instruction_data, updated_at)
            VALUES (?, ?, ?, ?, ?)
        '''
        
        values = (
            instruction_data["id"],
            instruction_data["title"],
            instruction_data["version"],
            json.dumps(instruction_data, ensure_ascii=False),
            datetime.now().isoformat()
        )
        
        cursor.execute(insert_query, values)
        instruction_db_id = cursor.lastrowid
        
        connection.commit()
        
        # Проверяем, что инструкция сохранена
        cursor.execute("SELECT id, instruction_id, version FROM research_instructions WHERE instruction_id = ?", 
                      (instruction_data["id"],))
        result = cursor.fetchone()
        
        if result:
            logger.info(f"✅ Инструкция успешно обновлена в БД:")
            logger.info(f"   🆔 ID в БД: {result[0]}")
            logger.info(f"   📋 Instruction ID: {result[1]}")
            logger.info(f"   📊 Версия: {result[2]}")
        else:
            logger.error("❌ Инструкция не найдена в БД после сохранения")
            return False
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка обновления инструкции: {e}")
        if 'connection' in locals():
            connection.rollback()
            connection.close()
        return False

def main():
    """Основная функция"""
    logger = setup_logging()
    
    print("🚀 Обновление инструкции web_research_standard_2025")
    print("=" * 60)
    
    if update_instruction_in_db():
        print("\n" + "=" * 60)
        print("🎉 ИНСТРУКЦИЯ УСПЕШНО ОБНОВЛЕНА!")
        print("=" * 60)
        print("✅ Количество вторичных поисков изменено с 4 на 3")
        print("✅ Убрана инструкция поиска по site:{brand_domain}")
        print("✅ Версия обновлена до 1.1")
        print("✅ Инструкция сохранена в базе данных")
        print("\n🔍 ТЕКУЩИЕ ПОИСКОВЫЕ ЗАПРОСЫ:")
        print("   1. {keyword} условия тарифы")
        print("   2. {keyword} документы требования") 
        print("   3. {keyword} калькулятор стоимость {year}")
        print("=" * 60)
    else:
        print("\n❌ Ошибка обновления инструкции")

if __name__ == "__main__":
    main()

