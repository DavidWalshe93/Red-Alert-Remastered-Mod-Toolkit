"""
Author:     David Walshe
Date:       04 July 2020
"""

from PyQt5.QtWidgets import QMainWindow
from src.view.core.app import Ui_MainWindow


class View(Ui_MainWindow, QMainWindow):

    def __init__(self, *args, **kwargs):
        """
        Abstract base for all views in the application.
        """
        super().__init__(*args, **kwargs)
        self.DEFAULT_STYLE_TEMPLATE = "{  background-color : white; color : black; font-size: 15px; height: 22px; }"
        self.CUSTOM_STYLE_TEMPLATE = "{ background-color : black; color : white; font-size: 15px; height: 22px; }"

    def default_style(self, widget):
        return f"{type(widget).__name__} {self.DEFAULT_STYLE_TEMPLATE}"

    def custom_style(self, widget):
        return f"{type(widget).__name__} {self.CUSTOM_STYLE_TEMPLATE}"

    def set_custom_view(self, widget_name):
        widget = self.__getattribute__(widget_name)
        style = self.custom_style(widget)
        self.__getattribute__(widget_name).setStyleSheet(style)

    def set_default_view(self, widget_name):
        widget = self.__getattribute__(widget_name)
        style = self.default_style(widget)
        self.__getattribute__(widget_name).setStyleSheet(style)
