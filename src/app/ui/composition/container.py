from app.config import Settings
from app.database import Database
from app.modules.seller.controllers import SellerController
from app.modules.seller.repositories import SellerRepository
from app.modules.seller.services import SellerService
from app.modules.store.controllers import DepartmentController, StoreController
from app.modules.store.repositories import DepartmentRepository, StoreRepository
from app.modules.store.services import DepartmentService, StoreService


class UiContainer:
    def __init__(self, notify) -> None:
        database = Database(Settings().mongo_uri, Settings().mongo_database)
        stores = StoreRepository(database.database["stores"])
        sellers = SellerRepository(database.database["sellers"])
        departments = DepartmentRepository(database.database["stores"])
        self.database = database
        self.store_controller = StoreController(StoreService(stores, sellers), notify)
        self.department_controller = DepartmentController(
            DepartmentService(departments, stores, sellers), notify
        )
        self.seller_controller = SellerController(SellerService(sellers, stores), notify)

    def close(self) -> None:
        self.database.close()
