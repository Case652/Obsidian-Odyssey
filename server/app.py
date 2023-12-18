#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, session
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from models import User, Character,Deck,Card,CardType,MobDeck,Mob,Fight
from seed import starter_deck

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
    def get(self):
        all_users = [u.to_dict() for u in User.query.all()]
        return make_response(all_users)
api.add_resource(Users,'/api/v1/users')

class Characters(Resource):
    def get(self):
        all_characters = [c.to_dict(rules={
            #general rules
            '-user',
            #deck rules
            '-decks.card_id',
            '-decks.character_id',
            #card rules
            # "-decks.card.created_at",
            # "-decks.card.updated_at",
            }) for c in Character.query.all()]
        return make_response(all_characters)

    def post(self):
        data = request.get_json()
        user_id = session.get('user_id')
        if not user_id:
            return make_response({'error': 'User not logged in'}, 401)

        character = Character(character_name=data['character_name'],user_id=user_id)
        db.session.add(character)
        db.session.commit()

        for card_info in starter_deck:
            card_name = card_info["card_name"]
            card = Card.query.filter_by(card_name=card_name).first()
            if card:
                deck = Deck(character_id=character.id, card_id=card.id)
                db.session.add(deck)
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

    def delete(self,id):
        if 'user_id' not in session:
            return make_response({'error': 'User not logged in'}, 401)
        character = Character.query.get(id)
        if not character:
            return make_response({"error":"Character not found"},404)
        if character.user_id != session['user_id']:
            return make_response({"error": "Unauthorized to delete this character"}, 403)
        db.session.delete(character)
        db.session.commit()
        session['character_id'] = None
        return make_response("Can't see me",204)

api.add_resource(CharacterById,'/api/v1/character/<id>')
class CharacterFightById(Resource):
    def get(self,id):
        character = Character.query.get(id)
        if not character:
            return make_response({"error": "No character found"}, 404)
        ongoing_fight = Fight.query.filter_by(character_id=character.id, status='Ongoing').first()
    # def post
        if not ongoing_fight:
            new_fight = Fight(character=character)

            
            db.session.add(new_fight)
            db.session.commit()
            character.draw_hand()
            return make_response(new_fight.to_dict(rules={'-character.user'}), 201)
        else:
            return make_response(ongoing_fight.to_dict(rules={'-character.user',}), 200)

api.add_resource(CharacterFightById,'/api/v1/fight/<id>')

class Fights(Resource):
    def get(self):
        all_fights = [f.to_dict(rules={
            #general rules
            '-character.user',
            }) for f in Fight.query.all()]
        return make_response(all_fights)
api.add_resource(Fights,'/api/v1/fight')
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
@app.route('/api/v1/changeChar',methods=['POST'])
def changeChar():
    data = request.get_json()
    try:
        user = User.query.filter_by(id=session.get('user_id')).first()
        if not user:
            return make_response({'error': 'User not found'}, 404)
        character_id = data.get('character_id')
        character = Character.query.filter_by(id=character_id, user_id=user.id).first()
        if character:
            session['character_id'] = character.id
            return make_response({'message':'Changed character successfully'},200)
        else:
            return make_response({'error': 'Character not found for the user'}, 404)
    except:
        return make_response({'error':'Something went wrong'},500)

@app.route('/api/v1/authorized')
def authorized():
    try:
        user = User.query.filter_by(id=session.get('user_id')).first()
        return make_response(user.to_dict(),200)
    except:
        return make_response({'error':'User not Found'},404)
@app.route('/api/v1/authCharacter')
def authCharacter():
    try:
        user = User.query.filter_by(id=session.get('user_id')).first()
        if user:
            character = Character.query.filter_by(id=session.get('character_id'), user_id=user.id).first()
            if character:
                return make_response(character.to_dict(rules={'-user'}), 200)
            else:
                return make_response({'error': 'Character not Found'}, 404)
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