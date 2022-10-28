import FreeCAD as App

def _refreshApp() -> None:
        App.ActiveDocument.recompute()
        return