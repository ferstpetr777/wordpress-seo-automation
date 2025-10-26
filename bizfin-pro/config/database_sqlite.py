#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Конфигурация SQLite для BizFin Pro SEO Pipeline (для тестирования)
"""

import os
from typing import Dict, Any

class SQLiteConfig:
    """Конфигурация для SQLite"""
    
    # Путь к базе данных
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'bizfin_pro.db')
    
    # Создаем директорию если не существует
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    @classmethod
    def get_connection_string(cls) -> str:
        """Получение строки подключения для SQLite"""
        return f"sqlite:///{cls.DATABASE_PATH}"
    
    @classmethod
    def get_config_dict(cls) -> Dict[str, Any]:
        """Получение конфигурации SQLite"""
        return {
            'database': cls.DATABASE_PATH,
            'check_same_thread': False
        }

# Используем SQLite по умолчанию для тестирования
DB_CONFIG = SQLiteConfig


