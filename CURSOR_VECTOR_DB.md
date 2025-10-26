# WordPress SEO Automation Platform - Документация для Cursor Vector DB

## Описание проекта

**WordPress SEO Automation Platform** - это комплексная система автоматизации создания, оптимизации и публикации SEO-статей в WordPress. Платформа объединяет исследование конкурентов, AI-генерацию контента, SEO-оптимизацию и автоматическую публикацию с полным контролем качества.

## Архитектура системы

### Основные компоненты

1. **Research Engine** - Исследование конкурентов и анализ ключевых слов
2. **AI Content Generator** - Генерация контента с помощью GPT и CrewAI
3. **SEO Optimizer** - Техническая SEO-оптимизация с Yoast интеграцией
4. **WordPress Publisher** - Публикация через REST API
5. **Quality Controller** - Контроль качества и аудит статей
6. **Analytics Engine** - Аналитика и отчетность

### Технический стек

- **Backend**: Python 3.8+, FastAPI, SQLite/MySQL
- **AI/ML**: OpenAI GPT-4, LangChain, CrewAI, Sentence Transformers
- **Database**: SQLite (разработка), MySQL (продакшн)
- **WordPress**: REST API, Yoast SEO, Custom Fields
- **Web Scraping**: BeautifulSoup4, Requests, Selenium
- **Templates**: Jinja2, Custom JSON templates
- **Monitoring**: Structured logging, Prometheus metrics

## Структура кода

### Основные модули

```
wordpress-seo-automation/
├── # Основные скрипты автоматизации
├── wordPress_automation_final.py      # Финальная версия автоматизации
├── enhanced_wordpress_automation.py   # Улучшенная версия с AI
├── enhanced_content_generator.py      # Генератор контента
├── run_enhanced_pipeline.py           # Запуск пайплайна
├── 
├── # Проект BizFin Pro (основной)
├── bizfin-pro/
│   ├── config/                        # Конфигурации
│   │   ├── database.py               # Настройки БД
│   │   ├── wordpress.py              # Настройки WordPress
│   │   └── company_profile.py        # Профиль компании
│   ├── modules/                      # Основные модули
│   │   ├── research/                 # Исследование конкурентов
│   │   │   ├── competitor_analyzer.py # Анализатор конкурентов
│   │   │   ├── ai_web_researcher.py  # AI веб-исследователь
│   │   │   └── bizfinpro_researcher.py # Специализированный исследователь
│   │   ├── ai_agent/                 # AI агенты
│   │   │   ├── ai_assistant_client.py # AI ассистент
│   │   │   └── server.py             # AI сервер
│   │   └── alwrity_integration/      # Интеграция с Alwrity
│   │       └── alwrity_client.py     # Alwrity клиент
│   ├── scripts/                      # Скрипты запуска
│   │   ├── pipeline_v2.py            # Основной пайплайн v2
│   │   ├── init_database.py          # Инициализация БД
│   │   ├── demo_pipeline.py          # Демонстрация
│   │   └── auto_research.py          # Автоматическое исследование
│   └── templates/                    # Шаблоны
│       ├── research/                 # Шаблоны исследования
│       └── articles/                 # Шаблоны статей
├── 
├── # Дополнительные проекты
├── geser-platform/                   # Next.js платформа
├── grapesjs-ai-project/              # AI интерфейс
└── docs/                             # Документация
```

### Ключевые файлы

- `wordPress_automation_final.py` - Основной класс автоматизации WordPress
- `enhanced_wordpress_automation.py` - Улучшенная версия с AI интеграцией
- `enhanced_content_generator.py` - Генератор высококачественного контента
- `bizfin-pro/modules/research/competitor_analyzer.py` - Анализатор конкурентов
- `bizfin-pro/scripts/pipeline_v2.py` - Основной пайплайн обработки

## Пайплайны обработки

### Enhanced Pipeline (Рекомендуемый)

