#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
enhanced_auto_research.py — Улучшенный автоматический веб-исследователь
Поддерживает групповую обработку, очередь задач и отслеживание времени выполнения
"""

import sys
import os
import json
import sqlite3
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Добавляем путь к проекту
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.database_sqlite import DB_CONFIG

class TaskQueue:
    """Класс для управления очередью задач"""
    
    def __init__(self):
        self.db_config = DB_CONFIG.get_config_dict()
        self.db_path = self.db_config['database']
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных для очереди задач"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Таблица для очереди задач
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT UNIQUE NOT NULL,
                keyword TEXT NOT NULL,
                priority INTEGER DEFAULT 1,
                status TEXT DEFAULT 'pending',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                started_at DATETIME,
                completed_at DATETIME,
                execution_time_seconds REAL,
                error_message TEXT,
                result_data TEXT
            )
        ''')
        
        # Таблица для групп задач
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id TEXT UNIQUE NOT NULL,
                group_name TEXT NOT NULL,
                total_tasks INTEGER DEFAULT 0,
                completed_tasks INTEGER DEFAULT 0,
                failed_tasks INTEGER DEFAULT 0,
                status TEXT DEFAULT 'pending',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                started_at DATETIME,
                completed_at DATETIME,
                total_execution_time_seconds REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_group(self, group_name: str, keywords: List[str]) -> str:
        """Создание группы задач"""
        group_id = f"group_{int(datetime.now().timestamp())}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Создаем группу
        cursor.execute('''
            INSERT INTO task_groups (group_id, group_name, total_tasks, status)
            VALUES (?, ?, ?, ?)
        ''', (group_id, group_name, len(keywords), 'pending'))
        
        # Добавляем задачи в очередь
        for i, keyword in enumerate(keywords):
            task_id = f"{group_id}_task_{i+1}"
            cursor.execute('''
                INSERT INTO task_queue (task_id, keyword, priority, status)
                VALUES (?, ?, ?, ?)
            ''', (task_id, keyword, 1, 'pending'))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Группа создана: {group_id}")
        print(f"📊 Задач в группе: {len(keywords)}")
        return group_id
    
    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """Получение следующей задачи из очереди"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, task_id, keyword, priority
            FROM task_queue 
            WHERE status = 'pending'
            ORDER BY priority DESC, created_at ASC
            LIMIT 1
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'task_id': result[1],
                'keyword': result[2],
                'priority': result[3]
            }
        return None
    
    def start_task(self, task_id: str) -> bool:
        """Отметка задачи как выполняющейся"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE task_queue 
            SET status = 'running', started_at = CURRENT_TIMESTAMP
            WHERE task_id = ?
        ''', (task_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def complete_task(self, task_id: str, execution_time: float, result_data: str, error: str = None):
        """Завершение задачи"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        status = 'completed' if not error else 'failed'
        
        cursor.execute('''
            UPDATE task_queue 
            SET status = ?, completed_at = CURRENT_TIMESTAMP, 
                execution_time_seconds = ?, result_data = ?, error_message = ?
            WHERE task_id = ?
        ''', (status, execution_time, result_data, error, task_id))
        
        # Обновляем статистику группы
        cursor.execute('''
            UPDATE task_groups 
            SET completed_tasks = completed_tasks + 1
            WHERE group_id = ?
        ''', (task_id.split('_task_')[0],))
        
        conn.commit()
        conn.close()
    
    def get_group_status(self, group_id: str) -> Dict[str, Any]:
        """Получение статуса группы"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT total_tasks, completed_tasks, failed_tasks, status
            FROM task_groups WHERE group_id = ?
        ''', (group_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'total_tasks': result[0],
                'completed_tasks': result[1],
                'failed_tasks': result[2],
                'status': result[3],
                'progress_percent': round((result[1] + result[2]) / result[0] * 100, 2)
            }
        return {}

class EnhancedWebResearcher:
    """Улучшенный веб-исследователь с отслеживанием времени"""
    
    def __init__(self):
        self.db_config = DB_CONFIG.get_config_dict()
        self.db_path = self.db_config['database']
    
    def get_instruction_from_db(self):
        """Получение инструкции из БД"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT instruction_data FROM research_instructions 
                WHERE instruction_id = "web_research_standard_2025"
            ''')
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return json.loads(result[0])
            else:
                print("❌ Инструкция не найдена в БД!")
                return None
                
        except Exception as e:
            print(f"❌ Ошибка получения инструкции: {e}")
            return None
    
    def perform_web_search_analysis(self, keyword: str) -> Dict[str, Any]:
        """Выполнение веб-поиска и анализа с измерением времени"""
        start_time = time.time()
        
        try:
            # Получаем инструкцию
            instruction = self.get_instruction_from_db()
            if not instruction:
                return {"error": "Instruction not found"}
            
            # Генерируем поисковые запросы
            search_queries = self.generate_search_queries(keyword, instruction)
            
            # Симуляция веб-поиска (в реальности здесь вызов web_search())
            search_results = []
            search_start = time.time()
            
            for query in search_queries:
                query_start = time.time()
                # Здесь будет реальный web_search(query)
                result = {
                    "query": query,
                    "results_found": True,
                    "execution_time": time.time() - query_start
                }
                search_results.append(result)
            
            search_time = time.time() - search_start
            
            # Анализ согласно инструкции
            analysis_start = time.time()
            analysis_data = self.create_full_analysis(keyword, search_results, instruction)
            analysis_time = time.time() - analysis_start
            
            total_time = time.time() - start_time
            
            # Добавляем метрики времени
            analysis_data['execution_metrics'] = {
                'total_execution_time_seconds': round(total_time, 2),
                'search_time_seconds': round(search_time, 2),
                'analysis_time_seconds': round(analysis_time, 2),
                'queries_count': len(search_queries),
                'average_query_time': round(search_time / len(search_queries), 2)
            }
            
            return analysis_data
            
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                "error": str(e),
                "execution_time_seconds": round(execution_time, 2)
            }
    
    def generate_search_queries(self, keyword: str, instruction: Dict[str, Any]) -> List[str]:
        """Генерация поисковых запросов"""
        queries = []
        
        # Основной поиск
        primary_query = instruction['web_search_strategy']['primary_search']['query'].format(keyword=keyword)
        queries.append(primary_query)
        
        # Дополнительные поиски
        for search in instruction['web_search_strategy']['secondary_searches']:
            query = search['query'].format(
                keyword=keyword,
                brand_domain="example.com",
                year="2025"
            )
            queries.append(query)
        
        return queries
    
    def create_full_analysis(self, keyword: str, search_results: List[Dict], instruction: Dict[str, Any]) -> Dict[str, Any]:
        """Создание полного анализа согласно инструкции"""
        return {
            'keyword': keyword,
            'created_at': datetime.now().isoformat(),
            'instruction_applied': 'web_research_standard_2025',
            'search_queries': [r['query'] for r in search_results],
            'search_results_count': len(search_results),
            'intent_analysis': {'intent': 'Информационный'},
            'serp_analysis': {'total_results': len(search_results)},
            'semantic_clusters': {'primary': {'keywords': [keyword]}},
            'content_gaps': ['Контент-гэп 1', 'Контент-гэп 2'],
            'facts_and_figures': [{'fact': 'Факт 1', 'source': 'example.com'}],
            'seo_elements': {'title_variants': [f'{keyword}: полное руководство']},
            'faq': [{'question': 'Вопрос 1', 'answer': 'Ответ 1'}],
            'kpi_brief': {'goal': 'Информировать о теме', 'volume': '2500 слов'}
        }
    
    def save_to_database(self, keyword: str, analysis_data: Dict[str, Any]) -> int:
        """Сохранение результатов в БД"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS enhanced_web_research (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT NOT NULL,
                    research_data TEXT NOT NULL,
                    execution_metrics TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'completed'
                )
            ''')
            
            insert_query = '''
                INSERT INTO enhanced_web_research (keyword, research_data, execution_metrics, status)
                VALUES (?, ?, ?, ?)
            '''
            
            cursor.execute(insert_query, (
                keyword,
                json.dumps(analysis_data, ensure_ascii=False),
                json.dumps(analysis_data.get('execution_metrics', {}), ensure_ascii=False),
                'completed'
            ))
            
            research_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return research_id
            
        except Exception as e:
            print(f"❌ Ошибка сохранения в БД: {e}")
            return None

