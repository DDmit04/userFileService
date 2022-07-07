from app_factory import setup_app
from dependency.dependency_container import di_container


file_sync_service = di_container.get_file_sync_service("")
file_sync_service.sync_storage_data()
file_sync_service.clean_up_tmp_dir()
di_container.close_database_session("")

app = di_container.get_flask_app()
app = setup_app(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
