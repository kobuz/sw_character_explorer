from django.contrib import admin

from characters.models import Collection


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["created", "target_file"]
