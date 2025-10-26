# WordPress SEO Automation Platform

## 🎯 Описание проекта

Комплексная платформа для автоматизации создания, оптимизации и публикации SEO-статей в WordPress. Система включает в себя исследование конкурентов, генерацию высококачественного контента, SEO-оптимизацию и автоматическую публикацию с полным контролем качества.

## 🏗️ Архитектура системы

### Основные компоненты

1. **Research Engine** - Исследование конкурентов и анализ ключевых слов
2. **Content Generator** - Генерация статей на основе AI и шаблонов
3. **SEO Optimizer** - Техническая SEO-оптимизация с Yoast интеграцией
4. **WordPress Publisher** - Публикация через REST API
5. **Quality Controller** - Контроль качества и аудит статей
6. **Analytics Engine** - Аналитика и отчетность

### Технический стек

- **Backend**: Python 3.8+, FastAPI, SQLite/MySQL
- **AI/ML**: OpenAI GPT, LangChain, CrewAI
- **Database**: SQLite (разработка), MySQL (продакшн)
- **WordPress**: REST API, Yoast SEO
- **Web Scraping**: BeautifulSoup4, Requests
- **Templates**: Jinja2, Custom JSON templates
- **Monitoring**: Structured logging, Prometheus metrics

## 📁 Структура проекта

```
wordpress-seo-automation/
├── README.md                           # Основная документация
├── CURSOR_VECTOR_DB.md                # Документация для Cursor
├── requirements.txt                    # Python зависимости
├── .env.example                       # Пример переменных окружения
├── .gitignore                         # Git исключения
├── 
├── # Основные модули
├── wordPress_automation_final.py      # Финальная версия автоматизации
├── enhanced_wordpress_automation.py   # Улучшенная версия с AI
├── enhanced_content_generator.py      # Генератор контента
├── run_enhanced_pipeline.py           # Запуск пайплайна
├── 
├── # Проект BizFin Pro
├── bizfin-pro/                        # Основной проект
│   ├── README.md                      # Документация BizFin Pro
│   ├── PROJECT_SUMMARY.md             # Итоговый отчет
│   ├── requirements.txt               # Зависимости
│   ├── config/                        # Конфигурации
│   │   ├── database.py               # Настройки БД
│   │   ├── wordpress.py              # Настройки WordPress
│   │   └── company_profile.py        # Профиль компании
│   ├── db/                           # База данных
│   │   ├── schema.sql                # Схема БД
│   │   └── migrations/               # Миграции
│   ├── modules/                      # Основные модули
│   │   ├── research/                 # Исследование конкурентов
│   │   ├── ai_agent/                 # AI агенты
│   │   └── alwrity_integration/      # Интеграция с Alwrity
│   ├── templates/                    # Шаблоны
│   │   ├── research/                 # Шаблоны исследования
│   │   └── articles/                 # Шаблоны статей
│   ├── scripts/                      # Скрипты запуска
│   │   ├── pipeline_v2.py            # Основной пайплайн
│   │   ├── init_database.py          # Инициализация БД
│   │   └── demo_pipeline.py          # Демонстрация
│   └── data/                         # Данные проекта
│       ├── bizfin_pro.db             # SQLite БД
│       └── logs/                     # Логи
├── 
├── # Дополнительные проекты
├── geser-platform/                   # Next.js платформа
├── grapesjs-ai-project/              # AI интерфейс
├── 
├── # Документация
├── docs/                             # Документация
│   ├── architecture/                 # Архитектурные диаграммы
│   ├── api/                          # API документация
│   └── deployment/                   # Инструкции развертывания
├── 
├── # Тестирование
├── tests/                            # Тесты
│   ├── unit/                         # Юнит-тесты
│   ├── integration/                  # Интеграционные тесты
│   └── e2e/                          # End-to-end тесты
├── 
└── # Утилиты
    ├── scripts/                      # Утилиты
    ├── tools/                        # Инструменты
    └── monitoring/                   # Мониторинг
```

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
# Клонирование репозитория
git clone https://github.com/ferstpetr777/wordpress-seo-automation.git
cd wordpress-seo-automation

# Установка Python зависимостей
pip install -r requirements.txt

