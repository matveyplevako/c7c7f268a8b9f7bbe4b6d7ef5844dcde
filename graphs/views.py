from django.shortcuts import redirect
from .tasks import generate_image


def redirect_back_to_admin(request, obj_pk):
    # need addition redirect as redirecting directly in admin leads to halt
    res = generate_image.delay(obj_pk)
    res.get()
    return redirect("/admin/graphs/graph/")
