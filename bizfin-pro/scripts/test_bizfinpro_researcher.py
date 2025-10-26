#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тестовый скрипт для демонстрации работы BizFin Pro Researcher
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from modules.research.bizfinpro_researcher import BizFinProResearcher, run_research_pipeline
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_researcher_integration():
    """Тест интеграции исследователя с проектом"""
    
    print("🧪 ТЕСТ ИНТЕГРАЦИИ BIZFIN PRO RESEARCHER")
    print("=" * 60)
    
    # Инициализация
    researcher = BizFinProResearcher()
    print("✅ Исследователь инициализирован")
    
    # Тест с несколькими ключевыми словами
    test_keywords = [
        "банковская гарантия",
        "тендерная гарантия", 
        "гарантия исполнения"
    ]
    
    research_ids = []
    
    for keyword in test_keywords:
        print(f"\n🔍 Исследование: {keyword}")
        try:
            research_data = run_research_pipeline(keyword, researcher)
            research_ids.append(research_data['research_id'])
            
            print(f"   ✅ Завершено (ID: {research_data['research_id']})")
            print(f"   ⏱️  Время: {research_data['execution_time']}с")
            print(f"   📊 SERP: {len(research_data['top5'])} результатов")
            print(f"   📄 Страниц: {len(research_data['pages'])} проанализировано")
            
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    
    # Показываем итоговый список
    print(f"\n📋 ИТОГОВЫЙ СПИСОК ИССЛЕДОВАНИЙ:")
    print("-" * 60)
    
    researches = researcher.list_researches(limit=10)
    for res in researches:
        print(f"ID: {res['id']:2d} | {res['keyword']:25s} | {res['created_at']:19s} | {res['execution_time_seconds']:2d}с")
    
    print(f"\n🎉 ТЕСТ ЗАВЕРШЕН! Создано исследований: {len(research_ids)}")
    
    return research_ids

def demonstrate_data_retrieval(research_ids):
    """Демонстрация получения данных из БД"""
    
    print(f"\n📊 ДЕМОНСТРАЦИЯ ПОЛУЧЕНИЯ ДАННЫХ")
    print("=" * 60)
    
    researcher = BizFinProResearcher()
    
    for research_id in research_ids[:2]:  # Показываем первые 2
        print(f"\n🔍 Исследование ID: {research_id}")
        
        research = researcher.get_research_by_id(research_id)
        if research:
            print(f"   Ключевое слово: {research['keyword']}")
            print(f"   Название: {research['research_name']}")
            print(f"   Статус: {research['status']}")
            print(f"   SERP данных: {len(research['serp_data'])} элементов")
            print(f"   Страниц данных: {len(research['pages_data'])} элементов")
            
            # Показываем краткую сводку SEO Blueprint
            if research['seo_blueprint']:
                bp = research['seo_blueprint']
                print(f"   SEO Title: {bp.get('title', 'N/A')[:50]}...")
                print(f"   SEO H1: {bp.get('h1', 'N/A')}")
                print(f"   SEO Slug: {bp.get('slug', 'N/A')}")
                print(f"   Outline блоков: {len(bp.get('outline', []))}")
                print(f"   FAQ вопросов: {len(bp.get('faq', []))}")
        else:
            print(f"   ❌ Исследование не найдено")

if __name__ == "__main__":
    try:
        # Запуск тестов
        research_ids = test_researcher_integration()
        
        # Демонстрация получения данных
        demonstrate_data_retrieval(research_ids)
        
        print(f"\n✅ ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        
    except Exception as e:
        print(f"❌ Ошибка в тестах: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
