"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import json
from typing import Any
import pathlib

import reflex as rx


def key_recursion(t: dict[str, Any], prefix: str = '') -> dict[str, Any]:
    """
    Returns a 'flatten' dictionary
    :param t:
    :param prefix:
    :return:
    """
    ret = {}
    for k, v in t.items():
        if len(prefix) > 0:
            k = prefix + '.' + k

        if isinstance(v, dict):
            ret.update(key_recursion(v, k))
        else:
            ret[k] = v
    return ret


class State(rx.State):
    """The app state."""

    language: str = 'en'
    path: str = 'assets/locales'
    strings: dict[str, str] = {}
    LANGUAGES: list[str] = [f.name.lower() for f in pathlib.Path(path).iterdir() if f.is_dir()]

    def click_language(self, lng: str):
        if lng.lower() in self.LANGUAGES:
            self.language = lng
            self.update_strings()

    def update_strings(self):
        dd = json.loads((pathlib.Path(self.path) / self.language / 'translation.json').read_text(encoding='utf-8'))
        dd = key_recursion(dd)
        self.strings = dd


def index() -> rx.Component:

    return rx.container(
        rx.text(State.strings['hello']),
        rx.text(State.strings['description.part1']),
        rx.text(State.strings['description.part2']),
        rx.button(
            'EN',
            on_click=lambda: State.click_language('en')
        ),
        rx.button(
            'IT',
            on_click=lambda: State.click_language('it')
        ),
        on_mount=State.update_strings
    )


app = rx.App()
app.add_page(index)
