from typing import Any

from PySide6.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QSpinBox


class SellerDialog(QDialog):
    def __init__(
        self, stores: list[Any], departments: list[Any], current: Any = None, parent=None
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Edit seller" if current else "Add seller")
        self.setMinimumSize(620, 560)
        self.fields = {
            "first_name": QLineEdit(self),
            "last_name": QLineEdit(self),
            "age": QSpinBox(self),
            "phone": QLineEdit(self),
            "email": QLineEdit(self),
            "position": QLineEdit(self),
            "salary": QLineEdit(self),
        }
        self.fields["age"].setRange(18, 80)
        for widget in self.fields.values():
            widget.setMinimumWidth(420)
            widget.setMinimumHeight(30)
        self.store = QComboBox(self)
        self.department = QComboBox(self)
        for item in stores:
            self.store.addItem(item.name, item.id)
        for item in departments:
            self.department.addItem(item.name, item.id)
        if current:
            for key in ("first_name", "last_name", "phone", "email", "position"):
                self.fields[key].setText(str(getattr(current, key)))
            self.fields["age"].setValue(current.age)
            self.fields["salary"].setText(str(current.salary))
            self.store.setCurrentIndex(max(0, self.store.findData(current.store_id)))
            self.department.setCurrentIndex(max(0, self.department.findData(current.department_id)))
        layout = QFormLayout(self)
        for key, widget in self.fields.items():
            layout.addRow(key.replace("_", " ").title(), widget)
        layout.addRow("Store", self.store)
        layout.addRow("Department", self.department)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def values(self) -> dict[str, object]:
        return {
            **{
                key: (widget.value() if isinstance(widget, QSpinBox) else widget.text().strip())
                for key, widget in self.fields.items()
            },
            "store_id": self.store.currentData(),
            "department_id": self.department.currentData(),
        }
