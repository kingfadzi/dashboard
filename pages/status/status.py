# File: pages/status.py
import dash

import callbacks.status.status_callbacks
from pages.status.status_layout import get_status_layout

dash.register_page(__name__, path="/status", name="Status")

layout = get_status_layout()
