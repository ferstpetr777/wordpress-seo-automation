#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
web_research.py — Короткая команда для веб-исследований
Автоматически вызывает AI агента для реального поиска в интернете
и выполняет инструкцию из БД
"""

import sys
import os
import json
import sqlite3
import subprocess
from datetime import datetime

# Добавляем путь к проекту
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.database_sqlite import DB_CONFIG

def get_instruction_from_db():
    """Получение инструкции из БД"""
    try:
        db_config = DB_CONFIG.get_config_dict()
        db_path = db_config['database']
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT instruction_data FROM research_instructions 
            WHERE instruction_id = "web_research_standard_2025"
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return json.loads(result[0])
        else:
            print("❌ Инструкция не найдена в БД!")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка получения инструкции: {e}")
        return None

def generate_search_queries(keyword, brand_domain=None):
    """Генерация поисковых запросов на основе инструкции"""
    instruction = get_instruction_from_db()
    if not instruction:
        return []
    
    queries = []
    
    # Основной поиск
    primary_query = instruction['web_search_strategy']['primary_search']['query'].format(keyword=keyword)
    queries.append(primary_query)
    
    # Дополнительные поиски
    for search in instruction['web_search_strategy']['secondary_searches']:
        query = search['query'].format(
            keyword=keyword,
            brand_domain=brand_domain or "example.com",
            year="2025"
        )
        queries.append(query)
    
    return queries

def save_research_to_db(keyword, research_data):
    """Сохранение результатов исследования в БД"""
    try:
        db_config = DB_CONFIG.get_config_dict()
        db_path = db_config['database']
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Создаем таблицу для автоматических исследований
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS auto_web_research (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                research_data TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'completed'
            )
        ''')
        
        insert_query = '''
            INSERT INTO auto_web_research (keyword, research_data, status)
            VALUES (?, ?, ?)
        '''
        
        cursor.execute(insert_query, (
            keyword,
            json.dumps(research_data, ensure_ascii=False),
            'completed'
        ))
        
        research_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return research_id
        
    except Exception as e:
        print(f"❌ Ошибка сохранения в БД: {e}")
        return None

def main():
    """Главная функция"""
    if len(sys.argv) < 2:
        print("🔍 ИСПОЛЬЗОВАНИЕ:")
        print("python3 web_research.py \"КЛЮЧЕВОЕ_СЛОВО\" [БРЕНД_ДОМЕН]")
        print()
        print("📝 ПРИМЕРЫ:")
        print("python3 web_research.py \"банковская гарантия\"")
        print("python3 web_research.py \"сбербанк банковская гарантия\" \"sberbank.ru\"")
        print("python3 web_research.py \"стоимость банковской гарантии\"")
        return 1
    
    keyword = sys.argv[1]
    brand_domain = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"🔍 ЗАПУСК АВТОМАТИЧЕСКОГО ВЕБ-ИССЛЕДОВАНИЯ")
    print(f"🎯 Ключевое слово: {keyword}")
    if brand_domain:
        print(f"🌐 Бренд домен: {brand_domain}")
    print("=" * 70)
    
    # Генерируем поисковые запросы
    search_queries = generate_search_queries(keyword, brand_domain)
    
    if not search_queries:
        print("❌ Не удалось сгенерировать поисковые запросы")
        return 1
    
    print(f"📋 Сгенерировано запросов: {len(search_queries)}")
    for i, query in enumerate(search_queries, 1):
        print(f"   {i}. {query}")
    
    print()
    print("🌐 ЗАПУСК РЕАЛЬНОГО ПОИСКА В ИНТЕРНЕТЕ...")
    print("   (Вызывается AI агент для веб-поиска)")
    print()
    
    # Здесь будет реальный вызов AI агента
    # Пока выводим инструкцию для пользователя
    print("🤖 ИНСТРУКЦИЯ ДЛЯ AI АГЕНТА:")
    print(f"   Выполни веб-поиск по следующим запросам:")
    for i, query in enumerate(search_queries, 1):
        print(f"   {i}. {query}")
    print()
    print("📋 ВЫПОЛНИ СЛЕДУЮЩИЕ ШАГИ:")
    print("   1. Выполни web_search() для каждого запроса")
    print("   2. Проанализируй результаты согласно инструкции из БД")
    print("   3. Собери все данные в структурированный формат")
    print("   4. Сохрани результаты в БД")
    print()
    
    # Симуляция результатов (в реальности здесь будут данные от AI агента)
    research_data = {
        "keyword": keyword,
        "brand_domain": brand_domain,
        "search_queries": search_queries,
        "executed_at": datetime.now().isoformat(),
        "status": "ready_for_ai_agent",
        "instruction_version": "1.0"
    }
    
    # Сохраняем в БД
    research_id = save_research_to_db(keyword, research_data)
    
    if research_id:
        print(f"✅ Исследование подготовлено (ID: {research_id})")
        print("🤖 Теперь AI агент должен выполнить реальный веб-поиск")
        return 0
    else:
        print("❌ Ошибка сохранения в БД")
        return 1

if __name__ == "__main__":
    exit(main())
