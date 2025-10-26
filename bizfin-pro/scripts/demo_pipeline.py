#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Демонстрационный скрипт BizFin Pro SEO Pipeline v2
"""

import sys
import os
import sqlite3
import json
import time
from datetime import datetime

# Добавляем путь к модулям проекта
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.database_sqlite import DB_CONFIG
from modules.research.competitor_analyzer import CompetitorAnalyzer

class DemoPipeline:
    """Демонстрационный пайплайн"""
    
    def __init__(self):
        self.config = DB_CONFIG.get_config_dict()
        self.db_path = self.config['database']
        self.analyzer = CompetitorAnalyzer(max_competitors=2, delay=0.5)
        
        # Создаем директорию если не существует
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def create_database(self):
        """Создание базы данных"""
        print("🗄️ Создание базы данных...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Создаем таблицы
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL UNIQUE,
                date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending',
                source TEXT DEFAULT 'manual',
                priority TEXT DEFAULT 'medium',
                target_volume INTEGER DEFAULT 2500,
                target_intent TEXT DEFAULT 'informational',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword_id INTEGER NOT NULL,
                sources TEXT,
                structure TEXT,
                gaps TEXT,
                recommendations TEXT,
                competitors_data TEXT,
                lsi_keywords TEXT,
                search_volume INTEGER,
                competition_level TEXT DEFAULT 'medium',
                date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
                analysis_duration INTEGER,
                FOREIGN KEY (keyword_id) REFERENCES keywords(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword_id INTEGER NOT NULL,
                analysis_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content_raw TEXT NOT NULL,
                html_raw TEXT NOT NULL,
                word_count INTEGER DEFAULT 0,
                reading_time INTEGER DEFAULT 0,
                structure TEXT,
                lsi_keywords_used TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                generation_duration INTEGER,
                FOREIGN KEY (keyword_id) REFERENCES keywords(id),
                FOREIGN KEY (analysis_id) REFERENCES analysis(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ База данных создана")
    
    def add_keyword(self, keyword: str) -> int:
        """Добавление ключевого слова"""
        print(f"📝 Добавление ключевого слова: '{keyword}'")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO keywords (keyword, status, priority, target_volume)
            VALUES (?, ?, ?, ?)
        ''', (keyword, 'pending', 'medium', 2500))
        
        keyword_id = cursor.lastrowid
        if keyword_id == 0:
            cursor.execute('SELECT id FROM keywords WHERE keyword = ?', (keyword,))
            keyword_id = cursor.fetchone()[0]
        
        conn.commit()
        conn.close()
        
        print(f"✅ Ключевое слово добавлено (ID: {keyword_id})")
        return keyword_id
    
    def analyze_competitors(self, keyword_id: int, keyword: str) -> int:
        """Анализ конкурентов"""
        print(f"🔍 Анализ конкурентов для: '{keyword}'")
        
        # Симулируем анализ (так как реальный поиск может не работать)
        mock_analysis = {
            'keyword': keyword,
            'competitors': [
                {
                    'url': 'https://example-bank1.ru',
                    'title': f'{keyword}: полное руководство',
                    'meta_description': f'Получите {keyword} быстро и выгодно',
                    'h1': f'Что такое {keyword}',
                    'word_count': 2800,
                    'reading_time': 14,
                    'images_count': 8,
                    'faq_count': 6,
                    'cta_count': 4,
                    'lsi_keywords': ['банк', 'кредит', 'финансы', 'бизнес'],
                    'structure': {'h1': 1, 'h2': 8, 'h3': 15},
                    'domain': 'example-bank1.ru'
                },
                {
                    'url': 'https://example-bank2.ru',
                    'title': f'{keyword}: как получить',
                    'meta_description': f'Профессиональная помощь в получении {keyword}',
                    'h1': f'Виды {keyword}',
                    'word_count': 2200,
                    'reading_time': 11,
                    'images_count': 5,
                    'faq_count': 4,
                    'cta_count': 3,
                    'lsi_keywords': ['гарантия', 'залог', 'документы', 'сроки'],
                    'structure': {'h1': 1, 'h2': 6, 'h3': 12},
                    'domain': 'example-bank2.ru'
                }
            ],
            'statistics': {
                'avg_word_count': 2500,
                'avg_reading_time': 12,
                'avg_images': 6,
                'avg_faq': 5,
                'avg_cta': 3,
                'total_competitors': 2
            },
            'lsi_keywords': ['банк', 'кредит', 'гарантия', 'залог', 'финансы', 'бизнес', 'документы', 'сроки'],
            'gaps': ['Недостаточно интерактивных элементов', 'Слабые CTA'],
            'recommendations': [
                'Добавить калькулятор стоимости',
                'Улучшить призывы к действию',
                'Добавить больше FAQ',
                'Создать интерактивные элементы'
            ],
            'status': 'completed'
        }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analysis (keyword_id, sources, structure, gaps, recommendations,
                                competitors_data, lsi_keywords, search_volume, analysis_duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            keyword_id,
            json.dumps([c['url'] for c in mock_analysis['competitors']]),
            json.dumps(mock_analysis['statistics']),
            json.dumps(mock_analysis['gaps']),
            json.dumps(mock_analysis['recommendations']),
            json.dumps(mock_analysis['competitors']),
            json.dumps(mock_analysis['lsi_keywords']),
            mock_analysis['statistics']['avg_word_count'],
            45
        ))
        
        analysis_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ Анализ завершен (ID: {analysis_id})")
        print(f"   📊 Найдено конкурентов: {len(mock_analysis['competitors'])}")
        print(f"   🔑 LSI ключевые слова: {', '.join(mock_analysis['lsi_keywords'][:5])}")
        print(f"   ⚠️ Пробелы: {', '.join(mock_analysis['gaps'])}")
        
        return analysis_id
    
    def generate_article(self, analysis_id: int, keyword: str) -> int:
        """Генерация статьи"""
        print(f"✍️ Генерация статьи для: '{keyword}'")
        
        # Генерируем статью на основе анализа
        title = f"{keyword}: полное руководство по получению в 2024 году"
        
        content_raw = f"""
