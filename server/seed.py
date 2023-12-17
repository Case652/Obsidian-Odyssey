#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Character,Deck,Card,Mob,MobDeck

starter_deck = [
    {"card_name": "Magic Bolt"},
    {"card_name": "Magic Bolt"},
    {"card_name": "Magic Ward"},
    {"card_name": "Magic Ward"},
    {"card_name": "Magic Band-aid"},
    {"card_name": "Magic Band-aid"},
    {"card_name": "Vitality Transfusion"},
    {"card_name": "Wack Em"},
    {"card_name": "Wack Em"},
    {"card_name": "Wack Em"},
    {"card_name": "Hide Behind Somthing"},
    {"card_name": "Hide Behind Somthing"},
    {"card_name": "Hide Behind Somthing"},
]

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Dropping Undesirables...")
        User.query.delete()
        Character.query.delete()
        Deck.query.delete()
        Card.query.delete()
        Mob.query.delete()
        MobDeck.query.delete()
        db.session.commit()
        print("Starting seed...")
        # Seed code goes here!
        print('Seeding Cards...')
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
                description="Short and Simple \nFire a bolt that hits {damage} damage",
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
            ),
            Card(
                card_name="Goblin Scratch",
                gold_cost=50,
                mana_cost=2,
                mana_gain=0,
                hp_cost=0,
                damage=5,
                block=0,
                heal=0,
                description="Basic attack: Scratch for {damage} damage.",
            ),
            Card(
                card_name="Goblin Defend",
                gold_cost=50,
                mana_cost=1,
                mana_gain=0,
                hp_cost=0,
                damage=0,
                block=3,
                heal=0,
                description="Defend and block {block} incoming damage.",
            )
        ]
        db.session.add_all(cards_to_commit)
        db.session.commit()
        print('Seeding Mobs...')
        mobs_to_commit = [
            {
                "mob_name": "Goblin",
                "hitpoints": "50",
                "max_hitpoints": "50",
                "mana": "50",
                "max_mana": "50",
                "draw": "2",
                "block": "0",
                "mob_decks": [
                    {"card_name": "Goblin Scratch"},
                    {"card_name": "Goblin Scratch"},
                    {"card_name": "Goblin Scratch"},
                    {"card_name": "Goblin Scratch"},
                    {"card_name": "Goblin Scratch"},
                    {"card_name": "Goblin Scratch"},
                    {"card_name": "Goblin Scratch"},
                    {"card_name": "Goblin Defend"},
                    {"card_name": "Goblin Defend"},
                    {"card_name": "Goblin Defend"},
                ],
            },
            {
                "mob_name": "Slightly-Goblin",
                "hitpoints": "50",
                "max_hitpoints": "50",
                "mana": "50",
                "max_mana": "50",
                "draw": "2",
                "block": "0",
                "mob_decks": [
                    {"card_name": "Magic Bolt"}
                ],
            },
        ]

        for mob_info in mobs_to_commit:
            mob_decks_info = mob_info.pop("mob_decks", [])
            mob = Mob(**mob_info)
            db.session.add(mob)
            db.session.commit()

            for deck_info in mob_decks_info:
                card_name = deck_info["card_name"]
                card = Card.query.filter_by(card_name=card_name).first()

                if card:
                    deck = MobDeck(mob_id=mob.id, card_id=card.id)
                    db.session.add(deck)

        db.session.commit()