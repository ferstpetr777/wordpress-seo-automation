#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Дизайн-система BizFin Pro для SEO Pipeline
"""

from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class DesignSystem:
    """Дизайн-система сайта bizfin-pro.ru"""
    
    # Цветовая палитра
    colors: Dict[str, str] = None
    
    # Типографика
    typography: Dict[str, str] = None
    
    # Стили компонентов
    components: Dict[str, Dict[str, Any]] = None
    
    # Отступы и размеры
    spacing: Dict[str, str] = None
    
    # Тени и эффекты
    effects: Dict[str, str] = None
    
    def __post_init__(self):
        if self.colors is None:
            self.colors = {
                "primary_bg": "#F5F5F5",        # Чистый базовый бело-серый фон
                "accent_orange": "#E85A00",     # Основной оранжевый акцент
                "accent_orange_alt": "#FF6B00", # Альтернативный оранжевый
                "text_primary": "#333333",      # Основной текст
                "text_secondary": "#666666",    # Вторичный текст
                "white": "#FFFFFF",             # Белый
                "border_light": "#E0E0E0",      # Светлые границы
                "success": "#28A745",           # Успех
                "warning": "#FFC107",           # Предупреждение
                "error": "#DC3545"              # Ошибка
            }
        
        if self.typography is None:
            self.typography = {
                "primary_font": "Open Sans, sans-serif",
                "fallback_font": "Arial, sans-serif",
                "heading_font": "Open Sans, sans-serif",
                "body_font": "Open Sans, sans-serif"
            }
        
        if self.components is None:
            self.components = {
                "cta_button": {
                    "background": "#E85A00",
                    "color": "#FFFFFF",
                    "border_radius": "25px",
                    "padding": "12px 24px",
                    "font_weight": "600",
                    "transition": "all 0.3s ease",
                    "box_shadow": "0 4px 15px rgba(232, 90, 0, 0.3)"
                },
                "card": {
                    "background": "#FFFFFF",
                    "border_radius": "12px",
                    "box_shadow": "0 2px 10px rgba(0, 0, 0, 0.1)",
                    "padding": "24px",
                    "margin_bottom": "20px"
                },
                "section": {
                    "background": "#FFFFFF",
                    "border_radius": "15px",
                    "box_shadow": "0 3px 15px rgba(0, 0, 0, 0.08)",
                    "padding": "30px",
                    "margin_bottom": "25px"
                },
                "highlight_box": {
                    "background": "linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%)",
                    "border": "2px solid #E85A00",
                    "border_radius": "10px",
                    "padding": "20px"
                }
            }
        
        if self.spacing is None:
            self.spacing = {
                "xs": "4px",
                "sm": "8px",
                "md": "16px",
                "lg": "24px",
                "xl": "32px",
                "xxl": "48px"
            }
        
        if self.effects is None:
            self.effects = {
                "shadow_light": "0 2px 8px rgba(0, 0, 0, 0.1)",
                "shadow_medium": "0 4px 15px rgba(0, 0, 0, 0.15)",
                "shadow_heavy": "0 8px 25px rgba(0, 0, 0, 0.2)",
                "transition": "all 0.3s ease",
                "hover_lift": "transform: translateY(-2px)"
            }

class DesignGenerator:
    """Генератор дизайн-элементов"""
    
    def __init__(self):
        self.design = DesignSystem()
    
    def generate_css_styles(self) -> str:
        """Генерация CSS стилей для статьи"""
        return f"""
        /* BizFin Pro Design System */
        .bizfin-article {{
            font-family: {self.design.typography['primary_font']};
            background-color: {self.design.colors['primary_bg']};
            color: {self.design.colors['text_primary']};
            line-height: 1.6;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .bizfin-section {{
            background: {self.design.components['section']['background']};
            border-radius: {self.design.components['section']['border_radius']};
            box-shadow: {self.design.components['section']['box_shadow']};
            padding: {self.design.components['section']['padding']};
            margin-bottom: {self.design.components['section']['margin_bottom']};
        }}
        
        .bizfin-card {{
            background: {self.design.components['card']['background']};
            border-radius: {self.design.components['card']['border_radius']};
            box-shadow: {self.design.components['card']['box_shadow']};
            padding: {self.design.components['card']['padding']};
            margin-bottom: {self.design.components['card']['margin_bottom']};
        }}
        
        .bizfin-cta-button {{
            background: {self.design.components['cta_button']['background']};
            color: {self.design.components['cta_button']['color']};
            border: none;
            border-radius: {self.design.components['cta_button']['border_radius']};
            padding: {self.design.components['cta_button']['padding']};
            font-weight: {self.design.components['cta_button']['font_weight']};
            transition: {self.design.components['cta_button']['transition']};
            box-shadow: {self.design.components['cta_button']['box_shadow']};
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            font-family: {self.design.typography['primary_font']};
        }}
        
        .bizfin-cta-button:hover {{
            background: {self.design.colors['accent_orange_alt']};
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(232, 90, 0, 0.4);
        }}
        
        .bizfin-highlight {{
            background: {self.design.components['highlight_box']['background']};
            border: {self.design.components['highlight_box']['border']};
            border-radius: {self.design.components['highlight_box']['border_radius']};
            padding: {self.design.components['highlight_box']['padding']};
            margin: 20px 0;
        }}
        
        .bizfin-h1 {{
            color: {self.design.colors['text_primary']};
            font-family: {self.design.typography['heading_font']};
            font-size: 2.2em;
            font-weight: 700;
            margin-bottom: 20px;
            line-height: 1.3;
        }}
        
        .bizfin-h2 {{
            color: {self.design.colors['text_primary']};
            font-family: {self.design.typography['heading_font']};
            font-size: 1.8em;
            font-weight: 600;
            margin-bottom: 16px;
            margin-top: 30px;
            line-height: 1.4;
        }}
        
        .bizfin-h3 {{
            color: {self.design.colors['accent_orange']};
            font-family: {self.design.typography['heading_font']};
            font-size: 1.4em;
            font-weight: 600;
            margin-bottom: 12px;
            margin-top: 24px;
        }}
        
        .bizfin-p {{
            color: {self.design.colors['text_primary']};
            font-family: {self.design.typography['body_font']};
            font-size: 1.05em;
            line-height: 1.7;
            margin-bottom: 16px;
        }}
        
        .bizfin-ul, .bizfin-ol {{
            color: {self.design.colors['text_primary']};
            font-family: {self.design.typography['body_font']};
            line-height: 1.7;
            margin-bottom: 16px;
            padding-left: 20px;
        }}
        
        .bizfin-li {{
            margin-bottom: 8px;
        }}
        
        .bizfin-table {{
            width: 100%;
            border-collapse: collapse;
            background: {self.design.colors['white']};
            border-radius: 8px;
            overflow: hidden;
            box-shadow: {self.design.effects['shadow_light']};
            margin: 20px 0;
        }}
        
        .bizfin-table th {{
            background: {self.design.colors['accent_orange']};
            color: {self.design.colors['white']};
            padding: 12px;
            font-weight: 600;
            text-align: left;
        }}
        
        .bizfin-table td {{
            padding: 12px;
            border-bottom: 1px solid {self.design.colors['border_light']};
        }}
        
        .bizfin-table tr:nth-child(even) {{
            background: #FAFAFA;
        }}
        
        .bizfin-faq {{
            background: {self.design.colors['white']};
            border-radius: 8px;
            margin-bottom: 15px;
            box-shadow: {self.design.effects['shadow_light']};
            overflow: hidden;
        }}
        
        .bizfin-faq-question {{
            background: {self.design.colors['accent_orange']};
            color: {self.design.colors['white']};
            padding: 15px 20px;
            cursor: pointer;
            font-weight: 600;
            transition: {self.design.effects['transition']};
        }}
        
        .bizfin-faq-question:hover {{
            background: {self.design.colors['accent_orange_alt']};
        }}
        
        .bizfin-faq-answer {{
            padding: 20px;
            color: {self.design.colors['text_primary']};
            line-height: 1.6;
        }}
        
        /* Адаптивность */
        @media (max-width: 768px) {{
            .bizfin-article {{
                padding: 15px;
            }}
            
            .bizfin-section {{
                padding: 20px;
            }}
            
            .bizfin-h1 {{
                font-size: 1.8em;
            }}
            
            .bizfin-h2 {{
                font-size: 1.5em;
            }}
        }}
        """
    
    def generate_inline_styles(self, element_type: str) -> str:
        """Генерация инлайн стилей для конкретного элемента"""
        if element_type == "cta_button":
            return (
                f"background: {self.design.components['cta_button']['background']}; "
                f"color: {self.design.components['cta_button']['color']}; "
                f"border: none; "
                f"border-radius: {self.design.components['cta_button']['border_radius']}; "
                f"padding: {self.design.components['cta_button']['padding']}; "
                f"font-weight: {self.design.components['cta_button']['font_weight']}; "
                f"transition: {self.design.components['cta_button']['transition']}; "
                f"box-shadow: {self.design.components['cta_button']['box_shadow']}; "
                f"cursor: pointer; "
                f"text-decoration: none; "
                f"display: inline-block; "
                f"font-family: {self.design.typography['primary_font']};"
            )
        elif element_type == "card":
            return (
                f"background: {self.design.components['card']['background']}; "
                f"border-radius: {self.design.components['card']['border_radius']}; "
                f"box-shadow: {self.design.components['card']['box_shadow']}; "
                f"padding: {self.design.components['card']['padding']}; "
                f"margin-bottom: {self.design.components['card']['margin_bottom']};"
            )
        elif element_type == "highlight":
            return (
                f"background: {self.design.components['highlight_box']['background']}; "
                f"border: {self.design.components['highlight_box']['border']}; "
                f"border-radius: {self.design.components['highlight_box']['border_radius']}; "
                f"padding: {self.design.components['highlight_box']['padding']}; "
                f"margin: 20px 0;"
            )
        
        return ""

# Экспорт
__all__ = ['DesignSystem', 'DesignGenerator']


