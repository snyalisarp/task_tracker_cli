import json
from pathlib import Path

class JSONManager:
    def __init__(self, filename: str):
        self.file_path = Path(filename)
        self._initialize_db()

    def _initialize_db(self):
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            self._write_all([])

    def _read_all(self) -> list:
        try:
            return json.loads(self.file_path.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_all(self, data: list) -> bool:
        try:
            content = json.dumps(data, indent=4, ensure_ascii=False)
            self.file_path.write_text(content, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Yazma hatası: {e}")
            return False

    def get_all(self) -> list:
        """Public method to retrieve all records."""
        return self._read_all()

    def get_next_id(self) -> int:
        data = self._read_all()
        return max([item['id'] for item in data], default=0) + 1

    def save(self, task_dict: dict) -> bool:
        data = self._read_all()
        existing_index = next((i for i, t in enumerate(data) if t['id'] == task_dict['id']), None)
        
        if existing_index is not None:
            data[existing_index] = task_dict
        else:
            data.append(task_dict)
            
        return self._write_all(data)
    
    def delete(self, search_key: str, search_value) -> bool:
        data = self._read_all()
        initial_count = len(data)
        
        data = [item for item in data if item.get(search_key) != search_value]
        
        if len(data) < initial_count:
            return self._write_all(data)
        return False