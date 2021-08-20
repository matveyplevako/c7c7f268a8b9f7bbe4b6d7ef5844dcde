from django.contrib import admin
from django.shortcuts import redirect

from .models import Graph


class GraphAdmin(admin.ModelAdmin):
    list_display = ('function_text', 'image_tag', "interval_days", "step_hours", "process_time")
    fields = ['function_text', "interval_days", "step_hours"]
    readonly_fields = ['image_tag']

    def response_add(self, request, obj, post_url_continue=None):
        return redirect(f'/wait_for_results/{obj.pk}')

    def response_change(self, request, obj):
        return redirect(f'/wait_for_results/{obj.pk}')


admin.site.register(Graph, GraphAdmin)
