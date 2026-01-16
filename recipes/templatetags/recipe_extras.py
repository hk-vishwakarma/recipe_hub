from django import template
import math

register = template.Library()

@register.filter
def stars(rating):
    return '⭐' * rating



@register.filter
def render_stars(rating):
    """
    Returns SVG HTML for star rating (supports half stars).
    """
    try:
        rating = float(rating)
    except (ValueError, TypeError):
        rating = 0

    full_stars = int(rating)
    half_star = (rating - full_stars) >= 0.5
    empty_stars = 5 - full_stars - (1 if half_star else 0)

    # SVG icons for stars
    full_svg = '<svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-yellow-400 inline" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.236 3.79a1 1 0 00.95.69h3.993c.969 0 1.371 1.24.588 1.81l-3.23 2.347a1 1 0 00-.364 1.118l1.236 3.79c.3.921-.755 1.688-1.54 1.118l-3.23-2.347a1 1 0 00-1.176 0l-3.23 2.347c-.785.57-1.84-.197-1.54-1.118l1.236-3.79a1 1 0 00-.364-1.118L2.182 9.217c-.783-.57-.38-1.81.588-1.81h3.993a1 1 0 00.95-.69l1.236-3.79z" /></svg>'
    half_svg = '<svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-yellow-400 inline" viewBox="0 0 24 24" fill="currentColor"><defs><linearGradient id="half-grad"><stop offset="50%" stop-color="currentColor"/><stop offset="50%" stop-color="transparent"/></linearGradient></defs><path fill="url(#half-grad)" d="M12 .587l3.668 7.431 8.2 1.192-5.934 5.782 1.401 8.168L12 18.896l-7.335 3.864 1.401-8.168L.132 9.21l8.2-1.192z"/></svg>'
    empty_svg = '<svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-gray-300 inline" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.236 3.79a1 1 0 00.95.69h3.993c.969 0 1.371 1.24.588 1.81l-3.23 2.347a1 1 0 00-.364 1.118l1.236 3.79c.3.921-.755 1.688-1.54 1.118l-3.23-2.347a1 1 0 00-1.176 0l-3.23 2.347c-.785.57-1.84-.197-1.54-1.118l1.236-3.79a1 1 0 00-.364-1.118L2.182 9.217c-.783-.57-.38-1.81.588-1.81h3.993a1 1 0 00.95-.69l1.236-3.79z" /></svg>'

    html = full_svg * full_stars
    if half_star:
        html += half_svg
    html += empty_svg * empty_stars

    return html