"""
Author:     David Walshe
Date:       03 July 2020
"""


from src.view.views.unit import UnitStructureView


class MainWindow(UnitStructureView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
