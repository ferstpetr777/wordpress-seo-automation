#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест интеграции ALwrity с BizFin Pro SEO Pipeline
"""

import sys
import os
import json
import time
from datetime import datetime

# Добавляем путь к модулям проекта
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.alwrity_integration.alwrity_client import ALwrityClient
from config.company_profile import CompanyData
from config.legal_compliance import ComplianceChecker

def test_alwrity_integration():
    """Тестирование интеграции ALwrity"""
    print("🧪 ТЕСТИРОВАНИЕ ИНТЕГРАЦИИ ALWRITY")
    print("=" * 60)
    
    # Инициализация
    alwrity_client = ALwrityClient()
    company_data = CompanyData()
    
    # Тестовое ключевое слово
    test_keyword = "тендерная гарантия"
    
    print(f"🔑 Тестовое ключевое слово: '{test_keyword}'")
    print(f"🏢 Компания: {company_data.get_company_stats()['experience']}")
    
    # Тест 1: Проверка правовых требований
    print("\n1️⃣ ТЕСТ: Правовые требования")
    print("-" * 40)
    
    if ComplianceChecker.check_internet_access():
        print("✅ Доступ к интернету: OK")
    else:
        print("❌ Доступ к интернету: НЕТ")
        return False
    
    # Тест 2: Исследование конкурентов
    print("\n2️⃣ ТЕСТ: Исследование конкурентов")
    print("-" * 40)
    
    try:
        start_time = time.time()
        research_result = alwrity_client.research_competitors(test_keyword, num_results=3)
        research_time = time.time() - start_time
        
        print(f"⏱️ Время исследования: {research_time:.2f} секунд")
        print(f"📊 Статус: {research_result.get('status', 'unknown')}")
        print(f"🔍 Найдено конкурентов: {research_result.get('total_found', 0)}")
        
        if research_result.get('competitors'):
            print("🏆 Топ конкуренты:")
            for i, competitor in enumerate(research_result['competitors'][:3], 1):
                print(f"   {i}. {competitor.get('title', 'Без заголовка')}")
        
        if research_result.get('common_themes'):
            print(f"🎯 Общие темы: {', '.join(research_result['common_themes'][:3])}")
        
        if research_result.get('gaps'):
            print(f"⚠️ Пробелы: {', '.join(research_result['gaps'][:2])}")
        
    except Exception as e:
        print(f"❌ Ошибка исследования: {e}")
        return False
    
    # Тест 3: Генерация статьи
    print("\n3️⃣ ТЕСТ: Генерация статьи")
    print("-" * 40)
    
    try:
        start_time = time.time()
        article_data = alwrity_client.generate_article(
            keyword=test_keyword,
            competitors_data=research_result,
            company_profile=company_data.get_company_stats(),
            target_words=2500
        )
        generation_time = time.time() - start_time
        
        print(f"⏱️ Время генерации: {generation_time:.2f} секунд")
        print(f"📝 Заголовок: {article_data.get('title', 'Без заголовка')}")
        print(f"📊 Слов: {article_data.get('word_count', 0)}")
        print(f"⏱️ Время чтения: {article_data.get('reading_time', 0)} минут")
        
        if article_data.get('structure'):
            print(f"🏗️ Структура: {len(article_data['structure'])} разделов")
        
    except Exception as e:
        print(f"❌ Ошибка генерации: {e}")
        return False
    
    # Тест 4: SEO-оптимизация
    print("\n4️⃣ ТЕСТ: SEO-оптимизация")
    print("-" * 40)
    
    try:
        seo_result = alwrity_client.optimize_seo(article_data['content'], test_keyword)
        
        print(f"📈 SEO балл: {seo_result.get('score', 0)}")
        print(f"🔑 Плотность ключевого слова: {seo_result.get('keyword_density', 0)}%")
        print(f"📖 Читаемость: {seo_result.get('readability_score', 0)}")
        
        if seo_result.get('suggestions'):
            print(f"💡 Рекомендации: {len(seo_result['suggestions'])}")
        
    except Exception as e:
        print(f"❌ Ошибка SEO-оптимизации: {e}")
        return False
    
    # Тест 5: Генерация FAQ
    print("\n5️⃣ ТЕСТ: Генерация FAQ")
    print("-" * 40)
    
    try:
        faq_data = alwrity_client.generate_faq(test_keyword, article_data['content'])
        
        print(f"❓ Вопросов FAQ: {len(faq_data.get('questions', []))}")
        print("📋 Вопросы:")
        for i, question in enumerate(faq_data.get('questions', [])[:3], 1):
            print(f"   {i}. {question}")
        
        if faq_data.get('json_ld'):
            print("✅ JSON-LD схема создана")
        
    except Exception as e:
        print(f"❌ Ошибка генерации FAQ: {e}")
        return False
    
    # Итоговый отчет
    print("\n" + "=" * 60)
    print("📊 ИТОГОВЫЙ ОТЧЕТ ТЕСТИРОВАНИЯ")
    print("=" * 60)
    
    print("✅ Все тесты пройдены успешно!")
    print(f"🔑 Ключевое слово: {test_keyword}")
    print(f"📊 Найдено конкурентов: {research_result.get('total_found', 0)}")
    print(f"📝 Сгенерировано слов: {article_data.get('word_count', 0)}")
    print(f"📈 SEO балл: {seo_result.get('score', 0)}")
    print(f"❓ FAQ вопросов: {len(faq_data.get('questions', []))}")
    
    print("\n🚀 ALwrity интеграция готова к использованию!")
    
    return True

def test_end_to_end():
    """End-to-end тест полного пайплайна"""
    print("\n🔄 END-TO-END ТЕСТ ПОЛНОГО ПАЙПЛАЙНА")
    print("=" * 60)
    
    try:
        from scripts.pipeline_v2 import BizFinProPipeline
        
        pipeline = BizFinProPipeline()
        
        # Тестовое ключевое слово
        test_keyword = "банковская гарантия для ИП"
        
        print(f"🔑 Тестируем пайплайн с ключевым словом: '{test_keyword}'")
        
        # Запускаем пайплайн
        result = pipeline.run_full_pipeline(
            keyword=test_keyword,
            priority='medium',
            target_volume=2500,
            target_intent='informational'
        )
        
        print(f"📊 Результат пайплайна:")
        print(f"   Статус: {result.status}")
        print(f"   Время выполнения: {result.execution_time:.2f} секунд")
        print(f"   Keyword ID: {result.keyword_id}")
        
        if result.data:
            print(f"   Данные: {json.dumps(result.data, indent=2, ensure_ascii=False)}")
        
        if result.errors:
            print(f"   Ошибки: {', '.join(result.errors)}")
        
        return result.status == 'completed'
        
    except Exception as e:
        print(f"❌ Ошибка E2E теста: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 ТЕСТИРОВАНИЕ BIZFIN PRO + ALWRITY ИНТЕГРАЦИИ")
    print("=" * 80)
    
    # Тест интеграции ALwrity
    integration_success = test_alwrity_integration()
    
    if integration_success:
        # End-to-end тест
        e2e_success = test_end_to_end()
        
        print("\n" + "=" * 80)
        print("🎉 ФИНАЛЬНЫЙ РЕЗУЛЬТАТ")
        print("=" * 80)
        
        if e2e_success:
            print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
            print("🚀 Система готова к продуктивному использованию!")
            print("📈 ALwrity успешно интегрирован в BizFin Pro SEO Pipeline")
        else:
            print("⚠️ Интеграция ALwrity работает, но E2E тест требует доработки")
    else:
        print("❌ Интеграция ALwrity требует настройки")
    
    print("\n📋 Следующие шаги:")
    print("1. Настроить API ключи для ALwrity")
    print("2. Протестировать с реальными данными")
    print("3. Запустить полный пайплайн на продакшене")

if __name__ == "__main__":
    main()