```python
class EnhancedWordPressAutomation:
    def __init__(self):
        self.content_generator = EnhancedContentGenerator()
        self.db_path = "wordpress_articles_enhanced.db"
        
    async def run_enhanced_automation(self):
        for keyword in self.keywords:
            # 1. Анализ намерений пользователя
            intent_analysis = await self.analyze_keyword_intent(keyword)
            
            # 2. Создание адаптивного оглавления
            outline = await self.create_adaptive_outline(keyword, intent_analysis)
            
            # 3. Генерация высококачественного контента
            content = await self.generate_high_quality_content(keyword, outline)
            
            # 4. SEO-оптимизация
            seo_optimized = await self.optimize_for_seo(content, keyword)
            
            # 5. Публикация в WordPress
            result = await self.publish_to_wordpress(seo_optimized)
            
            # 6. Сохранение в БД
            await self.save_article_to_db(result)
```

### BizFin Pro Pipeline v2

```python
class BizFinProPipeline:
    def __init__(self):
        self.competitor_analyzer = CompetitorAnalyzer()
        self.db_path = "bizfin_pro.db"
        
    async def run_pipeline_v2(self, keyword):
        # Этап 1: Исследование конкурентов
        analysis = await self.competitor_analyzer.analyze_competitors(keyword)
        
        # Этап 2: Генерация статьи
        article = await self.generate_article(keyword, analysis)
        
        # Этап 3: SEO-проверка
        seo_check = await self.seo_optimizer.check_article(article)
        
        # Этап 4: Улучшение статьи
        improved_article = await self.improve_article(article, seo_check)
        
        # Этап 5: Публикация
        result = await self.publish_to_wordpress(improved_article)
        
        # Этап 6: Верификация
        verification = await self.verify_publication(result)
```

## AI и машинное обучение

### Генерация контента

```python
class EnhancedContentGenerator:
    def __init__(self):
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = "gpt-4"
        
    async def generate_section_content(self, section_type, keyword, context):
        """Генерация контента для конкретного раздела"""
        prompt = self.create_section_prompt(section_type, keyword, context)
        
        response = await self.openai_client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
```

### Анализ намерений

```python
async def analyze_keyword_intent(self, keyword):
    """Анализ намерений пользователя по ключевому слову"""
    intent_indicators = {
        'transactional': ['калькулятор', 'оформить', 'купить', 'заказать'],
        'informational': ['документы', 'проверить', 'как', 'что такое'],
        'general': ['виды', 'типы', 'сравнение', 'обзор']
    }
    
    keyword_lower = keyword.lower()
    for intent_type, indicators in intent_indicators.items():
        if any(indicator in keyword_lower for indicator in indicators):
            return {
                'intent': intent_type,
                'confidence': 0.9,
                'focus': self.determine_focus(intent_type)
            }
    
    return {'intent': 'general', 'confidence': 0.5, 'focus': 'overview'}
```

## База данных

### Схема основных таблиц

```sql
-- Ключевые слова
CREATE TABLE keywords (
    id INTEGER PRIMARY KEY,
    keyword TEXT NOT NULL,
    intent_type TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Анализ конкурентов
CREATE TABLE analysis (
    id INTEGER PRIMARY KEY,
    keyword_id INTEGER,
    competitor_url TEXT,
    title TEXT,
    word_count INTEGER,
    lsi_keywords TEXT,
    gaps TEXT,
    recommendations TEXT,
    FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

-- Статьи
CREATE TABLE articles (
    id INTEGER PRIMARY KEY,
    keyword_id INTEGER,
    title TEXT,
    content TEXT,
    word_count INTEGER,
    quality_score INTEGER,
    seo_score INTEGER,
    wp_post_id INTEGER,
    wp_post_url TEXT,
    status TEXT DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

-- Проверки качества
CREATE TABLE quality_checks (
    id INTEGER PRIMARY KEY,
    article_id INTEGER,
    check_type TEXT,
    score INTEGER,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (article_id) REFERENCES articles(id)
);
```

### Операции с базой данных

```python
class DatabaseManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.setup_tables()
    
    async def save_keyword_research(self, keyword, research_data):
        """Сохранение исследования ключевого слова"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO keyword_research (keyword, research_data, created_at)
            VALUES (?, ?, ?)
        """, (keyword, json.dumps(research_data), datetime.now()))
        self.conn.commit()
        return cursor.lastrowid
    
    async def save_article(self, article_data):
        """Сохранение статьи"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO articles (keyword, title, content, word_count, 
                                quality_score, seo_score, wp_post_id, wp_post_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            article_data['keyword'],
            article_data['title'],
            article_data['content'],
            article_data['word_count'],
            article_data['quality_score'],
            article_data['seo_score'],
            article_data['wp_post_id'],
            article_data['wp_post_url']
        ))
        self.conn.commit()
        return cursor.lastrowid
```

