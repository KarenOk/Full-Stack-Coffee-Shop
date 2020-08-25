import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
Uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES
'''
    GET /drinks
        - public endpoint
        - contains only the drink.short() data representation
        - returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks")
def get_drinks():
    drinks = Drink.query.all()
    return jsonify({
        "success": True,
        "drinks": [drink.short() for drink in drinks]
    })


'''
    GET /drinks-detail
        - requires the 'get:drinks-detail' permission
        - contains the drink.long() data representation
        - returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks-detail")
@requires_auth("get:drinks-detail")
def get_drinks_details(payload):
    drinks = Drink.query.all()
    return jsonify({
        "success": True,
        "drinks": [drink.long() for drink in drinks]
    })


'''
@TODO implement endpoint
    POST /drinks
        - create a new row in the drinks table
        - requires the 'post:drinks' permission
        - contains the drink.long() data representation
        - returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def create_drink(payload):
    body = request.get_json()
    title = body.get("title", None)
    recipe = body.get("recipe", None)

    if not title or not recipe:
        abort(400)

    for item in recipe:
        color = item.get("color", None)
        parts = item.get("parts", None)
        name = item.get("name", None)
        if not color or not parts or not name:
            abort(400)

    drink = Drink.query.filter_by(title=title).first()
    if drink:
        abort(409)

    drink = Drink(title=title, recipe=json.dumps(recipe))
    drink.insert()

    return jsonify({"success": True, "drinks": [drink.long()]})


'''
    PATCH /drinks/<id>
        where <id> is the existing model id
        - responds with a 404 error if <id> is not found
        - updates the corresponding row for <id>
        - requires the 'patch:drinks' permission
        - contains the drink.long() data representation
        - sreturns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks/<id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def update_drink(payload, id):
    drink = Drink.query.get(id)

    if not drink:
        abort(404)

    body = request.get_json()
    title = body.get("title", None)
    recipe = body.get("recipe", None)

    if title:
        drink.title = title

    if recipe:
        for item in recipe:
            color = item.get("color", None)
            parts = item.get("parts", None)
            name = item.get("name", None)
            if not color or not parts or not name:
                abort(400)

        drink.recipe = json.dumps(recipe)

    try:
        drink.update()
    except:
        db.session.rollback()
        abort(500)

    return jsonify({
        "success": True,
        "drinks": [drink.long()]
    })


'''
    DELETE /drinks/<id>
        where <id> is the existing model id
        - responds with a 404 error if <id> is not found
        - deletes the corresponding row for <id>
        - requires the 'delete:drinks' permission
        - returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks/<id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drink(payload, id):
    drink = Drink.query.get(id)

    if not drink:
        abort(404)

    try:
        drink.delete()
    except:
        db.session.rollback()
        abort(500)

    return jsonify({"success": True, "delete": id})


# Error Handling


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request."
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found."
    })


@app.errorhandler(409)
def conflict(error):
    return jsonify({
        "success": False,
        "error": 409,
        "message": "A conflict was found."
    }), 409


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable."
    }), 422


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error."
    }), 500


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error["description"]
    }), error.status_code
