from AppFactory import setup_app
from dependency.DependencyContainer import di_container

app = di_container.app
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
di_container.file_sync_service.sync_storage_data()
app = setup_app(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
