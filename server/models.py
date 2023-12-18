from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
import random
from config import db, SQLAlchemy, MetaData, bcrypt

# Models go here!
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True,nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime,server_default=db.func.now())
    updated_at = db.Column(db.DateTime,server_default=db.func.now(),onupdate=db.func.now())
    characters = db.relationship('Character',back_populates='user', cascade='all, delete-orphan')
    
    serialize_rules = ('-_password_hash','-characters.user')
    
    @property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self,plain_text_password):
        byte_object = plain_text_password.encode('utf-8')
        encrpyted_password_object = bcrypt.generate_password_hash(byte_object)
        hashed_password_string = encrpyted_password_object.decode('utf-8')
        self._password_hash = hashed_password_string
    def authenticate(self,password_string):
        byte_object = password_string.encode('utf-8')
        return bcrypt.check_password_hash(self.password_hash,byte_object)

class Character(db.Model,SerializerMixin):
    __tablename__ = 'characters'

    id = db.Column(db.Integer,primary_key=True)
    character_name = db.Column(db.String,nullable=False)

    # level = db.Column(db.Integer,default=1)
    # experience = db.Column(db.Integer,default=0)
    # experience_cap = db.Column(db.Integer,default=100)
    # skill_point = db.Column(db.Integer,default=0)

    gold = db.Column(db.Integer,default=500)

    hitpoints = db.Column(db.Integer,default=100)
    max_hitpoints = db.Column(db.Integer,default=100)
    mana = db.Column(db.Integer,default=100)
    max_mana = db.Column(db.Integer,default=100)
    draw = db.Column(db.Integer,default=5)
    block = db.Column(db.Integer,default=0)
    created_at = db.Column(db.DateTime,server_default=db.func.now())
    updated_at = db.Column(db.DateTime,server_default=db.func.now(),onupdate=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User',back_populates='characters')

    decks = db.relationship('Deck',back_populates='character',cascade='all,delete-orphan')
    cards = association_proxy('decks','card')

    fights = db.relationship('Fight',back_populates='character',cascade='all,delete-orphan')

    serialize_rules = ('-user.characters', '-decks.character','-fights.character')

    def discard_hand(self):
        drawn_decks = Deck.query.filter_by(character_id=self.id, status='Drawn').all()

        for drawn_deck in drawn_decks:
            drawn_deck.status = 'Discarded'
            db.session.add(drawn_deck)
        db.session.commit()
    def shuffle_deck_all(self):
        decks = Deck.query.filter_by(character_id=self.id).all()

        for deck in decks:
            deck.status = 'Undrawn'
            db.session.add(deck)

        db.session.commit()
    def shuffle_discarded_into_deck(self):
        discarded_decks = Deck.query.filter_by(character_id=self.id, status='Discarded').all()

        for discarded_deck in discarded_decks:
            discarded_deck.status = 'Undrawn'
            db.session.add(discarded_deck)
        db.session.commit()
    def draw_card(self):
        undrawn_decks = Deck.query.filter_by(character_id=self.id, status='Undrawn').all()

        if not undrawn_decks:
            self.shuffle_discarded_into_deck()
            undrawn_decks = Deck.query.filter_by(character_id=self.id, status='Undrawn').all()

        if undrawn_decks:
            drawn_deck = random.choice(undrawn_decks)
            drawn_deck.status = 'Drawn'
            db.session.commit()
            return drawn_deck
        else:
            return None
    def draw_hand(self):
        undrawn_decks = Deck.query.filter_by(character_id=self.id, status='Undrawn').all()
        discarded_decks = Deck.query.filter_by(character_id=self.id, status='Discarded').all()

        total_cards = len(undrawn_decks) + len(discarded_decks)
        i = min(self.draw, total_cards)

        if total_cards < self.draw:
            i = total_cards

        for _ in range(i):
            drawn_deck = self.draw_card()

            if drawn_deck is None:

                break

        return i

class Deck(db.Model,SerializerMixin):
    __tablename__ = 'decks'

    id = db.Column(db.Integer,primary_key=True)
    status = db.Column(db.String,default="Undrawn")

    character_id = db.Column(db.Integer, db.ForeignKey('characters.id', ondelete='CASCADE'))
    character = db.relationship('Character',back_populates='decks')
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    card = db.relationship('Card',back_populates='decks')

    serialize_rules = ('-card.decks','-character.decks','-card.mob_decks')

class Card(db.Model,SerializerMixin):
    __tablename__ = 'cards'
    id = db.Column(db.Integer,primary_key=True)
    card_name = db.Column(db.String,nullable=False)
    gold_cost = db.Column(db.Integer)
    mana_cost = db.Column(db.Integer)
    mana_gain = db.Column(db.Integer)
    hp_cost = db.Column(db.Integer)
    damage = db.Column(db.Integer)
    block = db.Column(db.Integer)
    heal = db.Column(db.Integer)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime,server_default=db.func.now())
    updated_at = db.Column(db.DateTime,server_default=db.func.now(),onupdate=db.func.now())
    
    decks = db.relationship('Deck',back_populates='card')
    characters = association_proxy('decks','character')
    mob_decks = db.relationship('MobDeck',back_populates='card')
    mob = association_proxy('decks','mob')
    in_fight_mob_decks = db.relationship('InFightMobDeck', back_populates='card')
    
    serialize_rules = ('-decks.card','-mob_decks.card','-in_fight_mob_decks')

class CardType(db.Model, SerializerMixin): #cut Content.
    __tablename__ = 'card_types'
    id = db.Column(db.Integer,primary_key=True)
    tag = db.Column(db.String,default='custom')
    #relationship between this and Card

