#!/bin/bash

# WordPress SEO Automation Platform - GitHub Upload Script
# Автор: ferstpetr777
# Дата: $(date)

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Конфигурация
GITHUB_USERNAME="ferstpetr777"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"
REPO_NAME="wordpress-seo-automation"
REPO_DESCRIPTION="Comprehensive platform for automated SEO article creation and publishing in WordPress with AI integration"
REPO_TOPICS="wordpress,seo,automation,ai,content-generation,openai,fastapi,python"

echo -e "${BLUE}🚀 WordPress SEO Automation Platform - GitHub Upload${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Проверка наличия Git
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git не установлен. Установите Git и попробуйте снова.${NC}"
    exit 1
fi

# Проверка наличия curl
if ! command -v curl &> /dev/null; then
    echo -e "${RED}❌ curl не установлен. Установите curl и попробуйте снова.${NC}"
    exit 1
fi

# Проверка токена GitHub
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}❌ GitHub токен не установлен. Установите переменную GITHUB_TOKEN.${NC}"
    echo -e "${YELLOW}Пример: export GITHUB_TOKEN=your_token_here${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Информация о репозитории:${NC}"
echo -e "   Пользователь: ${GREEN}$GITHUB_USERNAME${NC}"
echo -e "   Репозиторий: ${GREEN}$REPO_NAME${NC}"
echo -e "   Описание: ${GREEN}$REPO_DESCRIPTION${NC}"
echo ""

# Создание репозитория на GitHub
echo -e "${YELLOW}🔧 Создание репозитория на GitHub...${NC}"

CREATE_REPO_RESPONSE=$(curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d "{
    \"name\": \"$REPO_NAME\",
    \"description\": \"$REPO_DESCRIPTION\",
    \"private\": false,
    \"has_issues\": true,
    \"has_projects\": true,
    \"has_wiki\": true,
    \"auto_init\": false
  }")

# Проверка ответа
if echo "$CREATE_REPO_RESPONSE" | grep -q '"message"'; then
    ERROR_MSG=$(echo "$CREATE_REPO_RESPONSE" | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
    if [[ "$ERROR_MSG" == *"already exists"* ]]; then
        echo -e "${YELLOW}⚠️  Репозиторий уже существует. Продолжаем...${NC}"
    else
        echo -e "${RED}❌ Ошибка создания репозитория: $ERROR_MSG${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Репозиторий успешно создан на GitHub${NC}"
fi

# Добавление тегов к репозиторию
echo -e "${YELLOW}🏷️  Добавление тегов к репозиторию...${NC}"

curl -s -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/$GITHUB_USERNAME/$REPO_NAME/topics \
  -d "{
    \"names\": [\"wordpress\", \"seo\", \"automation\", \"ai\", \"content-generation\", \"openai\", \"fastapi\", \"python\", \"machine-learning\", \"nlp\"]
  }" > /dev/null

echo -e "${GREEN}✅ Теги добавлены${NC}"

# Настройка remote origin
echo -e "${YELLOW}🔗 Настройка remote origin...${NC}"

# Удаление существующего origin если есть
git remote remove origin 2>/dev/null || true

# Добавление нового origin
git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git

echo -e "${GREEN}✅ Remote origin настроен${NC}"

# Проверка статуса Git
echo -e "${YELLOW}📊 Проверка статуса Git...${NC}"
git status

# Загрузка на GitHub
echo -e "${YELLOW}⬆️  Загрузка проекта на GitHub...${NC}"

# Принудительная загрузка (если репозиторий уже существовал)
git push -u origin main --force

echo ""
echo -e "${GREEN}🎉 Проект успешно загружен на GitHub!${NC}"
echo ""
echo -e "${BLUE}📋 Информация о загруженном проекте:${NC}"
echo -e "   URL: ${GREEN}https://github.com/$GITHUB_USERNAME/$REPO_NAME${NC}"
echo -e "   Клонирование: ${GREEN}git clone https://github.com/$GITHUB_USERNAME/$REPO_NAME.git${NC}"
echo ""

# Создание первого релиза
echo -e "${YELLOW}🏷️  Создание первого релиза v1.0.0...${NC}"

RELEASE_RESPONSE=$(curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/$GITHUB_USERNAME/$REPO_NAME/releases \
  -d "{
    \"tag_name\": \"v1.0.0\",
    \"target_commitish\": \"main\",
    \"name\": \"WordPress SEO Automation Platform v1.0.0\",
    \"body\": \"## 🎉 Первый релиз WordPress SEO Automation Platform\\n\\n### Основные возможности:\\n- 🤖 AI-генерация контента с OpenAI GPT\\n- 🔍 Исследование конкурентов и анализ ключевых слов\\n- 📝 Автоматическая публикация в WordPress\\n- 🎯 SEO-оптимизация с Yoast интеграцией\\n- 📊 Система контроля качества\\n- 🗄️ Поддержка SQLite и MySQL\\n- 🐳 Docker контейнеризация\\n- 📈 Мониторинг и аналитика\\n\\n### Технический стек:\\n- Python 3.8+, FastAPI, OpenAI GPT-4\\n- WordPress REST API, Yoast SEO\\n- SQLite/MySQL, BeautifulSoup4\\n- Prometheus, Grafana\\n\\n### Готовность:\\n✅ Готов к продакшн использованию\\n✅ Полная документация\\n✅ Тесты и CI/CD\\n✅ Безопасность и производительность\",
    \"draft\": false,
    \"prerelease\": false
  }")

if echo "$RELEASE_RESPONSE" | grep -q '"html_url"'; then
    RELEASE_URL=$(echo "$RELEASE_RESPONSE" | grep -o '"html_url":"[^"]*"' | cut -d'"' -f4)
    echo -e "${GREEN}✅ Релиз v1.0.0 создан: $RELEASE_URL${NC}"
else
    echo -e "${YELLOW}⚠️  Не удалось создать релиз автоматически${NC}"
fi

echo ""
echo -e "${GREEN}🎊 Загрузка завершена успешно!${NC}"
echo ""
echo -e "${BLUE}📚 Следующие шаги:${NC}"
echo -e "   1. Перейдите на ${GREEN}https://github.com/$GITHUB_USERNAME/$REPO_NAME${NC}"
echo -e "   2. Проверьте настройки репозитория"
echo -e "   3. Настройте GitHub Actions для CI/CD"
echo -e "   4. Добавьте Issues для планирования развития"
echo -e "   5. Создайте Wiki для дополнительной документации"
echo ""
echo -e "${BLUE}🔗 Полезные ссылки:${NC}"
echo -e "   - Репозиторий: ${GREEN}https://github.com/$GITHUB_USERNAME/$REPO_NAME${NC}"
echo -e "   - Issues: ${GREEN}https://github.com/$GITHUB_USERNAME/$REPO_NAME/issues${NC}"
echo -e "   - Wiki: ${GREEN}https://github.com/$GITHUB_USERNAME/$REPO_NAME/wiki${NC}"
echo -e "   - Actions: ${GREEN}https://github.com/$GITHUB_USERNAME/$REPO_NAME/actions${NC}"
echo ""
echo -e "${GREEN}✨ Проект готов к использованию!${NC}"