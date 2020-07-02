from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flaskr.models import setup_db, User


def paginate_users(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 3
    end = start + 3

    users = [user.format() for user in selection]
    current_users = users[start:end]

    return current_users


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
        users = User.query.order_by(User.id).all()
        current_users = paginate_users(request, users)

        if len(current_users) == 0:
            abort(404)

        try:
            return jsonify({
                'success': True,
                'users': current_users,
                'total_users': len(User.query.all())
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

    @app.route('/users/<int:user_id>', methods=['PATCH'])
    def update_user(user_id):
        body = request.get_json()

        try:
            user = User.query.filter(User.id == user_id).one_or_none()
            if user is None:
                abort(404)

            if 'name' in body:
                user.name = str(body.get('name'))
            else:
                abort(400)

            user.update()

            return jsonify({
                'success': True,
            })

        except:
            abort(400)

    @app.route('/users', methods=['POST'])
    def create_user():
        body = request.get_json()

        name = body.get('name', None)
        email = body.get('email', None)

        try:
            user = User(name=name, email=email)
            user.insert()

            users = User.query.order_by(User.id).all()
            current_users = paginate_users(request, users)

            return jsonify({
                'success': True,
                'created': user.id,
                'users': current_users,
                'total_users': len(User.query.all())
            })

        except:
            abort(422)

    @app.route('/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        try:
            user = User.query.filter(User.id == user_id).one_or_none()

            if user is None:
                abort(404)

            user.delete()

            users = User.query.order_by(User.id).all()
            current_users = paginate_users(request, users)

            return jsonify({
                'success': True,
                'deleted': user_id,
                'users': current_users,
                'total_users': len(User.query.all())
            })

        except:
            abort(422)

    @app.route('/users/search', methods=['POST'])
    def search_user():
        try:
            body = request.get_json()
            name = str(body.get('name'))

            users = User.query.filter(User.name.ilike(
                '%{}%'.format(name))).all()

            if users is None:
                abort(404)

            current_users = paginate_users(request, users)

            return jsonify({
                'success': True,
                'users': current_users,
                'total_users': len(users)
            })
        except:
            abort(422)

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
