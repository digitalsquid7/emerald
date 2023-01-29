"""initial tables creation

Revision ID: 693d102a040f
Revises: 
Create Date: 2022-12-25 23:57:27.529501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '693d102a040f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "email_request",
        sa.Column('id', sa.Integer, sa.Identity(start=1, cycle=True), primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )


def downgrade() -> None:
    op.drop_table('email_request')
