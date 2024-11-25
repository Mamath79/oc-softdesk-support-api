from django.contrib import admin
from projects.models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'type', 'date_created')  # Colonnes affichées
    search_fields = ('title', 'author__username')  # Champs de recherche
    list_filter = ('type', 'date_created')  # Filtres

