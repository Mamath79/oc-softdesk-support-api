from django.db import models
from users.models import User


class Project(models.Model):

    PROJECT_TYPES = [
        ('back-end', 'Back-end'),
        ('front-end', 'Front-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('users.User',on_delete=models.CASCADE, related_name='created_projects')
    type = models.CharField(max_length=50, choices=PROJECT_TYPES)

    def __str__(self):
        return self.title
    
class Contributor(models.Model):
    ROLE_CHOICES = [
        ('AUTHOR', 'Auteur'),
        ('CONTRIBUTOR', 'Contributeur'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CONTRIBUTOR')

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'project')  # Évite les doublons de contributeurs

    def __str__(self):
        return f"{self.user.username} - {self.project.title} ({self.role})"
    
    