# Установка зависимостей BizFin Pro
pip install -r bizfin-pro/requirements.txt
```

### 2. Настройка окружения

```bash
# Копирование файла окружения
cp .env.example .env

# Редактирование переменных
nano .env
```

### 3. Инициализация базы данных

```bash
# Инициализация основной БД
python bizfin-pro/scripts/init_database.py

# Инициализация SQLite для тестирования
python bizfin-pro/scripts/init_sqlite_db.py
```

### 4. Запуск системы

```bash
# Запуск улучшенного пайплайна
python run_enhanced_pipeline.py

# Или запуск BizFin Pro пайплайна
python bizfin-pro/scripts/pipeline_v2.py --keyword "банковская гарантия"
```

## 🔄 Пайплайны обработки

### Enhanced Pipeline (Рекомендуемый)

1. **Анализ намерений** - Определение типа запроса пользователя
2. **Создание структуры** - Адаптивное оглавление под запрос
3. **Генерация контента** - Высококачественный контент с AI
4. **SEO-оптимизация** - Автоматическая оптимизация для поиска
5. **Публикация** - Автоматическая публикация в WordPress
6. **Контроль качества** - Аудит и улучшение статей

### BizFin Pro Pipeline v2

1. **Исследование конкурентов** - Анализ топ-сайтов
2. **Генерация статьи** - Создание контента по шаблонам
3. **SEO-проверка** - Техническая оптимизация
4. **Улучшение статьи** - Доработка контента
5. **Публикация** - Отправка в WordPress
6. **Верификация** - Проверка качества публикации

## 📊 Возможности системы

### Исследование и анализ

- **Анализ конкурентов** - Поиск и анализ топ-сайтов
- **LSI ключевые слова** - Извлечение семантических слов
- **Анализ структуры** - Изучение заголовков и контента
- **Выявление пробелов** - Поиск возможностей для улучшения

### Генерация контента

- **AI-генерация** - Создание контента с помощью GPT
- **Адаптивные шаблоны** - Структуры под разные типы запросов
- **Реальные данные** - Использование актуальной информации
- **Качество контента** - Система оценки 0-100 баллов

### SEO-оптимизация

- **Yoast SEO интеграция** - Автоматическая настройка мета-данных
- **Структурированные данные** - Schema.org разметка
- **Внутренние ссылки** - Автоматическое создание связей
- **Оптимизация заголовков** - H1-H6 структура

### Публикация и контроль

- **WordPress REST API** - Автоматическая публикация
- **Контроль качества** - Аудит после публикации
- **Мониторинг** - Отслеживание статуса статей
- **Аналитика** - Метрики эффективности

## 🎯 Типы поддерживаемых запросов

### Transactional (Транзакционные)
- Калькуляторы стоимости
- Оформление услуг
- Заказ документов
- **Структура**: 7 разделов с фокусом на действиях

### Informational (Информационные)
- Списки документов
- Инструкции проверки
- Объяснения процессов
- **Структура**: 7 разделов с фокусом на информации

### General (Общие)
- Определения понятий
- Виды и типы
- Сравнения и советы
- **Структура**: 7 разделов с общим обзором

## 📈 Система оценки качества

### Оценка контента (0-100 баллов)
- **Объем статьи** (30 баллов): 2000+ слов = 30, 1500-1999 = 20, 1000-1499 = 10
- **Структура** (25 баллов): H1 + H2 + H3 заголовки
- **Разнообразие** (25 баллов): списки, таблицы, нумерованные списки
- **Уникальность** (20 баллов): оптимальное вхождение ключевых слов

### SEO-оценка (0-100 баллов)
- **Заголовок H1** (25 баллов): наличие ключевого слова
- **Начало статьи** (25 баллов): ключевое слово в первых 200 символах
- **Структура** (25 баллов): H2 и H3 заголовки
- **Ссылки** (25 баллов): внутренние ссылки

## 🗄️ База данных

### Основные таблицы

- **keywords** - Ключевые слова для анализа
- **analysis** - Результаты исследования конкурентов
- **articles** - Сгенерированные статьи
- **seo_checks** - SEO-проверки и рекомендации
- **articles_final** - Финальные версии статей
- **published** - Опубликованные статьи
- **quality_checks** - Результаты проверок качества

### Дополнительные таблицы

- **templates** - Шаблоны генерации
- **company_cards** - Карточки предприятий
- **article_metrics** - Метрики статей
- **system_logs** - Логи системы

## 🔧 Конфигурация

### Переменные окружения

```bash
# WordPress настройки
WP_URL=https://your-site.com/wp-json/wp/v2
WP_USERNAME=your_username
WP_APP_PASSWORD=your_app_password

