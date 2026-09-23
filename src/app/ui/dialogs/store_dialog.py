from typing import Any

from PySide6.QtWidgets import QCheckBox, QDialog, QDialogButtonBox, QFormLayout, QLineEdit


class StoreDialog(QDialog):
    def __init__(self, current: Any = None, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Edit store" if current else "Add store")
        self.setMinimumSize(520, 320)
        self.fields = {
            key: QLineEdit(self) for key in ("name", "city", "street", "building", "contact_phone")
        }
        self.active = QCheckBox("Store is active", self)
        for widget in self.fields.values():
            widget.setMinimumWidth(360)
            widget.setMinimumHeight(30)
        if current:
            values = {
                "name": current.name,
                "city": current.address.city,
                "street": current.address.street,
                "building": current.address.building,
                "contact_phone": current.contact_phone,
            }
            for key, value in values.items():
                self.fields[key].setText(str(value))
            self.active.setChecked(current.is_active)
        else:
            self.active.setChecked(True)
        layout = QFormLayout(self)
        for key, widget in self.fields.items():
            layout.addRow(key.replace("_", " ").title(), widget)
        layout.addRow("", self.active)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def values(self) -> dict[str, object]:
        return {
            **{key: widget.text().strip() for key, widget in self.fields.items()},
            "is_active": self.active.isChecked(),
        }
