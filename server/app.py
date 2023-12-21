#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, session
from flask_restful import Resource
from sqlalchemy import or_
from random import randint,choice
# Local imports
from config import app, db, api
# Add your model imports
from models import User, Character,Deck,Card,CardType,MobDeck,Mob,Fight,InFightMobDeck,LevelChart
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

        character = Character(character_name=data['character_name'],image=data['image'],user_id=user_id)
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
api.add_resource(Characters,'/api/v1/character',endpoint="character")
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
api.add_resource(CharacterById,'/api/v1/character/<id>',endpoint="characterid")
class CharacterFightById(Resource):
    def get(self,id):
        character = Character.query.get(id)
        if not character:
            return make_response({"error": "No character found"}, 404)
        ongoing_fight = Fight.query.filter_by(character_id=character.id, status='Ongoing').first()
    # def post
        if not ongoing_fight:
            available_mobs = Mob.query.filter(or_(Mob.level == character.level, Mob.level < character.level)).all()
            if not available_mobs:
                return make_response({"error": "No suitable mob found for the character's level"}, 404)
            random_mob = choice(available_mobs)

            new_fight = Fight(character=character)
            
            new_fight.mob_name = random_mob.mob_name
            new_fight.image = random_mob.image
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
api.add_resource(CharacterFightById,'/api/v1/fight/<id>',endpoint="characterfight")
class Flee(Resource):
    def get(self):
        character_id = session.get('character_id')
        character = Character.query.filter_by(id=character_id).first()
        if not character:
            return make_response({"error": "No character found"}, 404)
        ongoing_fight = Fight.query.filter_by(character_id=character.id, status='Ongoing').first()
        if not ongoing_fight:
            return make_response({"error": "No Fight found"}, 408)
        ongoing_fight.status = 'Defeat'
        character.discard_hand()
        db.session.commit()
        return make_response({"Message":"You Ran"},202)
api.add_resource(Flee,'/api/v1/flee',endpoint="flee")
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
        deck = Deck.query.filter_by(card_id=id, character_id=character_id, status='Drawn').first() #small bug where you can play a card thats not drawn if a card you have drawn is the same card. cancels itself out because you techncially have that card drawn. WIP
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
                            character.block = 0
                            victory_gold = ongoing_fight.max_hitpoints * 4
                            victory_experience = ongoing_fight.max_hitpoints
                            character.experience += victory_experience
                            character.gold += victory_gold
                            db.session.commit()
                            if character.experience >= character.experience_cap:
                                character.level += 1
                                character.experience = 0
                                character.skill_point += 1
                                character.mana = character.max_mana
                                character.hitpoints = character.max_hitpoints
                                db.session.commit()
                                next_level = LevelChart.query.filter_by(level=character.level).first()
                                if next_level:
                                    character.experience_cap = next_level.experience_cap
                                    db.session.commit()
                            character.shuffle_deck_all()
                            db.session.commit()
                            return make_response(ongoing_fight.to_dict(rules={'-character.user',}),202)
                            # return make_response({
                            #     "Victory": "You defeated the mob",
                            #     "Gold": victory_gold,
                            #     "Experience": victory_experience,
                            #     "Level": character.level
                            # }, 202)
                    deck.status = 'Discarded'
                    db.session.commit()
                    return make_response(ongoing_fight.to_dict(rules={'-character.user',}), 200)
                else:
                    return make_response({"error": "Not enough mana or hitpoints to play this card"}, 400)
            else:
                return make_response({"error": "No onGoing fight"},418)
        else:
            return make_response({"error":"Character does not have this Drawn"},404)
api.add_resource(PlayCardById,'/api/v1/playcard/<id>',endpoint="playcard")
class EndTurnById(Resource):
    def get(self,id):
        ongoing_fight = Fight.query.filter_by(id=id, status='Ongoing').first()
        if ongoing_fight:
            character = ongoing_fight.character
            drawn_mob_decks = [mob_deck for mob_deck in ongoing_fight.in_fight_mob_decks if mob_deck.status == 'Drawn']
            for mob_deck in drawn_mob_decks:
                card = mob_deck.card
                max_hitpoints = ongoing_fight.max_hitpoints
                ongoing_fight.hitpoints = min(ongoing_fight.hitpoints + card.heal, max_hitpoints)
                max_mana = ongoing_fight.max_mana
                ongoing_fight.mana = min(ongoing_fight.mana + card.mana_gain, max_mana)
                ongoing_fight.block += card.block

                character_damage = card.damage
                if character.block > 0:
                    block_damage = min(character.block, character_damage)
                    character.block -= block_damage
                    character_damage -= block_damage
                if character_damage > 0:
                    character.hitpoints -= character_damage
                    if character.hitpoints <= 0:
                        ongoing_fight.status = 'Defeat'
                        session['character_id'] = None
                        db.session.delete(character)
                        db.session.commit()
                        return make_response({"Defeat": "Character has been Slayn"},418)
                mob_deck.status = 'Discarded'
            character.mana = min(character.mana + int(0.1 * character.max_mana), character.max_mana)
            ongoing_fight.turn += 1
            ongoing_fight.discard_hand()
            character.discard_hand()
            ongoing_fight.draw_hand()
            character.draw_hand()
            db.session.commit()
            return make_response(ongoing_fight.to_dict(rules={'-character.user'}), 200)
        else:
            return make_response({"error": "This is not an ongoing fight"}, 404)