# База данных
DB_HOST=localhost
DB_PORT=3306
DB_NAME=wordpress_seo
DB_USER=username
DB_PASSWORD=password

# AI настройки
OPENAI_API_KEY=your_openai_key
AI_MODEL=gpt-4
AI_TEMPERATURE=0.7

# Мониторинг
LOG_LEVEL=INFO
METRICS_ENABLED=true
```

### Настройки WordPress

- **REST API** - Включен для публикации
- **Yoast SEO** - Для SEO-оптимизации
- **Custom Fields** - Для мета-данных
- **User Roles** - Настроенные права доступа

## 📊 Мониторинг и аналитика

### Метрики системы

- **Время генерации** - Скорость создания статей
- **Качество контента** - Оценки 0-100 баллов
- **SEO-оценки** - Показатели оптимизации
- **Успешность публикации** - Процент успешных публикаций

### Логирование

- **Структурированные логи** - JSON формат
- **Уровни логирования** - DEBUG, INFO, WARNING, ERROR
- **Ротация логов** - Автоматическая очистка старых логов
- **Мониторинг ошибок** - Отслеживание проблем

## 🚀 Развертывание

### Локальная разработка

```bash
# Клонирование и установка
git clone https://github.com/ferstpetr777/wordpress-seo-automation.git
cd wordpress-seo-automation
pip install -r requirements.txt

# Запуск в режиме разработки
python run_enhanced_pipeline.py --dev
```

### Продакшн развертывание

```bash
# Docker развертывание
docker-compose up -d

# Или прямое развертывание
python run_enhanced_pipeline.py --production
```

### Мониторинг

- **Health checks** - Проверка состояния системы
- **Metrics endpoint** - Метрики для Prometheus
- **Log aggregation** - Централизованное логирование
- **Alerting** - Уведомления о проблемах

## 🧪 Тестирование

### Запуск тестов

```bash
# Все тесты
pytest tests/ -v

# Юнит-тесты
pytest tests/unit/ -v

# Интеграционные тесты
pytest tests/integration/ -v

# E2E тесты
pytest tests/e2e/ -v
```

### Покрытие кода

```bash
# Генерация отчета покрытия
pytest --cov=. --cov-report=html

# Просмотр отчета
open htmlcov/index.html
```

## 📚 API Документация

### Основные эндпоинты

- `POST /api/v1/research` - Исследование ключевого слова
- `POST /api/v1/generate` - Генерация статьи
- `POST /api/v1/publish` - Публикация в WordPress
- `GET /api/v1/status/{id}` - Статус обработки
- `GET /api/v1/metrics` - Метрики системы

### Примеры запросов

```bash
# Исследование ключевого слова
curl -X POST "http://localhost:8000/api/v1/research" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "банковская гарантия", "language": "ru"}'

# Генерация статьи
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "банковская гарантия", "template": "financial"}'
```

## 🤝 Контрибьюция

### Процесс разработки

1. Fork репозитория
2. Создание feature branch
3. Написание тестов
4. Code review
5. Merge в main

### Требования к коду

- **Покрытие тестами** > 80%
- **Соответствие PEP 8** - Python стиль
- **Типизация** - Type hints для всех функций
- **Документация** - Docstrings для всех методов

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 👥 Команда

- **ferstpetr777** - Архитектура и разработка
- **AI Assistant** - Техническая поддержка
- **BizFin Pro Team** - Бизнес-требования

## 📞 Поддержка

- **GitHub Issues** - Для багов и feature requests
- **Email** - Для критических вопросов
- **Документация** - В репозитории

## 🔗 Полезные ссылки

- [WordPress REST API](https://developer.wordpress.org/rest-api/)
- [Yoast SEO API](https://developer.yoast.com/customization/apis/)
- [OpenAI API](https://platform.openai.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Проект готов к продуктивному использованию!** 🚀
