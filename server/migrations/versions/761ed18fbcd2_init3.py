"""init3

Revision ID: 761ed18fbcd2
Revises: 7153c4b0dd0a
Create Date: 2023-12-11 16:02:54.237535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '761ed18fbcd2'
down_revision = '7153c4b0dd0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('decks', schema=None) as batch_op:
        batch_op.drop_constraint('fk_decks_card_id_characters', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_decks_card_id_cards'), 'cards', ['card_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('decks', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_decks_card_id_cards'), type_='foreignkey')
        batch_op.create_foreign_key('fk_decks_card_id_characters', 'characters', ['card_id'], ['id'])

    # ### end Alembic commands ###
