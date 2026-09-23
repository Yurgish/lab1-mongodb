from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import messagebox, ttk
from typing import Any

from app.common.query import QueryOptions


class MainWindow:
    """Single-screen view for stores, departments and sellers."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Store management")
        self.root.minsize(1200, 800)
        self.store_controller: Any = None
        self.department_controller: Any = None
        self.seller_controller: Any = None
        self.stores: list[Any] = []
        self.departments: list[Any] = []
        self.sellers: list[Any] = []
        self._loading = False
        self.store_tree: ttk.Treeview
        self.department_tree: ttk.Treeview
        self.seller_tree: ttk.Treeview
        self.search_vars: dict[str, tk.StringVar] = {}
        self._sort_fields = {"stores": "name", "departments": "name", "sellers": "last_name"}
        self._descending = {"stores": False, "departments": False, "sellers": False}
        self._heading_titles: dict[str, dict[str, str]] = {}
        self._build()

    def set_controllers(
        self, store_controller: Any, department_controller: Any, seller_controller: Any
    ) -> None:
        self.store_controller = store_controller
        self.department_controller = department_controller
        self.seller_controller = seller_controller

    def run(self) -> None:
        self._load_stores()
        self.root.mainloop()

    def show_error(self, title: str, message: str) -> None:
        messagebox.showerror(title, message, parent=self.root)

    def show_success(self, message: str) -> None:
        messagebox.showinfo("Success", message, parent=self.root)
        self._reload_selected()

    def show_stores(self, stores: list[Any]) -> None:
        selected_id = self._selected_id(self.store_tree)
        self.stores = stores
        self._loading = True
        try:
            self._fill(
                self.store_tree,
                stores,
                lambda item: (
                    item.name,
                    item.address.city,
                    item.address.street,
                    item.contact_phone,
                    "Yes" if item.is_active else "No",
                    item.departments_count,
                    item.created_at.strftime("%Y-%m-%d %H:%M"),
                    item.updated_at.strftime("%Y-%m-%d %H:%M"),
                ),
            )
            self._select_id_or_first(self.store_tree, selected_id)
        finally:
            self._loading = False
        self._load_departments()

    def show_departments(self, departments: list[Any]) -> None:
        selected_id = self._selected_id(self.department_tree)
        self.departments = departments
        self._loading = True
        try:
            self._fill(
                self.department_tree,
                departments,
                lambda item: (
                    item.name,
                    item.floor,
                    item.sellers_count,
                    item.description,
                    item.created_at.strftime("%Y-%m-%d %H:%M"),
                    item.updated_at.strftime("%Y-%m-%d %H:%M"),
                ),
            )
            self._select_id(self.department_tree, selected_id)
        finally:
            self._loading = False
        self._load_sellers()

    def show_sellers(self, sellers: list[Any]) -> None:
        self.sellers = sellers
        self._fill(
            self.seller_tree,
            sellers,
            lambda item: (
                item.first_name,
                item.last_name,
                item.position,
                item.salary,
                item.email,
                item.created_at.strftime("%Y-%m-%d %H:%M"),
                item.updated_at.strftime("%Y-%m-%d %H:%M"),
            ),
        )

    def _build(self) -> None:
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill="x", padx=8, pady=8)
        ttk.Button(toolbar, text="Refresh", command=self._load_stores).pack(side="left")

        content = ttk.PanedWindow(self.root, orient="vertical")
        content.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        stores = ttk.LabelFrame(content, text="Stores")
        departments = ttk.LabelFrame(content, text="Departments of selected store")
        sellers = ttk.LabelFrame(content, text="Sellers of selected store/department")
        content.add(stores, weight=1)
        content.add(departments, weight=1)
        content.add(sellers, weight=1)
        self._build_table(
            stores,
            "stores",
            [
                ("name", "Name", 170),
                ("city", "City", 110),
                ("street", "Street", 130),
                ("phone", "Phone", 125),
                ("is_active", "Active", 70),
                ("departments", "Departments", 100),
                ("created_at", "Created at", 145),
                ("updated_at", "Updated at", 145),
            ],
            self._store_form,
            self._edit_store,
            self._delete_store,
        )
        self._build_table(
            departments,
            "departments",
            [
                ("name", "Name", 170),
                ("floor", "Floor", 60),
                ("sellers", "Sellers", 70),
                ("description", "Description", 300),
                ("created_at", "Created at", 145),
                ("updated_at", "Updated at", 145),
            ],
            self._department_form,
            self._edit_department,
            self._delete_department,
        )
        self._build_table(
            sellers,
            "sellers",
            [
                ("first_name", "First name", 110),
                ("last_name", "Last name", 110),
                ("position", "Position", 130),
                ("salary", "Salary", 90),
                ("email", "Email", 200),
                ("created_at", "Created at", 145),
                ("updated_at", "Updated at", 145),
            ],
            self._seller_form,
            self._edit_seller,
            self._delete_seller,
        )
        self.store_tree.bind(
            "<<TreeviewSelect>>", lambda _: None if self._loading else self._load_departments()
        )
        self.department_tree.bind(
            "<<TreeviewSelect>>", lambda _: None if self._loading else self._load_sellers()
        )

    def _build_table(
        self,
        parent: ttk.LabelFrame,
        key: str,
        columns: list[tuple[str, str, int]],
        add: Callable[[], None],
        edit: Callable[[], None],
        delete: Callable[[], None],
    ) -> None:
        buttons = ttk.Frame(parent)
        buttons.pack(fill="x", pady=4)
        ttk.Button(buttons, text="Add", command=add).pack(side="left")
        ttk.Button(buttons, text="Edit", command=edit).pack(side="left", padx=4)
        ttk.Button(buttons, text="Delete", command=delete).pack(side="left")
        if key == "departments":
            ttk.Button(
                buttons, text="All sellers in store", command=self._show_all_store_sellers
            ).pack(side="left", padx=12)
        search_var = tk.StringVar()
        self.search_vars[key] = search_var
        ttk.Label(buttons, text="Search:").pack(side="left", padx=(20, 4))
        search = ttk.Entry(buttons, textvariable=search_var, width=24)
        search.pack(side="left")
        search.bind("<Return>", lambda _, group=key: self._reload_group(group))
        ttk.Button(
            buttons, text="Search", command=lambda group=key: self._reload_group(group)
        ).pack(side="left", padx=4)
        tree = ttk.Treeview(parent, columns=[item[0] for item in columns], show="headings")
        self._heading_titles[key] = {name: title for name, title, _ in columns}
        for name, title, width in columns:
            tree.heading(
                name, text=title, command=lambda field=name, group=key: self._sort(group, field)
            )
            tree.column(name, width=width, anchor="w")
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        setattr(self, f"{key[:-1] if key.endswith('s') else key}_tree", tree)

    def _sort(self, group: str, field: str) -> None:
        if self._sort_fields[group] == field:
            self._descending[group] = not self._descending[group]
        else:
            self._sort_fields[group] = field
            self._descending[group] = False
        self._update_heading_indicators(group)
        self._reload_group(group)

    def _update_heading_indicators(self, group: str) -> None:
        tree = getattr(self, f"{group[:-1] if group.endswith('s') else group}_tree")
        selected_field = self._sort_fields[group]
        for field, title in self._heading_titles[group].items():
            indicator = " [DESC]" if self._descending[group] else " [ASC]"
            tree.heading(field, text=f"{title}{indicator if field == selected_field else ''}")

    def _options(self, group: str) -> QueryOptions:
        return QueryOptions(
            sort_by=self._sort_fields[group],
            descending=self._descending[group],
            search=self.search_vars[group].get().strip() or None,
        )

    def _load_stores(self) -> None:
        self.store_controller.load(self._options("stores"))

    def _load_departments(self) -> None:
        store = self._selected(self.store_tree, self.stores)
        self._clear(self.department_tree)
        self._clear(self.seller_tree)
        self.departments, self.sellers = [], []
        if store:
            self.department_controller.load(store.id, self._options("departments"))

    def _load_sellers(self) -> None:
        store = self._selected(self.store_tree, self.stores)
        department = self._selected(self.department_tree, self.departments)
        if store:
            self.seller_controller.load(
                store.id, department.id if department else None, self._options("sellers")
            )

    def _reload_selected(self) -> None:
        self._load_stores()

    def _reload_group(self, group: str) -> None:
        if group == "stores":
            self._load_stores()
        elif group == "departments":
            self._load_departments()
        else:
            self._load_sellers()

    def _show_all_store_sellers(self) -> None:
        self._loading = True
        try:
            self.department_tree.selection_remove(self.department_tree.selection())
        finally:
            self._loading = False
        self._load_sellers()

    def _fill(
        self, tree: ttk.Treeview, values: list[Any], row: Callable[[Any], tuple[Any, ...]]
    ) -> None:
        self._clear(tree)
        for value in values:
            tree.insert("", "end", iid=value.id, values=row(value))

    @staticmethod
    def _clear(tree: ttk.Treeview) -> None:
        tree.delete(*tree.get_children())

    @staticmethod
    def _select_first_if_needed(tree: ttk.Treeview) -> None:
        children = tree.get_children()
        if children and not tree.selection():
            tree.selection_set(children[0])

    @staticmethod
    def _selected(tree: ttk.Treeview, values: list[Any]) -> Any | None:
        selection = tree.selection()
        if not selection:
            return None
        item_id = selection[0]
        return next((value for value in values if value.id == item_id), None)

    @staticmethod
    def _selected_id(tree: ttk.Treeview) -> str | None:
        selection = tree.selection()
        return selection[0] if selection else None

    @staticmethod
    def _select_id_or_first(tree: ttk.Treeview, item_id: str | None) -> None:
        children = tree.get_children()
        target = item_id if item_id in children else (children[0] if children else None)
        if target is not None:
            tree.selection_set(target)

    @staticmethod
    def _select_id(tree: ttk.Treeview, item_id: str | None) -> None:
        if item_id is not None and item_id in tree.get_children():
            tree.selection_set(item_id)

    def _form(
        self,
        title: str,
        fields: list[tuple[str, str, Any]],
        submit: Callable[[dict[str, Any]], None],
    ) -> None:
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.transient(self.root)
        dialog.grab_set()
        entries: dict[str, ttk.Entry] = {}
        for index, (name, label, value) in enumerate(fields):
            ttk.Label(dialog, text=f"{label}:").grid(
                row=index, column=0, sticky="w", padx=8, pady=4
            )
            entry = ttk.Entry(dialog, width=40)
            entry.insert(0, str(value))
            entry.grid(row=index, column=1, padx=8, pady=4)
            entries[name] = entry
        ttk.Button(
            dialog,
            text="Save",
            command=lambda: (
                submit({name: entry.get() for name, entry in entries.items()}),
                dialog.destroy(),
            ),
        ).grid(row=len(fields), columnspan=2, pady=8)

    def _store_form(self, store: Any | None = None) -> None:
        address = getattr(store, "address", None)
        fields = [
            ("name", "Name", getattr(store, "name", "")),
            ("city", "City", getattr(address, "city", "")),
            ("street", "Street", getattr(address, "street", "")),
            ("building", "Building", getattr(address, "building", "")),
            ("contact_phone", "Phone", getattr(store, "contact_phone", "")),
            ("is_active", "Active (yes/no)", "yes" if not store or store.is_active else "no"),
        ]

        def submit(data: dict[str, Any]) -> None:
            data["is_active"] = str(data["is_active"]).lower() in {"yes", "true", "1"}
            data["address"] = {key: data.pop(key) for key in ("city", "street", "building")}
            (
                self.store_controller.update(store.id, data)
                if store
                else self.store_controller.create(data)
            )

        self._form("Edit store" if store else "Add store", fields, submit)

    def _edit_store(self) -> None:
        store = self._selected(self.store_tree, self.stores)
        if store:
            self._store_form(store)

    def _delete_store(self) -> None:
        store = self._selected(self.store_tree, self.stores)
        if store and messagebox.askyesno(
            "Confirm", "Delete store and related sellers?", parent=self.root
        ):
            self.store_controller.delete(store.id)

    def _department_form(self, department: Any | None = None) -> None:
        store = self._selected(self.store_tree, self.stores)
        if not store:
            return self.show_error("Selection required", "Select a store first.")
        fields = [
            ("name", "Name", getattr(department, "name", "")),
            ("floor", "Floor", getattr(department, "floor", "")),
            ("description", "Description", getattr(department, "description", "")),
        ]

        def submit(data: dict[str, Any]) -> None:
            data["floor"] = int(data["floor"])
            (
                self.department_controller.update(store.id, department.id, data)
                if department
                else self.department_controller.create(store.id, data)
            )

        self._form("Edit department" if department else "Add department", fields, submit)

    def _edit_department(self) -> None:
        department = self._selected(self.department_tree, self.departments)
        if department:
            self._department_form(department)

    def _delete_department(self) -> None:
        store = self._selected(self.store_tree, self.stores)
        department = self._selected(self.department_tree, self.departments)
        if (
            store
            and department
            and messagebox.askyesno(
                "Confirm", "Delete department and related sellers?", parent=self.root
            )
        ):
            self.department_controller.delete(store.id, department.id)

    def _seller_form(self, seller: Any | None = None) -> None:
        store = self._selected(self.store_tree, self.stores)
        if not store or not self.departments:
            return self.show_error(
                "Selection required", "Select a store with at least one department."
            )
        department = self._selected(self.department_tree, self.departments) or self.departments[0]
        fields = [
            ("first_name", "First name", getattr(seller, "first_name", "")),
            ("last_name", "Last name", getattr(seller, "last_name", "")),
            ("age", "Age", getattr(seller, "age", "")),
            ("phone", "Phone", getattr(seller, "phone", "")),
            ("email", "Email", getattr(seller, "email", "")),
            ("position", "Position", getattr(seller, "position", "")),
            ("salary", "Salary", getattr(seller, "salary", "")),
        ]

        def submit(data: dict[str, Any]) -> None:
            data["age"], data["salary"] = int(data["age"]), float(data["salary"])
            data["store_id"] = store.id
            data["department_id"] = getattr(seller, "department_id", department.id)
            (
                self.seller_controller.update(seller.id, data)
                if seller
                else self.seller_controller.create(data)
            )

        self._form("Edit seller" if seller else "Add seller", fields, submit)

    def _edit_seller(self) -> None:
        seller = self._selected(self.seller_tree, self.sellers)
        if seller:
            self._seller_form(seller)

    def _delete_seller(self) -> None:
        seller = self._selected(self.seller_tree, self.sellers)
        if seller and messagebox.askyesno("Confirm", "Delete seller?", parent=self.root):
            self.seller_controller.delete(seller.id)
