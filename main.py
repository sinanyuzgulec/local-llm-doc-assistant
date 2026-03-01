#!/usr/bin/env python

from nicegui import ui
from app.ui import setup_ui
from config import config

setup_ui()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(host=config.APP_HOST, port=config.APP_PORT, dark=True)
