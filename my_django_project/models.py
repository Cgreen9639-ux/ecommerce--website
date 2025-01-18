from django.db import models # type: ignore

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Project(models.Model):
    name = models.CharField(max_length=100, default="Neuro Wear")
    description = models.TextField()

    def __str__(self):
        return self.name