class BatchProcessor:
    """Обработчик пакетных задач"""
    
    def __init__(self, max_workers: int = 3):
        self.queue = TaskQueue()
        self.researcher = EnhancedWebResearcher()
        self.max_workers = max_workers
    
    def process_single_keyword(self, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Обработка одного ключевого слова"""
        task_id = task_info['task_id']
        keyword = task_info['keyword']
        
        print(f"🔍 Обработка: {keyword}")
        
        # Отмечаем задачу как выполняющуюся
        if not self.queue.start_task(task_id):
            return {"error": "Failed to start task"}
        
        start_time = time.time()
        
        try:
            # Выполняем исследование
            analysis_data = self.researcher.perform_web_search_analysis(keyword)
            
            if "error" in analysis_data:
                execution_time = time.time() - start_time
                self.queue.complete_task(task_id, execution_time, "", analysis_data["error"])
                return {"error": analysis_data["error"], "task_id": task_id}
            
            # Сохраняем в БД
            research_id = self.researcher.save_to_database(keyword, analysis_data)
            
            execution_time = time.time() - start_time
            result_data = json.dumps({
                "research_id": research_id,
                "keyword": keyword,
                "execution_time": execution_time
            })
            
            # Завершаем задачу
            self.queue.complete_task(task_id, execution_time, result_data)
            
            print(f"✅ Завершено: {keyword} (время: {execution_time:.2f}с)")
            return {"success": True, "task_id": task_id, "research_id": research_id}
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = str(e)
            self.queue.complete_task(task_id, execution_time, "", error_msg)
            print(f"❌ Ошибка: {keyword} - {error_msg}")
            return {"error": error_msg, "task_id": task_id}
    
    def process_group(self, group_id: str) -> Dict[str, Any]:
        """Обработка группы задач"""
        print(f"🚀 ЗАПУСК ОБРАБОТКИ ГРУППЫ: {group_id}")
        print("=" * 60)
        
        start_time = time.time()
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Запускаем задачи параллельно
            future_to_task = {}
            
            while True:
                task = self.queue.get_next_task()
                if not task:
                    break
                
                # Фильтруем только задачи из нашей группы
                if not task['task_id'].startswith(group_id):
                    continue
                
                future = executor.submit(self.process_single_keyword, task)
                future_to_task[future] = task
            
            # Собираем результаты
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    # Показываем прогресс
                    status = self.queue.get_group_status(group_id)
                    print(f"📊 Прогресс: {status['completed_tasks']}/{status['total_tasks']} ({status['progress_percent']}%)")
                    
                except Exception as e:
                    print(f"❌ Ошибка выполнения задачи {task['task_id']}: {e}")
                    results.append({"error": str(e), "task_id": task['task_id']})
        
        total_time = time.time() - start_time
        
        # Обновляем статистику группы
        conn = sqlite3.connect(self.queue.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE task_groups 
            SET status = 'completed', completed_at = CURRENT_TIMESTAMP, 
                total_execution_time_seconds = ?
            WHERE group_id = ?
        ''', (total_time, group_id))
        
        conn.commit()
        conn.close()
        
        return {
            "group_id": group_id,
            "total_execution_time": total_time,
            "results": results,
            "successful": len([r for r in results if "success" in r]),
            "failed": len([r for r in results if "error" in r])
        }

def main():
    """Главная функция"""
    if len(sys.argv) < 2:
        print("🔍 ИСПОЛЬЗОВАНИЕ:")
        print("python3 enhanced_auto_research.py \"ключевое слово\"")
        print("python3 enhanced_auto_research.py --group \"название группы\" \"ключ1\" \"ключ2\" ...")
        print("python3 enhanced_auto_research.py --process-group \"group_id\"")
        print("python3 enhanced_auto_research.py --status \"group_id\"")
        return 1
    
    if sys.argv[1] == "--group" and len(sys.argv) > 3:
        # Групповая обработка
        group_name = sys.argv[2]
        keywords = sys.argv[3:]
        
        print(f"🔍 СОЗДАНИЕ ГРУППЫ ЗАДАЧ")
        print(f"📝 Название группы: {group_name}")
        print(f"📊 Количество ключевых слов: {len(keywords)}")
        print("=" * 60)
        
        queue = TaskQueue()
        group_id = queue.create_group(group_name, keywords)
        
        print(f"✅ Группа создана: {group_id}")
        print(f"🚀 Для запуска обработки выполните:")
        print(f"python3 enhanced_auto_research.py --process-group {group_id}")
        
        return 0
    
    elif sys.argv[1] == "--process-group" and len(sys.argv) > 2:
        # Обработка группы
        group_id = sys.argv[2]
        
        processor = BatchProcessor(max_workers=3)
        result = processor.process_group(group_id)
        
        print(f"\n✅ ГРУППА ОБРАБОТАНА!")
        print(f"🆔 Group ID: {result['group_id']}")
        print(f"⏱️ Общее время: {result['total_execution_time']:.2f} секунд")
        print(f"✅ Успешно: {result['successful']}")
        print(f"❌ Ошибок: {result['failed']}")
        
        return 0
    
    elif sys.argv[1] == "--status" and len(sys.argv) > 2:
        # Статус группы
        group_id = sys.argv[2]
        
        queue = TaskQueue()
        status = queue.get_group_status(group_id)
        
        if status:
            print(f"📊 СТАТУС ГРУППЫ: {group_id}")
            print(f"📈 Прогресс: {status['completed_tasks']}/{status['total_tasks']} ({status['progress_percent']}%)")
            print(f"✅ Завершено: {status['completed_tasks']}")
            print(f"❌ Ошибок: {status['failed_tasks']}")
            print(f"📋 Статус: {status['status']}")
        else:
            print(f"❌ Группа {group_id} не найдена")
        
        return 0
    
    else:
        # Одиночная обработка
        keyword = sys.argv[1]
        
        print(f"🔍 ОДИНОЧНАЯ ОБРАБОТКА")
        print(f"🎯 Ключевое слово: {keyword}")
        print("=" * 60)
        
        researcher = EnhancedWebResearcher()
        
        start_time = time.time()
        analysis_data = researcher.perform_web_search_analysis(keyword)
        total_time = time.time() - start_time
        
        if "error" in analysis_data:
            print(f"❌ Ошибка: {analysis_data['error']}")
            return 1
        
        # Сохраняем в БД
        research_id = researcher.save_to_database(keyword, analysis_data)
        
        metrics = analysis_data.get('execution_metrics', {})
        
        print(f"\n✅ ИССЛЕДОВАНИЕ ЗАВЕРШЕНО!")
        print(f"🆔 ID в БД: {research_id}")
        print(f"🎯 Ключевое слово: {keyword}")
        print(f"⏱️ Общее время: {metrics.get('total_execution_time_seconds', 0):.2f}с")
        print(f"🔍 Время поиска: {metrics.get('search_time_seconds', 0):.2f}с")
        print(f"📊 Время анализа: {metrics.get('analysis_time_seconds', 0):.2f}с")
        print(f"📋 Запросов: {metrics.get('queries_count', 0)}")
        
        return 0

if __name__ == "__main__":
    exit(main())
