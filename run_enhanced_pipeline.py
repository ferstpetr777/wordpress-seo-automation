#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Финальный скрипт для запуска улучшенного пайплайна создания SEO-статей
"""

import sys
import os
from datetime import datetime

def main():
    """Запуск улучшенного пайплайна"""
    print("🚀 ЗАПУСК УЛУЧШЕННОГО ПАЙПЛАЙНА СОЗДАНИЯ SEO-СТАТЕЙ")
    print(f"📅 Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    try:
        # Импортируем улучшенный пайплайн
        from enhanced_wordpress_automation import EnhancedWordPressAutomation
        
        print("✅ Модули успешно загружены")
        
        # Создаем экземпляр улучшенного пайплайна
        automation = EnhancedWordPressAutomation()
        
        print("✅ Улучшенный пайплайн инициализирован")
        print("\n🎯 Начинаем создание высококачественных SEO-статей...")
        
        # Запускаем улучшенную автоматизацию
        automation.run_enhanced_automation()
        
        print("\n🎉 ПАЙПЛАЙН УСПЕШНО ЗАВЕРШЕН!")
        print("📊 Созданы высококачественные SEO-статьи с улучшенным контентом")
        
    except ImportError as e:
        print(f"❌ Ошибка импорта модулей: {e}")
        print("💡 Убедитесь, что файлы enhanced_content_generator.py и enhanced_wordpress_automation.py находятся в той же директории")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
