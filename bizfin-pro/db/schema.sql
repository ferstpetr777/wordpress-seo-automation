-- =====================================================
-- BizFin Pro - SEO Article Generation Pipeline v2
-- Database Schema
-- =====================================================

-- Создание базы данных
CREATE DATABASE IF NOT EXISTS bizfin_pro_seo;
USE bizfin_pro_seo;

-- =====================================================
-- ОСНОВНЫЕ ТАБЛИЦЫ ПАЙПЛАЙНА
-- =====================================================

-- Таблица ключевых слов (Этап 0)
CREATE TABLE keywords (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    keyword VARCHAR(255) NOT NULL UNIQUE,
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'analyzing', 'generating', 'published', 'error') DEFAULT 'pending',
    source VARCHAR(100) DEFAULT 'manual',
    frequency INTEGER DEFAULT 1,
    user_id INTEGER DEFAULT 1,
    priority ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium',
    target_volume INTEGER DEFAULT 2500,
    target_intent ENUM('informational', 'commercial', 'educational', 'faq', 'review') DEFAULT 'informational',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_priority (priority),
    INDEX idx_date_added (date_added)
);

-- Таблица анализа конкурентов (Этап 1)
CREATE TABLE analysis (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    keyword_id INTEGER NOT NULL,
    sources JSON, -- URL источников для анализа
    structure JSON, -- Структура найденных статей
    gaps JSON, -- Выявленные пробелы
    recommendations JSON, -- Рекомендации по улучшению
    competitors_data JSON, -- Данные о конкурентах
    lsi_keywords JSON, -- LSI ключевые слова
    search_volume INTEGER, -- Объем поиска
    competition_level ENUM('low', 'medium', 'high') DEFAULT 'medium',
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    analysis_duration INTEGER, -- Время анализа в секундах
    FOREIGN KEY (keyword_id) REFERENCES keywords(id) ON DELETE CASCADE,
    INDEX idx_keyword_id (keyword_id),
    INDEX idx_date_created (date_created)
);

-- Таблица статей (Этап 2)
CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    keyword_id INTEGER NOT NULL,
    analysis_id INTEGER NOT NULL,
    title VARCHAR(500) NOT NULL,
    content_raw TEXT NOT NULL,
    html_raw LONGTEXT NOT NULL,
    word_count INTEGER DEFAULT 0,
    reading_time INTEGER DEFAULT 0, -- В минутах
    structure JSON, -- Структура статьи
    lsi_keywords_used JSON, -- Использованные LSI ключи
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    generation_duration INTEGER, -- Время генерации в секундах
    FOREIGN KEY (keyword_id) REFERENCES keywords(id) ON DELETE CASCADE,
    FOREIGN KEY (analysis_id) REFERENCES analysis(id) ON DELETE CASCADE,
    INDEX idx_keyword_id (keyword_id),
    INDEX idx_analysis_id (analysis_id),
    INDEX idx_word_count (word_count)
);

-- Таблица SEO-проверок (Этап 3)
CREATE TABLE seo_checks (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    article_id INTEGER NOT NULL,
    keyword_id INTEGER NOT NULL,
    seo_score INTEGER DEFAULT 0, -- Общий SEO балл (0-100)
    issues JSON, -- Найденные проблемы
    recommendations JSON, -- Рекомендации по исправлению
    focus_keyword_present BOOLEAN DEFAULT FALSE,
    meta_description_length INTEGER DEFAULT 0,
    title_length INTEGER DEFAULT 0,
    h1_present BOOLEAN DEFAULT FALSE,
    internal_links_count INTEGER DEFAULT 0,
    external_links_count INTEGER DEFAULT 0,
    images_alt_count INTEGER DEFAULT 0,
    readability_score INTEGER DEFAULT 0,
    date_checked DATETIME DEFAULT CURRENT_TIMESTAMP,
    check_duration INTEGER, -- Время проверки в секундах
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (keyword_id) REFERENCES keywords(id) ON DELETE CASCADE,
    INDEX idx_article_id (article_id),
    INDEX idx_seo_score (seo_score),
    INDEX idx_date_checked (date_checked)
);

-- Таблица финальных статей (Этап 4)
CREATE TABLE articles_final (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    article_id INTEGER NOT NULL,
    seo_check_id INTEGER NOT NULL,
    content_final TEXT NOT NULL,
    html_final LONGTEXT NOT NULL,
    json_ld JSON, -- Structured data
    meta_title VARCHAR(500) NOT NULL,
    meta_description TEXT NOT NULL,
    focus_keyword VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    canonical_url VARCHAR(500),
    internal_links JSON, -- Внутренние ссылки
    external_links JSON, -- Внешние ссылки
    images_data JSON, -- Данные об изображениях
    faq_schema JSON, -- FAQ Schema.org
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    improvement_duration INTEGER, -- Время улучшения в секундах
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (seo_check_id) REFERENCES seo_checks(id) ON DELETE CASCADE,
    INDEX idx_article_id (article_id),
    INDEX idx_slug (slug),
    INDEX idx_focus_keyword (focus_keyword)
);

