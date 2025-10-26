#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
batch_research_demo.py — Демонстрация массовой обработки ключевых слов
Пример для обработки 50 ключевых слов по банковским гарантиям
"""

import sys
import os
import subprocess

# Добавляем путь к проекту
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def create_large_group():
    """Создание большой группы из 50 ключевых слов"""
    
    keywords = [
        "банковская гарантия",
        "стоимость банковской гарантии", 
        "срок банковской гарантии",
        "оформление банковской гарантии",
        "получение банковской гарантии",
        "проверка банковской гарантии",
        "банковская гарантия для МСБ",
        "банковская гарантия по 44-ФЗ",
        "банковская гарантия по 223-ФЗ",
        "тендерная банковская гарантия",
        "банковская гарантия на исполнение",
        "банковская гарантия на аванс",
        "банковская гарантия возврат аванса",
        "независимая банковская гарантия",
        "отзывная банковская гарантия",
        "безотзывная банковская гарантия",
        "банковская гарантия Сбербанк",
        "банковская гарантия ВТБ",
        "банковская гарантия Альфа-Банк",
        "банковская гарантия ПСБ",
        "банковская гарантия Совкомбанк",
        "банковская гарантия Райффайзенбанк",
        "банковская гарантия Газпромбанк",
        "банковская гарантия Россельхозбанк",
        "банковская гарантия МКБ",
        "калькулятор банковской гарантии",
        "тарифы банковской гарантии",
        "условия банковской гарантии",
        "требования банковской гарантии",
        "документы банковской гарантии",
        "список банков гарантий",
        "реестр банковских гарантий",
        "проверка банковской гарантии онлайн",
        "поддельная банковская гарантия",
        "мошенничество банковская гарантия",
        "риски банковской гарантии",
        "преимущества банковской гарантии",
        "недостатки банковской гарантии",
        "поручительство банковская гарантия",
        "залог банковская гарантия",
        "страхование банковская гарантия",
        "кредит банковская гарантия",
        "лизинг банковская гарантия",
        "факторинг банковская гарантия",
        "государственная банковская гарантия",
        "коммерческая банковская гарантия",
        "международная банковская гарантия",
        "валютная банковская гарантия",
        "рублевая банковская гарантия"
    ]
    
    print("🚀 СОЗДАНИЕ МАССОВОЙ ГРУППЫ ЗАДАЧ")
    print("=" * 60)
    print(f"📊 Количество ключевых слов: {len(keywords)}")
    print(f"📝 Тематика: Банковские гарантии")
    print(f"🎯 Тип обработки: Массовый анализ")
    print()
    
    # Формируем команду
    cmd = [
        "python3", "scripts/enhanced_auto_research.py", 
        "--group", "Массовый анализ БГ 50 ключей"
    ] + keywords
    
    print("🔧 Команда для создания группы:")
    print(" ".join(cmd))
    print()
    
    # Выполняем команду
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            print("✅ Группа успешно создана!")
            print("📤 Вывод команды:")
            print(result.stdout)
            
            # Извлекаем group_id из вывода
            lines = result.stdout.split('\n')
            group_id = None
            for line in lines:
                if "group_" in line and "создана" in line:
                    group_id = line.split(": ")[-1]
                    break
            
            if group_id:
                print(f"\n🚀 Для запуска массовой обработки выполните:")
                print(f"python3 scripts/enhanced_auto_research.py --process-group {group_id}")
                print()
                print("📊 Для отслеживания прогресса:")
                print(f"python3 scripts/enhanced_auto_research.py --status {group_id}")
                
                return group_id
            else:
                print("⚠️ Не удалось извлечь group_id из вывода")
                return None
                
        else:
            print("❌ Ошибка создания группы:")
            print(result.stderr)
            return None
            
    except Exception as e:
        print(f"❌ Ошибка выполнения команды: {e}")
        return None

def show_usage():
    """Показ инструкций по использованию"""
    print("🔍 ИНСТРУКЦИЯ ПО МАССОВОЙ ОБРАБОТКЕ")
    print("=" * 60)
    print()
    print("1️⃣ СОЗДАНИЕ ГРУППЫ (50 ключевых слов):")
    print("   python3 scripts/batch_research_demo.py")
    print()
    print("2️⃣ ЗАПУСК ОБРАБОТКИ:")
    print("   python3 scripts/enhanced_auto_research.py --process-group GROUP_ID")
    print()
    print("3️⃣ ОТСЛЕЖИВАНИЕ ПРОГРЕССА:")
    print("   python3 scripts/enhanced_auto_research.py --status GROUP_ID")
    print()
    print("4️⃣ ОДИНОЧНАЯ ОБРАБОТКА:")
    print("   python3 scripts/enhanced_auto_research.py \"ключевое слово\"")
    print()
    print("📊 ОСОБЕННОСТИ МАССОВОЙ ОБРАБОТКИ:")
    print("   • Параллельная обработка (3 потока)")
    print("   • Отслеживание времени выполнения")
    print("   • Восстановление после сбоев")
    print("   • Детальная статистика")
    print("   • Сохранение в БД с метриками")

def main():
    """Главная функция"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        show_usage()
        return 0
    
    print("🎯 ДЕМОНСТРАЦИЯ МАССОВОЙ ОБРАБОТКИ")
    print("=" * 60)
    print()
    
    choice = input("Выберите действие:\n1. Создать группу из 50 ключевых слов\n2. Показать инструкции\nВведите номер (1 или 2): ")
    
    if choice == "1":
        group_id = create_large_group()
        if group_id:
            print(f"\n🎉 Готово! Group ID: {group_id}")
            print("\n💡 Следующие шаги:")
            print(f"1. Запустите обработку: python3 scripts/enhanced_auto_research.py --process-group {group_id}")
            print(f"2. Отслеживайте прогресс: python3 scripts/enhanced_auto_research.py --status {group_id}")
        else:
            print("\n❌ Не удалось создать группу")
            return 1
    
    elif choice == "2":
        show_usage()
    
    else:
        print("❌ Неверный выбор")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
