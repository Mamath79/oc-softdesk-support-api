from django.contrib import admin
from projects.models import Project, Contributor

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'type', 'date_created')  # Colonnes affichées
    search_fields = ('title', 'author__username')  # Champs de recherche
    list_filter = ('type', 'date_created')  # Filtres


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role', 'date_created')  # Colonnes affichées
    search_fields = ('user__username', 'project__title')  # Champs de recherche
    list_filter = ('role', 'date_created')  # Filtres
    autocomplete_fields = ('user', 'project')  # Améliore l'expérience pour les relations ForeignKey