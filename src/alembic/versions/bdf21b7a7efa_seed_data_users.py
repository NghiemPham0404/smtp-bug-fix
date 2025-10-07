"""seed data users

Revision ID: bdf21b7a7efa
Revises: 5e9d550cca18
Create Date: 2025-09-11 13:59:47.021325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bdf21b7a7efa'
down_revision: Union[str, None] = '5e9d550cca18'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- existing media_files seeding here ---

    op.execute("""
        INSERT INTO users (id, name, email, avatar, joined_date, last_login, is_active, role_id)
        VALUES
        -- Admins
        (2, 'Admin One', 'admin1@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 2),
        (3, 'Admin Two', 'admin2@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 2),

        -- Staff
        (4, 'Staff One', 'staff1@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 3),
        (5, 'Staff Two', 'staff2@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 3),
        (6, 'Staff Three', 'staff3@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 3),
        (7, 'Staff Four', 'staff4@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 3),
        (8, 'Staff Five', 'staff5@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 3),

        -- Contributors
        (9, 'Contributor One', 'contrib1@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 4),
        (10, 'Contributor Two', 'contrib2@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 4),
        (11, 'Contributor Three', 'contrib3@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 4),
        (12, 'Contributor Four', 'contrib4@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 4),
        (13, 'Contributor Five', 'contrib5@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 4),
        (14, 'Contributor Six', 'contrib6@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 4),
        (15, 'Contributor Seven', 'contrib7@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 4),
        (16, 'Contributor Eight', 'contrib8@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 4),
        (17, 'Contributor Nine', 'contrib9@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 4),
        (18, 'Contributor Ten', 'contrib10@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 4),

        -- Users
        (19, 'User One', 'user1@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 5),
        (20, 'User Two', 'user2@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 5),
        (21, 'User Three', 'user3@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 5),
        (22, 'User Four', 'user4@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 5),
        (23, 'User Five', 'user5@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 5),
        (24, 'User Six', 'user6@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 5),
        (25, 'User Seven', 'user7@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 5),
        (26, 'User Eight', 'user8@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 5),
        (27, 'User Nine', 'user9@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 5),
        (28, 'User Ten', 'user10@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 5),
        (29, 'User Eleven', 'user11@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 5),
        (30, 'User Twelve', 'user12@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 5),
        (31, 'User Thirteen', 'user13@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 5),
        (32, 'User Fourteen', 'user14@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 5),
        (33, 'User Fifteen', 'user15@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 5),
        (34, 'User Sixteen', 'user16@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 5),
        (35, 'User Seventeen', 'user17@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 5),
        (36, 'User Eighteen', 'user18@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 5),
        (37, 'User Nineteen', 'user19@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 5),
        (38, 'User Twenty', 'user20@example.com', NULL, CURRENT_DATE, NOW(), TRUE, 5);
    """)

    # update users sequence
    op.execute("SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));")


def downgrade() -> None:
    op.execute("""
        DELETE FROM users
        WHERE id BETWEEN 2 AND 38;
    """)
    op.execute("SELECT setval('users_id_seq', COALESCE((SELECT MAX(id) FROM users), 1));")

