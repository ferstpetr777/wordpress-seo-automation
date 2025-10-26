#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для инициализации SQLite базы данных BizFin Pro
"""

import os
import sys
import sqlite3
import logging
from datetime import datetime

def setup_logging():
    """Настройка логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def create_tables():
    """Создание таблиц в SQLite"""
    logger = setup_logging()
    
    try:
        # Путь к базе данных SQLite
        db_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'bizfin_pro.db')
        
        # Подключаемся к базе данных
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        logger.info(f"🗄️ Подключение к базе данных: {db_path}")
        
        # SQL для создания таблицы keywords (адаптированный для SQLite)
        create_keywords_table = """
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL UNIQUE,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'analyzing', 'generating', 'published', 'error')),
            source TEXT DEFAULT 'manual',
            frequency INTEGER DEFAULT 1,
            user_id INTEGER DEFAULT 1,
            priority TEXT DEFAULT 'medium' CHECK(priority IN ('low', 'medium', 'high', 'urgent')),
            target_volume INTEGER DEFAULT 2500,
            target_intent TEXT DEFAULT 'informational' CHECK(target_intent IN ('informational', 'commercial', 'educational', 'faq', 'review')),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        # SQL для создания таблицы analysis
        create_analysis_table = """
        CREATE TABLE IF NOT EXISTS analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword_id INTEGER NOT NULL,
            sources TEXT, -- JSON как TEXT
            structure TEXT, -- JSON как TEXT
            gaps TEXT, -- JSON как TEXT
            recommendations TEXT, -- JSON как TEXT
            competitors_data TEXT, -- JSON как TEXT
            lsi_keywords TEXT, -- JSON как TEXT
            search_volume INTEGER,
            competition_level TEXT DEFAULT 'medium' CHECK(competition_level IN ('low', 'medium', 'high')),
            date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
            analysis_duration INTEGER,
            FOREIGN KEY (keyword_id) REFERENCES keywords(id) ON DELETE CASCADE
        );
        """
        
        # SQL для создания таблицы articles
        create_articles_table = """
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword_id INTEGER NOT NULL,
            analysis_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content_raw TEXT NOT NULL,
            html_raw TEXT NOT NULL,
            word_count INTEGER DEFAULT 0,
            reading_time INTEGER DEFAULT 0,
            structure TEXT, -- JSON как TEXT
            lsi_keywords_used TEXT, -- JSON как TEXT
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            generation_duration INTEGER,
            FOREIGN KEY (keyword_id) REFERENCES keywords(id) ON DELETE CASCADE,
            FOREIGN KEY (analysis_id) REFERENCES analysis(id) ON DELETE CASCADE
        );
        """
        
        # SQL для создания таблицы seo_checks
        create_seo_checks_table = """
        CREATE TABLE IF NOT EXISTS seo_checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER NOT NULL,
            keyword_id INTEGER NOT NULL,
            seo_score INTEGER DEFAULT 0,
            issues TEXT, -- JSON как TEXT
            recommendations TEXT, -- JSON как TEXT
            focus_keyword_present BOOLEAN DEFAULT FALSE,
            meta_description_length INTEGER DEFAULT 0,
            title_length INTEGER DEFAULT 0,
            h1_present BOOLEAN DEFAULT FALSE,
            internal_links_count INTEGER DEFAULT 0,
            external_links_count INTEGER DEFAULT 0,
            images_alt_count INTEGER DEFAULT 0,
            readability_score INTEGER DEFAULT 0,
            date_checked DATETIME DEFAULT CURRENT_TIMESTAMP,
            check_duration INTEGER,
            FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
            FOREIGN KEY (keyword_id) REFERENCES keywords(id) ON DELETE CASCADE
        );
        """
        
        # SQL для создания таблицы articles_final
        create_articles_final_table = """
        CREATE TABLE IF NOT EXISTS articles_final (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER NOT NULL,
            seo_check_id INTEGER NOT NULL,
            content_final TEXT NOT NULL,
            html_final TEXT NOT NULL,
            json_ld TEXT, -- JSON как TEXT
            meta_title TEXT NOT NULL,
            meta_description TEXT NOT NULL,
            focus_keyword TEXT NOT NULL,
            slug TEXT NOT NULL,
            canonical_url TEXT,
            internal_links TEXT, -- JSON как TEXT
            external_links TEXT, -- JSON как TEXT
            images_data TEXT, -- JSON как TEXT
            faq_schema TEXT, -- JSON как TEXT
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            improvement_duration INTEGER,
            FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
            FOREIGN KEY (seo_check_id) REFERENCES seo_checks(id) ON DELETE CASCADE
        );
        """
        
        # SQL для создания таблицы publish_queue
        create_publish_queue_table = """
        CREATE TABLE IF NOT EXISTS publish_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_final_id INTEGER NOT NULL,
            eec_json TEXT NOT NULL, -- JSON как TEXT
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'processing', 'published', 'failed')),
            priority TEXT DEFAULT 'medium' CHECK(priority IN ('low', 'medium', 'high', 'urgent')),
            retry_count INTEGER DEFAULT 0,
            max_retries INTEGER DEFAULT 3,
            error_message TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            scheduled_at DATETIME,
            FOREIGN KEY (article_final_id) REFERENCES articles_final(id) ON DELETE CASCADE
        );
        """
        
        # SQL для создания таблицы published
        create_published_table = """
        CREATE TABLE IF NOT EXISTS published (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            publish_queue_id INTEGER NOT NULL,
            wp_post_id INTEGER NOT NULL,
            permalink TEXT NOT NULL,
            response_code INTEGER,
            response_data TEXT, -- JSON как TEXT
            publish_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            publish_duration INTEGER,
            FOREIGN KEY (publish_queue_id) REFERENCES publish_queue(id) ON DELETE CASCADE
        );
        """
        
        # SQL для создания таблицы publish_status
        create_publish_status_table = """
        CREATE TABLE IF NOT EXISTS publish_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            published_id INTEGER NOT NULL,
            keyword_id INTEGER NOT NULL,
            article_id INTEGER NOT NULL,
            seo_check_id INTEGER NOT NULL,
            article_final_id INTEGER NOT NULL,
            status TEXT DEFAULT 'success' CHECK(status IN ('success', 'failed', 'partial')),
            url TEXT,
            http_code INTEGER,
            response_time INTEGER,
            checked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (published_id) REFERENCES published(id) ON DELETE CASCADE,
            FOREIGN KEY (keyword_id) REFERENCES keywords(id) ON DELETE CASCADE,
            FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
            FOREIGN KEY (seo_check_id) REFERENCES seo_checks(id) ON DELETE CASCADE,
            FOREIGN KEY (article_final_id) REFERENCES articles_final(id) ON DELETE CASCADE
        );
        """
        
        # Создаем все таблицы
        tables = [
            ("keywords", create_keywords_table),
            ("analysis", create_analysis_table),
            ("articles", create_articles_table),
            ("seo_checks", create_seo_checks_table),
            ("articles_final", create_articles_final_table),
            ("publish_queue", create_publish_queue_table),
            ("published", create_published_table),
            ("publish_status", create_publish_status_table)
        ]
        
        for table_name, create_sql in tables:
            try:
                cursor.execute(create_sql)
                logger.info(f"✅ Таблица '{table_name}' создана или уже существует")
            except Exception as e:
                logger.error(f"❌ Ошибка создания таблицы '{table_name}': {e}")
        
        # Создаем индексы
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_keywords_status ON keywords(status);",
            "CREATE INDEX IF NOT EXISTS idx_keywords_priority ON keywords(priority);",
            "CREATE INDEX IF NOT EXISTS idx_keywords_date_added ON keywords(date_added);",
            "CREATE INDEX IF NOT EXISTS idx_analysis_keyword_id ON analysis(keyword_id);",
            "CREATE INDEX IF NOT EXISTS idx_articles_keyword_id ON articles(keyword_id);",
            "CREATE INDEX IF NOT EXISTS idx_seo_checks_article_id ON seo_checks(article_id);",
            "CREATE INDEX IF NOT EXISTS idx_seo_checks_seo_score ON seo_checks(seo_score);"
        ]
        
        for index_sql in indexes:
            try:
                cursor.execute(index_sql)
                logger.info(f"✅ Индекс создан")
            except Exception as e:
                logger.warning(f"⚠️ Ошибка создания индекса: {e}")
        
        # Сохраняем изменения
        connection.commit()
        
        # Проверяем созданные таблицы
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        logger.info(f"\n📊 СОЗДАННЫЕ ТАБЛИЦЫ:")
        for table in tables:
            logger.info(f"   📋 {table[0]}")
        
        cursor.close()
        connection.close()
        
        logger.info("✅ База данных SQLite инициализирована успешно!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации базы данных: {e}")
        return False

def main():
    """Основная функция"""
    logger = setup_logging()
    
    print("🚀 Инициализация SQLite базы данных BizFin Pro")
    print("=" * 60)
    
    if create_tables():
        print("\n" + "=" * 60)
        print("🎉 ИНИЦИАЛИЗАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
        print("=" * 60)
        print("✅ Все таблицы созданы")
        print("✅ Индексы созданы")
        print("✅ База данных готова к работе")
        print("\n🚀 Теперь можно добавлять ключевые слова!")
    else:
        print("\n❌ Ошибка инициализации базы данных")

if __name__ == "__main__":
    main()

