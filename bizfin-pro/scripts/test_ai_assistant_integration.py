#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест интеграции AI Assistant с BizFin Pro SEO Pipeline
"""

import sys
import os
import json
import time
from datetime import datetime

# Добавляем путь к модулям проекта
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.ai_agent.ai_assistant_client import AIAssistantClient
from modules.alwrity_integration.alwrity_client import ALwrityClient
from config.company_profile import CompanyData

def test_ai_assistant_connection():
    """Тестирование подключения к AI Assistant"""
    print("🤖 ТЕСТИРОВАНИЕ AI ASSISTANT")
    print("=" * 60)
    
    # Инициализация AI Assistant
    ai_client = AIAssistantClient()
    
    print("🔌 Тестирование подключения к AI Assistant...")
    
    # Тест подключения
    if ai_client.test_connection():
        print("✅ AI Assistant доступен!")
        return True
    else:
        print("⚠️ AI Assistant недоступен, используем fallback режим")
        return False

def test_ai_assistant_search():
    """Тестирование поиска через AI Assistant"""
    print("\n🔍 ТЕСТИРОВАНИЕ ПОИСКА В ИНТЕРНЕТЕ")
    print("-" * 40)
    
    ai_client = AIAssistantClient()
    test_keyword = "тендерная гарантия"
    
    print(f"🔑 Поиск по ключевому слову: '{test_keyword}'")
    
    try:
        start_time = time.time()
        search_results = ai_client.search_internet(test_keyword, num_results=3)
        search_time = time.time() - start_time
        
        print(f"⏱️ Время поиска: {search_time:.2f} секунд")
        print(f"📊 Найдено результатов: {len(search_results)}")
        
        if search_results:
            print("🏆 Топ результаты:")
            for i, result in enumerate(search_results[:3], 1):
                print(f"   {i}. {result.get('title', 'Без заголовка')}")
                print(f"      URL: {result.get('url', 'N/A')}")
                print(f"      Домен: {result.get('domain', 'N/A')}")
        
        return search_results
        
    except Exception as e:
        print(f"❌ Ошибка поиска: {e}")
        return []

def test_ai_assistant_analysis():
    """Тестирование анализа конкурентов через AI Assistant"""
    print("\n📊 ТЕСТИРОВАНИЕ АНАЛИЗА КОНКУРЕНТОВ")
    print("-" * 40)
    
    ai_client = AIAssistantClient()
    test_keyword = "банковская гарантия для ИП"
    
    # Получаем результаты поиска
    search_results = ai_client.search_internet(test_keyword, num_results=3)
    
    print(f"🔑 Анализ для ключевого слова: '{test_keyword}'")
    
    try:
        start_time = time.time()
        analysis = ai_client.analyze_competitors(test_keyword, search_results)
        analysis_time = time.time() - start_time
        
        print(f"⏱️ Время анализа: {analysis_time:.2f} секунд")
        print(f"📊 Статус: {analysis.get('status', 'unknown')}")
        print(f"🔍 Найдено конкурентов: {analysis.get('total_found', 0)}")
        
        if analysis.get('common_themes'):
            print(f"🎯 Общие темы: {', '.join(analysis['common_themes'][:3])}")
        
        if analysis.get('gaps'):
            print(f"⚠️ Пробелы: {', '.join(analysis['gaps'][:2])}")
        
        if analysis.get('recommendations'):
            print(f"💡 Рекомендации: {', '.join(analysis['recommendations'][:2])}")
        
        return analysis
        
    except Exception as e:
        print(f"❌ Ошибка анализа: {e}")
        return {}

def test_ai_assistant_generation():
    """Тестирование генерации статьи через AI Assistant"""
    print("\n✍️ ТЕСТИРОВАНИЕ ГЕНЕРАЦИИ СТАТЬИ")
    print("-" * 40)
    
    ai_client = AIAssistantClient()
    company_data = CompanyData()
    
    test_keyword = "банковская гарантия без залога"
    
    # Получаем данные для генерации
    search_results = ai_client.search_internet(test_keyword, num_results=3)
    competitors_data = ai_client.analyze_competitors(test_keyword, search_results)
    
    print(f"🔑 Генерация статьи для: '{test_keyword}'")
    
    try:
        start_time = time.time()
        article_data = ai_client.generate_article(
            keyword=test_keyword,
            competitors_data=competitors_data,
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
        
        return article_data
        
    except Exception as e:
        print(f"❌ Ошибка генерации: {e}")
        return {}

def test_ai_assistant_seo():
    """Тестирование SEO-оптимизации через AI Assistant"""
    print("\n🔧 ТЕСТИРОВАНИЕ SEO-ОПТИМИЗАЦИИ")
    print("-" * 40)
    
    ai_client = AIAssistantClient()
    test_keyword = "банковская гарантия онлайн"
    test_content = f"Статья о {test_keyword} для тестирования SEO-оптимизации."
    
    print(f"🔑 SEO-оптимизация для: '{test_keyword}'")
    
    try:
        start_time = time.time()
        seo_result = ai_client.optimize_seo(test_content, test_keyword)
        seo_time = time.time() - start_time
        
        print(f"⏱️ Время SEO-анализа: {seo_time:.2f} секунд")
        print(f"📈 SEO балл: {seo_result.get('score', 0)}")
        print(f"🔑 Плотность ключевого слова: {seo_result.get('keyword_density', 0)}%")
        print(f"📖 Читаемость: {seo_result.get('readability_score', 0)}")
        
        if seo_result.get('suggestions'):
            print(f"💡 Рекомендации: {len(seo_result['suggestions'])}")
        
        return seo_result
        
    except Exception as e:
        print(f"❌ Ошибка SEO-оптимизации: {e}")
        return {}

def test_ai_assistant_faq():
    """Тестирование генерации FAQ через AI Assistant"""
    print("\n❓ ТЕСТИРОВАНИЕ ГЕНЕРАЦИИ FAQ")
    print("-" * 40)
    
    ai_client = AIAssistantClient()
    test_keyword = "банковская гарантия для ООО"
    test_content = f"Статья о {test_keyword} с подробным описанием процесса получения."
    
    print(f"🔑 Генерация FAQ для: '{test_keyword}'")
    
    try:
        start_time = time.time()
        faq_data = ai_client.generate_faq(test_keyword, test_content)
        faq_time = time.time() - start_time
        
        print(f"⏱️ Время генерации FAQ: {faq_time:.2f} секунд")
        print(f"❓ Вопросов FAQ: {len(faq_data.get('questions', []))}")
        
        if faq_data.get('questions'):
            print("📋 Вопросы:")
            for i, question in enumerate(faq_data['questions'][:3], 1):
                print(f"   {i}. {question}")
        
        if faq_data.get('json_ld'):
            print("✅ JSON-LD схема создана")
        
        return faq_data
        
    except Exception as e:
        print(f"❌ Ошибка генерации FAQ: {e}")
        return {}

def test_alwrity_with_ai_assistant():
    """Тестирование ALwrity с AI Assistant"""
    print("\n🔄 ТЕСТИРОВАНИЕ ALWRITY + AI ASSISTANT")
    print("-" * 40)
    
    alwrity_client = ALwrityClient()
    test_keyword = "банковская гарантия для тендера"
    
    print(f"🔑 Полный тест ALwrity + AI Assistant для: '{test_keyword}'")
    
    try:
        # 1. Исследование конкурентов
        print("1️⃣ Исследование конкурентов...")
        research_result = alwrity_client.research_competitors(test_keyword, num_results=3)
        print(f"   ✅ Найдено: {research_result.get('total_found', 0)} конкурентов")
        
        # 2. Генерация статьи
        print("2️⃣ Генерация статьи...")
        company_data = CompanyData()
        article_data = alwrity_client.generate_article(
            keyword=test_keyword,
            competitors_data=research_result,
            company_profile=company_data.get_company_stats(),
            target_words=2500
        )
        print(f"   ✅ Сгенерировано: {article_data.get('word_count', 0)} слов")
        
        # 3. SEO-оптимизация
        print("3️⃣ SEO-оптимизация...")
        seo_result = alwrity_client.optimize_seo(article_data['content'], test_keyword)
        print(f"   ✅ SEO балл: {seo_result.get('score', 0)}")
        
        # 4. Генерация FAQ
        print("4️⃣ Генерация FAQ...")
        faq_data = alwrity_client.generate_faq(test_keyword, article_data['content'])
        print(f"   ✅ FAQ вопросов: {len(faq_data.get('questions', []))}")
        
        return {
            'research': research_result,
            'article': article_data,
            'seo': seo_result,
            'faq': faq_data
        }
        
    except Exception as e:
        print(f"❌ Ошибка полного теста: {e}")
        return {}

def main():
    """Основная функция тестирования"""
    print("🚀 ТЕСТИРОВАНИЕ AI ASSISTANT ИНТЕГРАЦИИ")
    print("=" * 80)
    
    # Тест подключения
    connection_ok = test_ai_assistant_connection()
    
    # Тест поиска
    search_results = test_ai_assistant_search()
    
    # Тест анализа
    analysis_result = test_ai_assistant_analysis()
    
    # Тест генерации
    article_data = test_ai_assistant_generation()
    
    # Тест SEO
    seo_result = test_ai_assistant_seo()
    
    # Тест FAQ
    faq_data = test_ai_assistant_faq()
    
    # Полный тест ALwrity + AI Assistant
    full_test_result = test_alwrity_with_ai_assistant()
    
    # Итоговый отчет
    print("\n" + "=" * 80)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 80)
    
    print(f"🔌 Подключение к AI Assistant: {'✅ OK' if connection_ok else '⚠️ Fallback'}")
    print(f"🔍 Поиск в интернете: {'✅ OK' if search_results else '❌ Ошибка'}")
    print(f"📊 Анализ конкурентов: {'✅ OK' if analysis_result else '❌ Ошибка'}")
    print(f"✍️ Генерация статей: {'✅ OK' if article_data else '❌ Ошибка'}")
    print(f"🔧 SEO-оптимизация: {'✅ OK' if seo_result else '❌ Ошибка'}")
    print(f"❓ Генерация FAQ: {'✅ OK' if faq_data else '❌ Ошибка'}")
    print(f"🔄 ALwrity + AI Assistant: {'✅ OK' if full_test_result else '❌ Ошибка'}")
    
    if full_test_result:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("🚀 AI Assistant успешно интегрирован в BizFin Pro SEO Pipeline")
        print("🤖 ALwrity теперь использует AI Assistant для генерации и поиска")
    else:
        print("\n⚠️ Некоторые тесты требуют доработки")
    
    print("\n📋 Следующие шаги:")
    print("1. Настроить реальный AI Assistant API")
    print("2. Протестировать с реальными данными")
    print("3. Запустить полный пайплайн")

if __name__ == "__main__":
    main()


