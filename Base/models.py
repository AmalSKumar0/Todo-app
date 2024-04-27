from django.db import models
from django.contrib.auth.models import User

class List(models.Model):
    list_name = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.list_name
    
class ListItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)  # Change default to your chosen default user
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    item = models.CharField(max_length=500)
    status = models.BooleanField(default=False)

