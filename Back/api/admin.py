from django.contrib import admin
from api.models import User


@admin.register(User)
class DetectionAdmin(admin.ModelAdmin):
    """
    Представление таблици PortfolioStatus в admin
    """
    list_display = ('email','first_name','last_name','gender','avatar_tag')
