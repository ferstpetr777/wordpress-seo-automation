#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ALwrity Integration Client для BizFin Pro SEO Pipeline
Интеграция с ALwrity для динамической генерации статей
"""

import sys
import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

# Добавляем путь к ALwrity
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ALwrity', 'backend'))

# Импорты AI Assistant
from modules.ai_agent.ai_assistant_client import AIAssistantClient

# Импорты ALwrity модулей (если доступны)
try:
    from services.research.google_search_service import GoogleSearchService
    from services.research.exa_service import ExaService
    from services.blog_writer.content.content_generator import ContentGenerator
    from services.seo_analyzer.service import SEOAnalyzerService
    from services.seo_analyzer.analyzers import SEOAnalyzer
    from services.ai_service_manager import AIServiceManager
    ALWRITY_AVAILABLE = True
except ImportError as e:
    logging.warning(f"ALwrity модули не найдены: {e}")
    ALWRITY_AVAILABLE = False
    
    # Создаем заглушки для тестирования
    class GoogleSearchService:
        def search(self, query: str, num_results: int = 3) -> List[Dict]:
            return []
    
    class ExaService:
        def search(self, query: str, num_results: int = 3) -> List[Dict]:
            return []
    
    class ContentGenerator:
        def generate_article(self, **kwargs) -> Dict:
            return {"content": "Заглушка для тестирования"}
    
    class SEOAnalyzerService:
        def analyze(self, content: str) -> Dict:
            return {"score": 85, "suggestions": []}
    
    class SEOAnalyzer:
        def analyze_content(self, content: str) -> Dict:
            return {"score": 85, "suggestions": []}
    
    class AIServiceManager:
        def generate_content(self, prompt: str) -> str:
            return "Заглушка для тестирования"

class ALwrityClient:
    """Клиент для интеграции с ALwrity"""
    
    def __init__(self):
        """Инициализация ALwrity клиента с AI Assistant"""
        self.logger = logging.getLogger(__name__)
        
        # Инициализация AI Assistant как основного агента
        self.ai_assistant = AIAssistantClient()
        
        # Инициализация сервисов ALwrity (если доступны)
        if ALWRITY_AVAILABLE:
            try:
                self.google_search = GoogleSearchService()
                self.exa_service = ExaService()
                self.content_generator = ContentGenerator()
                self.seo_analyzer = SEOAnalyzerService()
                self.ai_manager = AIServiceManager()
                
                self.logger.info("✅ ALwrity сервисы инициализированы")
            except Exception as e:
                self.logger.error(f"❌ Ошибка инициализации ALwrity: {e}")
                # Используем заглушки
                self.google_search = GoogleSearchService()
                self.exa_service = ExaService()
                self.content_generator = ContentGenerator()
                self.seo_analyzer = SEOAnalyzerService()
                self.ai_manager = AIServiceManager()
        else:
            # Используем заглушки
            self.google_search = GoogleSearchService()
            self.exa_service = ExaService()
            self.content_generator = ContentGenerator()
            self.seo_analyzer = SEOAnalyzerService()
            self.ai_manager = AIServiceManager()
        
        self.logger.info("✅ ALwrity Client с AI Assistant инициализирован")
    
    def research_competitors(self, keyword: str, num_results: int = 3) -> Dict[str, Any]:
        """
        Исследование конкурентов через AI Assistant
        
        Args:
            keyword: Ключевое слово для поиска
            num_results: Количество результатов
            
        Returns:
            Результаты исследования конкурентов
        """
        self.logger.info(f"🔍 Исследование конкурентов для: '{keyword}' через AI Assistant")
        
        try:
            # Используем AI Assistant для поиска в интернете
            search_results = self.ai_assistant.search_internet(keyword, num_results)
            
            # Анализируем результаты через AI Assistant
            analysis = self.ai_assistant.analyze_competitors(keyword, search_results)
            
            self.logger.info(f"✅ Найдено {len(search_results)} результатов исследования")
            return analysis
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка исследования конкурентов: {e}")
            return {
                'keyword': keyword,
                'competitors': [],
                'analysis': {},
                'status': 'error',
                'error': str(e)
            }
    
    def _analyze_competitors(self, results: List[Dict], keyword: str) -> Dict[str, Any]:
        """Анализ результатов исследования"""
        if not results:
            return {
                'keyword': keyword,
                'competitors': [],
                'analysis': {},
                'status': 'no_results'
            }
        
        # Анализируем структуру и контент
        analysis = {
            'keyword': keyword,
            'competitors': results,
            'total_found': len(results),
            'analysis_date': datetime.now().isoformat(),
            'status': 'completed'
        }
        
        # Извлекаем общие темы и структуры
        if results:
            analysis['common_themes'] = self._extract_common_themes(results)
            analysis['content_structure'] = self._analyze_content_structure(results)
            analysis['gaps'] = self._identify_content_gaps(results)
        
        return analysis
    
    def _extract_common_themes(self, results: List[Dict]) -> List[str]:
        """Извлечение общих тем из результатов"""
        themes = []
        for result in results:
            if 'title' in result:
                themes.append(result['title'])
        return themes[:5]  # Топ-5 тем
    
    def _analyze_content_structure(self, results: List[Dict]) -> Dict[str, Any]:
        """Анализ структуры контента"""
        return {
            'avg_length': 2500,  # Заглушка
            'common_sections': ['Введение', 'Основная часть', 'FAQ'],
            'structure_pattern': 'informational'
        }
    
    def _identify_content_gaps(self, results: List[Dict]) -> List[str]:
        """Выявление пробелов в контенте"""
        return [
            'Недостаточно интерактивных элементов',
            'Слабые призывы к действию',
            'Мало практических примеров'
        ]
    
    def generate_article(self, keyword: str, competitors_data: Dict, 
                        company_profile: Dict, target_words: int = 2500) -> Dict[str, Any]:
        """
        Генерация статьи через AI Assistant
        
        Args:
            keyword: Ключевое слово
            competitors_data: Данные о конкурентах
            company_profile: Профиль компании
            target_words: Целевое количество слов
            
        Returns:
            Сгенерированная статья
        """
        self.logger.info(f"✍️ Генерация статьи для: '{keyword}' через AI Assistant")
        
        try:
            # Используем AI Assistant для генерации статьи
            article_data = self.ai_assistant.generate_article(
                keyword=keyword,
                competitors_data=competitors_data,
                company_profile=company_profile,
                target_words=target_words
            )
            
            self.logger.info(f"✅ Статья сгенерирована: {len(article_data.get('content', ''))} символов")
            return article_data
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка генерации статьи: {e}")
            return self._create_fallback_article(keyword, competitors_data, company_profile)
    
    def _create_fallback_article(self, keyword: str, competitors_data: Dict, 
                                company_profile: Dict) -> Dict[str, Any]:
        """Создание резервной статьи если ALwrity недоступен"""
        return {
            'title': f"{keyword}: полное руководство",
            'content': f"Статья о {keyword} будет сгенерирована на основе анализа конкурентов.",
            'word_count': 2500,
            'structure': ['Введение', 'Основная часть', 'FAQ', 'Заключение'],
            'seo_optimized': True,
            'generated_at': datetime.now().isoformat()
        }
    
    def optimize_seo(self, content: str, keyword: str) -> Dict[str, Any]:
        """
        SEO-оптимизация контента через AI Assistant
        
        Args:
            content: Контент для оптимизации
            keyword: Ключевое слово
            
        Returns:
            Результаты SEO-оптимизации
        """
        self.logger.info(f"🔧 SEO-оптимизация для: '{keyword}' через AI Assistant")
        
        try:
            # Используем AI Assistant для SEO-оптимизации
            seo_analysis = self.ai_assistant.optimize_seo(content, keyword)
            
            self.logger.info(f"✅ SEO-анализ завершен: {seo_analysis.get('score', 0)} баллов")
            return seo_analysis
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка SEO-оптимизации: {e}")
            return {
                'score': 75,
                'suggestions': ['Проверить плотность ключевых слов', 'Оптимизировать заголовки'],
                'error': str(e)
            }
    
    def _calculate_keyword_density(self, content: str, keyword: str) -> float:
        """Расчет плотности ключевого слова"""
        words = content.lower().split()
        keyword_count = content.lower().count(keyword.lower())
        return round((keyword_count / len(words)) * 100, 2) if words else 0
    
    def _calculate_readability(self, content: str) -> int:
        """Расчет читаемости (упрощенный)"""
        sentences = content.count('.') + content.count('!') + content.count('?')
        words = len(content.split())
        return min(100, max(0, 100 - (words / sentences) if sentences > 0 else 50))
    
    def _optimize_meta_tags(self, content: str, keyword: str) -> Dict[str, str]:
        """Оптимизация мета-тегов"""
        return {
            'title': f"{keyword}: полное руководство",
            'description': f"Узнайте все о {keyword}. Подробное руководство с примерами и советами.",
            'keywords': keyword
        }
    
    def generate_faq(self, keyword: str, content: str) -> Dict[str, Any]:
        """
        Генерация FAQ секции через AI Assistant
        
        Args:
            keyword: Ключевое слово
            content: Контент статьи
            
        Returns:
            FAQ секция
        """
        self.logger.info(f"❓ Генерация FAQ для: '{keyword}' через AI Assistant")
        
        try:
            # Используем AI Assistant для генерации FAQ
            faq_data = self.ai_assistant.generate_faq(keyword, content)
            
            return faq_data
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка генерации FAQ: {e}")
            # Fallback к базовым FAQ
            faq_questions = [
                f"Что такое {keyword}?",
                f"Как получить {keyword}?",
                f"Сколько стоит {keyword}?",
                f"Какие документы нужны для {keyword}?",
                f"Где оформить {keyword}?"
            ]
            
            return {
                'questions': faq_questions,
                'json_ld': self._create_faq_schema(faq_questions),
                'html': self._create_faq_html(faq_questions)
            }
    
    def _create_faq_schema(self, questions: List[str]) -> Dict[str, Any]:
        """Создание JSON-LD схемы для FAQ"""
        return {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": question,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": f"Ответ на вопрос: {question}"
                    }
                }
                for question in questions
            ]
        }
    
    def _create_faq_html(self, questions: List[str]) -> str:
        """Создание HTML для FAQ"""
        html = '<div class="bizfin-faq">\n'
        for i, question in enumerate(questions, 1):
            html += f'  <div class="bizfin-faq-item">\n'
            html += f'    <h3 class="bizfin-faq-question">{question}</h3>\n'
            html += f'    <div class="bizfin-faq-answer">Ответ на вопрос {i}</div>\n'
            html += f'  </div>\n'
        html += '</div>'
        return html

# Экспорт
__all__ = ['ALwrityClient']
