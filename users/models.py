from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# The Student class is a model that represents a student with a unique student ID, name, and email.
class Student(models.Model):
    ID = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=64)
    lname = models.CharField(max_length=64)
    email = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.ID} | {self.email}'
    
    def get_full_name(self):
        return f'{self.fname} {self.lname}'