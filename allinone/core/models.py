from django.db import models

# Create your models here.
from django.db import models

class AIRequest(models.Model):
    user_input = models.TextField()
    ai_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_input[:50]
    
class history(models.Model):
    name=models.CharField(max_length=100)
    search=models.CharField(max_length=100)
    date=models.DateField()
    time=models.TimeField()
    def __str__(self):  # Fixed '__str__' method (double underscores)
        return f"{self.name} - {self.search} ({self.date} {self.time})"






