"""seed data roles and permissions

Revision ID: c6a26997ff09
Revises: 258b56f4dfba
Create Date: 2025-09-10 14:40:28.430415
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c6a26997ff09'
down_revision: Union[str, None] = '258b56f4dfba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Insert roles
    op.execute("""
        INSERT INTO roles (id, name) VALUES
        (1, 'owner'),
        (2, 'admin'),
        (3, 'staff'),
        (4, 'user'),
        (5, 'contributor');
    """)

    # Set sequence for roles table
    op.execute("SELECT setval('roles_id_seq', 6, false);")

    # Insert base permissions (1–19)
    op.execute("""
        INSERT INTO permissions (id, name) VALUES
        (1, 'create_spot'),
        (2, 'edit_spot'),
        (3, 'delete_spot'),
        (4, 'approve_spot'),
        (5, 'assign_spot'),
        (6, 'submit_feedback'),
        (7, 'edit_feedback'),
        (8, 'delete_feedback'),
        (9, 'moderate_feedback'),
        (10, 'upload_media'),
        (11, 'delete_media'),
        (12, 'moderate_media'),
        (13, 'create_tag'),
        (14, 'edit_tag'),
        (15, 'manage_attributes'),
        (16, 'manage_users'),
        (17, 'view_user_data'),
        (18, 'view_spots'),
        (19, 'interact_spots');
    """)

    # --- New permissions for uncovered entities (20–42) ---
    op.execute("""
        INSERT INTO permissions (id, name) VALUES
        -- Cities
        (20, 'create_city'),
        (21, 'edit_city'),
        (22, 'delete_city'),
        (23, 'view_cities'),

        -- Spot Types
        (24, 'create_spot_type'),
        (25, 'edit_spot_type'),
        (26, 'delete_spot_type'),
        (27, 'view_spot_types'),

        -- User Spots
        (28, 'add_user_spot'),
        (29, 'remove_user_spot'),
        (30, 'view_user_spots'),

        -- Feedback Media Files
        (31, 'add_feedback_media'),
        (32, 'remove_feedback_media'),
        (33, 'view_feedback_media'),

        -- Feedback Likes
        (34, 'like_feedback'),
        (35, 'unlike_feedback'),
        (36, 'view_feedback_likes'),

        -- Tokens
        (37, 'create_token'),
        (38, 'revoke_token'),
        (39, 'view_tokens'),

        -- Auth Providers
        (40, 'link_auth_provider'),
        (41, 'unlink_auth_provider'),
        (42, 'view_auth_providers');
    """)

    # Update sequence for permissions table
    op.execute("SELECT setval('permissions_id_seq', 43, false);")

    # Insert role_permissions
    values = []

    # Owner: all permissions (42 total)
    values += [(1, pid) for pid in range(1, 43)]
    # Admin: all except manage_users (id 16) (41 total)
    values += [(2, pid) for pid in range(1, 43) if pid != 16]
    # Staff: same as before + safe new ones
    values += [(3, pid) for pid in [
        1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,18,19,
        20,21,23,24,25,27,28,29,30,31,32,33,34,35,36
    ]]
    # Contributor: same as before + limited new ones
    values += [(5, pid) for pid in [
        1,2,6,7,8,10,11,18,19,
        28,29,30,31,32,33,34,35
    ]]
    # User: same as before + minimal new ones
    values += [(4, pid) for pid in [
        6,7,8,10,11,18,19,
        28,30,31,33,34,36
    ]]

    insert_values = ",\n".join([f"({rid}, {pid})" for rid, pid in values])

    op.execute(f"""
        INSERT INTO role_permissions (role_id, permission_id) VALUES
        {insert_values};
    """)

def downgrade() -> None:
    # Delete data
    op.execute("DELETE FROM role_permissions WHERE role_id BETWEEN 1 AND 5;")
    op.execute("DELETE FROM permissions WHERE id BETWEEN 1 AND 42;")
    op.execute("DELETE FROM roles WHERE id BETWEEN 1 AND 5;")

    # Reset sequences
    op.execute("SELECT setval('roles_id_seq', 1, false);")
    op.execute("SELECT setval('permissions_id_seq', 1, false);")