## WordPress интеграция

### REST API клиент

```python
class WordPressClient:
    def __init__(self, wp_url, username, app_password):
        self.wp_url = wp_url
        self.auth = (username, app_password)
        
    async def create_post(self, post_data):
        """Создание поста в WordPress"""
        response = requests.post(
            f"{self.wp_url}/posts",
            json=post_data,
            auth=self.auth,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Ошибка создания поста: {response.text}")
    
    async def update_post_meta(self, post_id, meta_data):
        """Обновление мета-данных поста"""
        for key, value in meta_data.items():
            response = requests.post(
                f"{self.wp_url}/posts/{post_id}/meta",
                json={'key': key, 'value': value},
                auth=self.auth
            )
            
            if response.status_code != 201:
                raise Exception(f"Ошибка обновления мета: {response.text}")
```

### Yoast SEO интеграция

```python
class YoastSEOOptimizer:
    def __init__(self, wp_client):
        self.wp_client = wp_client
        
    async def optimize_post(self, post_id, keyword, content):
        """Оптимизация поста для Yoast SEO"""
        meta_data = {
            '_yoast_wpseo_focuskw': keyword,
            '_yoast_wpseo_metadesc': self.generate_meta_description(content, keyword),
            '_yoast_wpseo_title': self.generate_seo_title(content, keyword),
            '_yoast_wpseo_canonical': f"https://site.com/post/{post_id}",
            '_yoast_wpseo_meta-robots-noindex': '0',
            '_yoast_wpseo_meta-robots-nofollow': '0'
        }
        
        await self.wp_client.update_post_meta(post_id, meta_data)
        return meta_data
```

## Система оценки качества

### Оценка контента

```python
class ContentQualityEvaluator:
    def evaluate_content_quality(self, content, keyword):
        """Оценка качества контента (0-100 баллов)"""
        scores = {
            'volume': self.evaluate_volume(content),
            'structure': self.evaluate_structure(content),
            'diversity': self.evaluate_diversity(content),
            'uniqueness': self.evaluate_uniqueness(content, keyword)
        }
        
        total_score = sum(scores.values())
        return {
            'total_score': total_score,
            'breakdown': scores,
            'grade': self.get_grade(total_score)
        }
    
    def evaluate_volume(self, content):
        """Оценка объема статьи (30 баллов)"""
        word_count = len(content.split())
        if word_count >= 2000:
            return 30
        elif word_count >= 1500:
            return 20
        elif word_count >= 1000:
            return 10
        else:
            return 0
    
    def evaluate_structure(self, content):
        """Оценка структуры (25 баллов)"""
        score = 0
        
        # H1 заголовок
        if '<h1' in content:
            score += 5
            
        # H2 заголовки
        h2_count = content.count('<h2')
        score += min(h2_count * 2, 10)
        
        # H3 заголовки
        h3_count = content.count('<h3')
        score += min(h3_count, 10)
        
        return score
```

### SEO оценка

```python
class SEOEvaluator:
    def evaluate_seo_quality(self, content, keyword):
        """Оценка SEO качества (0-100 баллов)"""
        scores = {
            'h1_keyword': self.check_h1_keyword(content, keyword),
            'keyword_density': self.check_keyword_density(content, keyword),
            'structure': self.check_heading_structure(content),
            'internal_links': self.check_internal_links(content)
        }
        
        total_score = sum(scores.values())
        return {
            'total_score': total_score,
            'breakdown': scores,
            'recommendations': self.generate_recommendations(scores)
        }
```

## Мониторинг и аналитика

### Структурированное логирование

