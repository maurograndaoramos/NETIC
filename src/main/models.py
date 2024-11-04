from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100)
    curso = models.CharField(max_length=100)
    email = models.EmailField()
    synopsis = models.TextField()
    instagram = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    otherlink = models.URLField(blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name