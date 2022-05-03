import sys
from PyQt5 import QtWidgets

from window_logic import ResearchApp


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ResearchApp()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
