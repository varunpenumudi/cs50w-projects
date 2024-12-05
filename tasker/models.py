from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ...

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    task_name = models.CharField(max_length=64)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_important = models.BooleanField()
    is_urgent = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.task_name}"
    
    @property
    def get_progress(self):
        if not self.subtasks.all(): return 0
        
        completed, total = 0, 0
        for subtask in self.subtasks.all():
            total += 1
            completed += int(subtask.completed)
        
        return int((completed/total) * 100)
    
    def preview_serialize(self):
        return {
            "id":self.pk,
            "progress":self.get_progress,
            "name":self.task_name,
            "description":self.description if len(self.description)<45 else self.description[:45]+"......",
            "last_updated":self.updated.strftime('%b %d, %I:%M %p').lower(),
        }
    
    def serialize(self):
        return {
            "id":self.pk,
            "progress":self.get_progress,
            "name":self.task_name,
            "description":self.description,
            "last_updated":self.updated.strftime('%b %d, %I:%M %p').lower(),
            "important": self.is_important,
            "urgent": self.is_urgent,
            "subtasks": [subtask.subtask_name for subtask in self.subtasks.all()],
        }

class SubTask(models.Model):
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
    subtask_name = models.CharField(max_length=64)
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.subtask_name}: \n parent task: {self.parent_task} \n status: {self.completed}"
    
    def serialize(self) -> dict:
        return {
            "id": self.id,
            "subtask_name": self.subtask_name,
            "completed": self.completed,
        }