-- Таблица очереди публикации (Этап 5)
CREATE TABLE publish_queue (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    article_final_id INTEGER NOT NULL,
    eec_json JSON NOT NULL, -- Einstein-Email-Code
    status ENUM('pending', 'processing', 'published', 'failed') DEFAULT 'pending',
    priority ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium',
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    error_message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    scheduled_at DATETIME, -- Планируемое время публикации
    FOREIGN KEY (article_final_id) REFERENCES articles_final(id) ON DELETE CASCADE,
    INDEX idx_status (status),
    INDEX idx_priority (priority),
    INDEX idx_scheduled_at (scheduled_at)
);

-- Таблица опубликованных статей (Этап 6)
CREATE TABLE published (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    publish_queue_id INTEGER NOT NULL,
    wp_post_id INTEGER NOT NULL,
    permalink VARCHAR(500) NOT NULL,
    response_code INTEGER,
    response_data JSON, -- Полный ответ от WordPress API
    publish_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    publish_duration INTEGER, -- Время публикации в секундах
    FOREIGN KEY (publish_queue_id) REFERENCES publish_queue(id) ON DELETE CASCADE,
    INDEX idx_wp_post_id (wp_post_id),
    INDEX idx_publish_date (publish_date)
);

-- Таблица статуса публикации (Этап 7)
CREATE TABLE publish_status (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    published_id INTEGER NOT NULL,
    keyword_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    seo_check_id INTEGER NOT NULL,
    article_final_id INTEGER NOT NULL,
    status ENUM('success', 'failed', 'partial') DEFAULT 'success',
    url VARCHAR(500),
    http_code INTEGER,
    response_time INTEGER, -- В миллисекундах
    checked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (published_id) REFERENCES published(id) ON DELETE CASCADE,
    FOREIGN KEY (keyword_id) REFERENCES keywords(id) ON DELETE CASCADE,
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (seo_check_id) REFERENCES seo_checks(id) ON DELETE CASCADE,
    FOREIGN KEY (article_final_id) REFERENCES articles_final(id) ON DELETE CASCADE,
    INDEX idx_status (status),
    INDEX idx_checked_at (checked_at)
);

-- =====================================================
-- ПОСТ-ПУБЛИКАЦИОННЫЙ КОНТРОЛЬНЫЙ КОНТУР
-- =====================================================

-- Таблица ожидаемых SEO-мета (Этап 8)
CREATE TABLE seo_meta_expected (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    article_final_id INTEGER NOT NULL,
    keyword_id INTEGER NOT NULL,
    focus_keyword VARCHAR(255) NOT NULL,
    title VARCHAR(500) NOT NULL,
    meta_description TEXT NOT NULL,
    begins_with_kw BOOLEAN NOT NULL,
    length_le_160 BOOLEAN NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (article_final_id) REFERENCES articles_final(id) ON DELETE CASCADE,
    FOREIGN KEY (keyword_id) REFERENCES keywords(id) ON DELETE CASCADE,
    INDEX idx_article_final_id (article_final_id),
    INDEX idx_keyword_id (keyword_id)
);

-- Таблица верификации WordPress мета (Этап 9)
CREATE TABLE wp_meta_verification (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    published_id INTEGER NOT NULL,
    keyword_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    article_final_id INTEGER NOT NULL,
    wp_post_id INTEGER NOT NULL,
    permalink VARCHAR(500) NOT NULL,
    wp_focuskw VARCHAR(255),
    wp_metadesc TEXT,
    focuskw_match BOOLEAN NOT NULL,
    metadesc_match BOOLEAN NOT NULL,
    metadesc_begins_with_kw BOOLEAN NOT NULL,
    metadesc_length_le_160 BOOLEAN NOT NULL,
    yoast_indexable_ok BOOLEAN,
    yoast_seo_score INTEGER,
    checked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (published_id) REFERENCES published(id) ON DELETE CASCADE,
    FOREIGN KEY (keyword_id) REFERENCES keywords(id) ON DELETE CASCADE,
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (article_final_id) REFERENCES articles_final(id) ON DELETE CASCADE,
    INDEX idx_wp_post_id (wp_post_id),
    INDEX idx_checked_at (checked_at)
);

