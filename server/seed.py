#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Character

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Dropping Undesirables...")
        User.query.delete()
        Character.query.delete()
        db.session.commit()
        print("Starting seed...")
        # Seed code goes here!