api.add_resource(EndTurnById,'/api/v1/endturn/<id>',endpoint="endturn")
class ShopThree(Resource):
    def get(self):
        character_id = session.get('character_id')
        character = Character.query.filter_by(id=character_id).first()
        if character.gold >= 100:
            min_card_id = 17
            available_cards = (
            db.session.query(Card)
            .filter(Card.id >= min_card_id)
            .order_by(db.func.random())
            .limit(3)
            .all()
        )
            character.gold -= 100
            db.session.commit()
            response_data = {
                'character': character.to_dict(),
                'available_cards': [card.to_dict(rules={'-decks',"-mob_decks",'-updated_at','-created_at'}) for card in available_cards],
            }
            return make_response(response_data, 200)
        else:
            return make_response({"Message": "Not Enough Gold"},402)
api.add_resource(ShopThree,'/api/v1/shop100',endpoint="shopthree")
class ShopNine(Resource):
    def get(self):
        character_id = session.get('character_id')
        character = Character.query.filter_by(id=character_id).first()
        if character.gold >= 300:
            min_card_id = 17
            available_cards = (
            db.session.query(Card)
            .filter(Card.id >= min_card_id)
            .order_by(db.func.random())
            .limit(9)
            .all()
        )
            character.gold -= 300
            db.session.commit()
            response_data = {
                'character': character.to_dict(),
                'available_cards': [card.to_dict(rules={'-decks',"-mob_decks",'-updated_at','-created_at'}) for card in available_cards],
            }
            return make_response(response_data, 200)
        else:
            return make_response({"Message": "Not Enough Gold"},402)
api.add_resource(ShopNine,'/api/v1/shop300',endpoint="shopnine")
class UseSkillPoint(Resource):
    def post(self):
        data = request.get_json()

        if 'action' not in data:
            return make_response({'error': '404 not found action'}, 404)
        character_id = session.get('character_id')
        character = Character.query.filter_by(id=character_id).first()
        if not character:
            return make_response({'error': 'Character not found'}, 404)
        action = data['action']
            
        if action == 'hp':
            if character.skill_point > 0:
                character.max_hitpoints += 10
                character.skill_point -= 1
            else:
                return make_response({"Message": "You don't Have a skill point to spend"},402)
        elif action == 'mana':
            if character.skill_point > 0:
                character.max_mana += 10
                character.skill_point -= 1
            else:
                return make_response({"Message": "You don't Have a skill point to spend"},402)
        elif action == 'draw':
            if character.skill_point > 4:
                character.draw += 1
                character.skill_point -= 5
            else:
                return make_response({"Message": "You don't Have 5 skill points to spend"},402)
        else:
            return make_response({'error': 'unknown action'}, 400)
        character.mana = character.max_mana
        character.hitpoints = character.max_hitpoints
        db.session.commit()
        response_data = {
            "message": "Successfully upgraded",
            "character": character.to_dict(rules={'-user',})
        }
        return make_response(response_data,200)
api.add_resource(UseSkillPoint,'/api/v1/skillpoint',endpoint="skillpoint")
class BuyCardById(Resource):
    def get(self,id):
        card = Card.query.filter_by(id=id).first()
        if not card:
            return make_response({"message": "Card not found"}, 404)
        character_id = session.get('character_id')
        character = Character.query.filter_by(id=character_id).first()
        if not character:
            return make_response({"message": "Character not found"}, 404)
        if character.gold >= card.gold_cost:
            character.gold -= card.gold_cost
            new_deck_entry = Deck(character=character, card=card)
            db.session.add(new_deck_entry)
            db.session.commit()
            response_data = {
                'character': character.to_dict(),
                'new_card': card.to_dict(rules={'-decks',"-mob_decks",'-updated_at','-created_at'}),
            }
            return make_response(response_data, 200)
        else:
            return make_response({"message": "Not enough gold to buy the card"}, 402)
api.add_resource(BuyCardById,'/api/v1/buycard/<id>',endpoint="buycard")
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
@app.route('/api/v1/logoutchar',methods=['DELETE'])
def logoutchar():
    session['character_id'] = None
    return make_response('',204)
@app.route('/')
def index():
    return '<h1>Project Server</h1>'
@app.before_request
def check_logged_id():
    if request.endpoint in ['character','characterid'] and not session.get('user_id'):
        return make_response({'error':'Unauthorized, Must be logged In'},401)
    if request.endpoint in ['characterfight','playcard','endturn','shopthree','shopnine','skillpoint','buycard','flee'] and not session.get('character_id'):
        return make_response({'error': 'Unauthorized, Must be playing a character'},401)
if __name__ == '__main__':
    app.run(port=5555, debug=True)