-- Таблица аудита SEO-мета (Этап 10)
CREATE TABLE seo_meta_audit_log (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    publish_status_id INTEGER NOT NULL,
    wp_meta_verif_id INTEGER,
    status ENUM('ok', 'mismatch', 'wp_error', 'partial') NOT NULL,
    issues JSON, -- Детали проблем
    resolved BOOLEAN DEFAULT FALSE,
    resolution_attempts INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at DATETIME,
    FOREIGN KEY (publish_status_id) REFERENCES publish_status(id) ON DELETE CASCADE,
    FOREIGN KEY (wp_meta_verif_id) REFERENCES wp_meta_verification(id) ON DELETE SET NULL,
    INDEX idx_status (status),
    INDEX idx_resolved (resolved),
    INDEX idx_created_at (created_at)
);

-- =====================================================
-- ТЕХНИЧЕСКАЯ БИБЛИОТЕКА
-- =====================================================

-- Таблица шаблонов
CREATE TABLE templates (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    type ENUM('research', 'article', 'seo', 'wordpress', 'email', 'social') NOT NULL,
    structure JSON NOT NULL,
    description TEXT,
    version VARCHAR(20) DEFAULT '1.0',
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_type (type),
    INDEX idx_is_active (is_active)
);

-- Таблица карточек предприятий
CREATE TABLE company_cards (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    description TEXT,
    contact_info JSON, -- Контактная информация
    brand_colors JSON, -- Фирменные цвета
    fonts JSON, -- Фирменные шрифты
    style_guide JSON, -- Руководство по стилю
    wp_config JSON, -- Конфигурация WordPress
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_domain (domain),
    INDEX idx_industry (industry)
);

-- Таблица технических особенностей сайтов
CREATE TABLE site_technical_specs (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    company_id INTEGER NOT NULL,
    wp_version VARCHAR(20),
    theme_name VARCHAR(100),
    plugins JSON, -- Список плагинов
    api_endpoints JSON, -- API endpoints
    custom_fields JSON, -- Пользовательские поля
    seo_plugin VARCHAR(50), -- SEO плагин (Yoast, RankMath, etc.)
    performance_config JSON, -- Настройки производительности
    security_config JSON, -- Настройки безопасности
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES company_cards(id) ON DELETE CASCADE,
    INDEX idx_company_id (company_id)
);

-- =====================================================
-- АНАЛИТИКА И МОНИТОРИНГ
-- =====================================================

-- Таблица метрик статей
CREATE TABLE article_metrics (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    article_id INTEGER NOT NULL,
    published_id INTEGER,
    keyword_id INTEGER NOT NULL,
    page_views INTEGER DEFAULT 0,
    unique_visitors INTEGER DEFAULT 0,
    bounce_rate DECIMAL(5,2) DEFAULT 0.00,
    avg_time_on_page INTEGER DEFAULT 0, -- В секундах
    conversion_rate DECIMAL(5,2) DEFAULT 0.00,
    organic_traffic INTEGER DEFAULT 0,
    ranking_position INTEGER, -- Позиция в поиске
    date_measured DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (published_id) REFERENCES published(id) ON DELETE SET NULL,
    FOREIGN KEY (keyword_id) REFERENCES keywords(id) ON DELETE CASCADE,
    INDEX idx_article_id (article_id),
    INDEX idx_date_measured (date_measured)
);

-- Таблица логов системы
CREATE TABLE system_logs (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    level ENUM('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL') NOT NULL,
    module VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    context JSON, -- Дополнительный контекст
    keyword_id INTEGER,
    article_id INTEGER,
    execution_time INTEGER, -- В миллисекундах
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (keyword_id) REFERENCES keywords(id) ON DELETE SET NULL,
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE SET NULL,
    INDEX idx_level (level),
    INDEX idx_module (module),
    INDEX idx_created_at (created_at)
);

-- =====================================================
-- ИНДЕКСЫ И ОПТИМИЗАЦИЯ
-- =====================================================

-- Составные индексы для частых запросов
CREATE INDEX idx_keywords_status_priority ON keywords(status, priority);
CREATE INDEX idx_articles_keyword_created ON articles(keyword_id, created_at);
CREATE INDEX idx_published_wp_post_date ON published(wp_post_id, publish_date);
CREATE INDEX idx_metrics_article_date ON article_metrics(article_id, date_measured);

-- =====================================================
-- ТРИГГЕРЫ ДЛЯ АВТОМАТИЗАЦИИ
-- =====================================================

-- Триггер для обновления updated_at
DELIMITER //
CREATE TRIGGER update_keywords_timestamp 
    BEFORE UPDATE ON keywords 
    FOR EACH ROW 
BEGIN 
    SET NEW.updated_at = CURRENT_TIMESTAMP; 
END//

CREATE TRIGGER update_templates_timestamp 
    BEFORE UPDATE ON templates 
    FOR EACH ROW 
BEGIN 
    SET NEW.updated_at = CURRENT_TIMESTAMP; 
END//

