import AppFactory
from src.dependency.DependencyContainer import injector


if __name__ == '__main__':
    container_app = injector.app
    injector.file_sync_service.refresh_data_before_start()
    app = AppFactory.setup_app(container_app)
    app.run()
