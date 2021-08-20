from django.db import models
from django.utils.html import mark_safe
from graphs.storage import OverwriteStorage


class Graph(models.Model):
    function_text = models.CharField(max_length=255, verbose_name="Функция")
    graph = models.ImageField(upload_to="graphs/", storage=OverwriteStorage(), blank=True, null=True)
    error = models.CharField(max_length=1024, blank=True, null=True)
    interval_days = models.IntegerField(verbose_name="Интервал t, дней")
    step_hours = models.IntegerField(verbose_name="Шаг t, часы")
    process_time = models.DateTimeField(blank=True, null=True, verbose_name="Дата обработки")

    def image_tag(self):
        if self.error:
            return f"Error: {self.error}"
        elif self.graph:
            path = f"/media/{self.graph}"
            return mark_safe(
                f'<a href="{path}" target="_blank"><img src="{path}" width="400" height="300" />')

    image_tag.short_description = 'График'
