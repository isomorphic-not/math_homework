import sys

from PyQt5.QtWidgets import QApplication

from mathsapp import MathScratchPadApp


def main() -> None:
    app = QApplication(sys.argv)
    ex = MathScratchPadApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
