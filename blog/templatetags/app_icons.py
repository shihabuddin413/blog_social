import os
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe


register = template.Library()

ICON_PATH = os.path.join(settings.BASE_DIR, "blog", "static", "icons")

@register.simple_tag
def get_icon(name, size=20, cls=""):
    """Load inline SVG icon by name"""
    file_path = os.path.join(ICON_PATH, f"{name}.svg")

    try:
        with open(file_path, "r") as f:
            svg = f.read()
        # optional class & size inject
        svg = svg.replace("<svg", f'<svg width="{size}" height="{size}" class="{cls}"')
        return mark_safe(svg)
    except FileNotFoundError:
        return f"<!-- icon '{name}' not found -->"
