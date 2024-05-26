"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import json
from typing import Any
import pathlib

import reflex as rx


class DynamicDict(dict):

    def __init__(self):
        super().__init__()

    def __contains__(self, item: str) -> bool:
        res = True
        if isinstance(item, str):
            if item in self.keys():
                return True
            t = self
            for k in item.split('.'):
                if k in t.keys():
                    t = t.get(k, {})
                else:
                    res = False
            return res
        return False

    def __getitem__(self, item: str) -> Any:
        if isinstance(item, str):
            if item in self.keys():
                return self.get(item)
            t = self
            for k in item.split('.'):
                if k in t.keys():
                    t = t.get(k, {})
                else:
                    raise KeyError(f'{item=} not found')
            self[item] = t
            return t
        raise ValueError(f'{item=} must be a string')

    def __setitem__(self, key: str, value: Any) -> None:
        if isinstance(key, str):
            keys = key.split('.')
            n = len(keys) - 2
            t = self
            for i, k in enumerate(keys):
                t = t.setdefault(k, {})
                if i == n:
                    t.update({k: value})
                    return
        raise ValueError(f'{key=} must be a string')

    def update(self, __m, **kwargs):
        super().update(__m, **kwargs)



class State(rx.State):
    """The app state."""

    language: str = 'en'
    path: str = 'assets/locales'
    strings: dict[str, str] = {}  # DynamicDict()  # json.loads((pathlib.Path(path) / language / 'translation.json').read_text(encoding='utf-8')))

    def click_en(self):
        self.language = 'en'
        self.update_strings()

    def click_it(self):
        self.language = 'it'
        self.update_strings()


    @staticmethod
    def key_recursion(t: dict[str, Any], prefix: str = '') -> dict[str, Any]:
        ret = {}
        for k, v in t.items():
            if len(prefix) > 0:
                k = prefix + '.' + k

            if isinstance(v, dict):
                ret.update(State.key_recursion(v, k))
            else:
                ret[k] = v
        return ret

    def update_strings(self):
        dd = DynamicDict()
        dd.update(json.loads((pathlib.Path(self.path) / self.language / 'translation.json').read_text(encoding='utf-8')))
        # TODO recursively add the the sub keys
        dd = State.key_recursion(dd)
        self.strings = dd


def index() -> rx.Component:

    return rx.container(
        rx.text(State.strings['hello']),
        rx.text(State.strings['description.part1']),
        rx.text(State.strings['description.part2']),
        rx.button(
            'EN',
            on_click=State.click_en
        ),
        rx.button(
            'IT',
            on_click=State.click_it
        ),

    )


app = rx.App()
app.add_page(index)


def test():
    dd = DynamicDict()
    dd.update({
  "hello": "This is the 'Hello World' message in English",
  "description": {
    "part1": "This is the first part",
    "part2": "This is the second part"
  }
})
    assert dd['description.part1'] == 'This is the first part'

    dd['2.2'] = 'd'
    assert dd['2.2'] == 'd'


