import sys
import logging
from PyQt6.QtWidgets import QApplication
from presentation.gui import MainWindow

if __name__ == "__main__":
    logging.config.fileConfig('log/logging.conf')
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
