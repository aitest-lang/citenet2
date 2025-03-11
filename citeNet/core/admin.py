from django.contrib import admin
from .models import History

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'formatted_history', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('user__username', 'history')
    ordering = ('-timestamp',)

    def formatted_history(self, obj):
        """Custom method to display JSON data in a readable format."""
        return str(obj.history)  # Converts the dictionary to a string for display
    formatted_history.short_description = 'History'  # Column header name