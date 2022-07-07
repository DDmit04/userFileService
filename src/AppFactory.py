from flask import jsonify, make_response, Flask
from jsonschema.exceptions import ValidationError

from controller.FileController import file_controller_blueprint
from controller.FileEditController import file_edit_controller_blueprint
from controller.FileRecordController import file_record_controller_blueprint


def setup_app(app: Flask) -> Flask:

    app.register_blueprint(file_controller_blueprint,
                           url_prefix='/file')
    app.register_blueprint(file_record_controller_blueprint,
                           url_prefix='/file/info')
    app.register_blueprint(file_edit_controller_blueprint,
                           url_prefix='/file/edit')

    @app.errorhandler(400)
    def bad_request(error):
        if isinstance(error.description, ValidationError):
            original_error = error.description
            return make_response(jsonify({'error': original_error.message}), 400)
        return error
    return app