```python
import structlog

logger = structlog.get_logger(__name__)

class PipelineMonitor:
    def __init__(self):
        self.metrics = {}
        
    async def log_pipeline_step(self, step, keyword, duration, success):
        """Логирование шага пайплайна"""
        logger.info(
            "Pipeline step completed",
            step=step,
            keyword=keyword,
            duration=duration,
            success=success,
            timestamp=datetime.now().isoformat()
        )
        
        # Обновление метрик
        self.update_metrics(step, duration, success)
    
    def update_metrics(self, step, duration, success):
        """Обновление метрик"""
        if step not in self.metrics:
            self.metrics[step] = {
                'total_count': 0,
                'success_count': 0,
                'total_duration': 0,
                'avg_duration': 0
            }
        
        metrics = self.metrics[step]
        metrics['total_count'] += 1
        metrics['total_duration'] += duration
        metrics['avg_duration'] = metrics['total_duration'] / metrics['total_count']
        
        if success:
            metrics['success_count'] += 1
```

### Prometheus метрики

```python
from prometheus_client import Counter, Histogram, Gauge

# Метрики
pipeline_requests_total = Counter('pipeline_requests_total', 'Total pipeline requests', ['step'])
pipeline_duration_seconds = Histogram('pipeline_duration_seconds', 'Pipeline duration', ['step'])
pipeline_quality_score = Gauge('pipeline_quality_score', 'Content quality score', ['keyword'])
pipeline_seo_score = Gauge('pipeline_seo_score', 'SEO score', ['keyword'])

class MetricsCollector:
    def record_pipeline_step(self, step, duration, success):
        """Запись метрик шага пайплайна"""
        pipeline_requests_total.labels(step=step).inc()
        pipeline_duration_seconds.labels(step=step).observe(duration)
    
    def record_quality_scores(self, keyword, quality_score, seo_score):
        """Запись оценок качества"""
        pipeline_quality_score.labels(keyword=keyword).set(quality_score)
        pipeline_seo_score.labels(keyword=keyword).set(seo_score)
```

## API эндпоинты

### FastAPI приложение

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="WordPress SEO Automation API")

class KeywordRequest(BaseModel):
    keyword: str
    language: str = "ru"
    template: str = "financial"

class ArticleResponse(BaseModel):
    article_id: int
    title: str
    content: str
    quality_score: int
    seo_score: int
    wp_post_id: int
    wp_post_url: str

@app.post("/api/v1/research", response_model=dict)
async def research_keyword(request: KeywordRequest):
    """Исследование ключевого слова"""
    try:
        pipeline = BizFinProPipeline()
        analysis = await pipeline.research_keyword(request.keyword)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/generate", response_model=ArticleResponse)
async def generate_article(request: KeywordRequest):
    """Генерация статьи"""
    try:
        automation = EnhancedWordPressAutomation()
        result = await automation.process_keyword(request.keyword)
        return ArticleResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/status/{article_id}")
async def get_article_status(article_id: int):
    """Получение статуса статьи"""
    try:
        db_manager = DatabaseManager("wordpress_articles_enhanced.db")
        status = await db_manager.get_article_status(article_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=404, detail="Article not found")
```

## Развертывание

### Docker конфигурация

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  wordpress-seo-automation:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - WP_URL=${WP_URL}
      - WP_USERNAME=${WP_USERNAME}
      - WP_APP_PASSWORD=${WP_APP_PASSWORD}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      - mysql
      
  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
      - MYSQL_DATABASE=wordpress_seo
      - MYSQL_USER=wp_user
      - MYSQL_PASSWORD=wp_password
    volumes:
      - mysql_data:/var/lib/mysql
      
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  mysql_data:
  grafana_data:
```

## Тестирование

### Юнит-тесты

```python
import pytest
from unittest.mock import Mock, patch
from enhanced_content_generator import EnhancedContentGenerator

class TestEnhancedContentGenerator:
    @pytest.fixture
    def generator(self):
        return EnhancedContentGenerator()
    
    @pytest.mark.asyncio
    async def test_generate_section_content(self, generator):
        """Тест генерации контента раздела"""
        with patch('openai.OpenAI') as mock_openai:
            mock_response = Mock()
            mock_response.choices[0].message.content = "Test content"
            mock_openai.return_value.chat.completions.create.return_value = mock_response
            
            result = await generator.generate_section_content(
                "definition", "банковская гарантия", {}
            )
            
            assert result == "Test content"
    
    def test_analyze_keyword_intent(self, generator):
        """Тест анализа намерений"""
        result = generator.analyze_keyword_intent("калькулятор банковской гарантии")
        assert result['intent'] == 'transactional'
        assert result['focus'] == 'calculations'
```

