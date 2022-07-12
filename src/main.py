from botocore.exceptions import ClientError

from app_factory import setup_app
from dependency.dependency_container import di_container

sync_service = di_container.get_file_sync_service("")
sync_service.sync_storage_data()
di_container.close_database_session("")

app = di_container.get_flask_app()
app = setup_app(app)


def bucket_exists(client, bucket_name):
    try:
        client.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            return False
        else:
            raise e
    return True


boto_client = di_container.get_boto_client()
config = di_container.get_config()
default_bucket_name = config['DEFAULT_BUCKET_NAME']
if not bucket_exists(boto_client, default_bucket_name):
    boto_client.create_bucket(Bucket=default_bucket_name)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
