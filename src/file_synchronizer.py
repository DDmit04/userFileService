from dependency.dependency_container import di_container


def sync_file_storage():
    file_sync_service = di_container.get_file_sync_service("")
    file_sync_service.sync_storage_data()
    file_sync_service.clean_up_tmp_dir()
    di_container.close_database_session("")


sync_file_storage()
