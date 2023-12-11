from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

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
    hitpoints = db.Column(db.Integer,default=100)
    block = db.Column(db.Integer,default=0)
    mana = db.Column(db.Integer,default=100)
    gold = db.Column(db.Integer,default=500)
    created_at = db.Column(db.DateTime,server_default=db.func.now())
    updated_at = db.Column(db.DateTime,server_default=db.func.now(),onupdate=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User',back_populates='characters')
    serialize_rules = ('-user.characters',)