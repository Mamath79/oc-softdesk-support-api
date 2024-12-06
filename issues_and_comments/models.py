from django.db import models
from projects.models import Project
from users.models import User
import uuid


class Issue(models.Model):
    PRIORITY_CHOICES =[
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH','High')
    ]

    TAG_CHOICES =[
        ('BUG','Bug'),
        ('FEATURE', 'Feature'),
        ('TASK','Task')
    ]

    STATUS_CHOICES =[
        ('TODO', 'To_Do'),
        ('IN_PROGRESS', 'In_Progress'),
        ('FINISH', 'Finish')
    ]

    # Détails de l'issue
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # Relations
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')  # Lien vers le projet
    author_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_issues')  # Créateur de l'issue
    assigned_contributor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')  # Contributeur assigné

    # Métadonnées de l'issue
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    tag = models.CharField(max_length=10, choices=TAG_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='TODO')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title}({self.status})"


class Comment(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Ajout de l'UUID
    content = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')  # Lien avec une issue
    author_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  # Auteur du commentaire
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author_user.username} on {self.issue.title}"