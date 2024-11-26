from django.contrib import admin
from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'birth_date', 'is_staff')
    search_fields = ('username', 'email')
