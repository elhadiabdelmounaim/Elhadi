from django.contrib import admin
from .models import Contact, CVItem, CVProfile, CVSection

admin.site.register(Contact)


class CVItemInline(admin.TabularInline):
    model = CVItem
    extra = 0


@admin.register(CVSection)
class CVSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "key", "order", "is_visible")
    inlines = [CVItemInline]


@admin.register(CVProfile)
class CVProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not CVProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
