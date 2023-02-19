"""initial tables creation

Revision ID: 693d102a040f
Revises: 
Create Date: 2022-12-25 23:57:27.529501

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "693d102a040f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "email_recipient",
        sa.Column("id", sa.Integer, sa.Identity(start=1, cycle=True), primary_key=True),
        sa.Column("email_address", sa.String(250), nullable=False),
        sa.Column("first_name", sa.String(50), nullable=False),
    )

    email_type = op.create_table(
        "email_type",
        sa.Column("id", sa.Integer, sa.Identity(start=1, cycle=True), primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("subject", sa.String(250), nullable=False),
        sa.Column("file_name", sa.String(50), nullable=False),
    )

    op.create_table(
        "email_request",
        sa.Column("id", sa.Integer, sa.Identity(start=1, cycle=True), primary_key=True),
        sa.Column("email_recipient_id", sa.Integer, sa.ForeignKey("email_recipient.id"), nullable=False),
        sa.Column("email_type_id", sa.Integer, sa.ForeignKey("email_type.id"), nullable=False),
        sa.Column("created_datetime", sa.DateTime, nullable=False, server_default="NOW()"),
        sa.Column("sent_datetime", sa.DateTime),
    )

    op.bulk_insert(
        email_type,
        [
            {"name": "Welcome", "subject": "Welcome to Emerald!", "file_name": "welcome.html"},
            {"name": "Invoice", "subject": "Your latest Emerald invoice", "file_name": "invoice.html"},
        ]
    )


def downgrade() -> None:
    op.drop_table("email_request")
    op.drop_table("email_type")
    op.drop_table("email_recipient")
