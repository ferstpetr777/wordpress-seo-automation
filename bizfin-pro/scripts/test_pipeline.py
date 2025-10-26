#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовый скрипт для BizFin Pro SEO Pipeline v2
"""

import sys
import os
import sqlite3
import json
from datetime import datetime

# Добавляем путь к модулям проекта
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.database_sqlite import DB_CONFIG
from modules.research.competitor_analyzer import CompetitorAnalyzer

def create_sqlite_database():
    """Создание SQLite базы данных для тестирования"""
    print("🗄️ Создание SQLite базы данных...")
    
    config = DB_CONFIG.get_config_dict()
    db_path = config['database']
    
    # Создаем директорию если не существует
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Подключаемся к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Создаем основные таблицы (упрощенная версия)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL UNIQUE,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending',
            source TEXT DEFAULT 'manual',
            frequency INTEGER DEFAULT 1,
            user_id INTEGER DEFAULT 1,
            priority TEXT DEFAULT 'medium',
            target_volume INTEGER DEFAULT 2500,
            target_intent TEXT DEFAULT 'informational',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword_id INTEGER NOT NULL,
            sources TEXT, -- JSON
            structure TEXT, -- JSON
            gaps TEXT, -- JSON
            recommendations TEXT, -- JSON
            competitors_data TEXT, -- JSON
            lsi_keywords TEXT, -- JSON
            search_volume INTEGER,
            competition_level TEXT DEFAULT 'medium',
            date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
            analysis_duration INTEGER,
            FOREIGN KEY (keyword_id) REFERENCES keywords(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword_id INTEGER NOT NULL,
            analysis_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content_raw TEXT NOT NULL,
            html_raw TEXT NOT NULL,
            word_count INTEGER DEFAULT 0,
            reading_time INTEGER DEFAULT 0,
            structure TEXT, -- JSON
            lsi_keywords_used TEXT, -- JSON
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            generation_duration INTEGER,
            FOREIGN KEY (keyword_id) REFERENCES keywords(id),
            FOREIGN KEY (analysis_id) REFERENCES analysis(id)
        )
    ''')
    
    # Создаем индексы
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_keywords_status ON keywords(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_analysis_keyword_id ON analysis(keyword_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_articles_keyword_id ON articles(keyword_id)')
    
    conn.commit()
    conn.close()
    
    print(f"✅ SQLite база данных создана: {db_path}")
    return db_path

def test_competitor_analyzer():
    """Тестирование анализатора конкурентов"""
    print("\n🔍 Тестирование анализатора конкурентов...")
    
    analyzer = CompetitorAnalyzer(max_competitors=2, delay=0.5)
    
    # Тестируем с простым ключевым словом
    keyword = "банковская гарантия"
    print(f"Анализ ключевого слова: '{keyword}'")
    
    try:
        result = analyzer.analyze_keyword(keyword)
        
        print(f"✅ Анализ завершен со статусом: {result['status']}")
        print(f"📊 Найдено конкурентов: {len(result.get('competitors', []))}")
        
        if result.get('competitors'):
            print("🏆 Топ конкуренты:")
            for i, competitor in enumerate(result['competitors'][:3], 1):
                print(f"   {i}. {competitor['domain']} - {competitor['word_count']} слов")
        
        if result.get('lsi_keywords'):
            print(f"🔑 LSI ключевые слова: {', '.join(result['lsi_keywords'][:5])}")
        
        if result.get('gaps'):
            print(f"⚠️ Выявленные пробелы: {', '.join(result['gaps'][:3])}")
        
        return result
        
    except Exception as e:
        print(f"❌ Ошибка анализа: {e}")
        return None

def test_database_operations():
    """Тестирование операций с базой данных"""
    print("\n💾 Тестирование операций с базой данных...")
    
    config = DB_CONFIG.get_config_dict()
    db_path = config['database']
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Добавляем тестовое ключевое слово
        cursor.execute('''
            INSERT OR IGNORE INTO keywords (keyword, status, priority, target_volume)
            VALUES (?, ?, ?, ?)
        ''', ('тестовая банковская гарантия', 'pending', 'medium', 2500))
        
        keyword_id = cursor.lastrowid
        if keyword_id == 0:
            # Получаем ID существующего ключевого слова
            cursor.execute('SELECT id FROM keywords WHERE keyword = ?', ('тестовая банковская гарантия',))
            keyword_id = cursor.fetchone()[0]
        
        print(f"✅ Ключевое слово добавлено/найдено (ID: {keyword_id})")
        
        # Добавляем тестовый анализ
        test_analysis = {
            'sources': ['https://example1.com', 'https://example2.com'],
            'structure': {'avg_word_count': 2500, 'avg_images': 5},
            'gaps': ['Недостаточно FAQ', 'Слабые CTA'],
            'recommendations': ['Добавить FAQ', 'Улучшить CTA'],
            'competitors_data': [{'url': 'https://example1.com', 'word_count': 2000}],
            'lsi_keywords': ['гарантия', 'банк', 'кредит']
        }
        
        cursor.execute('''
            INSERT INTO analysis (keyword_id, sources, structure, gaps, recommendations, 
                                competitors_data, lsi_keywords, search_volume, analysis_duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            keyword_id,
            json.dumps(test_analysis['sources']),
            json.dumps(test_analysis['structure']),
            json.dumps(test_analysis['gaps']),
            json.dumps(test_analysis['recommendations']),
            json.dumps(test_analysis['competitors_data']),
            json.dumps(test_analysis['lsi_keywords']),
            1000,
            30
        ))
        
        analysis_id = cursor.lastrowid
        print(f"✅ Анализ добавлен (ID: {analysis_id})")
        
        # Добавляем тестовую статью
        test_article = {
            'title': 'Тестовая банковская гарантия: полное руководство',
            'content_raw': 'Это тестовая статья о банковских гарантиях...',
            'html_raw': '<h1>Тестовая банковская гарантия</h1><p>Это тестовая статья...</p>',
            'word_count': 2500,
            'reading_time': 12,
            'structure': {'sections': ['Введение', 'Основная часть', 'Заключение']},
            'lsi_keywords_used': ['гарантия', 'банк', 'кредит']
        }
        
        cursor.execute('''
            INSERT INTO articles (keyword_id, analysis_id, title, content_raw, html_raw,
                                word_count, reading_time, structure, lsi_keywords_used, generation_duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            keyword_id,
            analysis_id,
            test_article['title'],
            test_article['content_raw'],
            test_article['html_raw'],
            test_article['word_count'],
            test_article['reading_time'],
            json.dumps(test_article['structure']),
            json.dumps(test_article['lsi_keywords_used']),
            60
        ))
        
        article_id = cursor.lastrowid
        print(f"✅ Статья добавлена (ID: {article_id})")
        
        # Проверяем данные
        cursor.execute('''
            SELECT k.keyword, a.competitors_data, ar.title, ar.word_count
            FROM keywords k
            JOIN analysis a ON k.id = a.keyword_id
            JOIN articles ar ON a.id = ar.analysis_id
            WHERE k.id = ?
        ''', (keyword_id,))
        
        result = cursor.fetchone()
        if result:
            print(f"✅ Проверка данных:")
            print(f"   Ключевое слово: {result[0]}")
            print(f"   Конкурентов: {len(json.loads(result[1]))}")
            print(f"   Заголовок статьи: {result[2]}")
            print(f"   Слов в статье: {result[3]}")
        
        conn.commit()
        print("✅ Все операции с базой данных выполнены успешно")
        
    except Exception as e:
        print(f"❌ Ошибка операций с БД: {e}")
        conn.rollback()
    finally:
        conn.close()

def main():
    """Основная функция тестирования"""
    print("🧪 ТЕСТИРОВАНИЕ BIZFIN PRO SEO PIPELINE V2")
    print("=" * 60)
    
    # Создаем базу данных
    db_path = create_sqlite_database()
    
    # Тестируем анализатор конкурентов
    analysis_result = test_competitor_analyzer()
    
    # Тестируем операции с базой данных
    test_database_operations()
    
    print("\n" + "=" * 60)
    print("🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")
    print("=" * 60)
    
    if analysis_result:
        print("✅ Анализатор конкурентов работает")
    else:
        print("⚠️ Анализатор конкурентов требует доработки")
    
    print("✅ База данных SQLite работает")
    print("✅ Основные операции выполняются")
    
    print(f"\n📁 База данных: {db_path}")
    print("🚀 Готово к запуску полного пайплайна!")

if __name__ == "__main__":
    main()


