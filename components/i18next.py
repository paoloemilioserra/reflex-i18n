import typing
from functools import lru_cache

import reflex as rx
from reflex.utils import imports


class TranslationProvider(rx.Component):
    """Top level translation provider must be included in any app using translation components."""
    # The name of the npm package.
    library: str = "react-i18next"

    # Any additional libraries needed to use the component.
    lib_dependencies: list[str] = ["@babel/runtime", "html-parse-stringify"]

    tag = "I18nextProvider"

    # language: rx.vars.Var[str]

    # @classmethod
    # def create(cls) -> rx.Component:
    #     """Create a new TranslationProvider component.
    #
    #     Returns:
    #         A new TranslationProvider component.
    #     """
    #     return super().create(
    #         language=rx.vars.Var.create("withTranslation()", _var_is_local=False),
    #     )

    @classmethod
    @lru_cache(maxsize=None)
    def _get_dependencies_imports(cls) -> imports.ImportDict:
        """Get the imports from lib_dependencies for installing.

        Returns:
            The dependencies imports of the component.
        """
        return {
            dep: [imports.ImportVar(tag=None, render=False)]
            for dep in ["@babel/runtime", "html-parse-stringify"]
        }

    def _get_imports(self) -> imports.ImportDict:
        _imports = super()._get_imports()
        _imports.setdefault(self.__fields__["library"].default, []).append(
            imports.ImportVar(tag="withTranslation", is_default=False),
        )
        _imports.setdefault(self.__fields__["library"].default, []).append(
            imports.ImportVar(tag="useTranslation", is_default=False),
        )
        _imports.setdefault(self.__fields__["library"].default, []).append(
            imports.ImportVar(tag="Trans", is_default=False),
        )
        _imports.setdefault('/public/i18n.js', []).append(
            imports.ImportVar(tag="i18n", is_default=False),
        )
        return _imports


translation_provider = TranslationProvider.create()


class Translation(TranslationProvider):
    """Translation component."""

    # # The name of the npm package.
    # library: str = "react-i18next"
    #
    # # Any additional libraries needed to use the component.
    # lib_dependencies: list[str] = ["@babel/runtime", "html-parse-stringify"]

    # The name of the component to use from the package.
    tag: str = "Trans"

    i18n_key: typing.Optional[typing.Union[rx.Var[str], str]] = None
    translator: typing.Optional[typing.Union[rx.Var[tuple[typing.Any]], tuple[typing.Any]]] = None  # 0 is the tranlsator, 1 is the i18n

    # Trans is a default export from the module.
    is_default: bool = False

    @staticmethod
    @lru_cache(maxsize=None)
    def _get_app_wrap_components() -> dict[tuple[int, str], rx.Component]:
        return {
            (100, "i18n"): translation_provider,
        }

    @classmethod
    def create(cls, *children, key: str, **props) -> rx.Component:
        """Create a new Translation component.

        Returns:
            A new Translation component.
        """
        return super().create(
            i18n_key=rx.vars.Var.create(key, _var_is_local=False, _var_is_string=True),
            # translator=rx.vars.Var.create("useTranslation()", _var_is_local=False),
            *children,
            **props
        )

    # @classmethod
    # @lru_cache(maxsize=None)
    # def _get_dependencies_imports(cls) -> imports.ImportDict:
    #     """Get the imports from lib_dependencies for installing.
    #
    #     Returns:
    #         The dependencies imports of the component.
    #     """
    #     return {
    #         dep: [imports.ImportVar(tag=None, render=False)]
    #         for dep in ["@babel/runtime", "html-parse-stringify"]
    #     }

    # def _get_imports(self) -> imports.ImportDict:
    #     _imports = super()._get_imports()
    #     _imports.setdefault(self.__fields__["library"].default, []).append(
    #         imports.ImportVar(tag="withTranslation", is_default=False),
    #     )
    #     _imports.setdefault(self.__fields__["library"].default, []).append(
    #         imports.ImportVar(tag="useTranslation", is_default=False),
    #     )
    #     _imports.setdefault('/public/i18n.js', []).append(
    #         imports.ImportVar(tag="i18n", is_default=False),
    #     )
    #     return _imports


# Convenience function to create the Spline component.
translation = Translation.create
