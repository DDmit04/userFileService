import AppFactory
from src.dependency.DependencyContainer import di_container


if __name__ == '__main__':
    app = di_container.app
    di_container.file_sync_service.sync_storage_data()
    app = AppFactory.setup_app(app)
    app.run()
