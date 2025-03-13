import sys
from PyQt6.QtWidgets import QApplication
from gui import EokulFotoApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EokulFotoApp()
    window.show()
    sys.exit(app.exec())
