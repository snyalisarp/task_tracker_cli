import time
import unittest
import os
import json
from pathlib import Path
from app.models.taskmodel import Task, TaskStatus
from app.services.taskservice import TaskService
# To run the tests: python -m unittest discover tests
class TestTaskService(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_tasks.json"
        self.service = TaskService(db_path=self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_add_task(self):
        self.service.add_task("Test Görevi")
        
        with open(self.test_db, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['description'], "Test Görevi")
        self.assertEqual(data[0]['status'], TaskStatus.TODO.value)
    
    def test_add_task_empty_string(self):
        with self.assertRaises(Exception) as context:
            self.service.add_task("     ")

        self.assertEqual(str(context.exception), "Task must have a description")

    def test_update_task_status(self):
        self.service.add_task("Güncellenecek Görev")
        task_id = 1
        time.sleep(1.1)
        self.service.update_task_status(task_id, TaskStatus.IN_PROGRESS)
        
        with open(self.test_db, 'r', encoding='utf-8') as f:
            data = json.load(f)
            updated_task = data[0]

        self.assertEqual(updated_task['status'], TaskStatus.IN_PROGRESS.value)
        self.assertNotEqual(updated_task['createdAt'], updated_task['updatedAt'])

    def test_delete_task(self):
        self.service.add_task("Silinecek Görev")
        self.service.delete_task(1)
        
        with open(self.test_db, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 0)

    def test_task_model_logic(self):
        task = Task(
            task_id=99,
            task_description="Model Testi",
            task_status=TaskStatus.TODO,
            created_at="2026-01-01 10:00:00",
            updated_at="2026-01-01 10:00:00"
        )
        
        task.update_status(TaskStatus.DONE)
        
        self.assertEqual(task.task_status, TaskStatus.DONE)
        self.assertNotEqual(task.updated_at, "2026-01-01 10:00:00")

    def test_update_non_existent_task(self):
        self.service.update_task_status(999, TaskStatus.DONE)
        
        with open(self.test_db, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data), 0)

    def test_delete_non_existent_task(self):
        result = self.service.db.delete("id", 999)
        self.assertFalse(result)

    def test_invalid_task_creation(self):
        with self.assertRaises(ValueError):
            Task(
                task_id=1,
                task_description="Hatalı Görev",
                task_status="GEÇERSİZ_STATÜ",
                created_at="...",
                updated_at="..."
            )

    def test_corrupted_json_file(self):
        with open(self.test_db, 'w', encoding='utf-8') as f:
            f.write("{ bu bir geçerli json değildir }")
        
        data = self.service.db.get_all()
        self.assertEqual(data, [])

if __name__ == "__main__":
    unittest.main()