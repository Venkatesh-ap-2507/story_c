from django.db import models


# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Story(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    contributions = models.JSONField(default=list)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='stories')
    image = models.ImageField(upload_to='story_images/',null=True,blank=True)

    def __str__(self):
        return self.title