class MobDeck(db.Model,SerializerMixin):
    __tablename__ = 'mob_decks'
    
    id = db.Column(db.Integer,primary_key=True)

    mob_id = db.Column(db.Integer, db.ForeignKey('mobs.id'))
    mob = db.relationship('Mob',back_populates='mob_decks')
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    card = db.relationship('Card',back_populates='mob_decks')

    serialize_rules = ('-card.mob_decks','-mob.mob_decks')

class Mob(db.Model, SerializerMixin):
    __tablename__ = 'mobs'
    id = db.Column(db.Integer,primary_key=True)
    level = db.Column(db.Integer,default=1)
    mob_name = db.Column(db.String,nullable=False)
    # gold = db.Column(db.Integer,default=500)
    hitpoints = db.Column(db.Integer,default=100)
    max_hitpoints = db.Column(db.Integer,default=100)
    mana = db.Column(db.Integer,default=100)
    max_mana = db.Column(db.Integer,default=100)
    draw = db.Column(db.Integer,default=1)
    block = db.Column(db.Integer,default=0)
    created_at = db.Column(db.DateTime,server_default=db.func.now())
    updated_at = db.Column(db.DateTime,server_default=db.func.now(),onupdate=db.func.now())


    mob_decks = db.relationship('MobDeck',back_populates='mob')
    cards = association_proxy('mob_decks','card')
    serialize_rules = ('-mob_decks.mob',)

class Fight(db.Model,SerializerMixin):
    __tablename__ = 'fights'
    id = db.Column(db.Integer,primary_key=True) 
    turn = db.Column(db.Integer, default=1)
    status = db.Column(db.String, default='Ongoing')
    created_at = db.Column(db.DateTime,server_default=db.func.now())
    updated_at = db.Column(db.DateTime,server_default=db.func.now(),onupdate=db.func.now())
    #enemy Stats, not the ID because no cheese

    mob_name = db.Column(db.String,nullable=False)
    level = db.Column(db.String,default=1)
    hitpoints = db.Column(db.Integer,default=100)
    max_hitpoints = db.Column(db.Integer,default=100)
    mana = db.Column(db.Integer,default=100)
    max_mana = db.Column(db.Integer,default=100)
    draw = db.Column(db.Integer,default=1)
    block = db.Column(db.Integer,default=0)

    #a character ID
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    character = db.relationship('Character',back_populates='fights')
    
    in_fight_mob_decks = db.relationship('InFightMobDeck', back_populates='fight',cascade='all,delete-orphan')
    serialize_rules = ('-character.fights',"-in_fight_mob_decks.fight")
    def discard_hand(self):
        in_fight_mob_decks = InFightMobDeck.query.filter_by(fight_id=self.id, status='Undrawn').all()

        for in_fight_mob_deck in in_fight_mob_decks:
            in_fight_mob_deck.status = 'Discarded'
            db.session.add(in_fight_mob_deck)
        db.session.commit()
    def reset_deck_status(self):
        in_fight_mob_decks = InFightMobDeck.query.filter_by(fight_id=self.id).all()

        for in_fight_mob_deck in in_fight_mob_decks:
            in_fight_mob_deck.status = 'Undrawn'
            db.session.add(in_fight_mob_deck)
        db.session.commit()
    def shuffle_discarded_into_deck(self):
        discarded_in_fight_mob_decks = InFightMobDeck.query.filter_by(fight_id=self.id, status='Discarded').all()

        for discarded_in_fight_mob_deck in discarded_in_fight_mob_decks:
            discarded_in_fight_mob_deck.status = 'Undrawn'
            db.session.add(discarded_in_fight_mob_deck)
        db.session.commit()
    def draw_card(self):
        undrawn_in_fight_mob_decks = InFightMobDeck.query.filter_by(fight_id=self.id, status='Undrawn').all()

        if not undrawn_in_fight_mob_decks:
            self.shuffle_discarded_into_deck()
            undrawn_in_fight_mob_decks = InFightMobDeck.query.filter_by(fight_id=self.id, status='Undrawn').all()

        if undrawn_in_fight_mob_decks:
            drawn_in_fight_mob_deck = random.choice(undrawn_in_fight_mob_decks)
            drawn_in_fight_mob_deck.status = 'Drawn'
            db.session.commit()
            return drawn_in_fight_mob_deck
        else:
            return None
    def draw_hand(self):
            undrawn_in_fight_mob_decks = InFightMobDeck.query.filter_by(fight_id=self.id, status='Undrawn').all()
            discarded_in_fight_mob_decks = InFightMobDeck.query.filter_by(fight_id=self.id, status='Discarded').all()

            total_cards = len(undrawn_in_fight_mob_decks) + len(discarded_in_fight_mob_decks)
            i = min(self.draw, total_cards)

            if total_cards < self.draw:
                i = total_cards

            for _ in range(i):
                drawn_in_fight_mob_deck = self.draw_card()

                if drawn_in_fight_mob_deck is None:
                    break

            return i
class InFightMobDeck(db.Model,SerializerMixin):
    __tablename__ = 'in_fight_mob_decks'

    id = db.Column(db.Integer,primary_key=True)
    status = db.Column(db.String,default="Undrawn")

    fight_id = db.Column(db.Integer, db.ForeignKey('fights.id'))
    fight = db.relationship('Fight',back_populates='in_fight_mob_decks')
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    card = db.relationship('Card', back_populates='in_fight_mob_decks')
    serialize_rules = ('-card.decks','-character.decks','-card.mob_decks')
