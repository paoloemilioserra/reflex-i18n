"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import json
import pathlib

import reflex as rx


class State(rx.State):
    """The app state."""

    language: str = 'en'
    path: str = 'assets/locales'
    strings: dict[str, str] = json.loads((pathlib.Path(path) / language / 'translation.json').read_text(encoding='utf-8'))

    def click_en(self):
        self.language = 'en'
        self.update_strings()

    def click_it(self):
        self.language = 'it'
        self.update_strings()

    def update_strings(self):
        self.strings = json.loads((pathlib.Path(self.path) / self.language / 'translation.json').read_text(encoding='utf-8'))


def index() -> rx.Component:

    return rx.container(
        rx.text(State.strings['hello']),
        rx.button(
            'EN',
            on_click=State.click_en
        ),
        rx.button(
            'IT',
            on_click=State.click_it
        )
    )


app = rx.App()
app.add_page(index)
