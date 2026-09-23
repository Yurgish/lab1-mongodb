import tkinter as tk

from app.config import Settings
from app.database import Database
from app.modules.seller.controllers import SellerController
from app.modules.seller.repositories import SellerRepository
from app.modules.seller.services import SellerService
from app.modules.store.controllers import DepartmentController, StoreController
from app.modules.store.repositories import DepartmentRepository, StoreRepository
from app.modules.store.services import DepartmentService, StoreService
from app.ui.main_window import MainWindow


def main() -> None:
    settings = Settings()

    database = Database(uri=settings.mongo_uri, database_name=settings.mongo_database)

    try:
        database.connect()
        database.create_indexes()
        store_repository = StoreRepository(database.database["stores"])
        seller_repository = SellerRepository(database.database["sellers"])
        department_repository = DepartmentRepository(database.database["stores"])
        store_service = StoreService(store_repository, seller_repository)
        seller_service = SellerService(seller_repository, store_repository)
        department_service = DepartmentService(
            department_repository, store_repository, seller_repository
        )
        root = tk.Tk()
        view = MainWindow(root)
        view.set_controllers(
            StoreController(view, store_service),
            DepartmentController(view, department_service),
            SellerController(view, seller_service),
        )
        view.run()
    finally:
        database.close()


if __name__ == "__main__":
    main()