# {title}

## Введение

{keyword} — это важный финансовый инструмент для современного бизнеса. В данной статье мы рассмотрим все аспекты получения {keyword} в 2024 году, включая виды, стоимость, документы и реальные кейсы.

## Что такое {keyword}

{keyword} представляет собой письменное обязательство банка перед заказчиком выполнить определенные условия договора. Это надежный способ обеспечения исполнения обязательств в различных сферах бизнеса.

### Ключевые характеристики:

- **Размер:** от 0,5% до 30% от суммы контракта
- **Срок действия:** от 1 месяца до 3 лет
- **Автоматическое прекращение:** при выполнении обязательств
- **Возможность замены:** на другие виды обеспечения

## Виды {keyword}

### 1. Тендерная гарантия
Обеспечивает участие в торгах и заключение контракта.

### 2. Гарантия исполнения
Гарантирует выполнение условий заключенного договора.

### 3. Гарантия возврата аванса
Защищает интересы заказчика при выплате аванса.

## Стоимость и расчет {keyword}

Стоимость {keyword} зависит от нескольких факторов:

- Размер гарантии
- Срок действия
- Финансовое состояние компании
- Наличие обеспечения
- Банк-гарант

**Типичные тарифы:**
- Стандартные гарантии: 1,5-3% в год
- Сложные гарантии: 3-5% в год
- Срочные гарантии: +0,5-1% к базовому тарифу

## Документы для получения {keyword}

### Основные документы:
- Заявление на выдачу гарантии
- Учредительные документы
- Финансовая отчетность за 2 года
- Справки об отсутствии задолженности

### Дополнительные документы:
- Договор, для обеспечения которого нужна гарантия
- Бизнес-план или ТЭО
- Документы о залоге (при необходимости)

## Сравнение банков

| Банк | Комиссия | Срок рассмотрения | Мин. сумма | Особенности |
|------|----------|-------------------|------------|-------------|
| Сбербанк | 2,0-3,5% | 3-5 дней | 100 000 ₽ | Широкая сеть |
| ВТБ | 1,8-3,2% | 2-4 дня | 50 000 ₽ | Быстрое рассмотрение |
| Альфа-Банк | 2,5-4,0% | 3-6 дней | 100 000 ₽ | Индивидуальный подход |

## Реальный кейс успеха

Компания "ТехноСтрой" получила тендерную гарантию на 50 млн рублей за 3 дня благодаря профессиональной помощи наших экспертов. Это позволило им выиграть крупный контракт и увеличить оборот на 200%.

## Часто задаваемые вопросы

### Как быстро можно получить {keyword}?
Стандартные сроки: 3-7 рабочих дней. Экспресс-оформление возможно за 1-2 дня.

### Сколько стоит {keyword}?
Стоимость варьируется от 1,5% до 5% от суммы гарантии в год.

### Какие документы нужны для получения {keyword}?
Основной пакет включает учредительные документы, финансовую отчетность и справки об отсутствии задолженности.

### Можно ли получить {keyword} без залога?
Да, многие банки выдают непокрытые гарантии на основе анализа финансового состояния.

### Что делать если банк отказывает в выдаче {keyword}?
Рекомендуется обратиться в другие банки или улучшить финансовые показатели.

## Заключение

{keyword} — это надежный инструмент для развития бизнеса. Правильно оформленная гарантия открывает доступ к крупным контрактам и новым возможностям.

**Готовы получить {keyword}? Свяжитесь с нашими экспертами!**

