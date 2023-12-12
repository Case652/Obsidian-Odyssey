#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Character,Deck,Card




if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Dropping Undesirables...")
        User.query.delete()
        Character.query.delete()
        Deck.query.delete()
        Card.query.delete()
        db.session.commit()
        print("Starting seed...")
        # Seed code goes here!
        cards_to_commit = [
            Card(
                card_name="Magic Bolt",
                gold_cost=200,
                mana_cost=5,
                mana_gain=0,
                hp_cost=0,
                damage=10,
                block=0,
                heal=0,
                description="Short and Simple \nFire a bolt that hits{damage} damage",
            ),
            Card(
                card_name="Magic Ward",
                gold_cost=200,
                mana_cost=5,
                mana_gain=0,
                hp_cost=0,
                damage=0,
                block=10,
                heal=0,
                description="Short and Simple \nBlock {block} incoming damage",
            ),
            Card(
                card_name="Magic Band-aid",
                gold_cost=200,
                mana_cost=10,
                mana_gain=0,
                hp_cost=0,
                damage=0,
                block=0,
                heal=10,
                description="Short and Simple \nRecover {heal} Hp",
            ),
            Card(
                card_name="Vitality Transfusion",
                gold_cost=400,
                mana_cost=0,
                mana_gain=20,
                hp_cost=10,
                damage=0,
                block=0,
                heal=0,
                description="Short and What? \nTrade {hp_cost} Hp\nFor {mana_gain} Mana",
            ),
            Card(
                card_name="Wack Em",
                gold_cost=100,
                mana_cost=0,
                mana_gain=0,
                hp_cost=0,
                damage=5,
                block=0,
                heal=0,
                description="Better Then Nothing...\nRight? \nWackEm {damage} Damage",
            ),
            Card(
                card_name="Hide Behind Somthing",
                gold_cost=100,
                mana_cost=0,
                mana_gain=0,
                hp_cost=0,
                damage=0,
                block=5,
                heal=0,
                description="Better Then Nothing...\nRight? \nBlock {block} incoming damage",
            )
        ]
        db.session.add_all(cards_to_commit)
        db.session.commit()