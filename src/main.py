from app_factory import setup_app
from dependency.dependency_container import di_container


app = di_container.get_flask_app()
app = setup_app(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
