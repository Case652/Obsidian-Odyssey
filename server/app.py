#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, session
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from models import User, Character,Deck,Card,CardType,MobDeck,Mob,Fight,InFightMobDeck
from seed import starter_deck
from random import randint
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
            all_mobs = Mob.query.all()
            random_index = randint(0,len(all_mobs) - 1)
            random_mob = all_mobs[random_index]
            new_fight = Fight(character=character)
            new_fight.mob_name = random_mob.mob_name
            new_fight.level = random_mob.level
            new_fight.hitpoints = random_mob.hitpoints
            new_fight.max_hitpoints = random_mob.max_hitpoints
            new_fight.mana = random_mob.mana
            new_fight.max_mana = random_mob.max_mana
            new_fight.draw = random_mob.draw
            new_fight.block = random_mob.block
            db.session.add(new_fight)
            db.session.commit()
            mob_decks = MobDeck.query.filter_by(mob=random_mob).all()
            for mob_deck in mob_decks:
                new_mob_deck = InFightMobDeck(status='Undrawn', fight=new_fight, card_id=mob_deck.card_id)
                db.session.add(new_mob_deck)
                db.session.commit()
            new_fight.draw_hand()
            character.draw_hand()
            db.session.commit()
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

class PlayCardById(Resource):
    def get(self,id):
        character_id = session.get('character_id')
        deck = Deck.query.filter_by(card_id=id, character_id=character_id, status='Drawn').first()
        if deck:
            card = deck.card
            character = Character.query.filter_by(id=character_id).first()
            ongoing_fight = Fight.query.filter_by(character_id=character.id, status='Ongoing').first()
            if ongoing_fight:
                if character.mana >= card.mana_cost and character.hitpoints > card.hp_cost:
                    character.mana -= card.mana_cost
                    character.hitpoints -= card.hp_cost
                    max_hitpoints = character.max_hitpoints
                    character.hitpoints = min(character.hitpoints + card.heal, max_hitpoints)
                    max_mana = character.max_mana
                    character.mana = min(character.mana + card.mana_gain, max_mana)
                    character.block += card.block

                    mob_damage = card.damage
                    if ongoing_fight.block > 0:
                        block_damage = min(ongoing_fight.block, mob_damage)
                        ongoing_fight.block -= block_damage
                        mob_damage -= block_damage
                    if mob_damage > 0:
                        ongoing_fight.hitpoints -= mob_damage
                        if ongoing_fight.hitpoints <= 0:
                            ongoing_fight.status = 'Victory'
                            character.shuffle_deck_all()
                            # finish fight somehow
                            pass
                    deck.status = 'Discarded'
                    db.session.commit()
                    return make_response(ongoing_fight.to_dict(rules={'-character.user',}), 200)
                else:
                    return make_response({"error": "Not enough mana or hitpoints to play this card"}, 400)
            else:
                return make_response({"error": "No onGoing fight"},418)
        else:
            return make_response({"error":"Character does not have this Drawn"},404)
api.add_resource(PlayCardById,'/api/v1/PlayCard/<id>')

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