#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для отображения результатов AI исследования
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from modules.research.ai_web_researcher import AIWebResearcher
import sqlite3
import pickle
import json
from config.database_sqlite import DB_CONFIG

def show_research_results(research_id: int = None):
    """Показать результаты исследования"""
    
    # Получаем данные из БД
    db_config = DB_CONFIG.get_config_dict()
    db_path = db_config['database']
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    if research_id:
        cursor.execute('''
            SELECT id, keyword, research_name, serp_data, pages_data, 
                   corpus_synthesis, seo_blueprint, created_at, execution_time_seconds
            FROM ai_web_research 
            WHERE id = ?
        ''', (research_id,))
    else:
        cursor.execute('''
            SELECT id, keyword, research_name, serp_data, pages_data, 
                   corpus_synthesis, seo_blueprint, created_at, execution_time_seconds
            FROM ai_web_research 
            ORDER BY id DESC 
            LIMIT 1
        ''')
    
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        print('❌ AI исследования не найдены')
        return
    
    research_id, keyword, research_name, serp_data, pages_data, corpus_synthesis, seo_blueprint, created_at, execution_time = result
    
    print('🔍 ДЕТАЛЬНЫЙ АНАЛИЗ AI ИССЛЕДОВАНИЯ')
    print('=' * 80)
    print(f'📊 ОБЩАЯ ИНФОРМАЦИЯ:')
    print(f'   ID: {research_id}')
    print(f'   Ключевое слово: {keyword}')
    print(f'   Название: {research_name}')
    print(f'   Время выполнения: {execution_time} секунд')
    print(f'   Создано: {created_at}')
    print()
    
    # Десериализируем данные с обработкой ошибок
    try:
        serp_items = pickle.loads(serp_data) if serp_data else []
        print(f'📈 SERP РЕЗУЛЬТАТЫ ({len(serp_items)} результатов):')
        for i, item in enumerate(serp_items, 1):
            print(f'   {i}. {item.get("title", "N/A")}')
            print(f'      URL: {item.get("url", "N/A")}')
            print(f'      Издатель: {item.get("publisher", "N/A")}')
            print(f'      Описание: {item.get("snippet", "N/A")[:100]}...')
            print()
    except Exception as e:
        print(f'❌ Ошибка десериализации SERP данных: {e}')
        serp_items = []
    
    try:
        pages = pickle.loads(pages_data) if pages_data else []
        print(f'📄 АНАЛИЗ СТРАНИЦ ({len(pages)} страниц):')
        for i, page in enumerate(pages, 1):
            print(f'   Страница {i}: {page.get("title", "N/A")}')
            print(f'      URL: {page.get("url", "N/A")}')
            print(f'      Издатель: {page.get("publisher", "N/A")}')
            print(f'      Слов: {page.get("word_count", 0)}')
            print(f'      Время чтения: {page.get("reading_time_min", 0)} мин')
            print(f'      H-заголовки ({len(page.get("h_outline", []))}):')
            for h in page.get("h_outline", [])[:3]:  # Показываем первые 3
                print(f'         - {h}')
            print(f'      FAQ ({len(page.get("faq", []))} вопросов):')
            for qa in page.get("faq", [])[:2]:  # Показываем первые 2
                print(f'         Q: {qa.get("q", "N/A")}')
                print(f'         A: {qa.get("a", "N/A")}')
            print(f'      Правовые ссылки: {page.get("legal_refs", [])}')
            print(f'      CTA: {page.get("ctas", [])}')
            print()
    except Exception as e:
        print(f'❌ Ошибка десериализации данных страниц: {e}')
        pages = []
    
    try:
        corpus = pickle.loads(corpus_synthesis) if corpus_synthesis else {}
        print(f'🧠 АНАЛИЗ КОРПУСА:')
        print(f'   Консенсусные данные: {len(corpus.get("consensus", []))} элементов')
        print(f'   Расхождения: {len(corpus.get("disagreements", []))} элементов')
        print(f'   Правовые якоря: {len(corpus.get("legal_anchors", []))} элементов')
        print(f'   Общая структура: {len(corpus.get("common_outline", []))} блоков')
        
        if corpus.get('consensus'):
            print(f'\\n   🔍 КОНСЕНСУСНЫЕ ДАННЫЕ:')
            for item in corpus['consensus'][:2]:
                print(f'   - {item.get("claim", "N/A")}')
        
        if corpus.get('disagreements'):
            print(f'\\n   ⚠️ РАСХОЖДЕНИЯ:')
            for item in corpus['disagreements'][:2]:
                print(f'   - {item}')
    except Exception as e:
        print(f'❌ Ошибка десериализации корпуса: {e}')
        corpus = {}
    
    try:
        blueprint = pickle.loads(seo_blueprint) if seo_blueprint else {}
        print(f'\\n🎯 SEO BLUEPRINT:')
        print(f'   Title: {blueprint.get("title", "N/A")}')
        print(f'   H1: {blueprint.get("h1", "N/A")}')
        print(f'   Slug: {blueprint.get("slug", "N/A")}')
        print(f'   Meta: {blueprint.get("meta_description", "N/A")[:100]}...')
        print()
        
        print(f'📋 РЕКОМЕНДУЕМАЯ СТРУКТУРА:')
        for outline in blueprint.get('outline', [])[:5]:
            print(f'   - {outline}')
        print()
        
        print(f'❓ FAQ БЛОКИ ({len(blueprint.get("faq", []))} вопросов):')
        for qa in blueprint.get('faq', [])[:3]:
            print(f'   Q: {qa.get("q", "N/A")}')
            print(f'   A: {qa.get("a", "N/A")}')
            print()
        
        print(f'🔗 ВНУТРЕННИЕ ССЫЛКИ:')
        for link in blueprint.get('internal_links', []):
            print(f'   - {link.get("anchor", "N/A")} → {link.get("target", "N/A")}')
        print()
        
        print(f'⚖️ E-E-A-T ТРЕБОВАНИЯ:')
        for eeat in blueprint.get('eeat', []):
            print(f'   - {eeat}')
        print()
        
        print(f'🏗️ ТЕХНИЧЕСКИЕ ТРЕБОВАНИЯ:')
        print(f'   - {", ".join(blueprint.get("tech", []))}')
        print()
        
        print(f'📊 SCHEMA.ORG:')
        print(f'   - {", ".join(blueprint.get("schema", []))}')
    except Exception as e:
        print(f'❌ Ошибка десериализации Blueprint: {e}')
        blueprint = {}
    
    print(f'\\n✅ AI ИССЛЕДОВАНИЕ АНАЛИЗ ЗАВЕРШЕН!')
    print(f'   🆔 ID в БД: {research_id}')
    print(f'   ⏱️ Время выполнения: {execution_time} секунд')
    print(f'   📊 SERP результатов: {len(serp_items)}')
    print(f'   📄 Проанализировано страниц: {len(pages)}')

def list_researches():
    """Список всех AI исследований"""
    
    db_config = DB_CONFIG.get_config_dict()
    db_path = db_config['database']
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, keyword, research_name, created_at, execution_time_seconds, status
        FROM ai_web_research 
        ORDER BY created_at DESC 
        LIMIT 10
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    print('📊 СПИСОК AI ИССЛЕДОВАНИЙ:')
    print('=' * 60)
    
    if results:
        for res in results:
            print(f'ID: {res[0]:2d} | {res[1]:30s} | {res[2]:20s} | {res[3]:19s} | {res[4]:2d}с')
    else:
        print('   Исследования не найдены')

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Показать результаты AI исследований")
    parser.add_argument("--show", type=int, help="Показать исследование по ID")
    parser.add_argument("--list", action="store_true", help="Показать список исследований")
    args = parser.parse_args()
    
    if args.list:
        list_researches()
    elif args.show:
        show_research_results(args.show)
    else:
        show_research_results()  # Показать последнее исследование
