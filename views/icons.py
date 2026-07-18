"""
Inline Lucide SVG icons.
Usage:  from views.icons import icon
        icon("film")          # returns <svg ...> string
        icon("search", size=20, color="#a5b4fc")
"""

_ICONS = {
    "film": (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"'
        ' stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/>'
        '<line x1="7" y1="2" x2="7" y2="22"/><line x1="17" y1="2" x2="17" y2="22"/>'
        '<line x1="2" y1="12" x2="22" y2="12"/>'
        '<line x1="2" y1="7" x2="7" y2="7"/><line x1="17" y1="7" x2="22" y2="7"/>'
        '<line x1="2" y1="17" x2="7" y2="17"/><line x1="17" y1="17" x2="22" y2="17"/>'
        '</svg>'
    ),
    "search": (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"'
        ' stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>'
        '</svg>'
    ),
    "sparkles": (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"'
        ' stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M12 3L13.5 8.5L19 10L13.5 11.5L12 17L10.5 11.5L5 10L10.5 8.5Z"/>'
        '<path d="M19 3L19.5 4.5L21 5L19.5 5.5L19 7L18.5 5.5L17 5L18.5 4.5Z"/>'
        '<path d="M5 17L5.5 18.5L7 19L5.5 19.5L5 21L4.5 19.5L3 19L4.5 18.5Z"/>'
        '</svg>'
    ),
    "flame": (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"'
        ' stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6'
        ' .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3'
        ' a2.5 2.5 0 0 0 2.5 2.5z"/>'
        '</svg>'
    ),
    "table": (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"'
        ' stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18'
        'm0 0h10a2 2 0 0 0 2-2V9M9 21H5a2 2 0 0 1-2-2V9m0 0h18"/>'
        '</svg>'
    ),
    # star  ← replaces ★
    "star": (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"'
        ' stroke="none">'
        '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02'
        ' 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>'
        '</svg>'
    ),
    # heart-pulse  ← replaces 💓
    "heart-pulse": (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"'
        ' stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2'
        '-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>'
        '<path d="M3.22 12H9.5l1.5-1.5 2 4.5 2-7 1.5 4h5.27"/>'
        '</svg>'
    ),
    # clapperboard  ← page icon (no emoji version, text fallback is fine)
    "clapperboard": (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"'
        ' stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M20.2 6 3 11l-.9-2.4c-.3-1.1.3-2.2 1.3-2.5l13.5-4c1-.3 2.1.3 2.4 1.3Z"/>'
        '<path d="m6.2 5.3 3.1 3.9"/><path d="m12.4 3.4 3.1 4"/>'
        '<path d="M3 11h18v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/>'
        '</svg>'
    ),
    # filter  ← replaces 🎭 for genre/filter tab
    "filter": (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"'
        ' stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>'
        '</svg>'
    ),
    # loader / zap  ← replaces ⚡
    "zap": (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"'
        ' stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>'
        '</svg>'
    ),
}


def icon(name: str, size: int = 16, color: str = "currentColor", cls: str = "") -> str:
    """Return an inline SVG string for the given Lucide icon name."""
    svg = _ICONS.get(name, _ICONS["film"])
    style = f'width:{size}px;height:{size}px;color:{color};vertical-align:middle;flex-shrink:0;'
    cls_attr = f' class="{cls}"' if cls else ""
    return svg.replace("<svg ", f'<svg style="{style}"{cls_attr} ', 1)
