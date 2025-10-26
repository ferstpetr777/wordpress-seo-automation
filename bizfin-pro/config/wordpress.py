#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Конфигурация WordPress для BizFin Pro SEO Pipeline
"""

import os
from typing import Dict, Any, List

class WordPressConfig:
    """Конфигурация подключения к WordPress"""
    
    # Основные настройки сайта
    SITE_URL = os.getenv('WP_SITE_URL', 'https://bizfin-pro.ru')
    API_URL = f"{SITE_URL}/wp-json/wp/v2"
    
    # Аутентификация
    USERNAME = os.getenv('WP_USERNAME', 'bizfin_pro_r')
    APP_PASSWORD = os.getenv('WP_APP_PASSWORD', 'U3Ep gU2T clRu FcwN QU6l Dsda')
    
    # Настройки API
    API_TIMEOUT = 30
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # секунды
    
    # Настройки публикации
    DEFAULT_STATUS = 'publish'
    DEFAULT_FORMAT = 'standard'
    DEFAULT_CATEGORY = 'Банковские гарантии'
    
    # Настройки SEO
    SEO_PLUGIN = 'yoast'  # yoast, rankmath, seopress
    FOCUS_KEYWORD_META = '_yoast_wpseo_focuskw'
    META_DESCRIPTION_META = '_yoast_wpseo_metadesc'
    TITLE_META = '_yoast_wpseo_title'
    
    # Настройки изображений
    IMAGE_QUALITY = 85
    MAX_IMAGE_SIZE = 1920  # пикселей
    SUPPORTED_FORMATS = ['jpg', 'jpeg', 'png', 'webp']
    
    # Настройки контента
    MAX_TITLE_LENGTH = 60
    MAX_META_DESCRIPTION_LENGTH = 160
    MIN_ARTICLE_LENGTH = 2000
    TARGET_ARTICLE_LENGTH = 2500
    
    @classmethod
    def get_auth_headers(cls) -> Dict[str, str]:
        """Получение заголовков аутентификации"""
        import base64
        credentials = f"{cls.USERNAME}:{cls.APP_PASSWORD}"
        token = base64.b64encode(credentials.encode()).decode('utf-8')
        
        return {
            'Authorization': f'Basic {token}',
            'Content-Type': 'application/json',
            'User-Agent': 'BizFin-Pro-SEO-Pipeline/2.0'
        }
    
    @classmethod
    def get_api_config(cls) -> Dict[str, Any]:
        """Получение конфигурации API"""
        return {
            'base_url': cls.API_URL,
            'timeout': cls.API_TIMEOUT,
            'max_retries': cls.MAX_RETRIES,
            'retry_delay': cls.RETRY_DELAY,
            'headers': cls.get_auth_headers()
        }
    
    @classmethod
    def get_publication_config(cls) -> Dict[str, Any]:
        """Получение конфигурации публикации"""
        return {
            'status': cls.DEFAULT_STATUS,
            'format': cls.DEFAULT_FORMAT,
            'category': cls.DEFAULT_CATEGORY,
            'seo_plugin': cls.SEO_PLUGIN
        }
    
    @classmethod
    def get_seo_meta_fields(cls) -> Dict[str, str]:
        """Получение полей SEO мета-данных"""
        if cls.SEO_PLUGIN == 'yoast':
            return {
                'focus_keyword': cls.FOCUS_KEYWORD_META,
                'meta_description': cls.META_DESCRIPTION_META,
                'title': cls.TITLE_META,
                'canonical': '_yoast_wpseo_canonical',
                'noindex': '_yoast_wpseo_meta-robots-noindex',
                'nofollow': '_yoast_wpseo_meta-robots-nofollow'
            }
        elif cls.SEO_PLUGIN == 'rankmath':
            return {
                'focus_keyword': '_rank_math_focus_keyword',
                'meta_description': '_rank_math_description',
                'title': '_rank_math_title',
                'canonical': '_rank_math_canonical_url',
                'noindex': '_rank_math_robots',
                'nofollow': '_rank_math_robots'
            }
        else:
            return {}

class BizFinProBrand:
    """Фирменные настройки BizFin Pro"""
    
    # Цветовая схема
    COLORS = {
        'primary_bg': '#FDFBF7',      # Светло-бежевый фон
        'text_color': '#333333',      # Темно-коричневый текст
        'accent_orange': '#FF8C00',   # Яркий оранжевый акцент
        'secondary_bg': '#FFFFFF',    # Белый фон для карточек
        'border_color': '#E0E0E0',    # Светло-серые границы
        'light_gray': '#F8F9FA',      # Светло-серый для фонов
        'success_green': '#28A745'    # Зеленый для успеха
    }
    
    # Шрифты
    FONTS = {
        'primary': 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        'heading': 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        'accent': 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    }
    
    # Стиль
    STYLE = {
        'gradients': True,
        'shadows': True,
        'border_radius': '8-15px',
        'spacing': 'consistent',
        'animations': True
    }
    
    # Контактная информация
    CONTACT = {
        'phone': '+7 (499) 757-01-25',
        'email': 'info@bizfin-pro.ru',
        'address': 'Москва',
        'website': 'https://bizfin-pro.ru'
    }
    
    # Социальные сети
    SOCIAL = {
        'telegram': '@bizfinpro_support',
        'whatsapp': '+7 (499) 757-01-25',
        'email': 'info@bizfin-pro.ru'
    }

class ContentTemplates:
    """Шаблоны контента"""
    
    # Шаблоны заголовков
    TITLE_TEMPLATES = [
        "{keyword}: полное руководство по получению в 2024 году",
        "{keyword}: как получить быстро и выгодно",
        "{keyword}: пошаговая инструкция для бизнеса",
        "{keyword}: все что нужно знать в 2024",
        "{keyword}: экспертное руководство"
    ]
    
    # Шаблоны мета-описаний
    META_DESCRIPTION_TEMPLATES = [
        "Получите {keyword} быстро и выгодно! Экспертное руководство по получению, стоимости, документам. Калькулятор расчета, сравнение банков, реальные кейсы. Консультация бесплатно!",
        "{keyword} за 1-3 дня! Профессиональная помощь в получении. Сравнение банков, калькулятор стоимости, документы. Бесплатная консультация эксперта.",
        "Как получить {keyword}? Полное руководство с примерами, калькулятором и сравнением банков. Помощь экспертов, быстрая обработка заявок."
    ]
    
    # Шаблоны CTA
    CTA_TEMPLATES = [
        "📞 Получить бесплатную консультацию",
        "🚀 Рассчитать стоимость",
        "📋 Получить помощь эксперта",
        "💬 Заказать звонок",
        "📞 Связаться с нами"
    ]
    
    # Шаблоны FAQ
    FAQ_TEMPLATES = [
        "Как быстро можно получить {keyword}?",
        "Сколько стоит {keyword}?",
        "Какие документы нужны для получения {keyword}?",
        "Можно ли получить {keyword} без залога?",
        "Что делать если банк отказывает в выдаче {keyword}?",
        "Как проверить подлинность {keyword}?",
        "Какова ответственность банка по {keyword}?"
    ]

# Экспорт конфигураций
__all__ = ['WordPressConfig', 'BizFinProBrand', 'ContentTemplates']


