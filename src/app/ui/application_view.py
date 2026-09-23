from typing import Any

from PySide6.QtWidgets import QDialog, QLabel, QMessageBox, QVBoxLayout, QWidget

from app.modules.controller_events import Failed
from app.modules.seller.schemas import SellerCreate, SellerUpdate
from app.modules.store.schemas import (
    AddressModel,
    DepartmentCreate,
    DepartmentUpdate,
    StoreCreate,
    StoreUpdate,
)

from .composition import UiContainer
from .dialogs import ConfirmationDialog, DepartmentDialog, SellerDialog, StoreDialog
from .presenters import DepartmentPresenter, SellerPresenter, StorePresenter
from .state import AppState
from .views import DepartmentsPanel, SellersPanel, StoresPanel


class ApplicationView(QWidget):
    """Composition root for the single-page stores, departments and sellers UI."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.state = AppState()
        self.status = QLabel("Select a store to view its departments and sellers.", self)
        self.container = UiContainer(self._controller_event)
        self.stores, self.departments, self.sellers = (
            StoresPanel(self),
            DepartmentsPanel(self),
            SellersPanel(self),
        )
        self.store_presenter = StorePresenter(
            self.container.store_controller, self.stores.model, self._notify
        )
        self.department_presenter = DepartmentPresenter(
            self.container.department_controller, self.departments.model, self._notify
        )
        self.seller_presenter = SellerPresenter(
            self.container.seller_controller, self.sellers.model, self._notify
        )
        self._connect()
        layout = QVBoxLayout(self)
        for widget in (self.status, self.stores, self.departments, self.sellers):
            layout.addWidget(widget)
        self.store_presenter.load()

    def _connect(self) -> None:
        self.stores.search.search_changed.connect(self.store_presenter.load)
        self.departments.search.search_changed.connect(
            lambda text: self.department_presenter.load(self.state.selection.store_id, text)
        )
        self.sellers.search.search_changed.connect(self._load_sellers)
        self.stores.sort_changed.connect(
            lambda sort_by, descending: self.store_presenter.load(
                self.stores.search.text(), sort_by, descending
            )
        )
        self.departments.sort_changed.connect(
            lambda sort_by, descending: self.department_presenter.load(
                self.state.selection.store_id, self.departments.search.text(), sort_by, descending
            )
        )
        self.sellers.sort_changed.connect(
            lambda sort_by, descending: self._load_sellers(
                self.sellers.search.text(), sort_by, descending
            )
        )
        self.stores.selected.connect(self._store_selected)
        self.departments.selected.connect(self._department_selected)
        self.sellers.all_store_sellers.clicked.connect(self._all_sellers)
        self.stores.table_actions.add_clicked.connect(self._add_store)
        self.stores.table_actions.edit_clicked.connect(self._edit_store)
        self.stores.table_actions.delete_clicked.connect(self._delete_store)
        self.departments.table_actions.add_clicked.connect(self._add_department)
        self.departments.table_actions.edit_clicked.connect(self._edit_department)
        self.departments.table_actions.delete_clicked.connect(self._delete_department)
        self.sellers.table_actions.add_clicked.connect(self._add_seller)
        self.sellers.table_actions.edit_clicked.connect(self._edit_seller)
        self.sellers.table_actions.delete_clicked.connect(self._delete_seller)

    def _controller_event(self, event) -> None:
        self.store_presenter.handle(event)
        self.department_presenter.handle(event)
        self.seller_presenter.handle(event)
        if hasattr(event, "resource"):
            items = list(event.items)
            setattr(self.state, event.resource, items)
            if event.resource == "stores":
                self._load_children()
        if isinstance(event, Failed):
            self._notify(event.message, True)

    def _notify(self, text: str, error: bool = False) -> None:
        (QMessageBox.critical if error else QMessageBox.information)(
            self, "Error" if error else "Information", text
        )

    def _store_selected(self, item: Any) -> None:
        if item:
            self.state.selection.select_store(item.id)
            self.status.setText(f"Selected store: {item.name}")
            self._load_children()

    def _department_selected(self, item: Any) -> None:
        if item:
            self.state.selection.select_department(item.id)
            self.status.setText(f"Selected department: {item.name}")
            self._load_sellers()

    def _load_children(self) -> None:
        selection = self.state.selection
        self.department_presenter.load(selection.store_id, self.departments.search.text())
        self._load_sellers()

    def _load_sellers(
        self, search: str = "", sort_by: str = "last_name", descending: bool = False
    ) -> None:
        selection = self.state.selection
        self.seller_presenter.load(
            selection.store_id,
            selection.department_id if selection.seller_scope == "department" else None,
            search or self.sellers.search.text(),
            sort_by,
            descending,
        )

    def _all_sellers(self) -> None:
        self.state.selection.show_all_sellers()
        self._load_sellers()

    def _selected(self, panel) -> Any:
        rows = panel.table.selectionModel().selectedRows()
        return panel.model.item_at(rows[0].row()) if rows else None

    def _add_store(self) -> None:
        dialog = StoreDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            values = dialog.values()
            payload = StoreCreate(
                name=str(values["name"]),
                address=AddressModel(
                    city=str(values["city"]),
                    street=str(values["street"]),
                    building=str(values["building"]),
                ),
                contact_phone=str(values["contact_phone"]),
                is_active=bool(values["is_active"]),
            )
            self.store_presenter.create(payload.model_dump())

    def _edit_store(self) -> None:
        item = self._selected(self.stores)
        if item:
            dialog = StoreDialog(item, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                values = dialog.values()
                payload = StoreUpdate(
                    name=str(values["name"]),
                    address=AddressModel(
                        city=str(values["city"]),
                        street=str(values["street"]),
                        building=str(values["building"]),
                    ),
                    contact_phone=str(values["contact_phone"]),
                    is_active=bool(values["is_active"]),
                )
                self.store_presenter.update(item.id, payload.model_dump(exclude_none=True))

    def _delete_store(self) -> None:
        item = self._selected(self.stores)
        if item and ConfirmationDialog.ask(self, "store"):
            self.store_presenter.delete(item.id)

    def _add_department(self) -> None:
        store_id = self.state.selection.store_id
        if not store_id:
            self._notify("Select a store first.", True)
            return
        dialog = DepartmentDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            values = dialog.values()
            payload = DepartmentCreate(
                name=str(values["name"]),
                floor=int(str(values["floor"])),
                description=str(values["description"]),
            )
            self.department_presenter.create(store_id, payload.model_dump())

    def _edit_department(self) -> None:
        item, store_id = self._selected(self.departments), self.state.selection.store_id
        if item and store_id:
            dialog = DepartmentDialog(item, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                values = dialog.values()
                payload = DepartmentUpdate(
                    name=str(values["name"]),
                    floor=int(str(values["floor"])),
                    description=str(values["description"]),
                )
                self.department_presenter.update(
                    store_id, item.id, payload.model_dump(exclude_none=True)
                )

    def _delete_department(self) -> None:
        item, store_id = self._selected(self.departments), self.state.selection.store_id
        if item and store_id and ConfirmationDialog.ask(self, "department"):
            self.department_presenter.delete(store_id, item.id)

    def _add_seller(self) -> None:
        if not self.state.selection.store_id:
            self._notify("Select a store first.", True)
            return
        dialog = SellerDialog(self.state.stores, self.state.departments, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            values = dialog.values()
            payload = SellerCreate(
                first_name=str(values["first_name"]),
                last_name=str(values["last_name"]),
                age=int(str(values["age"])),
                phone=str(values["phone"]),
                email=str(values["email"]),
                position=str(values["position"]),
                salary=float(str(values["salary"])),
                store_id=str(values["store_id"]),
                department_id=str(values["department_id"]),
            )
            self.seller_presenter.create(payload.model_dump())

    def _edit_seller(self) -> None:
        item = self._selected(self.sellers)
        if item:
            dialog = SellerDialog(self.state.stores, self.state.departments, item, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                values = dialog.values()
                payload = SellerUpdate(
                    first_name=str(values["first_name"]),
                    last_name=str(values["last_name"]),
                    age=int(str(values["age"])),
                    phone=str(values["phone"]),
                    email=str(values["email"]),
                    position=str(values["position"]),
                    salary=float(str(values["salary"])),
                    store_id=str(values["store_id"]),
                    department_id=str(values["department_id"]),
                )
                self.seller_presenter.update(item.id, payload.model_dump(exclude_none=True))

    def _delete_seller(self) -> None:
        item = self._selected(self.sellers)
        if item and ConfirmationDialog.ask(self, "seller"):
            self.seller_presenter.delete(item.id)

    def close_database(self) -> None:
        self.container.close()
