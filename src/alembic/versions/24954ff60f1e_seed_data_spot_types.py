"""seed data spot types

Revision ID: 24954ff60f1e
Revises: d23624a4c1e6
Create Date: 2025-09-10 17:19:41.588479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24954ff60f1e'
down_revision: Union[str, None] = 'd23624a4c1e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        INSERT INTO spot_types (id, name, icon_url, image_url, created_at, updated_at) VALUES
        (1, 'Tourist attraction', NULL, NULL, NOW(), NULL),
        (2, 'Natural feature', NULL, NULL, NOW(), NULL),
        (3, 'Museum', NULL, NULL, NOW(), NULL),
        (4, 'Park', NULL, NULL, NOW(), NULL),
        (5, 'Place of worship', NULL, NULL, NOW(), NULL),
        (6, 'Campground', NULL, NULL, NOW(), NULL),
        (7, 'Zoo', NULL, NULL, NOW(), NULL),
        (8, 'Aquarium', NULL, NULL, NOW(), NULL),
        (9, 'Art gallery', NULL, NULL, NOW(), NULL),
        (10, 'Stadium', NULL, NULL, NOW(), NULL),
        (11, 'Church', NULL, NULL, NOW(), NULL),
        (12, 'Hindu temple', NULL, NULL, NOW(), NULL),
        (13, 'Mosque', NULL, NULL, NOW(), NULL),
        (14, 'Synagogue', NULL, NULL, NOW(), NULL);
    """)
    # Set sequence for spot_types table
    op.execute("SELECT setval('spot_types_id_seq', 15, false);")

def downgrade() -> None:
    # Delete the inserted spot types
    op.execute("DELETE FROM spot_types WHERE id BETWEEN 1 AND 14;")
    # Reset sequence to the maximum ID or 1 if no records remain
    op.execute("SELECT setval('spot_types_id_seq', (SELECT COALESCE(MAX(id), 1) FROM spot_types), false);")
