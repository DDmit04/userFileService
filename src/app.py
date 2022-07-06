from AppFactory import setup_app
from dependency.DependencyContainer import di_container

app = di_container.app
di_container.file_sync_service.sync_storage_data()
app = setup_app(app)
