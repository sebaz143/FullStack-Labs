"""empty message

Revision ID: e63652354ffd
Revises: 833724243ce0
Create Date: 2022-03-28 21:38:46.330995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e63652354ffd'
down_revision = '833724243ce0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bags', sa.Column('title', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bags', 'title')
    # ### end Alembic commands ###