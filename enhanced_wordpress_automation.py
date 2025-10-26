#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Улучшенная версия WordPress Automation Script
- Качественный контент с реальными данными
- Адаптивная структура под ключевые слова
- SEO-оптимизация без переоптимизации
- Проверка качества контента
"""

import requests
import json
import sqlite3
import re
from datetime import datetime
import time
from enhanced_content_generator import EnhancedContentGenerator

class EnhancedWordPressAutomation:
    def __init__(self):
        self.wp_url = "https://bizfin-pro.ru/wp-json/wp/v2"
        self.wp_username = "bizfin_pro_r"
        self.wp_app_password = "U3Ep gU2T clRu FcwN QU6l Dsda"
        self.wp_auth = (self.wp_username, self.wp_app_password)
        self.db_path = "wordpress_articles_enhanced.db"
        self.conn = None
        
        # Ключевые слова для обработки
        self.keywords = [
            "банковская гарантия для исполнения контракта 44 фз онлайн",
            "калькулятор стоимости банковской гарантии 5 000 000 на 12 месяцев",
            "документы для банковской гарантии список 44-фз",
            "проверить банковскую гарантию в реестре как",
            "банковская гарантия возврат аванса образец текста",
            "банковская гарантия без залога для ИП",
            "срочная банковская гарантия сегодня успеть до … (дата)",
            "какой банк выдаёт бг дешевле исполнение контракта",
            "банковская гарантия для стройки/поставки/услуг",
            "оформить бг москва/спб/иркутск"
        ]
        
        # Инициализируем улучшенный генератор контента
        self.content_generator = EnhancedContentGenerator(
            self.wp_url, self.wp_username, self.wp_app_password, self.db_path
        )
        
        self.initialize_db()
    
    def initialize_db(self):
        """Инициализация базы данных"""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Таблица для исследований
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keyword_research (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                intent_analysis TEXT,
                user_goal TEXT,
                content_focus TEXT,
                priority_sections TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица для оглавлений
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS article_outlines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                outline_data TEXT,
                quality_score INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица для статей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                wp_post_id INTEGER,
                wp_post_url TEXT,
                status TEXT DEFAULT 'draft',
                word_count INTEGER DEFAULT 0,
                quality_score INTEGER DEFAULT 0,
                seo_score INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица для контроля качества
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quality_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER,
                check_type TEXT,
                result TEXT,
                score INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        print("✅ Улучшенная база данных инициализирована")
    
    def analyze_keyword(self, keyword):
        """Анализ ключевого слова с помощью улучшенного генератора"""
        print(f"   🔍 Анализ ключевого слова: {keyword}")
        
        try:
            # Используем улучшенный анализ намерений
            intent_analysis = self.content_generator.analyze_keyword_intent(keyword)
            
            print(f"   🎯 Намерение пользователя: {intent_analysis['intent']}")
            print(f"   📋 Цель пользователя: {intent_analysis['user_goal']}")
            print(f"   🎨 Фокус контента: {intent_analysis['content_focus']}")
            
            # Сохранение в БД
            self.save_intent_analysis(keyword, intent_analysis)
            
            return intent_analysis
            
        except Exception as e:
            print(f"   ⚠️ Ошибка анализа: {str(e)}")
            return self.get_fallback_intent(keyword)
    
    def save_intent_analysis(self, keyword, intent_analysis):
        """Сохранение анализа намерений в БД"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO keyword_research (
                keyword, intent_analysis, user_goal, content_focus, priority_sections
            ) VALUES (?, ?, ?, ?, ?)
        ''', (
            keyword,
            json.dumps(intent_analysis, ensure_ascii=False),
            intent_analysis['user_goal'],
            intent_analysis['content_focus'],
            json.dumps(intent_analysis['priority_sections'], ensure_ascii=False)
        ))
        
        self.conn.commit()
    
    def create_adaptive_outline(self, keyword, intent_analysis):
        """Создание адаптивного оглавления"""
        print(f"   📋 Создание адаптивного оглавления для: {keyword}")
        
        try:
            outline = self.content_generator.create_adaptive_outline(keyword, intent_analysis)
            
            # Оценка качества оглавления
            quality_score = self.evaluate_outline_quality(outline)
            outline['quality_score'] = quality_score
            
            # Сохранение в БД
            self.save_outline_to_db(keyword, outline)
            
            total_words = sum(section["word_count"] for section in outline["sections"])
            print(f"   📊 Планируемый объем статьи: {total_words} слов")
            print(f"   📋 Разделов в оглавлении: {len(outline['sections'])}")
            print(f"   ⭐ Оценка качества оглавления: {quality_score}/100")
            
            return outline
            
        except Exception as e:
            print(f"   ⚠️ Ошибка создания оглавления: {str(e)}")
            return self.get_fallback_outline(keyword)
    
    def evaluate_outline_quality(self, outline):
        """Оценка качества оглавления"""
        score = 0
        
        # Проверка структуры (40 баллов)
        if len(outline['sections']) >= 6:
            score += 20
        if len(outline['sections']) >= 8:
            score += 20
        
        # Проверка объема (30 баллов)
        total_words = sum(section["word_count"] for section in outline["sections"])
        if total_words >= 2000:
            score += 30
        elif total_words >= 1500:
            score += 20
        elif total_words >= 1000:
            score += 10
        
        # Проверка разнообразия разделов (30 баллов)
        unique_focuses = set(section.get("focus", "") for section in outline["sections"])
        if len(unique_focuses) >= 5:
            score += 30
        elif len(unique_focuses) >= 3:
            score += 20
        elif len(unique_focuses) >= 2:
            score += 10
        
        return min(score, 100)
    
    def save_outline_to_db(self, keyword, outline):
        """Сохранение оглавления в БД"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO article_outlines (keyword, outline_data, quality_score)
            VALUES (?, ?, ?)
        ''', (
            keyword, 
            json.dumps(outline, ensure_ascii=False),
            outline.get('quality_score', 0)
        ))
        
        self.conn.commit()
    
    def generate_high_quality_content(self, keyword, outline, intent_analysis):
        """Генерация высококачественного контента"""
        print(f"   ✍️ Генерация высококачественного контента для: {keyword}")
        
        try:
            content = self.content_generator.generate_high_quality_content(
                keyword, outline, intent_analysis
            )
            
            # Проверка качества контента
            quality_score = self.evaluate_content_quality(content, keyword)
            seo_score = self.evaluate_seo_quality(content, keyword)
            
            print(f"   📄 Фактический объем статьи: {len(content.split())} слов")
            print(f"   ⭐ Оценка качества контента: {quality_score}/100")
            print(f"   🔍 Оценка SEO: {seo_score}/100")
            print(f"   ✅ Контент сгенерирован по {len(outline['sections'])} разделам")
            
            return content, quality_score, seo_score
            
        except Exception as e:
            print(f"   ⚠️ Ошибка генерации контента: {str(e)}")
            return self.get_fallback_content(keyword), 0, 0
    
    def evaluate_content_quality(self, content, keyword):
        """Оценка качества контента"""
        score = 0
        
        # Проверка объема (30 баллов)
        word_count = len(content.split())
        if word_count >= 2000:
            score += 30
        elif word_count >= 1500:
            score += 20
        elif word_count >= 1000:
            score += 10
        
        # Проверка структуры (25 баллов)
        if '<h1>' in content:
            score += 5
        if '<h2>' in content:
            score += 10
        if '<h3>' in content:
            score += 10
        
        # Проверка разнообразия контента (25 баллов)
        if '<ul>' in content:
            score += 8
        if '<ol>' in content:
            score += 7
        if '<table' in content:
            score += 10
        
        # Проверка уникальности (20 баллов)
        keyword_occurrences = content.lower().count(keyword.lower())
        if keyword_occurrences <= 10 and keyword_occurrences >= 3:
            score += 20
        elif keyword_occurrences <= 15:
            score += 10
        
        return min(score, 100)
    
    def evaluate_seo_quality(self, content, keyword):
        """Оценка SEO качества"""
        score = 0
        
        # Проверка заголовка H1 (25 баллов)
        if f'<h1' in content and keyword.lower() in content.lower():
            score += 25
        
        # Проверка ключевого слова в начале (25 баллов)
        first_200_chars = content[:200].lower()
        if keyword.lower() in first_200_chars:
            score += 25
        
        # Проверка структуры заголовков (25 баллов)
        if '<h2>' in content:
            score += 15
        if '<h3>' in content:
            score += 10
        
        # Проверка внутренних ссылок (25 баллов)
        if '<a href=' in content:
            score += 25
        
        return min(score, 100)
    
    def publish_to_wordpress(self, keyword, content, title, slug, quality_score, seo_score):
        """Публикация статьи в WordPress с мета-данными"""
        print(f"   📤 Публикация в WordPress: {title}")
        
        # Создаем мета-описание
        meta_description = self.generate_meta_description(keyword, title, content)
        
        post_data = {
            'title': title,
            'content': content,
            'slug': slug,
            'status': 'draft',
            'meta': {
                '_yoast_wpseo_focuskw': keyword,
                '_yoast_wpseo_metadesc': meta_description,
                '_yoast_wpseo_title': title,
                '_yoast_wpseo_canonical': f"https://bizfin-pro.ru/{slug}/",
                '_yoast_wpseo_meta-robots-noindex': "0",
                '_yoast_wpseo_meta-robots-nofollow': "0",
                'quality_score': quality_score,
                'seo_score': seo_score
            }
        }
        
        try:
            response = requests.post(
                f"{self.wp_url}/posts",
                auth=self.wp_auth,
                json=post_data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 201:
                post = response.json()
                wp_id = post['id']
                wp_url = post['link']
                
                print(f"   ✅ Черновик создан в WordPress (ID: {wp_id})")
                print(f"   🔗 URL: {wp_url}")
                print(f"   📝 Статус: ЧЕРНОВИК (качество: {quality_score}/100, SEO: {seo_score}/100)")
                
                return {
                    'wp_id': wp_id,
                    'wp_url': wp_url,
                    'status': 'draft',
                    'quality_score': quality_score,
                    'seo_score': seo_score
                }
            else:
                print(f"   ❌ Ошибка публикации: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Ошибка при публикации: {str(e)}")
            return None
    
    def generate_meta_description(self, keyword, title, content):
        """Генерация мета-описания"""
        # Создаем описание с ключевым словом
        base_desc = f"{keyword} - подробное руководство. "
        
        # Добавляем описание
        additional_text = "Получите экспертную консультацию по оформлению банковской гарантии. Быстрое оформление, выгодные условия."
        
        meta_desc = base_desc + additional_text
        
        # Обрезаем до 160 символов
        if len(meta_desc) > 160:
            meta_desc = meta_desc[:157] + "..."
        
        return meta_desc
    
    def save_article_to_db(self, keyword, wp_result):
        """Сохранение статьи в базу данных"""
        if wp_result:
            cursor = self.conn.cursor()
            
            word_count = len(wp_result.get('content', '').split()) if 'content' in wp_result else 0
            
            cursor.execute('''
                INSERT INTO articles (
                    keyword, wp_post_id, wp_post_url, status, word_count, 
                    quality_score, seo_score
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                keyword,
                wp_result['wp_id'],
                wp_result['wp_url'],
                wp_result['status'],
                word_count,
                wp_result.get('quality_score', 0),
                wp_result.get('seo_score', 0)
            ))
            
            article_id = cursor.lastrowid
            self.conn.commit()
            
            print(f"   💾 Статья сохранена в БД с ID: {article_id}")
            return article_id
        
        return None
    
    def run_enhanced_automation(self):
        """Запуск улучшенной автоматизации"""
        print("🚀 Запуск УЛУЧШЕННОГО WordPress Automation Script")
        print(f"📅 Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎯 Цель: Создание высококачественных статей с адаптивной структурой")
        print("=" * 60)
        
        results = []
        
        for i, keyword in enumerate(self.keywords, 1):
            print(f"\n{'='*60}")
            print(f"📋 Обработка {i}/{len(self.keywords)}: {keyword}")
            print(f"{'='*60}")
            
            try:
                # 1. Анализ ключевого слова
                intent_analysis = self.analyze_keyword(keyword)
                
                # 2. Создание адаптивного оглавления
                outline = self.create_adaptive_outline(keyword, intent_analysis)
                
                # 3. Генерация высококачественного контента
                content, quality_score, seo_score = self.generate_high_quality_content(
                    keyword, outline, intent_analysis
                )
                
                # 4. Публикация в WordPress
                title = outline['title']
                slug = self.transliterate_keyword(keyword)
                
                wp_result = self.publish_to_wordpress(
                    keyword, content, title, slug, quality_score, seo_score
                )
                
                # 5. Сохранение в БД
                article_id = self.save_article_to_db(keyword, wp_result)
                
                if wp_result:
                    results.append({
                        'keyword': keyword,
                        'article_id': article_id,
                        'wp_id': wp_result['wp_id'],
                        'wp_url': wp_result['wp_url'],
                        'status': 'success',
                        'word_count': len(content.split()),
                        'quality_score': quality_score,
                        'seo_score': seo_score
                    })
                    print(f"   ✅ УСПЕХ: Статья создана (WP ID: {wp_result['wp_id']})")
                    print(f"   📊 Качество: {quality_score}/100, SEO: {seo_score}/100")
                else:
                    results.append({
                        'keyword': keyword,
                        'article_id': None,
                        'wp_id': None,
                        'wp_url': None,
                        'status': 'error',
                        'word_count': 0,
                        'quality_score': 0,
                        'seo_score': 0
                    })
                    print(f"   ❌ ОШИБКА при обработке '{keyword}'")
                
            except Exception as e:
                print(f"   ❌ Критическая ошибка при обработке '{keyword}': {str(e)}")
                results.append({
                    'keyword': keyword,
                    'article_id': None,
                    'wp_id': None,
                    'wp_url': None,
                    'status': 'error',
                    'word_count': 0,
                    'quality_score': 0,
                    'seo_score': 0
                })
            
            # Пауза между запросами
            time.sleep(2)
        
        # Отображение результатов
        self.display_enhanced_results(results)
        
        # Закрытие соединения с БД
        if self.conn:
            self.conn.close()
            print("\n🔒 Соединение с базой данных закрыто")
    
    def display_enhanced_results(self, results):
        """Отображение улучшенных результатов"""
        print(f"\n{'='*80}")
        print("📊 РЕЗУЛЬТАТЫ УЛУЧШЕННОГО СКРИПТА")
        print(f"{'='*80}")
        
        successful = [r for r in results if r['status'] == 'success']
        failed = [r for r in results if r['status'] == 'error']
        
        print(f"✅ Создано статей: {len(successful)}/{len(results)}")
        print(f"📅 Время завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if successful:
            avg_quality = sum(r['quality_score'] for r in successful) / len(successful)
            avg_seo = sum(r['seo_score'] for r in successful) / len(successful)
            avg_words = sum(r['word_count'] for r in successful) / len(successful)
            
            print(f"📊 Средняя оценка качества: {avg_quality:.1f}/100")
            print(f"🔍 Средняя SEO-оценка: {avg_seo:.1f}/100")
            print(f"📄 Средний объем статьи: {avg_words:.0f} слов")
        
        print(f"\n📋 СПИСОК СОЗДАННЫХ СТАТЕЙ:")
        print("-" * 80)
        
        for i, result in enumerate(results, 1):
            keyword = result['keyword']
            wp_id = result['wp_id']
            wp_url = result['wp_url']
            status = result['status']
            word_count = result['word_count']
            quality_score = result['quality_score']
            seo_score = result['seo_score']
            
            if status == 'success':
                print(f"{i:2d}. {keyword}")
                print(f"    ID в БД: {result['article_id']} | WP ID: {wp_id} | Статус: ✅ СОЗДАНА")
                print(f"    🔗 URL: {wp_url}")
                print(f"    📄 Объем: {word_count} слов | ⭐ Качество: {quality_score}/100 | 🔍 SEO: {seo_score}/100")
            else:
                print(f"{i:2d}. {keyword}")
                print(f"    ID в БД: None | WP ID: None | Статус: ❌ ОШИБКА")
                print(f"    🔗 URL: None")
            
            print()
    
    def transliterate_keyword(self, keyword):
        """Транслитерация ключевого слова для слага"""
        translit_map = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
            'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
        }
        
        result = keyword.lower()
        for ru, en in translit_map.items():
            result = result.replace(ru, en)
        
        # Замена пробелов и специальных символов
        result = re.sub(r'[^\w\-]', '-', result)
        result = re.sub(r'-+', '-', result)
        result = result.strip('-')
        
        return result
    
    def get_fallback_intent(self, keyword):
        """Резервный анализ намерений"""
        return {
            'intent': 'informational',
            'user_goal': 'Получить информацию о банковской гарантии',
            'content_focus': 'general',
            'priority_sections': ['overview', 'types', 'benefits']
        }
    
    def get_fallback_outline(self, keyword):
        """Резервное оглавление"""
        return {
            'title': f"Банковская гарантия: полное руководство",
            'sections': [
                {'title': 'Что такое банковская гарантия', 'word_count': 300, 'focus': 'definition'},
                {'title': 'Виды и типы', 'word_count': 350, 'focus': 'types'},
                {'title': 'Процесс оформления', 'word_count': 400, 'focus': 'process'},
                {'title': 'Требования и документы', 'word_count': 300, 'focus': 'requirements'},
                {'title': 'Стоимость и сроки', 'word_count': 250, 'focus': 'cost'},
                {'title': 'Практические советы', 'word_count': 200, 'focus': 'tips'}
            ],
            'quality_score': 60
        }
    
    def get_fallback_content(self, keyword):
        """Резервный контент"""
        return f"""<h1 class="entry-title">Банковская гарантия: полное руководство</h1>

<p>Банковская гарантия — это надежный способ обеспечения исполнения обязательств по контракту.</p>

<h2>Что такое банковская гарантия</h2>
<p>Банковская гарантия представляет собой письменное обязательство банка выплатить определенную сумму бенефициару в случае невыполнения принципалом своих обязательств.</p>

<h2>Основные виды</h2>
<ul>
<li>Исполнение контракта</li>
<li>Возврат аванса</li>
<li>Обеспечение заявки</li>
</ul>

<h2>Процесс оформления</h2>
<p>Процесс оформления банковской гарантии включает несколько этапов: подача заявки, анализ документов, принятие решения и выдача гарантии.</p>

<p>Для получения подробной консультации обращайтесь к нашим специалистам.</p>"""

def main():
    """Основная функция"""
    automation = EnhancedWordPressAutomation()
    automation.run_enhanced_automation()

if __name__ == "__main__":
    main()
