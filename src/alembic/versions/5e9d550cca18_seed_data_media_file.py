"""seed data media file

Revision ID: 5e9d550cca18
Revises: ac0564548603
Create Date: 2025-09-11 11:56:00.163665

"""
from typing import Sequence, Union
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '5e9d550cca18'
down_revision: Union[str, None] = 'ac0564548603'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        INSERT INTO media_files (id, url, format, type, size, created_by, created_at, updated_at)
        VALUES 
        (1, 'public/960px-Thap_Rua.jpg', 'jpg', 'IMAGE', 344064, 1, NOW(), NOW()),
        (2, 'public/Bao_tang_Chung_tich_Chien_tranh.webp', 'webp', 'IMAGE', 59187, 1, NOW(), NOW()),
        (3, 'public/Bao_tang_Dan_toc_hoc_.jpg', 'jpg', 'IMAGE', 12083, 1, NOW(), NOW()),
        (4, 'public/Chua_Mot_Cot.webp', 'webp', 'IMAGE', 45568, 1, NOW(), NOW()),
        (5, 'public/Dia_Dao_Cu_Chi.webp', 'webp','IMAGE', 150784, 1, NOW(), NOW()),
        (6, 'public/Ho_Tay.jpg', 'jpg', 'IMAGE', 290816, 1, NOW(), NOW()),
        (7, 'public/Khu_Pho_Co_Ha_Noi.webp', 'webp', 'IMAGE', 86937, 1, NOW(), NOW()),
        (8, 'public/Lang_Chu_tich_Ho_Chi_Minh.jpg', 'jpg', 'IMAGE', 50074, 1, NOW(), NOW()),
        (9, 'public/Nha_Tu_Hoa_Lo.webp', 'webp', 'IMAGE', 65331, 1, NOW(), NOW()),
        (10,'public/Van_Mieu_Quoc_Tu_Giam.jpg', 'jpg', 'IMAGE', 2306867, 1, NOW(), NOW());
    """)

    # update sequence to max id
    op.execute("SELECT setval('media_files_id_seq', (SELECT MAX(id) FROM media_files));")


def downgrade() -> None:
    op.execute("""
        DELETE FROM media_files
        WHERE id IN (
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10
        );
    """)

    # reset sequence after delete
    op.execute("SELECT setval('media_files_id_seq', COALESCE((SELECT MAX(id) FROM media_files), 1));")
