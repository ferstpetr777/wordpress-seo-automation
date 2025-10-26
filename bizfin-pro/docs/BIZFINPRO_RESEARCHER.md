# BizFin Pro Researcher - Модуль веб-исследований

## 📋 Описание

**BizFin Pro Researcher** — специализированный модуль веб-исследований для рынка банковских гарантий в России. Модуль обеспечивает комплексный анализ конкурентной среды и создание SEO-оптимизированного контента.

## 🎯 Основные возможности

### 1. **SERP-анализ**
- ТОП-5 органических результатов через DuckDuckGo HTML
- Анализ заголовков, сниппетов и доменов
- Фильтрация по релевантности и актуальности

### 2. **Парсинг страниц**
- Извлечение структуры H1/H2/H3
- Анализ таблиц и FAQ-секций
- Поиск калькуляторов и правовых ссылок
- Определение авторов и дат публикации
- Анализ schema.org разметки

### 3. **Синтез корпуса**
- Консенсус по числовым данным
- Выявление расхождений в информации
- Анализ правовых якорей
- Определение общей структуры контента

### 4. **SEO Blueprint**
- Генерация оптимизированных заголовков
- Создание мета-описаний
- Структурированные планы контента
- FAQ-блоки и внутренние ссылки

### 5. **Интеграция с БД**
- Сохранение результатов исследований
- Уникальные ID исследований
- Полная история анализов

## 🚀 Установка и настройка

### Зависимости
```bash
pip install requests beautifulsoup4 lxml pydantic tqdm
```

### Структура файлов
```
modules/research/
├── __init__.py
├── bizfinpro_researcher.py
└── README.md

scripts/
├── test_bizfinpro_researcher.py
└── ...

docs/
└── BIZFINPRO_RESEARCHER.md
```

## 💻 Использование

### CLI интерфейс

```bash
# Запуск исследования
python3 modules/research/bizfinpro_researcher.py --kw "банковская гарантия"

# Список исследований
python3 modules/research/bizfinpro_researcher.py --list

# Просмотр конкретного исследования
python3 modules/research/bizfinpro_researcher.py --show 1
```

### Программный интерфейс

```python
from modules.research.bizfinpro_researcher import BizFinProResearcher, run_research_pipeline

# Инициализация
researcher = BizFinProResearcher()

# Запуск исследования
research_data = run_research_pipeline("банковская гарантия", researcher)

# Получение данных из БД
research = researcher.get_research_by_id(research_data['research_id'])

# Список исследований
researches = researcher.list_researches()
```

## 📊 Структура данных

### Серп-результаты (SerpItem)
```python
{
    "rank": 1,
    "url": "https://example.com",
    "title": "Заголовок страницы",
    "publisher": "example.com",
    "snippet": "Описание страницы...",
    "content_type": "guide",
    "why_selected": "ТОП-результат органической выдачи DDG"
}
```

### Артефакты страниц (PageArtifact)
```python
{
    "url": "https://example.com",
    "title": "Заголовок",
    "h_outline": ["H1: Главный заголовок", "H2: Подзаголовок"],
    "content_plain": "Основной текст страницы...",
    "tables_tsv": ["Таблица в формате TSV"],
    "faq": [{"q": "Вопрос", "a": "Ответ"}],
    "legal_refs": ["44-ФЗ", "223-ФЗ"],
    "ctas": ["Оставить заявку", "Рассчитать стоимость"]
}
```

### SEO Blueprint
```python
{
    "title": "Банковская гарантия: стоимость, сроки и документы",
    "h1": "Банковская гарантия",
    "slug": "bankovskaya-garantiya",
    "meta_description": "Описание для поисковиков...",
    "outline": ["H2 Что такое банковская гарантия", "H2 Виды БГ"],
    "faq": [{"q": "Сколько стоит?", "a": "Зависит от суммы..."}],
    "internal_links": [{"anchor": "Калькулятор", "target": "/calculator/"}]
}
```

## 🗄️ База данных

### Таблица web_research
```sql
CREATE TABLE web_research (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    research_name TEXT NOT NULL,
    serp_data BLOB,
    pages_data BLOB,
    corpus_synthesis BLOB,
    seo_blueprint BLOB,
    evidence_pack TEXT,
    eeat_checks TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    execution_time_seconds INTEGER DEFAULT 0,
    status TEXT DEFAULT 'completed'
);
```

## 🔧 Интеграция с пайплайном

Модуль интегрирован в основную архитектуру BizFin Pro:

1. **Входные данные**: Ключевое слово от пользователя
2. **Обработка**: Веб-исследования и анализ
3. **Результат**: Готовые данные для генерации контента
4. **Сохранение**: В центральной БД проекта

## 📈 Производительность

- **Время выполнения**: 5-60 секунд (зависит от доступности сайтов)
- **Обрабатываемые страницы**: 3-5 из ТОП-5 SERP
- **Объем данных**: ~50-100KB на исследование
- **Успешность**: 90%+ при стабильном интернете

## 🛡️ Безопасность и надежность

- **User-Agent**: Реалистичный браузерный заголовок
- **Таймауты**: 15 секунд на запрос
- **Повторы**: До 3 попыток при ошибках
- **Фильтрация**: Блокировка UTM-параметров и рекламы

## 🎯 Специализация под БГ

Модуль оптимизирован для банковских гарантий:

- **Правовые ссылки**: 44-ФЗ, 223-ФЗ, ГК РФ
- **Калькуляторы**: Поиск форм расчета стоимости
- **CTA**: Специфичные призывы к действию
- **Терминология**: Бенефициар, принципал, контргарантия
- **YMYL**: Соблюдение требований Google для финансового контента

## 🚀 Примеры использования

### Базовое исследование
```python
researcher = BizFinProResearcher()
data = run_research_pipeline("банковская гарантия", researcher)
print(f"Исследование ID: {data['research_id']}")
```

### Анализ конкурентов
```python
# Получаем данные исследования
research = researcher.get_research_by_id(1)
serp_data = research['serp_data']

for item in serp_data:
    print(f"Позиция {item['rank']}: {item['title']}")
    print(f"Домен: {item['publisher']}")
```

### SEO-планирование
```python
research = researcher.get_research_by_id(1)
blueprint = research['seo_blueprint']

print(f"Рекомендуемый title: {blueprint['title']}")
print(f"Структура: {blueprint['outline']}")
print(f"FAQ: {len(blueprint['faq'])} вопросов")
```

## 📝 Логирование

Модуль ведет подробные логи:
- Инициализация компонентов
- Прогресс исследований
- Ошибки и предупреждения
- Статистика выполнения

## 🔄 Обновления и развитие

Планируемые улучшения:
- [ ] Поддержка Yandex SERP
- [ ] Расширенный анализ изображений
- [ ] Интеграция с Google Trends
- [ ] Автоматическое обновление данных
- [ ] Экспорт в различные форматы

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи в консоли
2. Убедитесь в стабильности интернет-соединения
3. Проверьте доступность DuckDuckGo
4. Обратитесь к разработчикам проекта

---

**BizFin Pro Researcher** — ваш надежный помощник в создании качественного SEO-контента для банковских гарантий! 🚀
