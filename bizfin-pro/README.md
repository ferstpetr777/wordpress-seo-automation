# BizFin Pro - SEO Article Generation Pipeline v2

## 🎯 Описание проекта

Автоматизированная система для генерации, оптимизации и публикации SEO-статей на WordPress сайт bizfin-pro.ru. Проект реализует расширенный пайплайн v2 с полной преемственностью данных и пост-публикационным контролем.

## 🏗️ Архитектура проекта

### Основные компоненты:
- **Research Engine** - исследование конкурентов и анализ ключевых слов
- **Content Generator** - генерация статей на основе шаблонов
- **SEO Optimizer** - техническая SEO-оптимизация
- **WordPress Publisher** - публикация через REST API
- **Post-Publish Verifier** - контроль качества после публикации
- **Analytics Engine** - аналитика и отчетность

### Технический стек:
- **Python 3.8+** - основной язык
- **SQLite/MySQL** - база данных
- **WordPress REST API** - интеграция с сайтом
- **BeautifulSoup4** - парсинг веб-страниц
- **Requests** - HTTP-запросы
- **Jinja2** - шаблонизация

## 📁 Структура проекта

```
bizfin-pro/
├── README.md                    # Документация проекта
├── requirements.txt             # Зависимости Python
├── config/                      # Конфигурационные файлы
│   ├── database.py             # Настройки БД
│   ├── wordpress.py            # Настройки WordPress
│   └── templates.py            # Настройки шаблонов
├── db/                         # База данных
│   ├── schema.sql              # Схема БД
│   ├── migrations/             # Миграции
│   └── seeds/                  # Начальные данные
├── modules/                    # Основные модули
│   ├── research/               # Исследование конкурентов
│   ├── generator/              # Генерация контента
│   ├── seo_optimizer/          # SEO-оптимизация
│   ├── publisher/              # Публикация в WordPress
│   ├── verifier/               # Пост-публикационный контроль
│   └── analytics/              # Аналитика
├── templates/                  # Шаблоны и библиотека
│   ├── research/               # Шаблоны исследования
│   ├── articles/               # Шаблоны статей
│   ├── seo/                    # SEO-шаблоны
│   └── wordpress/              # Шаблоны WordPress
├── data/                       # Данные проекта
│   ├── keywords/               # Ключевые слова
│   ├── articles/               # Сгенерированные статьи
│   ├── images/                 # Изображения
│   └── reports/                # Отчеты
├── scripts/                    # Скрипты запуска
│   ├── pipeline_v2.py          # Основной пайплайн
│   ├── research_runner.py      # Запуск исследования
│   └── publish_runner.py       # Запуск публикации
└── tests/                      # Тесты
    ├── unit/                   # Юнит-тесты
    └── integration/            # Интеграционные тесты
```

## 🔄 Пайплайн v2

### Этапы обработки:

1. **Ввод ключевого слова** → `keywords` table
2. **Исследование конкурентов** → `analysis` table
3. **Генерация статьи** → `articles` table
4. **SEO-проверка** → `seo_checks` table
5. **Улучшение статьи** → `articles_final` table
6. **Формирование EEC** → `publish_queue` table
7. **Публикация в WordPress** → `published` table
8. **Проверка публикации** → `publish_status` table
9. **Фиксация SEO-мета** → `seo_meta_expected` table
10. **Верификация WordPress** → `wp_meta_verification` table
11. **Финальный аудит** → `seo_meta_audit_log` table

### Цепочка преемственности:
```
keywords → analysis → articles → seo_checks → articles_final → 
publish_queue → published → publish_status → seo_meta_expected → 
wp_meta_verification → seo_meta_audit_log
```

## 🚀 Быстрый старт

1. **Установка зависимостей:**
```bash
pip install -r requirements.txt
```

2. **Инициализация базы данных:**
```bash
python scripts/init_database.py
```

3. **Запуск пайплайна:**
```bash
python scripts/pipeline_v2.py --keyword "банковская гарантия"
```

## 📊 Мониторинг и аналитика

- **Дашборд** - веб-интерфейс для мониторинга
- **Отчеты** - детальная аналитика по статьям
- **Логи** - полное логирование всех операций
- **Метрики** - KPI и эффективность пайплайна

## 🔧 Конфигурация

Все настройки находятся в папке `config/`:
- **database.py** - подключение к БД
- **wordpress.py** - настройки WordPress API
- **templates.py** - шаблоны генерации

## 📈 Расширения

Проект поддерживает:
- **Мультиязычность** - генерация на разных языках
- **A/B тестирование** - тестирование разных версий
- **Машинное обучение** - улучшение качества на основе данных
- **Интеграции** - подключение внешних сервисов

## 📝 Лицензия

Проект разработан для внутреннего использования BizFin Pro.

## 👥 Команда

- **AI Assistant** - архитектура и разработка
- **BizFin Pro Team** - бизнес-требования и тестирование


