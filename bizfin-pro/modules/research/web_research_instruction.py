#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
web_research_instruction.py — Эталонная инструкция для веб-исследований
Содержит стандартизированную методологию SEO-анализа через интернет
"""

from __future__ import annotations
import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Any
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config.database_sqlite import DB_CONFIG

class WebResearchInstruction:
    """Эталонная инструкция для веб-исследований"""
    
    def __init__(self):
        self.db_config = DB_CONFIG.get_config_dict()
        self.db_path = self.db_config['database']
        
        # Эталонная инструкция
        self.instruction = {
            "id": "web_research_standard_2025",
            "title": "Эталонная инструкция веб-исследования для SEO-анализа",
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "author": "AI Assistant",
            "description": "Стандартизированная методология получения и обработки данных из интернета для SEO-анализа",
            
            "parameters": {
                "keyword_field": "{KW}",
                "region_field": "{REGION}",
                "language_field": "{ru}",
                "target_audience": "{опиши сегмент}",
                "article_goal": "{информировать/генерировать лиды/объяснить как выбрать}",
                "freshness_limit": "{N} месяцев",
                "date_format": "ГГГГ-ММ-ДД",
                "timezone": "{Europe/Moscow или Europe/Amsterdam}"
            },
            
            "research_methodology": {
                "step_1": {
                    "title": "Определение интента и контекста",
                    "description": "Анализ интента запроса, этапа воронки, сезонности и локальных терминов",
                    "output": "intent_analysis"
                },
                "step_2": {
                    "title": "SERP анализ ТОП-10",
                    "description": "Анализ URL, типа страниц, дат публикации, длины контента, структуры H1-H3",
                    "output": "serp_analysis"
                },
                "step_3": {
                    "title": "Семантические кластеры",
                    "description": "Построение основного и поддерживающих кластеров, вопросов, сущностей",
                    "output": "semantic_clusters"
                },
                "step_4": {
                    "title": "Контент-гэпы",
                    "description": "Выявление тем, подразделов, примеров, данных отсутствующих в ТОП-10",
                    "output": "content_gaps"
                },
                "step_5": {
                    "title": "Цифры и факты",
                    "description": "Сбор цен, процентов, формул, сроков с указанием источников и дат",
                    "output": "facts_and_figures"
                },
                "step_6": {
                    "title": "Идеи усиления",
                    "description": "Таблицы, чеклисты, примеры, кейсы, мини-калькуляторы",
                    "output": "enhancement_ideas"
                },
                "step_7": {
                    "title": "Внутренние/внешние ссылки",
                    "description": "Предложения по внутренней перелинковке и внешним ссылкам",
                    "output": "internal_external_links"
                },
                "step_8": {
                    "title": "Schema.org",
                    "description": "Рекомендации по структурированным данным (Article/FAQ/HowTo/Breadcrumb)",
                    "output": "schema_org"
                },
                "step_9": {
                    "title": "Структура статьи",
                    "description": "Набросок H1 (3-5 вариантов), план H2-H3, целевой объем",
                    "output": "article_structure"
                },
                "step_10": {
                    "title": "SEO элементы",
                    "description": "Title (5-10 вариантов), meta description (3-5 вариантов), OG-теги",
                    "output": "seo_elements"
                },
                "step_11": {
                    "title": "FAQ блок",
                    "description": "10-20 вопросов с краткими точными ответами",
                    "output": "faq"
                },
                "step_12": {
                    "title": "Compliance/дисклеймеры",
                    "description": "YMYL требования для финансов/медицины/юридических тем",
                    "output": "compliance"
                },
                "step_13": {
                    "title": "KPI-бриф",
                    "description": "Цель, интент, объем, ключевые кластеры, E-E-A-T, медиаплан, CTA, дедлайны",
                    "output": "kpi_brief"
                },
                "step_14": {
                    "title": "Суммаризация контента",
                    "description": "Краткое описание полученных текстов статей",
                    "output": "content_summary"
                },
                "step_15": {
                    "title": "Анализ структуры",
                    "description": "Анализ структуры текста полученных страниц",
                    "output": "structure_analysis"
                }
            },
            
            "web_search_strategy": {
                "primary_search": {
                    "query": "{keyword}",
                    "purpose": "Основной поиск по ключевому слову",
                    "expected_results": "Общая информация о теме"
                },
                "secondary_searches": [
                    {
                        "query": "{keyword} условия тарифы",
                        "purpose": "Поиск коммерческой информации",
                        "expected_results": "Условия, цены, тарифы"
                    },
                    {
                        "query": "{keyword} документы требования",
                        "purpose": "Поиск технических требований",
                        "expected_results": "Список документов, процедуры"
                    },
                    {
                        "query": "{keyword} калькулятор стоимость {year}",
                        "purpose": "Поиск актуальных калькуляторов и цен",
                        "expected_results": "Текущие тарифы и расчеты"
                    }
                ]
            },
            
            "data_processing": {
                "extraction": {
                    "title": "Извлечение данных из результатов поиска",
                    "fields": ["title", "url", "snippet", "date", "domain"],
                    "method": "Парсинг HTML и структурированных данных"
                },
                "analysis": {
                    "title": "Анализ структуры контента",
                    "fields": ["h1", "h2", "h3", "content_type", "features"],
                    "method": "Семантический анализ и классификация"
                },
                "synthesis": {
                    "title": "Синтез в структурированный формат",
                    "output_format": "JSON",
                    "validation": "Проверка источников и дат"
                }
            },
            
            "output_format": {
                "description": "Описание структуры контента",
                "summary": "Суммаризированное описание контента",
                "brief": "Краткое резюме (5-7 пунктов)",
                "serp_table": "Таблица SERP (| Позиция | URL | Тип | Дата | Длина | H1 | Особенности |)",
                "semantic_table": "Таблица семантики (| Кластер | Ключ | Интент | Пример H2 | Примечания |)",
                "content_gaps": "Список контент-гэпов (маркдаун)",
                "facts_list": "Список цифр/фактов с источниками (маркдаун)",
                "structure_draft": "Черновик структуры (H1/H2/H3)",
                "seo_variants": "Варианты title/meta/OG",
                "links_list": "Список внутренних/внешних ссылок с анкорами",
                "schema_example": "Пример JSON-LD для выбранной схемы",
                "faq_list": "FAQ",
                "kpi_brief": "KPI-бриф"
            },
            
            "requirements": {
                "sources": "Для ключевых утверждений и цифр поставь ссылки на источники (разные домены, по возможности официальные)",
                "dates": "Все даты — абсолютные (не «в этом году», а «2025-10-10»)",
                "missing_info": "Если чего-то не хватает — пиши «Нужно уточнить: …»",
                "originality": "Не повторяйся, не копируй абзацы с сайтов (никакого плагиата)",
                "search_operators": "Укажи, какие запросы/операторы использовал (например: site:, intitle:, filetype:pdf, кавычки и т. п.)"
            },
            
            "final_action": {
                "description": "Упаковать полученную информацию в Формате Json и сохранить в БД с номером ИД и с названием соответствующему ключевому слову",
                "database_table": "web_research_analysis",
                "json_format": "Структурированный JSON с полным анализом",
                "id_assignment": "Уникальный ID для каждого исследования"
            }
        }
    
    def save_to_database(self) -> int:
        """Сохранение эталонной инструкции в базу данных"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Создаем таблицу для инструкций
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS research_instructions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    instruction_id TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    version TEXT NOT NULL,
                    instruction_data TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active'
                )
            ''')
            
            # Сохраняем инструкцию
            insert_query = '''
                INSERT OR REPLACE INTO research_instructions 
                (instruction_id, title, version, instruction_data, status)
                VALUES (?, ?, ?, ?, ?)
            '''
            
            values = (
                self.instruction["id"],
                self.instruction["title"],
                self.instruction["version"],
                json.dumps(self.instruction, ensure_ascii=False),
                'active'
            )
            
            cursor.execute(insert_query, values)
            instruction_db_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            print(f"✅ Эталонная инструкция сохранена в БД (ID: {instruction_db_id})")
            return instruction_db_id
            
        except Exception as e:
            print(f"❌ Ошибка сохранения инструкции: {e}")
            if 'conn' in locals():
                conn.rollback()
                conn.close()
            raise
    
    def get_instruction(self) -> Dict[str, Any]:
        """Получение эталонной инструкции"""
        return self.instruction
    
    def create_search_queries(self, keyword: str, brand_domain: str = None) -> List[Dict[str, str]]:
        """Создание списка поисковых запросов на основе инструкции"""
        queries = []
        
        # Основной поиск
        queries.append({
            "query": keyword,
            "purpose": "Основной поиск по ключевому слову",
            "type": "primary"
        })
        
        # Дополнительные поиски
        secondary_queries = [
            f"{keyword} условия тарифы",
            f"{keyword} документы требования", 
            f"{keyword} калькулятор стоимость 2025"
        ]
        
        for query in secondary_queries:
            queries.append({
                "query": query,
                "purpose": "Поиск дополнительной информации",
                "type": "secondary"
            })
        
        # Поиск на сайте бренда (если указан)
        if brand_domain:
            queries.append({
                "query": f"site:{brand_domain} {keyword}",
                "purpose": "Поиск на официальном сайте бренда",
                "type": "brand_site"
            })
        
        return queries

def main():
    """Создание и сохранение эталонной инструкции"""
    instruction = WebResearchInstruction()
    
    # Сохраняем в БД
    instruction_id = instruction.save_to_database()
    
    # Сохраняем в JSON файл
    with open('/root/seo_project/bizfin-pro/web_research_instruction_standard.json', 'w', encoding='utf-8') as f:
        json.dump(instruction.get_instruction(), f, ensure_ascii=False, indent=2)
    
    print(f"✅ Эталонная инструкция создана")
    print(f"🆔 ID в БД: {instruction_id}")
    print(f"📁 JSON файл: web_research_instruction_standard.json")
    print(f"📊 Версия: {instruction.get_instruction()['version']}")
    
    # Демонстрация создания поисковых запросов
    print(f"\n🔍 ПРИМЕР ПОИСКОВЫХ ЗАПРОСОВ:")
    queries = instruction.create_search_queries("совкомбанк банковская гарантия", "psbank.ru")
    for i, query in enumerate(queries, 1):
        print(f"{i}. {query['query']} ({query['type']}) - {query['purpose']}")

if __name__ == "__main__":
    main()
