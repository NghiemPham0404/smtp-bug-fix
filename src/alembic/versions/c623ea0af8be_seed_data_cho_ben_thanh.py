"""seed data Cho Ben Thanh

Revision ID: c623ea0af8be
Revises: bac4707a7baf
Create Date: 2025-10-03 14:58:30.539774

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c623ea0af8be'
down_revision: Union[str, None] = 'bac4707a7baf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        '''
        INSERT INTO media_files (id, url, format, type, size, created_by, created_at, updated_at) VALUES
        (11, 'private/spots/12/cho_ben_thanh_1.jpg', 'jpg', 'IMAGE', 769000, 1, '2025-10-03 14:54:24+07', '2025-10-03 14:54:24+07'), -- Image for Clock Tower attribute
        (12, 'private/spots/12/cho_ben_thanh_2.jpg', 'jpg', 'IMAGE', 469200, 1, '2025-10-03 14:54:24+07', '2025-10-03 14:54:24+07'),   -- Image for Food Court attribute
        (13, 'private/spots/12/cho_ben_thanh_4.jpg', 'jpg', 'IMAGE', 656400, 1, '2025-10-03 14:54:24+07', '2025-10-03 14:54:24+07'),  -- Image for Souvenirs attribute
        (14, 'private/spots/12/cho_ben_thanh_3.jpg', 'jpg', 'IMAGE', 322000, 1, '2025-10-03 14:54:24+07', '2025-10-03 14:54:24+07'),   -- Image for Textiles & Accessories attribute
        (15, 'private/spots/12/cho_ben_thanh_6.jpg', 'jpg', 'IMAGE', 152600, 1, '2025-10-03 14:54:24+07', '2025-10-03 14:54:24+07'), 
        (16, 'private/spots/12/cho_ben_thanh_7.jpg', 'jpg', 'IMAGE', 522800, 1, '2025-10-03 14:54:24+07', '2025-10-03 14:54:24+07'),  
        (17, 'private/spots/12/cho_ben_thanh_audio.mp3', 'mp3', 'AUDIO', 651900, 1, '2025-10-03 14:54:24+07', '2025-10-03 14:54:24+07'); 

        -- Step 2: Create the attributes for Chợ Bến Thành (spot_id = 12).
        -- We'll use IDs starting from 501 for these new attributes.
        INSERT INTO spot_attributes (id, spot_id, name, description, sort_order, created_at, created_by, updated_at) VALUES
        (1, 12, 'Cổng Chính & Tháp Đồng Hồ', 'Là biểu tượng mang tính lịch sử của chợ, Cổng Chính với tháp đồng hồ bốn mặt là điểm check-in không thể bỏ lỡ của mọi du khách khi đến Sài Gòn.', 1, '2025-10-03 14:54:24+07', 1, '2025-10-03 14:54:24+07'),
        (2, 12, 'Khu Ẩm Thực', 'Thiên đường dành cho tín đồ ăn uống với hàng chục quầy hàng phục vụ các món ăn đặc sản ba miền, từ phở, bún, cơm tấm đến các loại chè và nước giải khát.', 2, '2025-10-03 14:54:24+07', 1, '2025-10-03 14:54:24+07'),
        (3, 12, 'Khu Đồ Lưu Niệm & Thủ Công Mỹ Nghệ', 'Nơi trưng bày và bán các sản phẩm thủ công tinh xảo, áo dài, nón lá, tranh sơn mài và nhiều món quà lưu niệm đậm chất Việt Nam.', 3, '2025-10-03 14:54:24+07', 1, '2025-10-03 14:54:24+07'),
        (4, 12, 'Khu Vải Vóc & Quần Áo', 'Một khu vực sầm uất chuyên bán các loại vải, đặc biệt là lụa và gấm, cùng với quần áo may sẵn và dịch vụ may đo áo dài lấy nhanh.', 4, '2025-10-03 14:54:24+07', 1, '2025-10-03 14:54:24+07');

        -- Step 3: Link the spot attributes to their respective media files.
        INSERT INTO spot_attribute_media_files (spot_attribute_id, media_file_id) VALUES
        (1, 11), -- Link attribute 'Cổng Chính & Tháp Đồng Hồ' to its image
        (2, 12), -- Link attribute 'Khu Ẩm Thực' to its image
        (3, 13), -- Link attribute 'Khu Đồ Lưu Niệm' to its image
        (4, 14); -- Link attribute 'Khu Vải Vóc' to its image

        -- Step 4: Link the main scenic spot (Chợ Bến Thành) to its new general gallery media files.
        INSERT INTO spot_media_files (spot_id, media_file_id) VALUES
        (12, 15), 
        (12, 16), 
        (12, 17);
        '''
    )


def downgrade() -> None:
    op.execute(
        '''
        -- Step 1: Delete records from spot_media_files for spot_id = 12
        DELETE FROM spot_media_files WHERE spot_id = 12 AND media_file_id IN (15, 16, 17);

        -- Step 2: Delete records from spot_attribute_media_files for spot_attribute_id 1-54
        DELETE FROM spot_attribute_media_files WHERE spot_attribute_id IN (1, 2, 3, 4);

        -- Step 3: Delete records from spot_attributes for IDs 1-4
        DELETE FROM spot_attributes WHERE id IN (1, 2, 3, 4);

        -- Step 4: Delete records from media_files for IDs 11-17
        DELETE FROM media_files WHERE id IN (11, 12, 13, 14, 15, 16, 17);
        '''
    )
