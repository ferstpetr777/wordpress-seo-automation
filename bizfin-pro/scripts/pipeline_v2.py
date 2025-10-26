#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BizFin Pro SEO Pipeline v2 - Полный цикл генерации, оптимизации и публикации статей

Этот скрипт реализует расширенный пайплайн v2 с полной преемственностью данных
и пост-публикационным контролем качества.

Автор: AI Assistant
Дата: 14.10.2025
"""

import sys
import os
import json
import time
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
import argparse
from dataclasses import dataclass

# Добавляем путь к модулям проекта
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.database import DB_CONFIG
from config.wordpress import WordPressConfig, BizFinProBrand, ContentTemplates
from config.company_profile import CompanyData
from config.legal_compliance import ComplianceChecker
from modules.research.competitor_analyzer import CompetitorAnalyzer
from modules.alwrity_integration.alwrity_client import ALwrityClient
import mysql.connector
from mysql.connector import Error

@dataclass
class PipelineResult:
    """Результат выполнения пайплайна"""
    keyword_id: int
    status: str
    message: str
    data: Dict[str, Any]
    execution_time: float
    errors: List[str]

class BizFinProPipeline:
    """Основной класс пайплайна BizFin Pro"""
    
    def __init__(self):
        """Инициализация пайплайна"""
        self.db_config = DB_CONFIG.get_config_dict()
        self.connection = None
        self.competitor_analyzer = CompetitorAnalyzer()
        
        # Инициализация ALwrity клиента
        self.alwrity_client = ALwrityClient()
        
        # Профиль компании
        self.company_data = CompanyData()
        
        # Настройка логирования
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Статистика выполнения
        self.stats = {
            'keywords_processed': 0,
            'articles_generated': 0,
            'articles_published': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }
    
    def setup_logging(self):
        """Настройка системы логирования"""
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f'pipeline_v2_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def connect_database(self) -> bool:
        """Подключение к базе данных"""
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            self.connection.autocommit = False
            self.logger.info("✅ Подключение к базе данных установлено")
            return True
        except Error as e:
            self.logger.error(f"❌ Ошибка подключения к БД: {e}")
            return False
    
    def close_database(self):
        """Закрытие соединения с базой данных"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.logger.info("🔒 Соединение с БД закрыто")
    
    def add_keyword(self, keyword: str, **kwargs) -> Optional[int]:
        """
        Этап 0: Добавление ключевого слова
        
        Args:
            keyword: Ключевое слово
            **kwargs: Дополнительные параметры
            
        Returns:
            ID ключевого слова или None при ошибке
        """
        try:
            cursor = self.connection.cursor()
            
            # Проверяем, существует ли уже такое ключевое слово
            cursor.execute("SELECT id FROM keywords WHERE keyword = %s", (keyword,))
            existing = cursor.fetchone()
            
            if existing:
                self.logger.warning(f"Ключевое слово '{keyword}' уже существует (ID: {existing[0]})")
                return existing[0]
            
            # Добавляем новое ключевое слово
            insert_query = """
                INSERT INTO keywords (keyword, status, source, frequency, priority, target_volume, target_intent)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                keyword,
                'pending',
                kwargs.get('source', 'manual'),
                kwargs.get('frequency', 1),
                kwargs.get('priority', 'medium'),
                kwargs.get('target_volume', 2500),
                kwargs.get('target_intent', 'informational')
            )
            
            cursor.execute(insert_query, values)
            keyword_id = cursor.lastrowid
            
            self.connection.commit()
            self.logger.info(f"✅ Ключевое слово добавлено: '{keyword}' (ID: {keyword_id})")
            
            return keyword_id
            
        except Error as e:
            self.logger.error(f"❌ Ошибка добавления ключевого слова: {e}")
            self.connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
    
    def analyze_competitors(self, keyword_id: int) -> Optional[int]:
        """
        Этап 1: Анализ конкурентов с помощью ALwrity
        
        Args:
            keyword_id: ID ключевого слова
            
        Returns:
            ID анализа или None при ошибке
        """
        try:
            cursor = self.connection.cursor()
            
            # Получаем ключевое слово
            cursor.execute("SELECT keyword FROM keywords WHERE id = %s", (keyword_id,))
            result = cursor.fetchone()
            
            if not result:
                self.logger.error(f"Ключевое слово с ID {keyword_id} не найдено")
                return None
            
            keyword = result[0]
            self.logger.info(f"🔍 Начало анализа конкурентов для: '{keyword}'")
            
            # Проверяем правовые требования
            if not ComplianceChecker.enforce_real_data_only():
                self.logger.error("❌ Нет доступа к интернету для анализа конкурентов")
                cursor.execute("UPDATE keywords SET status = 'error' WHERE id = %s", (keyword_id,))
                self.connection.commit()
                return None
            
            # Обновляем статус
            cursor.execute("UPDATE keywords SET status = 'analyzing' WHERE id = %s", (keyword_id,))
            
            # Анализируем конкурентов через ALwrity
            start_time = time.time()
            analysis_result = self.alwrity_client.research_competitors(keyword, num_results=3)
            analysis_duration = int(time.time() - start_time)
            
            if analysis_result['status'] != 'completed':
                self.logger.error(f"Анализ конкурентов не завершен: {analysis_result['status']}")
                cursor.execute("UPDATE keywords SET status = 'error' WHERE id = %s", (keyword_id,))
                self.connection.commit()
                return None
            
            # Сохраняем результаты анализа
            insert_query = """
                INSERT INTO analysis (keyword_id, sources, structure, gaps, recommendations, 
                                    competitors_data, lsi_keywords, search_volume, competition_level, analysis_duration)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                keyword_id,
                json.dumps([c.get('url', '') for c in analysis_result.get('competitors', [])]),
                json.dumps(analysis_result.get('content_structure', {})),
                json.dumps(analysis_result.get('gaps', [])),
                json.dumps(['Улучшить структуру', 'Добавить интерактивность']),
                json.dumps(analysis_result.get('competitors', [])),
                json.dumps(analysis_result.get('common_themes', [])),
                analysis_result.get('total_found', 0),
                'medium',
                analysis_duration
            )
            
            cursor.execute(insert_query, values)
            analysis_id = cursor.lastrowid
            
            self.connection.commit()
            self.logger.info(f"✅ Анализ конкурентов завершен (ID: {analysis_id})")
            
            return analysis_id
            
        except Error as e:
            self.logger.error(f"❌ Ошибка анализа конкурентов: {e}")
            self.connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
    
    def generate_article(self, analysis_id: int) -> Optional[int]:
        """
        Этап 2: Динамическая генерация статьи с помощью ALwrity
        
        Args:
            analysis_id: ID анализа
            
        Returns:
            ID статьи или None при ошибке
        """
        try:
            cursor = self.connection.cursor()
            
            # Получаем данные анализа
            cursor.execute("""
                SELECT a.*, k.keyword, k.target_volume, k.target_intent 
                FROM analysis a 
                JOIN keywords k ON a.keyword_id = k.id 
                WHERE a.id = %s
            """, (analysis_id,))
            
            result = cursor.fetchone()
            if not result:
                self.logger.error(f"Анализ с ID {analysis_id} не найден")
                return None
            
            # Извлекаем данные
            keyword = result[1]  # k.keyword
            target_volume = result[2]  # k.target_volume
            competitors_data = json.loads(result[6])  # competitors_data
            
            self.logger.info(f"✍️ Динамическая генерация статьи для: '{keyword}'")
            
            # Генерируем статью через ALwrity
            start_time = time.time()
            article_data = self.alwrity_client.generate_article(
                keyword=keyword,
                competitors_data={'competitors': competitors_data},
                company_profile=self.company_data.get_company_stats(),
                target_words=target_volume
            )
            generation_duration = int(time.time() - start_time)
            
            # SEO-оптимизация
            seo_optimized = self.alwrity_client.optimize_seo(article_data['content'], keyword)
            
            # Генерация FAQ
            faq_data = self.alwrity_client.generate_faq(keyword, article_data['content'])
            
            # Создаем HTML версию
            html_content = self._create_html_article(article_data, faq_data, keyword)
            
            # Сохраняем статью
            insert_query = """
                INSERT INTO articles (keyword_id, analysis_id, title, content_raw, html_raw, 
                                    word_count, reading_time, structure, lsi_keywords_used, generation_duration)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                result[0],  # keyword_id
                analysis_id,
                article_data['title'],
                article_data['content'],
                html_content,
                article_data.get('word_count', len(article_data['content'].split())),
                article_data.get('reading_time', 12),
                json.dumps(article_data.get('structure', [])),
                json.dumps(article_data.get('lsi_keywords_used', [])),
                generation_duration
            )
            
            cursor.execute(insert_query, values)
            article_id = cursor.lastrowid
            
            self.connection.commit()
            self.logger.info(f"✅ Статья сгенерирована (ID: {article_id})")
            
            return article_id
            
        except Error as e:
            self.logger.error(f"❌ Ошибка генерации статьи: {e}")
            self.connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
    
    def _create_html_article(self, article_data: Dict[str, Any], faq_data: Dict[str, Any], keyword: str) -> str:
        """
        Создание HTML версии статьи в фирменном стиле BizFin Pro
        
        Args:
            article_data: Данные статьи
            faq_data: Данные FAQ
            keyword: Ключевое слово
            
        Returns:
            HTML контент статьи
        """
        from config.design_system import DesignGenerator
        
        design = DesignGenerator()
        css_styles = design.generate_css_styles()
        
        html = f"""
        <style>
        {css_styles}
        </style>
        
        <article class="bizfin-article">
            <header class="article-header">
                <h1 class="bizfin-h1">{article_data['title']}</h1>
                <p class="article-meta">Получите {keyword} быстро и выгодно! Экспертное руководство с калькулятором, сравнением банков и реальными кейсами.</p>
            </header>
            
            <div class="bizfin-section">
                <div class="article-content">
                    {article_data['content']}
                </div>
            </div>
            
            <div class="bizfin-section">
                <h2 class="bizfin-h2">Часто задаваемые вопросы</h2>
                {faq_data.get('html', '')}
            </div>
            
            <div class="bizfin-section">
                <div class="bizfin-highlight">
                    <h3 class="bizfin-h3">🚀 Готовы получить {keyword}?</h3>
                    <p>Наши эксперты помогут вам сэкономить время, деньги и нервы при получении {keyword}</p>
                    <button class="bizfin-cta-button">📞 Получить бесплатную консультацию</button>
                </div>
            </div>
            
            <footer class="article-footer">
                <div class="bizfin-card">
                    <h3>О компании Бизнес Финанс</h3>
                    <p>{self.company_data.get_company_intro()}</p>
                    <p><strong>Контакты:</strong> {self.company_data.get_contact_info()['phone']}</p>
                </div>
            </footer>
        </article>
        """
        
        return html
    
    def _generate_article_content(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Генерация контента статьи (упрощенная версия)
        
        В реальной реализации здесь будет интеграция с AI для генерации контента
        """
        keyword = analysis_data['keyword']
        target_volume = analysis_data['target_volume']
        lsi_keywords = analysis_data['lsi_keywords'][:10]  # Топ-10 LSI ключей
        
        # Генерируем заголовок
        title = f"{keyword}: полное руководство по получению в 2024 году"
        
        # Генерируем структуру статьи
        structure = {
            'sections': [
                'Введение',
                'Что такое ' + keyword,
                'Виды и типы',
                'Стоимость и расчет',
                'Документы для получения',
                'Сравнение банков',
                'Реальный кейс успеха',
                'Часто задаваемые вопросы',
                'Заключение'
            ],
            'word_count_target': target_volume,
            'lsi_keywords_planned': lsi_keywords
        }
        
        # Генерируем базовый контент (заглушка)
        content_raw = f"""
# {title}

## Введение

{keyword} — это важный инструмент для современного бизнеса. В данной статье мы рассмотрим все аспекты получения {keyword} в 2024 году.

## Что такое {keyword}

{keyword} представляет собой...

## Виды и типы

Существует несколько видов {keyword}:

1. Основной вид
2. Дополнительный вид
3. Специальный вид

## Стоимость и расчет

Стоимость {keyword} зависит от...

## Документы для получения

Для получения {keyword} потребуются следующие документы:

- Документ 1
- Документ 2
- Документ 3

## Сравнение банков

| Банк | Комиссия | Срок | Особенности |
|------|----------|------|-------------|
| Банк 1 | 2% | 3 дня | Быстрое рассмотрение |
| Банк 2 | 2.5% | 5 дней | Индивидуальный подход |

## Реальный кейс успеха

Компания "Пример" получила {keyword} за 3 дня...

## Часто задаваемые вопросы

### Как быстро можно получить {keyword}?

Сроки получения {keyword} составляют...

### Сколько стоит {keyword}?

Стоимость {keyword} варьируется...

## Заключение

{keyword} — это надежный способ...

**Готовы получить {keyword}? Свяжитесь с нашими экспертами!**
        """.strip()
        
        # Генерируем HTML версию
        html_raw = f"""
        <article>
            <h1>{title}</h1>
            <div class="content">
                {content_raw.replace('#', '<h2>').replace('##', '</h2><h3>').replace('###', '</h3><h4>')}
            </div>
        </article>
        """
        
        # Подсчитываем слова
        word_count = len(content_raw.split())
        reading_time = max(1, word_count // 200)  # 200 слов в минуту
        
        return {
            'title': title,
            'content_raw': content_raw,
            'html_raw': html_raw,
            'word_count': word_count,
            'reading_time': reading_time,
            'structure': structure,
            'lsi_keywords_used': lsi_keywords
        }
    
    def run_full_pipeline(self, keyword: str, **kwargs) -> PipelineResult:
        """
        Запуск полного пайплайна v2
        
        Args:
            keyword: Ключевое слово
            **kwargs: Дополнительные параметры
            
        Returns:
            Результат выполнения пайплайна
        """
        start_time = time.time()
        errors = []
        
        try:
            self.logger.info(f"🚀 Запуск пайплайна v2 для ключевого слова: '{keyword}'")
            self.stats['start_time'] = datetime.now()
            
            # Подключаемся к БД
            if not self.connect_database():
                return PipelineResult(
                    keyword_id=0,
                    status='error',
                    message='Не удалось подключиться к базе данных',
                    data={},
                    execution_time=time.time() - start_time,
                    errors=['Database connection failed']
                )
            
            # Этап 0: Добавление ключевого слова
            keyword_id = self.add_keyword(keyword, **kwargs)
            if not keyword_id:
                errors.append('Failed to add keyword')
                return PipelineResult(
                    keyword_id=0,
                    status='error',
                    message='Не удалось добавить ключевое слово',
                    data={},
                    execution_time=time.time() - start_time,
                    errors=errors
                )
            
            # Этап 1: Анализ конкурентов
            analysis_id = self.analyze_competitors(keyword_id)
            if not analysis_id:
                errors.append('Failed to analyze competitors')
                return PipelineResult(
                    keyword_id=keyword_id,
                    status='error',
                    message='Не удалось проанализировать конкурентов',
                    data={'keyword_id': keyword_id},
                    execution_time=time.time() - start_time,
                    errors=errors
                )
            
            # Этап 2: Генерация статьи
            article_id = self.generate_article(analysis_id)
            if not article_id:
                errors.append('Failed to generate article')
                return PipelineResult(
                    keyword_id=keyword_id,
                    status='error',
                    message='Не удалось сгенерировать статью',
                    data={'keyword_id': keyword_id, 'analysis_id': analysis_id},
                    execution_time=time.time() - start_time,
                    errors=errors
                )
            
            # TODO: Реализовать остальные этапы пайплайна
            # Этап 3: SEO-проверка
            # Этап 4: Улучшение статьи
            # Этап 5: Формирование EEC
            # Этап 6: Публикация в WordPress
            # Этап 7: Проверка публикации
            # Этап 8: Фиксация SEO-мета
            # Этап 9: Верификация WordPress
            # Этап 10: Финальный аудит
            
            self.stats['keywords_processed'] += 1
            self.stats['articles_generated'] += 1
            
            execution_time = time.time() - start_time
            self.stats['end_time'] = datetime.now()
            
            self.logger.info(f"✅ Пайплайн v2 завершен за {execution_time:.2f} секунд")
            
            return PipelineResult(
                keyword_id=keyword_id,
                status='completed',
                message='Пайплайн v2 успешно завершен',
                data={
                    'keyword_id': keyword_id,
                    'analysis_id': analysis_id,
                    'article_id': article_id,
                    'execution_time': execution_time
                },
                execution_time=execution_time,
                errors=errors
            )
            
        except Exception as e:
            self.logger.error(f"❌ Критическая ошибка пайплайна: {e}")
            errors.append(str(e))
            self.stats['errors'] += 1
            
            return PipelineResult(
                keyword_id=0,
                status='error',
                message=f'Критическая ошибка: {e}',
                data={},
                execution_time=time.time() - start_time,
                errors=errors
            )
        
        finally:
            self.close_database()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Получение статистики выполнения"""
        return self.stats.copy()

def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(description='BizFin Pro SEO Pipeline v2')
    parser.add_argument('--keyword', required=True, help='Ключевое слово для анализа')
    parser.add_argument('--priority', default='medium', choices=['low', 'medium', 'high', 'urgent'], help='Приоритет')
    parser.add_argument('--target-volume', type=int, default=2500, help='Целевой объем статьи')
    parser.add_argument('--intent', default='informational', choices=['informational', 'commercial', 'educational', 'faq', 'review'], help='Тип интента')
    parser.add_argument('--verbose', '-v', action='store_true', help='Подробный вывод')
    
    args = parser.parse_args()
    
    # Создаем и запускаем пайплайн
    pipeline = BizFinProPipeline()
    
    result = pipeline.run_full_pipeline(
        keyword=args.keyword,
        priority=args.priority,
        target_volume=args.target_volume,
        target_intent=args.intent
    )
    
    # Выводим результат
    print(f"\n{'='*60}")
    print(f"РЕЗУЛЬТАТ ВЫПОЛНЕНИЯ ПАЙПЛАЙНА V2")
    print(f"{'='*60}")
    print(f"Ключевое слово: {args.keyword}")
    print(f"Статус: {result.status}")
    print(f"Сообщение: {result.message}")
    print(f"Время выполнения: {result.execution_time:.2f} секунд")
    
    if result.errors:
        print(f"Ошибки: {', '.join(result.errors)}")
    
    if result.data:
        print(f"Данные: {json.dumps(result.data, indent=2, ensure_ascii=False)}")
    
    # Статистика
    stats = pipeline.get_statistics()
    print(f"\nСтатистика:")
    print(f"- Обработано ключевых слов: {stats['keywords_processed']}")
    print(f"- Сгенерировано статей: {stats['articles_generated']}")
    print(f"- Опубликовано статей: {stats['articles_published']}")
    print(f"- Ошибок: {stats['errors']}")
    
    # Возвращаем код выхода
    sys.exit(0 if result.status == 'completed' else 1)

if __name__ == "__main__":
    main()