📞 **Телефон:** +7 (499) 757-01-25
📧 **Email:** info@bizfin-pro.ru
🌐 **Сайт:** https://bizfin-pro.ru
        """.strip()
        
        # Генерируем HTML версию
        html_raw = f"""
        <article class="bizfin-article">
            <header class="article-header">
                <h1>{title}</h1>
                <p class="article-meta">Получите {keyword} быстро и выгодно! Экспертное руководство с калькулятором, сравнением банков и реальными кейсами.</p>
            </header>
            
            <div class="article-content">
                {content_raw.replace('#', '<h2>').replace('##', '</h2><h3>').replace('###', '</h3><h4>')}
            </div>
            
            <footer class="article-footer">
                <div class="cta-section">
                    <h3>🚀 Готовы получить {keyword}?</h3>
                    <p>Наши эксперты помогут вам сэкономить время, деньги и нервы при получении {keyword}</p>
                    <button class="cta-button">📞 Получить бесплатную консультацию</button>
                </div>
            </footer>
        </article>
        """
        
        # Подсчитываем слова
        word_count = len(content_raw.split())
        reading_time = max(1, word_count // 200)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Получаем keyword_id из analysis
        cursor.execute('SELECT keyword_id FROM analysis WHERE id = ?', (analysis_id,))
        keyword_id = cursor.fetchone()[0]
        
        cursor.execute('''
            INSERT INTO articles (keyword_id, analysis_id, title, content_raw, html_raw,
                                word_count, reading_time, structure, lsi_keywords_used, generation_duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            keyword_id,
            analysis_id,
            title,
            content_raw,
            html_raw,
            word_count,
            reading_time,
            json.dumps({'sections': ['Введение', 'Основная часть', 'FAQ', 'Заключение']}),
            json.dumps(['банк', 'кредит', 'гарантия', 'финансы', 'бизнес']),
            120
        ))
        
        article_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ Статья сгенерирована (ID: {article_id})")
        print(f"   📝 Заголовок: {title}")
        print(f"   📊 Слов: {word_count}")
        print(f"   ⏱️ Время чтения: {reading_time} минут")
        
        return article_id
    
    def show_results(self, keyword_id: int):
        """Показ результатов"""
        print(f"\n📊 РЕЗУЛЬТАТЫ ПАЙПЛАЙНА")
        print("=" * 50)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Получаем полную цепочку данных
        cursor.execute('''
            SELECT 
                k.keyword,
                k.status,
                k.target_volume,
                a.competitors_data,
                a.lsi_keywords,
                a.gaps,
                a.recommendations,
                ar.title,
                ar.word_count,
                ar.reading_time
            FROM keywords k
            LEFT JOIN analysis a ON k.id = a.keyword_id
            LEFT JOIN articles ar ON a.id = ar.analysis_id
            WHERE k.id = ?
        ''', (keyword_id,))
        
        result = cursor.fetchone()
        if result:
            keyword, status, target_volume, competitors_data, lsi_keywords, gaps, recommendations, title, word_count, reading_time = result
            
            print(f"🔑 Ключевое слово: {keyword}")
            print(f"📈 Статус: {status}")
            print(f"🎯 Целевой объем: {target_volume} слов")
            
            if competitors_data:
                competitors = json.loads(competitors_data)
                print(f"🏆 Проанализировано конкурентов: {len(competitors)}")
                
                if lsi_keywords:
                    lsi = json.loads(lsi_keywords)
                    print(f"🔑 LSI ключевые слова: {', '.join(lsi[:5])}")
                
                if gaps:
                    gaps_list = json.loads(gaps)
                    print(f"⚠️ Выявленные пробелы: {', '.join(gaps_list)}")
                
                if recommendations:
                    recs = json.loads(recommendations)
                    print(f"💡 Рекомендации: {', '.join(recs[:3])}")
            
            if title:
                print(f"📝 Заголовок статьи: {title}")
                print(f"📊 Фактический объем: {word_count} слов")
                print(f"⏱️ Время чтения: {reading_time} минут")
        
        conn.close()
    
    def run_demo(self, keyword: str):
        """Запуск демонстрации"""
        print(f"🚀 ДЕМОНСТРАЦИЯ BIZFIN PRO SEO PIPELINE V2")
        print(f"Ключевое слово: '{keyword}'")
        print("=" * 60)
        
        start_time = time.time()
        
        # Создаем базу данных
        self.create_database()
        
        # Этап 0: Добавляем ключевое слово
        keyword_id = self.add_keyword(keyword)
        
        # Этап 1: Анализируем конкурентов
        analysis_id = self.analyze_competitors(keyword_id, keyword)
        
        # Этап 2: Генерируем статью
        article_id = self.generate_article(analysis_id, keyword)
        
        execution_time = time.time() - start_time
        
        # Показываем результаты
        self.show_results(keyword_id)
        
        print(f"\n⏱️ Время выполнения: {execution_time:.2f} секунд")
        print("🎉 Демонстрация завершена успешно!")

def main():
    """Основная функция"""
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
    else:
        keyword = "тендерная гарантия"
    
    demo = DemoPipeline()
    demo.run_demo(keyword)

if __name__ == "__main__":
    main()


