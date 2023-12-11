#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, session
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from models import User, Character

# Views go here!
class Users(Resource):
    def post(self):
        data = request.get_json()
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            error_message = f"'{data['username']}' thats it? thats the best you got? someone already is named that, maybe be more..."
            return make_response({'error': error_message}, 418)
        user = User(username=data['username'],password_hash=data['password'])
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return make_response({'user':user.to_dict()},201)

api.add_resource(Users,'/api/v1/users')

class Characters(Resource):
    def get(self):
        all_characters = [c.to_dict(rules={'-user',}) for c in Character.query.all()]
        return make_response(all_characters)

    def post(self):
        data = request.get_json()
        user_id = session.get('user_id')
        if not user_id:
            return make_response({'error': 'User not logged in'}, 401)
        character = Character(character_name=data['character_name'],user_id=user_id)
        db.session.add(character)
        db.session.commit()
        session['character_id'] = character.id
        return make_response(character.to_dict(rules={'-user',}),201)

api.add_resource(Characters,'/api/v1/character')

class CharacterById(Resource):
    def get(self,id):
        character = Character.query.get(id)
        if not character:
            return make_response({"error":"Character not found"},404)
        return make_response(character.to_dict(rules={'-user',}),200)

api.add_resource(CharacterById,'/api/v1/character/<id>')

@app.route('/api/v1/login',methods=['POST'])

def login():
    data = request.get_json()
    try:
        user = User.query.filter_by(username=data['username']).first()
        if user:
            if user.authenticate(data['password']):
                session['user_id'] = user.id
                return make_response({'user':user.to_dict()},200)
            else:
                return make_response({'error':'password mismatch'},401)
        else:
            return make_response({'error':'Username not found'},401)
    except:
        return make_response({'error':'Somthing went wrong'},500)
@app.route('/api/v1/authorized')
def authorized():
    try:
        user = User.query.filter_by(id=session.get('user_id')).first()
        return make_response(user.to_dict(),200)
    except:
        return make_response({'error':'User not Found'},404)
@app.route('/api/v1/logout',methods=['DELETE'])
def logout():
    session['user_id'] = None
    session['character_id'] = None
    return make_response('',204)
@app.route('/')
def index():
    return '<h1>Project Server</h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)