import time
from datetime import timedelta, datetime

from django.utils import timezone
from django.core.files import File
import requests

from .models import Graph
from dashboard.celery import app
from .calc import NumericStringParser


def get_points(expression, now, interval, dt):
    lower_bound_unix = (now - timedelta(days=interval)).replace(tzinfo=timezone.utc).timestamp()
    higher_bound_unix = now.replace(tzinfo=timezone.utc).timestamp()
    current = lower_bound_unix
    points = []
    while current < higher_bound_unix:
        # eval is unsafe for production, so we need to use safe expression parser
        x = current
        y = NumericStringParser(current).eval(expression)
        current += dt * 60 * 60
        points.append([x, y])

    return points


@app.task
def generate_image(graph_id):
    try:
        graph_row = Graph.objects.get(pk=graph_id)
        now = timezone.now()
        graph_row.process_time = now

        try:
            left_part, right_part = graph_row.function_text.split("=")
            if left_part.strip() != "y":
                raise Exception("Expression should start with y=")

            points = get_points(right_part, now, graph_row.interval_days, graph_row.step_hours)
            response = requests.post("http://highcharts:8080", json={
                "infile": {"title": {"text": graph_row.function_text},
                           "series": [{"data": points}]}}, stream=True)
            assert response.status_code == 200, response.text
            graph_row.graph.save(f"graph_{graph_id}.png", File(response.raw), save=False)
            graph_row.error = ""
        except Exception as e:
            graph_row.graph = None
            graph_row.error = str(e)

        graph_row.save()


    except Graph.DoesNotExist:
        return "Invalid id specified"
    except Exception as e:
        return str(e)
