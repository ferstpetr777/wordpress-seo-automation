#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Конфигурация базы данных для BizFin Pro SEO Pipeline
"""

import os
from typing import Dict, Any

class DatabaseConfig:
    """Конфигурация подключения к базе данных"""
    
    # Основные настройки
    HOST = os.getenv('DB_HOST', 'localhost')
    PORT = int(os.getenv('DB_PORT', 3306))
    USER = os.getenv('DB_USER', 'bizfin_seo')
    PASSWORD = os.getenv('DB_PASSWORD', 'bizfin_seo_2024!')
    DATABASE = os.getenv('DB_NAME', 'bizfin_pro_seo')
    CHARSET = 'utf8mb4'
    
    # Настройки подключения
    CONNECTION_TIMEOUT = 30
    AUTOCOMMIT = False
    CONNECT_TIMEOUT = 10
    
    # Настройки пула соединений
    POOL_SIZE = 10
    MAX_OVERFLOW = 20
    POOL_TIMEOUT = 30
    POOL_RECYCLE = 3600
    
    @classmethod
    def get_connection_string(cls) -> str:
        """Получение строки подключения"""
        return f"mysql+pymysql://{cls.USER}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}/{cls.DATABASE}?charset={cls.CHARSET}"
    
    @classmethod
    def get_config_dict(cls) -> Dict[str, Any]:
        """Получение конфигурации в виде словаря"""
        return {
            'host': cls.HOST,
            'port': cls.PORT,
            'user': cls.USER,
            'password': cls.PASSWORD,
            'database': cls.DATABASE,
            'charset': cls.CHARSET,
            'autocommit': cls.AUTOCOMMIT,
            'connect_timeout': cls.CONNECT_TIMEOUT,
            'connection_timeout': cls.CONNECTION_TIMEOUT
        }
    
    @classmethod
    def get_pool_config(cls) -> Dict[str, Any]:
        """Получение конфигурации пула соединений"""
        return {
            'pool_size': cls.POOL_SIZE,
            'max_overflow': cls.MAX_OVERFLOW,
            'pool_timeout': cls.POOL_TIMEOUT,
            'pool_recycle': cls.POOL_RECYCLE
        }

class SQLiteConfig:
    """Конфигурация для SQLite (для разработки и тестирования)"""
    
    DATABASE_PATH = os.getenv('SQLITE_PATH', '/root/seo_project/bizfin-pro/data/bizfin_pro.db')
    
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

# Выбор конфигурации в зависимости от окружения
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    DB_CONFIG = DatabaseConfig
elif ENVIRONMENT == 'testing':
    DB_CONFIG = SQLiteConfig
else:
    DB_CONFIG = DatabaseConfig  # По умолчанию MySQL для разработки

# Экспорт конфигурации
__all__ = ['DB_CONFIG', 'DatabaseConfig', 'SQLiteConfig']