CREATE TRIGGER update_company_cards_timestamp 
    BEFORE UPDATE ON company_cards 
    FOR EACH ROW 
BEGIN 
    SET NEW.updated_at = CURRENT_TIMESTAMP; 
END//
DELIMITER ;

-- =====================================================
-- ПРЕДСТАВЛЕНИЯ ДЛЯ АНАЛИТИКИ
-- =====================================================

-- Представление для полной цепочки статей
CREATE VIEW article_pipeline_view AS
SELECT 
    k.id as keyword_id,
    k.keyword,
    k.status as keyword_status,
    a.id as analysis_id,
    a.competition_level,
    ar.id as article_id,
    ar.title,
    ar.word_count,
    sc.id as seo_check_id,
    sc.seo_score,
    af.id as article_final_id,
    af.meta_title,
    af.focus_keyword,
    pq.id as publish_queue_id,
    pq.status as publish_status,
    p.id as published_id,
    p.wp_post_id,
    p.permalink,
    ps.status as final_status
FROM keywords k
LEFT JOIN analysis a ON k.id = a.keyword_id
LEFT JOIN articles ar ON a.id = ar.analysis_id
LEFT JOIN seo_checks sc ON ar.id = sc.article_id
LEFT JOIN articles_final af ON sc.id = af.seo_check_id
LEFT JOIN publish_queue pq ON af.id = pq.article_final_id
LEFT JOIN published p ON pq.id = p.publish_queue_id
LEFT JOIN publish_status ps ON p.id = ps.published_id;

-- Представление для SEO-аудита
CREATE VIEW seo_audit_view AS
SELECT 
    k.keyword,
    af.meta_title,
    af.focus_keyword,
    af.meta_description,
    sme.begins_with_kw,
    sme.length_le_160,
    wmv.focuskw_match,
    wmv.metadesc_match,
    wmv.yoast_indexable_ok,
    smal.status as audit_status,
    smal.issues,
    smal.resolved
FROM keywords k
JOIN articles_final af ON k.id = af.keyword_id
LEFT JOIN seo_meta_expected sme ON af.id = sme.article_final_id
LEFT JOIN wp_meta_verification wmv ON af.id = wmv.article_final_id
LEFT JOIN seo_meta_audit_log smal ON wmv.id = smal.wp_meta_verif_id;

-- =====================================================
-- НАЧАЛЬНЫЕ ДАННЫЕ
-- =====================================================

-- Вставка карточки компании BizFin Pro
INSERT INTO company_cards (name, domain, industry, description, contact_info, brand_colors, fonts, style_guide, wp_config) VALUES
('BizFin Pro', 'bizfin-pro.ru', 'Финансовые услуги', 'Компания по банковским гарантиям и кредитованию для бизнеса', 
'{"phone": "+7 (499) 757-01-25", "email": "info@bizfin-pro.ru", "address": "Москва"}',
'{"primary": "#FDFBF7", "text": "#333333", "accent": "#FF8C00", "secondary": "#FFFFFF", "border": "#E0E0E0"}',
'{"primary": "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif", "heading": "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif"}',
'{"gradients": true, "shadows": true, "border_radius": "8-15px", "spacing": "consistent"}',
'{"api_url": "https://bizfin-pro.ru/wp-json/wp/v2", "username": "bizfin_pro_r", "app_password": "U3Ep gU2T clRu FcwN QU6l Dsda"}');

-- Вставка базовых шаблонов
INSERT INTO templates (name, type, structure, description) VALUES
('research_template_v1', 'research', '{"sources": 3, "analysis_depth": "deep", "competitors": true, "gaps": true}', 'Шаблон для исследования конкурентов'),
('article_structure_fintech_v1', 'article', '{"min_words": 2500, "sections": ["intro", "main", "faq", "cta"], "seo_optimized": true}', 'Структура статьи для финансовой тематики'),
('seo_checklist_v1', 'seo', '{"focus_keyword": true, "meta_description": true, "h1": true, "internal_links": true}', 'Чек-лист SEO-оптимизации'),
('wordpress_post_schema_v1', 'wordpress', '{"html": true, "meta": true, "schema": true, "images": true}', 'Схема публикации в WordPress');

-- =====================================================
-- ЗАВЕРШЕНИЕ
-- =====================================================

-- Создание пользователя для приложения
CREATE USER IF NOT EXISTS 'bizfin_seo'@'localhost' IDENTIFIED BY 'bizfin_seo_2024!';
GRANT SELECT, INSERT, UPDATE, DELETE ON bizfin_pro_seo.* TO 'bizfin_seo'@'localhost';
FLUSH PRIVILEGES;

-- Вывод информации о созданной схеме
SELECT 'Database schema created successfully!' as status;
SELECT COUNT(*) as total_tables FROM information_schema.tables WHERE table_schema = 'bizfin_pro_seo';


