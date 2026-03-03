from app.models.taskmodel import TaskStatus, Task
from app.utils.jsonmanager import JSONManager

class TaskService:
    def __init__(self, db_path: str = "tasks.json"):
        self.db = JSONManager(db_path)

    def add_task(self, description: str):
        new_task = Task(
            task_id=self.db.get_next_id(),
            task_description=description,
            task_status=TaskStatus.TODO
        )
        if self.db.save(new_task.to_dict()):
            print(f"Başarıyla eklendi. ID: {new_task.task_id}")

    def update_task_status(self, task_id: int, new_status: TaskStatus):
        # 1. Fetch data through the public interface
        data = self.db.get_all()
        task_data = next((item for item in data if item['id'] == task_id), None)
        
        if not task_data:
            print(f"Hata: {task_id} numaralı task bulunamadı.")
            return

        # 2. Convert to object and apply business logic
        task_obj = Task.from_dict(task_data)
        task_obj.update_status(new_status)

        # 3. Save the updated object (save() does its own internal read — no double-read here)
        if self.db.save(task_obj.to_dict()):
            print(f"Task {task_id} durumu '{new_status.value}' olarak güncellendi.")

    def list_tasks(self, status: str = None):
        tasks = [Task.from_dict(t) for t in self.db.get_all()]
        
        if status:
            tasks = [t for t in tasks if t.task_status.value == status]
        
        if not tasks:
            print("Görüntülenecek görev bulunamadı.")
            return

        print(f"\n{'ID':<5} {'Açıklama':<30} {'Durum':<15} {'Güncellenme'}")
        print("-" * 70)
        for t in tasks:
            print(f"{t.task_id:<5} {t.task_description:<30} {t.task_status.value:<15} {t.updated_at}")

    def delete_task(self, task_id: int):
        if self.db.delete("id", task_id):
            print(f"Task {task_id} başarıyla silindi.")
        else:
            print(f"Hata: {task_id} ID'li görev bulunamadı veya silinemedi.")

