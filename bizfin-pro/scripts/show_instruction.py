#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для вывода инструкции web_research_standard_2025 в читаемом виде
"""

import os
import sys
import sqlite3
import json
import logging
from datetime import datetime

def setup_logging():
    """Настройка логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def get_instruction_from_db():
    """Получение инструкции из базы данных"""
    logger = setup_logging()
    
    try:
        # Путь к базе данных SQLite
        db_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'bizfin_pro.db')
        
        # Подключаемся к базе данных
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        logger.info(f"🗄️ Подключение к базе данных: {db_path}")
        
        # Получаем инструкцию
        cursor.execute("""
            SELECT instruction_id, title, version, instruction_data, created_at, updated_at 
            FROM research_instructions 
            WHERE instruction_id = 'web_research_standard_2025'
        """)
        
        result = cursor.fetchone()
        
        if not result:
            logger.error("❌ Инструкция не найдена в базе данных")
            return None
        
        instruction_id, title, version, instruction_data, created_at, updated_at = result
        
        # Парсим JSON данные
        instruction = json.loads(instruction_data)
        
        cursor.close()
        connection.close()
        
        return instruction
        
    except Exception as e:
        logger.error(f"❌ Ошибка получения инструкции: {e}")
        if 'connection' in locals():
            connection.close()
        return None

def format_instruction_readable(instruction):
    """Форматирование инструкции в читаемый вид"""
    
    output = []
    output.append("=" * 80)
    output.append(f"📋 ИНСТРУКЦИЯ ВЕБ-ИССЛЕДОВАНИЯ ДЛЯ SEO-АНАЛИЗА")
    output.append("=" * 80)
    output.append("")
    
    # Основная информация
    output.append(f"🆔 Instruction ID: {instruction.get('id', 'N/A')}")
    output.append(f"📝 Название: {instruction.get('title', 'N/A')}")
    output.append(f"📊 Версия: {instruction.get('version', 'N/A')}")
    output.append(f"👤 Автор: {instruction.get('author', 'N/A')}")
    output.append(f"📅 Создано: {instruction.get('created_at', 'N/A')}")
    output.append("")
    
    # Описание
    output.append("📖 ОПИСАНИЕ:")
    output.append(f"   {instruction.get('description', 'N/A')}")
    output.append("")
    
    # Параметры
    output.append("⚙️ ПАРАМЕТРЫ:")
    params = instruction.get('parameters', {})
    for key, value in params.items():
        output.append(f"   • {key}: {value}")
    output.append("")
    
    # Стратегия веб-поиска
    output.append("🔍 СТРАТЕГИЯ ВЕБ-ПОИСКА:")
    web_search = instruction.get('web_search_strategy', {})
    
    # Основной поиск
    primary = web_search.get('primary_search', {})
    output.append("   🎯 ОСНОВНОЙ ПОИСК:")
    output.append(f"      Запрос: {primary.get('query', 'N/A')}")
    output.append(f"      Цель: {primary.get('purpose', 'N/A')}")
    output.append(f"      Ожидаемые результаты: {primary.get('expected_results', 'N/A')}")
    output.append("")
    
    # Вторичные поиски
    secondary = web_search.get('secondary_searches', [])
    output.append(f"   🔍 ВТОРИЧНЫЕ ПОИСКИ ({len(secondary)} шт.):")
    for i, search in enumerate(secondary, 1):
        output.append(f"      {i}. {search.get('query', 'N/A')}")
        output.append(f"         Цель: {search.get('purpose', 'N/A')}")
        output.append(f"         Результаты: {search.get('expected_results', 'N/A')}")
        output.append("")
    
    # Методология исследований
    output.append("📚 МЕТОДОЛОГИЯ ИССЛЕДОВАНИЙ:")
    methodology = instruction.get('research_methodology', {})
    for step_key, step_data in methodology.items():
        step_num = step_key.replace('step_', '')
        output.append(f"   {step_num}. {step_data.get('title', 'N/A')}")
        output.append(f"      Описание: {step_data.get('description', 'N/A')}")
        output.append(f"      Вывод: {step_data.get('output', 'N/A')}")
        output.append("")
    
    # Обработка данных
    output.append("🔄 ОБРАБОТКА ДАННЫХ:")
    data_processing = instruction.get('data_processing', {})
    for section, details in data_processing.items():
        output.append(f"   📊 {details.get('title', 'N/A')}:")
        if 'fields' in details:
            output.append(f"      Поля: {', '.join(details['fields'])}")
        if 'method' in details:
            output.append(f"      Метод: {details['method']}")
        output.append("")
    
    # Формат вывода
    output.append("📄 ФОРМАТ ВЫВОДА:")
    output_format = instruction.get('output_format', {})
    for key, value in output_format.items():
        output.append(f"   • {key}: {value}")
    output.append("")
    
    # Требования
    output.append("📋 ТРЕБОВАНИЯ:")
    requirements = instruction.get('requirements', {})
    for key, value in requirements.items():
        output.append(f"   • {key}: {value}")
    output.append("")
    
    # Финальное действие
    output.append("🎯 ФИНАЛЬНОЕ ДЕЙСТВИЕ:")
    final_action = instruction.get('final_action', {})
    output.append(f"   Описание: {final_action.get('description', 'N/A')}")
    output.append(f"   Таблица БД: {final_action.get('database_table', 'N/A')}")
    output.append(f"   Формат JSON: {final_action.get('json_format', 'N/A')}")
    output.append(f"   Назначение ID: {final_action.get('id_assignment', 'N/A')}")
    output.append("")
    
    output.append("=" * 80)
    
    return "\n".join(output)

def main():
    """Основная функция"""
    logger = setup_logging()
    
    print("🚀 Получение инструкции web_research_standard_2025 из базы данных")
    print("=" * 80)
    
    # Получаем инструкцию из БД
    instruction = get_instruction_from_db()
    
    if instruction:
        # Форматируем и выводим
        readable_text = format_instruction_readable(instruction)
        print(readable_text)
        
        # Дополнительная статистика
        print("\n📊 СТАТИСТИКА ИНСТРУКЦИИ:")
        print(f"   🔍 Всего шагов методологии: {len(instruction.get('research_methodology', {}))}")
        
        secondary_searches = instruction.get('web_search_strategy', {}).get('secondary_searches', [])
        print(f"   🔍 Количество вторичных поисков: {len(secondary_searches)}")
        
        print(f"   📊 Версия: {instruction.get('version', 'N/A')}")
        print("=" * 80)
        
    else:
        print("❌ Не удалось получить инструкцию из базы данных")

if __name__ == "__main__":
    main()

