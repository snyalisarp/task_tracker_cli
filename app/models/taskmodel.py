from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

# todo - in-progress - done
class TaskStatus(Enum):
    TODO = 'todo'
    IN_PROGRESS = 'in-progress'
    DONE = 'done' 

# field(default_factory=lambda: datetime.now(timezone.utc).isoformat(sep=' ', timespec='seconds'))
@dataclass
class Task:
    task_id: int
    task_description: str
    task_status: TaskStatus
    created_at: str = field(default_factory=lambda: datetime
                            .now()
                            .astimezone()
                            .isoformat(sep=' ', 
                                       timespec='seconds'))
    updated_at: str = field(default_factory=lambda: datetime
                            .now()
                            .astimezone()
                            .isoformat(sep=' ', 
                                       timespec='seconds'))

    def __post_init__(self):
        if not isinstance(self.task_status, TaskStatus):
            raise ValueError("Task status value should be one of them: ",
                             list(TaskStatus))
        if self.task_description.strip() == '':
            raise ValueError("Task must have a description")
        
    def update_status(self, new_status: TaskStatus):
        """Durum güncellenirken updatedAt alanını da günceller."""
        self.task_status = new_status
        self.updated_at = (datetime
                          .now()
                          .astimezone()
                          .isoformat(sep=' ',
                                     timespec='seconds'))
    
    def to_dict(self):
        return {
            "id": self.task_id,
            "description": self.task_description,
            "status": self.task_status.value,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }
    
    
    @classmethod
    def from_dict(cls, data: dict):
        """Sözlük verisinden nesne örneği oluşturur."""
        return cls(
            task_id=data['id'],
            task_description=data['description'],
            task_status=TaskStatus(data['status']),
            created_at=data['createdAt'],
            updated_at=data['updatedAt']
        )


# if __name__ == '__main__':
#     task1 = Task(task_id=1, 
#                  task_description="test", 
#                  task_status=TaskStatus.DONE)
#     print(task1.to_dict())
#     print(str(TaskStatus.DONE.value))
#     test_dict = {"tasks"}