### Интеграционные тесты

```python
@pytest.mark.integration
class TestWordPressIntegration:
    @pytest.mark.asyncio
    async def test_full_pipeline(self):
        """Тест полного пайплайна"""
        automation = EnhancedWordPressAutomation()
        
        # Тестовое ключевое слово
        test_keyword = "тест банковская гарантия"
        
        # Запуск пайплайна
        result = await automation.process_keyword(test_keyword)
        
        # Проверки
        assert result['success'] == True
        assert result['wp_post_id'] is not None
        assert result['quality_score'] >= 70
        assert result['seo_score'] >= 70
```

## Производительность

### Оптимизации

1. **Асинхронная обработка** - Все операции выполняются асинхронно
2. **Кэширование** - Кэширование результатов исследования
3. **Батчинг** - Обработка нескольких ключевых слов одновременно
4. **Connection pooling** - Пул соединений с базой данных

### Мониторинг производительности

```python
import time
from functools import wraps

def monitor_performance(func):
    """Декоратор для мониторинга производительности"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            
            logger.info(
                "Function completed",
                function=func.__name__,
                duration=duration,
                success=True
            )
            
            return result
        except Exception as e:
            duration = time.time() - start_time
            
            logger.error(
                "Function failed",
                function=func.__name__,
                duration=duration,
                error=str(e)
            )
            raise
    
    return wrapper
```

## Безопасность

### Аутентификация

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    """Проверка учетных данных"""
    correct_username = "admin"
    correct_password = "secure_password"
    
    if (credentials.username != correct_username or 
        credentials.password != correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credentials.username
```

### Валидация данных

```python
from pydantic import BaseModel, validator

class KeywordRequest(BaseModel):
    keyword: str
    language: str = "ru"
    template: str = "financial"
    
    @validator('keyword')
    def validate_keyword(cls, v):
        if len(v) < 3:
            raise ValueError('Keyword must be at least 3 characters long')
        if len(v) > 100:
            raise ValueError('Keyword must be less than 100 characters')
        return v
    
    @validator('language')
    def validate_language(cls, v):
        allowed_languages = ['ru', 'en', 'de', 'fr']
        if v not in allowed_languages:
            raise ValueError(f'Language must be one of: {allowed_languages}')
        return v
```

## Расширения

### Плагинная архитектура

```python
class PluginManager:
    def __init__(self):
        self.plugins = {}
    
    def register_plugin(self, name, plugin_class):
        """Регистрация плагина"""
        self.plugins[name] = plugin_class()
    
    async def execute_plugin(self, name, *args, **kwargs):
        """Выполнение плагина"""
        if name not in self.plugins:
            raise ValueError(f"Plugin {name} not found")
        
        plugin = self.plugins[name]
        return await plugin.execute(*args, **kwargs)

class ContentEnhancementPlugin:
    async def execute(self, content, keyword):
        """Улучшение контента"""
        # Логика улучшения контента
        enhanced_content = self.enhance_content(content, keyword)
        return enhanced_content
```

### API для внешних интеграций

```python
@app.post("/api/v1/webhooks/wordpress")
async def wordpress_webhook(request: Request):
    """Webhook для WordPress"""
    data = await request.json()
    
    if data.get('action') == 'post_published':
        post_id = data.get('post_id')
        await process_published_post(post_id)
    
    return {"status": "success"}

@app.post("/api/v1/integrations/ahrefs")
async def ahrefs_integration(request: AhrefsRequest):
    """Интеграция с Ahrefs"""
    try:
        ahrefs_data = await fetch_ahrefs_data(request.keyword)
        return ahrefs_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Заключение

WordPress SEO Automation Platform представляет собой комплексную систему для автоматизации создания и публикации SEO-оптимизированного контента. Платформа объединяет современные технологии AI, веб-скрапинга и WordPress интеграции для создания высококачественных статей с минимальным участием человека.

**Ключевые преимущества:**
- Полная автоматизация процесса создания статей
- AI-генерация высококачественного контента
- Интеграция с WordPress и Yoast SEO
- Система контроля качества
- Масштабируемая архитектура
- Подробная аналитика и мониторинг

**Готовность к продакшну:** ✅ Система готова к развертыванию и использованию в реальных проектах.
