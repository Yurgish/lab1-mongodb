from PySide6.QtWidgets import QApplication

from app.ui.app_window import AppWindow


def main() -> None:
    application = QApplication([])
    window = AppWindow()
    window.show()
    application.exec()


if __name__ == "__main__":
    main()
