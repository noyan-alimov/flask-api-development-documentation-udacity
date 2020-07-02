from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flaskr.models import setup_db, User


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/users')
    def get_users():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 3
        end = start + 3
        users = User.query.all()
        formatted_users = [user.format() for user in users]

        if formatted_users[start:end] == []:
            abort(404)

        try:
            return jsonify({
                'success': True,
                'users': formatted_users[start:end],
                'total_users': len(formatted_users)
            })
        except:
            abort(400)

    @app.route('/users/<int:user_id>')
    def get_specific_user(user_id):
        user = User.query.filter(User.id == user_id).one_or_none()

        if user is None:
            abort(404)

        else:
            return jsonify({
                'success': True,
                'user': user.format()
            })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    return app
