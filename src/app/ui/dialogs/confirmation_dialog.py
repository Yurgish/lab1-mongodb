from PySide6.QtWidgets import QMessageBox, QWidget


class ConfirmationDialog:
    @staticmethod
    def ask(parent: QWidget, entity: str) -> bool:
        return (
            QMessageBox.question(
                parent,
                f"Delete {entity}",
                f"Delete the selected {entity}? Related records may also be removed.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            == QMessageBox.StandardButton.Yes
        )
