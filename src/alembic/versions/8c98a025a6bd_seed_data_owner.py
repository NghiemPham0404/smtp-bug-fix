"""seed data owner

Revision ID: 8c98a025a6bd
Revises: c6a26997ff09
Create Date: 2025-09-10 15:32:47.200974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c98a025a6bd'
down_revision: Union[str, None] = 'c6a26997ff09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        '''
        INSERT INTO users (name,email,avatar,joined_date,last_login,is_active,role_id
        ) VALUES (
            'Footprints','owner@example.com',NULL,CURRENT_DATE,NOW(),TRUE,1
        );
        '''
    )
    pass


def downgrade() -> None:
    # Delete the inserted user
    op.execute("DELETE FROM users WHERE email = 'owner@example.com';")
    # Reset sequence to the maximum ID or 1 if no records remain
    op.execute("SELECT setval('users_id_seq', (SELECT COALESCE(MAX(id), 1) FROM users), false);")
