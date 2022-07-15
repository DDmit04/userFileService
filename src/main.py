from flask_jwt_extended import JWTManager

from app_factory import setup_app
from dependency.dependency_container import di_container
from test_runner import run_tests

config = di_container.get_config()
if config['ENV'] == "PROD":
    run_tests()

app = di_container.get_flask_app()
jwt = JWTManager(app)
app = setup_app(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
