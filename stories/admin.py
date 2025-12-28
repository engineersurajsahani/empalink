from django.contrib import admin
from .models import Category, Story


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'category', 'status', 'required_amount', 'collected_amount', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'creator__username')
    ordering = ('-created_at',)
    readonly_fields = ('collected_amount', 'created_at', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role != 'admin':
            # Non-admins can only see their own stories
            qs = qs.filter(creator=request.user)
        return qs
