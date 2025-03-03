from django.db import models

# Create your models here.
from django.db import models

class AIRequest(models.Model):
    user_input = models.TextField()
    ai_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_input[:50]
    





