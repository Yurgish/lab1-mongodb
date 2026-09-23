from typing import Any

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QPlainTextEdit,
    QSpinBox,
)


class DepartmentDialog(QDialog):
    def __init__(self, current: Any = None, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Edit department" if current else "Add department")
        self.setMinimumSize(620, 420)
        self.name, self.floor = QLineEdit(self), QSpinBox(self)
        self.description = QPlainTextEdit(self)
        self.name.setMinimumWidth(460)
        self.name.setMinimumHeight(30)
        self.description.setMinimumSize(460, 180)
        self.floor.setRange(1, 100)
        if current:
            self.name.setText(current.name)
            self.floor.setValue(current.floor)
            self.description.setPlainText(current.description)
        layout = QFormLayout(self)
        layout.addRow("Name", self.name)
        layout.addRow("Floor", self.floor)
        layout.addRow("Description", self.description)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def values(self) -> dict[str, object]:
        return {
            "name": self.name.text().strip(),
            "floor": self.floor.value(),
            "description": self.description.toPlainText().strip(),
        }
