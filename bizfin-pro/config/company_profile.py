#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Профиль компании BizFin Pro для SEO Pipeline
"""

from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class CompanyProfile:
    """Профиль компании Бизнес Финанс"""
    
    # Основная информация
    name: str = "Бизнес Финанс"
    legal_name: str = "ООО «Бизнес Финанс»"
    inn: str = "5257173950"
    website: str = "bizfin-pro.ru"
    domain: str = "bizfin-pro.ru"
    
    # Опыт и статистика
    experience_years: int = 14
    guarantees_issued: int = 150000
    approval_rate: float = 93.0  # процент
    partner_banks: int = 30
    processing_time_min: int = 10  # минут
    
    # Направления деятельности
    services: List[str] = None
    
    # География
    coverage: str = "вся Россия"
    online_service: bool = True
    
    # Конкурентные преимущества
    competitive_advantages: List[str] = None
    
    # УТП (Уникальное торговое предложение)
    utp: str = None
    
    # Контактная информация
    contact_info: Dict[str, str] = None
    
    def __post_init__(self):
        if self.services is None:
            self.services = [
                "Банковские гарантии (тендерные, исполнения контрактов)",
                "Кредитование под исполнение государственных контрактов (до 100 млн руб. без залога)",
                "Юридическое сопровождение",
                "Консультации в закупках",
                "Анализ документов",
                "Помощь с ЭЦП и сертификатами"
            ]
        
        if self.competitive_advantages is None:
            self.competitive_advantages = [
                "Оформление онлайн, с использованием ЭЦП — без визита в банк",
                "Прямое сотрудничество с банками без посреднической комиссии",
                "Высокий процент одобрения заявок (93%)",
                "Опыт работы в сложных ситуациях",
                "Полный пакет сопутствующих услуг",
                "Гибкие условия, скидки от банков за объём сотрудничества"
            ]
        
        if self.utp is None:
            self.utp = (
                "Бизнес Финанс — ваш партнёр в банковских гарантиях и финансировании контрактов. "
                "14 лет на рынке: оформление за 10 минут, без визитов, с 93% одобрений, "
                "и полное сопровождение бесплатно в рамках сделки."
            )
        
        if self.contact_info is None:
            self.contact_info = {
                "phone": "+7 (499) 757-01-25",
                "email": "info@bizfin-pro.ru",
                "website": "https://bizfin-pro.ru",
                "address": "Москва"
            }

class CompanyData:
    """Данные компании для использования в статьях"""
    
    @staticmethod
    def get_company_stats() -> Dict[str, Any]:
        """Получение статистики компании"""
        profile = CompanyProfile()
        return {
            "experience": f"{profile.experience_years} лет на рынке",
            "guarantees": f"{profile.guarantees_issued:,} выданных банковских гарантий",
            "approval_rate": f"{profile.approval_rate}% одобренных заявок с первого раза",
            "banks": f"{profile.partner_banks}+ банков-партнеров",
            "processing_time": f"от {profile.processing_time_min} минут"
        }
    
    @staticmethod
    def get_services_list() -> List[str]:
        """Получение списка услуг"""
        profile = CompanyProfile()
        return profile.services
    
    @staticmethod
    def get_advantages() -> List[str]:
        """Получение конкурентных преимуществ"""
        profile = CompanyProfile()
        return profile.competitive_advantages
    
    @staticmethod
    def get_utp() -> str:
        """Получение УТП"""
        profile = CompanyProfile()
        return profile.utp
    
    @staticmethod
    def get_contact_info() -> Dict[str, str]:
        """Получение контактной информации"""
        profile = CompanyProfile()
        return profile.contact_info
    
    @staticmethod
    def get_company_intro() -> str:
        """Получение введения о компании для статей"""
        stats = CompanyData.get_company_stats()
        return (
            f"Компания «Бизнес Финанс» — ведущий специалист в области банковских гарантий "
            f"с {stats['experience']}. За время работы мы выдали {stats['guarantees']}, "
            f"достигнув {stats['approval_rate']} одобренных заявок с первого раза. "
            f"Наши клиенты получают решения {stats['processing_time']} благодаря "
            f"партнерству с {stats['banks']}."
        )

# Экспорт
__all__ = ['CompanyProfile', 'CompanyData']


