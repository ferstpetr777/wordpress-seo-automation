#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для добавления группы ключевых слов в базу данных BizFin Pro
"""

import os
import sys
import mysql.connector
from mysql.connector import Error
import logging
from datetime import datetime

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

def add_keywords_group():
    """Добавление группы ключевых слов"""
    logger = setup_logging()
    
    # Список ключевых слов из группы "Группа ключей часть 1"
    keywords_list = [
        "банковская гарантия это простыми словами",
        "суть банковской гарантии",
        "независимая банковская гарантия",
        "виды банковских гарантий",
        "банковская гарантия является",
        "поручительство и банковская гарантия",
        "стоимость банковской гарантии",
        "калькулятор банковской гарантии",
        "сколько стоит банковская гарантия",
        "процент банковской гарантии",
        "оплата банковской гарантии",
        "срок банковской гарантии",
        "срок действия банковской гарантии",
        "оформление банковской гарантии",
        "действие банковской гарантии",
        "срок банковской гарантии по 44 фз",
        "обеспечение банковской гарантии",
        "залог банковская гарантия",
        "обеспечение обязательства банковская гарантия",
        "требования к банковской гарантии",
        "обеспечение исполнения обязательства банковской гарантией",
        "банковская гарантия по 44 фз",
        "банковская гарантия по 223 фз",
        "банковская гарантия на исполнение контракта",
        "банковская гарантия на гарантийные обязательства",
        "банковская гарантия на обеспечение заявки",
        "авансовая банковская гарантия",
        "как проверить банковскую гарантию",
        "реестр банковских гарантий",
        "реестр банковских гарантий по 44 фз",
        "официальный сайт банковских гарантий",
        "проверка банковской гарантии",
        "риски банковской гарантии",
        "возврат банковской гарантии",
        "взыскание банковской гарантии",
        "расторжение банковской гарантии",
        "отказ в банковской гарантии",
        "банки выдающие банковские гарантии по 44 фз",
        "альфа банк банковская гарантия",
        "банковская гарантия сбербанк",
        "совкомбанк банковская гарантия",
        "банки минфин по банковским гарантиям",
        "оформить банковскую гарантию",
        "банковская гарантия онлайн",
        "заявка на банковскую гарантию",
        "получение банковской гарантии",
        "выдача банковских гарантий",
        "банковская гарантия москва",
        "банковская гарантия для поставки товаров",
        "банковская гарантия для строительных работ"
    ]
    
    try:
        # Подключаемся к базе данных
        config = DatabaseConfig.get_config_dict()
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        logger.info(f"📝 Начинаем добавление группы ключевых слов...")
        logger.info(f"📊 Количество ключевых слов: {len(keywords_list)}")
        
        # Получаем текущий максимальный ID для определения группы
        cursor.execute("SELECT MAX(id) FROM keywords")
        max_id_result = cursor.fetchone()
        max_id = max_id_result[0] if max_id_result[0] else 0
        
        group_start_id = max_id + 1
        
        # Добавляем каждый ключевик
        added_keywords = []
        for i, keyword in enumerate(keywords_list, 1):
            try:
                # Проверяем, не существует ли уже такой ключевик
                cursor.execute("SELECT id FROM keywords WHERE keyword = %s", (keyword,))
                existing = cursor.fetchone()
                
                if existing:
                    logger.warning(f"⚠️ Ключевик уже существует: {keyword} (ID: {existing[0]})")
                    added_keywords.append({
                        'id': existing[0],
                        'keyword': keyword,
                        'status': 'existing'
                    })
                    continue
                
                # Определяем приоритет на основе позиции в списке
                if i <= 10:
                    priority = 'high'
                elif i <= 25:
                    priority = 'medium'
                else:
                    priority = 'low'
                
                # Определяем тип контента
                if any(word in keyword.lower() for word in ['что', 'как', 'почему', 'зачем']):
                    target_intent = 'informational'
                elif any(word in keyword.lower() for word in ['оформить', 'получить', 'заявка', 'стоимость', 'цена']):
                    target_intent = 'commercial'
                elif any(word in keyword.lower() for word in ['виды', 'типы', 'сравнение']):
                    target_intent = 'educational'
                else:
                    target_intent = 'informational'
                
                # Вставляем ключевик
                insert_query = """
                INSERT INTO keywords (
                    keyword, status, source, frequency, user_id, priority, 
                    target_volume, target_intent, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """
                
                now = datetime.now()
                values = (
                    keyword,
                    'pending',
                    'manual_group',
                    1,
                    1,
                    priority,
                    2500,
                    target_intent,
                    now,
                    now
                )
                
                cursor.execute(insert_query, values)
                keyword_id = cursor.lastrowid
                
                added_keywords.append({
                    'id': keyword_id,
                    'keyword': keyword,
                    'status': 'added',
                    'priority': priority,
                    'intent': target_intent
                })
                
                logger.info(f"✅ {i:2d}/50 - Добавлен: {keyword} (ID: {keyword_id}, Приоритет: {priority})")
                
            except Error as e:
                logger.error(f"❌ Ошибка добавления ключевика '{keyword}': {e}")
                continue
        
        # Сохраняем изменения
        connection.commit()
        
        # Получаем статистику
        cursor.execute("SELECT COUNT(*) FROM keywords WHERE source = 'manual_group'")
        total_group_keywords = cursor.fetchone()[0]
        
        cursor.execute("SELECT MIN(id), MAX(id) FROM keywords WHERE source = 'manual_group'")
        id_range = cursor.fetchone()
        
        logger.info(f"\n📊 СТАТИСТИКА ДОБАВЛЕНИЯ:")
        logger.info(f"   📝 Всего ключевиков в группе: {total_group_keywords}")
        logger.info(f"   🆔 Диапазон ID: {id_range[0]} - {id_range[1]}")
        logger.info(f"   ✅ Успешно добавлено: {len([k for k in added_keywords if k['status'] == 'added'])}")
        logger.info(f"   ⚠️ Уже существовало: {len([k for k in added_keywords if k['status'] == 'existing'])}")
        
        # Возвращаем информацию о группе
        group_info = {
            'group_name': 'Группа ключей часть 1',
            'total_keywords': len(keywords_list),
            'added_keywords': len([k for k in added_keywords if k['status'] == 'added']),
            'existing_keywords': len([k for k in added_keywords if k['status'] == 'existing']),
            'first_id': id_range[0],
            'last_id': id_range[1],
            'source': 'manual_group',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        cursor.close()
        connection.close()
        
        return group_info
        
    except Error as e:
        logger.error(f"❌ Ошибка подключения к базе данных: {e}")
        return None

def main():
    """Основная функция"""
    logger = setup_logging()
    
    print("🚀 Добавление группы ключевых слов в BizFin Pro")
    print("=" * 60)
    
    # Добавляем группу ключевых слов
    group_info = add_keywords_group()
    
    if group_info:
        print("\n" + "=" * 60)
        print("🎉 ГРУППА КЛЮЧЕВЫХ СЛОВ ДОБАВЛЕНА УСПЕШНО!")
        print("=" * 60)
        print(f"📋 Название группы: {group_info['group_name']}")
        print(f"📊 Всего ключевиков: {group_info['total_keywords']}")
        print(f"✅ Добавлено новых: {group_info['added_keywords']}")
        print(f"⚠️ Уже существовало: {group_info['existing_keywords']}")
        print(f"🆔 Диапазон ID: {group_info['first_id']} - {group_info['last_id']}")
        print(f"📅 Дата создания: {group_info['created_at']}")
        print(f"🏷️ Источник: {group_info['source']}")
        print("\n🎯 НОМЕР ГРУППЫ В БАЗЕ ДАННЫХ:")
        print(f"   Первый ID группы: {group_info['first_id']}")
        print(f"   Последний ID группы: {group_info['last_id']}")
        print("=" * 60)
        
        # Возвращаем номер группы для пользователя
        return group_info['first_id']
    else:
        logger.error("❌ Не удалось добавить группу ключевых слов")
        return None

if __name__ == "__main__":
    group_id = main()
    if group_id:
        print(f"\n🎯 НОМЕР ГРУППЫ В БАЗЕ ДАННЫХ: {group_id}")
    else:
        print("\n❌ Ошибка добавления группы")

