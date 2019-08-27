from PyQt5.QtWidgets import QApplication
from chess import Chess
import sys

app = QApplication([])
chess = Chess()
sys.exit(app.exec_())
