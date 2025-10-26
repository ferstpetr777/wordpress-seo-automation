#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль анализа конкурентов для BizFin Pro SEO Pipeline
КРИТИЧЕСКИ ВАЖНО: Только реальные данные из интернета! Симуляция запрещена!
"""

import requests
import json
import time
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from dataclasses import dataclass
from datetime import datetime
import logging
import sys
import os

# Добавляем путь к конфигурации
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from config.legal_compliance import LegalCompliance, ComplianceChecker

@dataclass
class CompetitorData:
    """Данные о конкуренте"""
    url: str
    title: str
    meta_description: str
    h1: str
    word_count: int
    structure: Dict[str, Any]
    lsi_keywords: List[str]
    internal_links: List[str]
    external_links: List[str]
    images_count: int
    faq_count: int
    cta_count: int
    reading_time: int
    domain: str
    analysis_date: datetime

class CompetitorAnalyzer:
    """Анализатор конкурентов"""
    
    def __init__(self, max_competitors: int = 3, delay: float = 1.0):
        """
        Инициализация анализатора
        
        Args:
            max_competitors: Максимальное количество конкурентов для анализа
            delay: Задержка между запросами (секунды)
        """
        self.max_competitors = max_competitors
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Настройка логирования
        self.logger = logging.getLogger(__name__)
        
        # Правовые требования
        self.compliance = LegalCompliance()
        self.retry_count = 0
        self.max_retries = self.compliance.RETRY_SETTINGS['max_retries']
    
    def search_competitors(self, keyword: str, search_engines: List[str] = None) -> List[str]:
        """
        Поиск конкурентов по ключевому слову
        КРИТИЧЕСКИ ВАЖНО: Только реальные данные из интернета!
        
        Args:
            keyword: Ключевое слово для поиска
            search_engines: Список поисковых систем
            
        Returns:
            Список URL конкурентов
        """
        # Проверяем доступ к интернету
        if not ComplianceChecker.check_internet_access():
            ComplianceChecker.notify_user(
                self.compliance.USER_NOTIFICATIONS["no_internet_access"], 
                critical=True
            )
            return []
        
        if search_engines is None:
            search_engines = ['google', 'yandex']
        
        competitors = []
        
        for engine in search_engines:
            try:
                if engine == 'google':
                    urls = self._search_google(keyword)
                elif engine == 'yandex':
                    urls = self._search_yandex(keyword)
                else:
                    continue
                
                competitors.extend(urls)
                time.sleep(self.delay)
                
            except Exception as e:
                self.logger.error(f"Ошибка поиска в {engine}: {e}")
                # Повторный запрос при ошибке
                if self.retry_count < self.max_retries:
                    self.retry_count += 1
                    ComplianceChecker.notify_user(
                        self.compliance.USER_NOTIFICATIONS["retry_request"]
                    )
                    time.sleep(self.compliance.RETRY_SETTINGS['retry_delay'])
                    continue
                else:
                    self.logger.critical(f"Превышено максимальное количество попыток для {engine}")
                    continue
        
        # Удаляем дубликаты и ограничиваем количество
        unique_competitors = list(dict.fromkeys(competitors))[:self.max_competitors]
        
        if not unique_competitors:
            ComplianceChecker.notify_user(
                self.compliance.USER_NOTIFICATIONS["analysis_required"], 
                critical=True
            )
        
        self.logger.info(f"Найдено {len(unique_competitors)} уникальных конкурентов")
        return unique_competitors
    
    def _search_google(self, keyword: str) -> List[str]:
        """Поиск в Google"""
        try:
            # Используем простой поиск через requests
            search_url = f"https://www.google.com/search?q={keyword}&num=10"
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                urls = []
                
                # Ищем ссылки в результатах поиска
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if href.startswith('/url?q='):
                        url = href.split('/url?q=')[1].split('&')[0]
                        if self._is_valid_url(url):
                            urls.append(url)
                
                return urls[:5]  # Берем первые 5 результатов
            
        except Exception as e:
            self.logger.error(f"Ошибка поиска в Google: {e}")
        
        return []
    
    def _search_yandex(self, keyword: str) -> List[str]:
        """Поиск в Yandex"""
        try:
            search_url = f"https://yandex.ru/search/?text={keyword}&lr=213"
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                urls = []
                
                # Ищем ссылки в результатах Yandex
                for link in soup.find_all('a', class_='link'):
                    href = link.get('href')
                    if href and self._is_valid_url(href):
                        urls.append(href)
                
                return urls[:5]  # Берем первые 5 результатов
            
        except Exception as e:
            self.logger.error(f"Ошибка поиска в Yandex: {e}")
        
        return []
    
    def _is_valid_url(self, url: str) -> bool:
        """Проверка валидности URL"""
        try:
            parsed = urlparse(url)
            return bool(parsed.netloc) and parsed.scheme in ['http', 'https']
        except:
            return False
    
    def analyze_competitor(self, url: str) -> Optional[CompetitorData]:
        """
        Анализ отдельного конкурента
        
        Args:
            url: URL для анализа
            
        Returns:
            Данные о конкуренте или None при ошибке
        """
        try:
            self.logger.info(f"Анализ конкурента: {url}")
            
            response = self.session.get(url, timeout=15)
            if response.status_code != 200:
                self.logger.warning(f"Не удалось загрузить {url}: {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Извлекаем основные данные
            title = self._extract_title(soup)
            meta_description = self._extract_meta_description(soup)
            h1 = self._extract_h1(soup)
            word_count = self._count_words(soup)
            structure = self._analyze_structure(soup)
            lsi_keywords = self._extract_lsi_keywords(soup)
            internal_links = self._extract_internal_links(soup, url)
            external_links = self._extract_external_links(soup, url)
            images_count = len(soup.find_all('img'))
            faq_count = self._count_faq(soup)
            cta_count = self._count_cta(soup)
            reading_time = self._calculate_reading_time(word_count)
            
            competitor_data = CompetitorData(
                url=url,
                title=title,
                meta_description=meta_description,
                h1=h1,
                word_count=word_count,
                structure=structure,
                lsi_keywords=lsi_keywords,
                internal_links=internal_links,
                external_links=external_links,
                images_count=images_count,
                faq_count=faq_count,
                cta_count=cta_count,
                reading_time=reading_time,
                domain=urlparse(url).netloc,
                analysis_date=datetime.now()
            )
            
            self.logger.info(f"Анализ завершен: {word_count} слов, {len(lsi_keywords)} LSI ключей")
            return competitor_data
            
        except Exception as e:
            self.logger.error(f"Ошибка анализа {url}: {e}")
            return None
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Извлечение заголовка страницы"""
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else ""
    
    def _extract_meta_description(self, soup: BeautifulSoup) -> str:
        """Извлечение мета-описания"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        return meta_desc.get('content', '').strip() if meta_desc else ""
    
    def _extract_h1(self, soup: BeautifulSoup) -> str:
        """Извлечение H1 заголовка"""
        h1_tag = soup.find('h1')
        return h1_tag.get_text().strip() if h1_tag else ""
    
    def _count_words(self, soup: BeautifulSoup) -> int:
        """Подсчет слов в тексте"""
        # Удаляем скрипты и стили
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        words = re.findall(r'\b\w+\b', text.lower())
        return len(words)
    
    def _analyze_structure(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Анализ структуры страницы"""
        structure = {
            'headings': {},
            'sections': [],
            'lists': 0,
            'tables': 0,
            'forms': 0
        }
        
        # Анализ заголовков
        for i in range(1, 7):
            headings = soup.find_all(f'h{i}')
            structure['headings'][f'h{i}'] = len(headings)
        
        # Анализ секций
        sections = soup.find_all(['section', 'article', 'div'], class_=re.compile(r'section|content|main'))
        structure['sections'] = [section.get('class', []) for section in sections[:10]]
        
        # Подсчет элементов
        structure['lists'] = len(soup.find_all(['ul', 'ol']))
        structure['tables'] = len(soup.find_all('table'))
        structure['forms'] = len(soup.find_all('form'))
        
        return structure
    
    def _extract_lsi_keywords(self, soup: BeautifulSoup) -> List[str]:
        """Извлечение LSI ключевых слов"""
        # Удаляем скрипты и стили
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text().lower()
        
        # Ищем часто встречающиеся слова (простая реализация)
        words = re.findall(r'\b[а-яё]{4,}\b', text)
        word_freq = {}
        
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Возвращаем топ-10 наиболее частых слов
        lsi_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        return [word for word, freq in lsi_keywords if freq > 2]
    
    def _extract_internal_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Извлечение внутренних ссылок"""
        base_domain = urlparse(base_url).netloc
        internal_links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            parsed_url = urlparse(full_url)
            
            if parsed_url.netloc == base_domain:
                internal_links.append(full_url)
        
        return list(set(internal_links))[:20]  # Максимум 20 ссылок
    
    def _extract_external_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Извлечение внешних ссылок"""
        base_domain = urlparse(base_url).netloc
        external_links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            parsed_url = urlparse(full_url)
            
            if parsed_url.netloc != base_domain and parsed_url.netloc:
                external_links.append(full_url)
        
        return list(set(external_links))[:10]  # Максимум 10 ссылок
    
    def _count_faq(self, soup: BeautifulSoup) -> int:
        """Подсчет FAQ секций"""
        faq_indicators = [
            'faq', 'вопрос', 'ответ', 'часто задаваемые',
            'question', 'answer', 'frequently asked'
        ]
        
        faq_count = 0
        text = soup.get_text().lower()
        
        for indicator in faq_indicators:
            faq_count += text.count(indicator)
        
        return faq_count
    
    def _count_cta(self, soup: BeautifulSoup) -> int:
        """Подсчет CTA элементов"""
        cta_indicators = [
            'заказать', 'купить', 'получить', 'связаться',
            'консультация', 'звонок', 'заявка', 'оставить',
            'order', 'buy', 'get', 'contact', 'consultation'
        ]
        
        cta_count = 0
        text = soup.get_text().lower()
        
        for indicator in cta_indicators:
            cta_count += text.count(indicator)
        
        return cta_count
    
    def _calculate_reading_time(self, word_count: int) -> int:
        """Расчет времени чтения в минутах"""
        # Средняя скорость чтения: 200 слов в минуту
        return max(1, word_count // 200)
    
    def analyze_keyword(self, keyword: str) -> Dict[str, Any]:
        """
        Полный анализ ключевого слова
        
        Args:
            keyword: Ключевое слово для анализа
            
        Returns:
            Результаты анализа
        """
        self.logger.info(f"Начало анализа ключевого слова: {keyword}")
        
        # Поиск конкурентов
        competitor_urls = self.search_competitors(keyword)
        
        if not competitor_urls:
            self.logger.warning("Конкуренты не найдены")
            return {
                'keyword': keyword,
                'competitors': [],
                'analysis_date': datetime.now(),
                'status': 'no_competitors'
            }
        
        # Анализ каждого конкурента
        competitors_data = []
        for url in competitor_urls:
            competitor_data = self.analyze_competitor(url)
            if competitor_data:
                competitors_data.append(competitor_data)
            time.sleep(self.delay)
        
        # Анализ результатов
        analysis_result = self._analyze_results(keyword, competitors_data)
        
        self.logger.info(f"Анализ завершен: {len(competitors_data)} конкурентов проанализировано")
        return analysis_result
    
    def _analyze_results(self, keyword: str, competitors: List[CompetitorData]) -> Dict[str, Any]:
        """Анализ результатов исследования"""
        if not competitors:
            return {
                'keyword': keyword,
                'competitors': [],
                'analysis_date': datetime.now(),
                'status': 'no_data'
            }
        
        # Статистика
        avg_word_count = sum(c.word_count for c in competitors) / len(competitors)
        avg_reading_time = sum(c.reading_time for c in competitors) / len(competitors)
        avg_images = sum(c.images_count for c in competitors) / len(competitors)
        avg_faq = sum(c.faq_count for c in competitors) / len(competitors)
        avg_cta = sum(c.cta_count for c in competitors) / len(competitors)
        
        # Общие LSI ключевые слова
        all_lsi = []
        for competitor in competitors:
            all_lsi.extend(competitor.lsi_keywords)
        
        # Топ LSI ключевые слова
        lsi_freq = {}
        for word in all_lsi:
            lsi_freq[word] = lsi_freq.get(word, 0) + 1
        
        top_lsi = sorted(lsi_freq.items(), key=lambda x: x[1], reverse=True)[:15]
        
        # Выявленные пробелы
        gaps = self._identify_gaps(competitors)
        
        # Рекомендации
        recommendations = self._generate_recommendations(competitors, gaps)
        
        return {
            'keyword': keyword,
            'competitors': [
                {
                    'url': c.url,
                    'title': c.title,
                    'meta_description': c.meta_description,
                    'h1': c.h1,
                    'word_count': c.word_count,
                    'reading_time': c.reading_time,
                    'images_count': c.images_count,
                    'faq_count': c.faq_count,
                    'cta_count': c.cta_count,
                    'lsi_keywords': c.lsi_keywords,
                    'structure': c.structure,
                    'domain': c.domain
                }
                for c in competitors
            ],
            'statistics': {
                'avg_word_count': int(avg_word_count),
                'avg_reading_time': int(avg_reading_time),
                'avg_images': int(avg_images),
                'avg_faq': int(avg_faq),
                'avg_cta': int(avg_cta),
                'total_competitors': len(competitors)
            },
            'lsi_keywords': [word for word, freq in top_lsi],
            'gaps': gaps,
            'recommendations': recommendations,
            'analysis_date': datetime.now(),
            'status': 'completed'
        }
    
    def _identify_gaps(self, competitors: List[CompetitorData]) -> List[str]:
        """Выявление пробелов у конкурентов"""
        gaps = []
        
        # Анализ длины статей
        word_counts = [c.word_count for c in competitors]
        if max(word_counts) < 2000:
            gaps.append("Короткие статьи (менее 2000 слов)")
        
        # Анализ FAQ
        faq_counts = [c.faq_count for c in competitors]
        if max(faq_counts) < 3:
            gaps.append("Недостаточно FAQ секций")
        
        # Анализ CTA
        cta_counts = [c.cta_count for c in competitors]
        if max(cta_counts) < 2:
            gaps.append("Недостаточно призывов к действию")
        
        # Анализ изображений
        image_counts = [c.images_count for c in competitors]
        if max(image_counts) < 5:
            gaps.append("Недостаточно визуального контента")
        
        return gaps
    
    def _generate_recommendations(self, competitors: List[CompetitorData], gaps: List[str]) -> List[str]:
        """Генерация рекомендаций"""
        recommendations = []
        
        # Рекомендации на основе пробелов
        if "Короткие статьи" in gaps:
            recommendations.append("Создать статью объемом 2500+ слов")
        
        if "Недостаточно FAQ" in gaps:
            recommendations.append("Добавить 5-7 FAQ вопросов")
        
        if "Недостаточно CTA" in gaps:
            recommendations.append("Добавить 3-4 призыва к действию")
        
        if "Недостаточно визуального контента" in gaps:
            recommendations.append("Добавить схемы, таблицы и изображения")
        
        # Общие рекомендации
        recommendations.extend([
            "Использовать LSI ключевые слова из анализа",
            "Создать интерактивные элементы (калькулятор, форма)",
            "Добавить реальные кейсы и примеры",
            "Оптимизировать для мобильных устройств"
        ])
        
        return recommendations
