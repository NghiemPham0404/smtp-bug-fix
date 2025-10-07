"""seed data feedbacks

Revision ID: ee08a274affd
Revises: bdf21b7a7efa
Create Date: 2025-09-12 09:02:23.133097

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee08a274affd'
down_revision: Union[str, None] = 'bdf21b7a7efa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.execute("""
        INSERT INTO feedbacks (id, spot_id, user_id, rating, text, created_at, updated_at) VALUES
        (1, 1, 19, 5, 'Hồ Hoàn Kiếm thật sự là trái tim của Hà Nội. Khung cảnh tuyệt đẹp, không gian yên tĩnh giữa lòng thành phố.', '2025-09-01 08:30:00+07', NULL),
        (2, 1, 20, 4, 'Địa điểm tuyệt vời để dạo bộ buổi sáng. Tuy nhiên hơi đông người vào cuối tuần.', '2025-09-02 19:15:30+07', NULL),
        (3, 1, 21, 5, 'Không khí trong lành, cảnh đẹp như tranh. Rất thích hợp cho các cặp đôi hẹn hò.', '2025-09-03 16:45:12+07', NULL),
        (4, 2, 22, 5, 'Văn Miếu - nơi thờ Khổng Tử tuyệt vời. Kiến trúc cổ kính, ý nghĩa lịch sử sâu sắc.', '2025-09-01 10:20:45+07', NULL),
        (5, 2, 23, 4, 'Địa điểm học tập lịch sử tốt. Hướng dẫn viên nhiệt tình, giải thích rõ ràng.', '2025-09-02 14:10:22+07', NULL),
        (6, 2, 24, 5, 'Không gian thiêng liêng, yên tĩnh. Rất phù hợp để suy ngẫm về giáo dục truyền thống.', '2025-09-03 11:35:18+07', NULL),
        (7, 3, 25, 5, 'Lăng Bác - nơi thiêng liêng nhất của dân tộc. Được tham quan là vinh dự lớn.', '2025-09-01 09:45:30+07', NULL),
        (8, 3, 26, 4, 'Trang nghiêm, uy nghiêm. Quy trình tham quan được tổ chức rất chu đáo.', '2025-09-02 15:20:15+07', NULL),
        (9, 4, 27, 4, 'Phố cổ Hà Nội có nét đẹp truyền thống. Nhiều quán ăn ngon, hàng thủ công mỹ nghệ độc đáo.', '2025-09-01 18:30:45+07', NULL),
        (10, 4, 28, 3, 'Khá đông đúc và ồn ào. Tuy nhiên vẫn có những góc yên tĩnh để khám phá.', '2025-09-02 20:10:30+07', NULL),
        (11, 5, 29, 4, 'Bảo tàng Dân tộc học rất phong phú. Hiểu thêm nhiều về các dân tộc Việt Nam.', '2025-09-01 13:25:20+07', NULL),
        (12, 5, 30, 5, 'Trưng bày đa dạng, sinh động. Đặc biệt ấn tượng với trang phục truyền thống.', '2025-09-02 16:45:10+07', NULL),
        (13, 6, 31, 4, 'Nhà tù Hỏa Lò - bài học lịch sử đau thương. Không gian tái hiện chân thực.', '2025-09-01 11:15:35+07', NULL),
        (14, 6, 32, 3, 'Hơi u ám nhưng có ý nghĩa giáo dục cao. Nên đi với người lớn hướng dẫn.', '2025-09-02 14:50:25+07', NULL),
        (15, 7, 33, 5, 'Chùa Một Cột - kiệt tác kiến trúc độc đáo. Tuy nhỏ nhưng rất linh thiêng.', '2025-09-01 07:30:40+07', NULL),
        (16, 8, 34, 4, 'Hồ Tây rộng lớn, thích hợp đạp xe quanh hồ. Nhiều quán cà phê view đẹp.', '2025-09-01 17:20:15+07', NULL),
        (17, 8, 35, 3, 'Khá to nhưng không có nhiều điểm nhấn đặc biệt. Phù hợp để thể dục buổi sáng.', '2025-09-02 06:45:30+07', NULL),
        (18, 9, 36, 5, 'Bảo tàng Chứng tích Chiến tranh làm tôi xúc động mạnh. Trưng bày rất chân thực.', '2025-09-01 14:30:20+07', NULL),
        (19, 9, 37, 4, 'Nội dung nặng nề nhưng rất ý nghĩa. Giúp hiểu thêm về lịch sử chiến tranh.', '2025-09-02 10:15:45+07', NULL),
        (20, 10, 38, 5, 'Địa đạo Củ Chi thật kỳ diệu! Không thể tin được người xưa có thể sống dưới đây.', '2025-09-01 09:20:30+07', NULL),
        (21, 10, 19, 4, 'Trải nghiệm thú vị, tuy hơi khó khăn khi di chuyển trong đường hầm hẹp.', '2025-09-02 13:40:15+07', NULL),
        (22, 11, 20, 4, 'Nhà thờ Đức Bà Sài Gòn - kiến trúc Gothic tuyệt đẹp. Điểm check-in không thể bỏ qua.', '2025-09-01 16:10:25+07', NULL),
        (23, 11, 21, 5, 'Công trình kiến trúc Pháp đặc sắc. Bên trong rất trang nghiêm và thanh tịnh.', '2025-09-02 11:30:40+07', NULL),
        (24, 12, 22, 3, 'Chợ Bến Thành khá đông đúc và nhiều tiểu thương hét giá cao. Cần biết mặc cả.', '2025-09-01 19:45:20+07', NULL),
        (25, 12, 23, 4, 'Mua được nhiều đặc sản và quà lưu niệm. Nên đi buổi sáng để tránh đông.', '2025-09-02 08:20:35+07', NULL),
        (26, 13, 24, 5, 'Dinh Độc Lập - nơi diễn ra nhiều sự kiện lịch sử quan trọng. Kiến trúc sang trọng.', '2025-09-01 15:15:10+07', NULL),
        (27, 13, 25, 4, 'Tham quan tòa nhà và nghe kể về lịch sử rất thú vị. Hướng dẫn viên giỏi.', '2025-09-02 12:50:45+07', NULL),
        (28, 14, 26, 4, 'Bưu điện Sài Gòn - kiến trúc Pháp cổ điển. Có thể gửi bưu thiếp từ đây.', '2025-09-01 17:35:25+07', NULL),
        (29, 15, 27, 5, 'Landmark 81 - tòa nhà cao nhất Việt Nam. View từ tầng cao thật nspectacular!', '2025-09-01 20:10:30+07', NULL),
        (30, 15, 28, 4, 'Tầng quan sát đắt nhưng view đáng giá. Nên đi lúc hoàng hôn để ngắm cảnh đẹp nhất.', '2025-09-02 18:25:15+07', NULL),
        (31, 16, 29, 4, 'Chùa Giác Lâm - ngôi chùa cổ nhất Sài Gòn. Kiến trúc truyền thống, không gian yên tĩnh.', '2025-09-01 07:45:40+07', NULL),
        (32, 17, 30, 5, 'Cầu Vàng - kỳ quan của Việt Nam! Cảm giác như đang đi trên những bàn tay khổng lồ.', '2025-09-01 14:20:25+07', NULL),
        (33, 17, 31, 4, 'Rất đẹp và ấn tượng, tuy nhiên khá đông khách du lịch. Nên đi sớm.', '2025-09-02 09:15:35+07', NULL),
        (34, 18, 32, 4, 'Ngũ Hành Sơn - năm ngọn núi đá vôi độc đáo. Leo lên được ngắm toàn cảnh Đà Nẵng.', '2025-09-01 11:40:20+07', NULL),
        (35, 18, 33, 5, 'Hang động tự nhiên tuyệt đẹp, tượng Phật linh thiêng. Rất đáng để khám phá.', '2025-09-02 16:30:45+07', NULL),
        (36, 19, 34, 5, 'Bãi biển Mỹ Khê - một trong những bãi biển đẹp nhất thế giới. Cát trắng, nước xanh.', '2025-09-01 12:25:15+07', NULL),
        (37, 19, 35, 4, 'Biển đẹp, sóng nhẹ phù hợp tắm. Nhiều hoạt động thể thao nước thú vị.', '2025-09-02 15:10:30+07', NULL),
        (38, 20, 36, 4, 'Cầu Rồng phun lửa rất spectacular! Nên đến vào cuối tuần để xem màn trình diễn.', '2025-09-01 21:45:20+07', NULL),
        (39, 21, 37, 5, 'Bán đảo Sơn Trà - "lá phổi xanh" của Đà Nẵng. Thiên nhiên hoang sơ, khí hậu mát mẻ.', '2025-09-01 10:30:40+07', NULL),
        (40, 22, 38, 5, 'Vịnh Hạ Long - di sản thế giới tuyệt vời! Cảnh đẹp như tranh vẽ, không thể tả.', '2025-09-01 08:15:25+07', NULL),
        (41, 22, 19, 5, 'Du thuyền qua vịnh là trải nghiệm không thể quên. Hang động kỳ thú, đảo đá độc đáo.', '2025-09-02 13:20:35+07', NULL),
        (42, 23, 20, 4, 'Hang Sửng Sốt tên đúng nghĩa! Thạch nhũ đẹp lung linh, không gian rộng lớn.', '2025-09-01 15:45:10+07', NULL),
        (43, 24, 21, 4, 'Đảo Ti Tốp có bãi tắm đẹp và điểm ngắm cảnh tuyệt vời. Leo lên đỉnh hơi mệt nhưng đáng.', '2025-09-01 14:10:45+07', NULL),
        (44, 25, 22, 5, 'Kinh thành Huế - di sản văn hóa vô giá. Kiến trúc cung đình tinh xảo, lịch sử phong phú.', '2025-09-01 09:35:20+07', NULL),
        (45, 25, 23, 4, 'Rất ấn tượng với quy mô và kiến trúc. Cần nhiều thời gian để tham quan hết.', '2025-09-02 11:50:35+07', NULL),
        (46, 27, 24, 4, 'Lăng Khải Định - phong cách kiến trúc độc đáo pha trộn Đông Tây. Rất đặc biệt.', '2025-09-01 16:25:15+07', NULL),
        (47, 28, 25, 5, 'Lăng Minh Mạng - kiến trúc hài hòa với thiên nhiên. Không gian yên bình, thơ mộng.', '2025-09-01 17:40:30+07', NULL),
        (48, 29, 26, 4, 'Sông Hương thơ mộng, êm đềm. Đi thuyền dragon boat là trải nghiệm tuyệt vời.', '2025-09-01 18:15:25+07', NULL),
        (49, 30, 27, 5, 'Phố cổ Hội An - bảo tàng sống của kiến trúc cổ. Đèn lồng lung linh, không khí cổ kính.', '2025-09-01 19:30:40+07', NULL),
        (50, 30, 28, 5, 'Dạo bộ phố cổ buổi tối thật lãng mạn. Ẩm thực đa dạng, người dân thân thiện.', '2025-09-02 20:45:15+07', NULL),
        (51, 31, 29, 4, 'Chùa Cầu - biểu tượng của Hội An. Nhỏ nhưng rất tinh xảo và có ý nghĩa văn hóa sâu sắc.', '2025-09-01 12:20:30+07', NULL),
        (52, 32, 30, 5, 'Thánh địa Mỹ Sơn - di tích Chăm cổ kính. Kiến trúc độc đáo, giá trị lịch sử cao.', '2025-09-01 10:45:25+07', NULL),
        (53, 33, 31, 5, 'Tràng An - "Hạ Long trên bờ". Cảnh đẹp hùng vĩ, chèo thuyền qua hang động thú vị.', '2025-09-01 13:35:40+07', NULL),
        (54, 33, 32, 4, 'Phong cảnh tuyệt đẹp nhưng tour hơi dài. Nên chuẩn bị nước uống và mũ chống nắng.', '2025-09-02 14:20:15+07', NULL),
        (55, 34, 33, 4, 'Tam Cốc - Bích Động có cảnh đẹp như tranh thủy mặc. Chèo thuyền qua 3 hang động rất thú vị.', '2025-09-01 15:10:30+07', NULL),
        (56, 35, 34, 5, 'Hang Múa - điểm ngắm cảnh Ninh Bình đẹp nhất. Leo 500 bậc thang để có view tuyệt vời.', '2025-09-01 07:25:45+07', NULL),
        (57, 36, 35, 4, 'Chùa Bái Đính - ngôi chùa lớn nhất Việt Nam. Tượng Phật khổng lồ rất ấn tượng.', '2025-09-01 08:40:20+07', NULL),
        (58, 37, 36, 5, 'Phong Nha - Kẻ Bàng - thiên đường của những hang động. Động Thiên Đường thật sự như tên gọi.', '2025-09-01 11:55:35+07', NULL),
        (59, 39, 37, 5, 'Động Thiên Đường - hang động đẹp nhất từng thấy. Thạch nhũ rực rỡ, không gian hùng vĩ.', '2025-09-01 16:30:10+07', NULL),
        (60, 40, 38, 4, 'Fansipan - nóc nhà Đông Dương. Cáp treo hiện đại, view từ đỉnh núi tuyệt đẹp.', '2025-09-01 06:45:25+07', NULL),
        (61, 41, 19, 5, 'Sa Pa - thị trấn trong mây. Khí hậu mát mẻ quanh năm, phong cảnh núi non hùng vĩ.', '2025-09-01 17:20:40+07', NULL),
        (62, 42, 20, 4, 'Bản Cát Cát - làng văn hóa H`Mông. Tìm hiểu được văn hóa dân tộc, thác nước đẹp.', '2025-09-01 14:35:15+07', NULL),
        (63, 43, 21, 5, 'Bãi Sao Phú Quốc - bãi biển đẹp nhất Việt Nam! Cát trắng mịn, nước trong xanh.', '2025-09-01 13:10:30+07', NULL),
        (64, 44, 22, 3, 'Nhà tù Phú Quốc - nơi ghi dấu lịch sử đau thương. Không gian nặng nề nhưng ý nghĩa.', '2025-09-01 10:25:45+07', NULL),
        (65, 45, 23, 4, 'Vườn quốc gia Phú Quốc - đa dạng sinh học phong phú. Trekking trong rừng nguyên sinh thú vị.', '2025-09-01 09:40:20+07', NULL),
        (66, 46, 24, 4, 'Hồ Xuân Hương - trái tim của Đà Lạt. Đạp xe vòng quanh hồ rất thú vị, không khí trong lành.', '2025-09-01 18:55:35+07', NULL),
        (67, 47, 25, 4, 'Thác Datanla - thác nước đẹp với trò trượt cáng thú vị. Phù hợp cho cả gia đình.', '2025-09-01 15:30:10+07', NULL),
        (68, 49, 26, 5, 'Thiền Viện Trúc Lâm - không gian thiền định tuyệt vời. Kiến trúc hài hòa với thiên nhiên.', '2025-09-01 07:15:25+07', NULL),
        (69, 50, 27, 4, 'Thung lũng Tình Yêu - địa điểm lãng mạn cho các cặp đôi. Hoa đẹp, cảnh thơ mộng.', '2025-09-01 16:40:40+07', NULL),
        (70, 51, 28, 5, 'Biển Nha Trang xanh biếc, cát trắng mịn. Nhiều hoạt động thể thao nước hấp dẫn.', '2025-09-01 12:25:15+07', NULL),
        (71, 52, 29, 4, 'Tháp Bà Po Nagar - kiến trúc Chăm cổ kính. View nhìn ra biển Nha Trang tuyệt đẹp.', '2025-09-01 11:10:30+07', NULL),
        (72, 53, 30, 3, 'Hòn Chồng - hòn đá tự nhiên độc đáo. Hơi đông khách, không gian không quá rộng.', '2025-09-01 14:45:45+07', NULL),
        (73, 54, 31, 5, 'VinWonders Nha Trang - công viên giải trí hiện đại. Trò chơi đa dạng, phù hợp mọi lứa tuổi.', '2025-09-01 13:20:20+07', NULL),
        (74, 55, 32, 4, 'Đồi Cát Đỏ Mũi Né - trải nghiệm trượt cát thú vị. Cảnh hoang sơ, ánh sáng đẹp lúc bình minh.', '2025-09-01 05:35:35+07', NULL),
        (75, 56, 33, 4, 'Suối Tiên - dòng suối trong vắt giữa sa mạc. Cảnh tự nhiên độc đáo, không gian yên tĩnh.', '2025-09-01 08:50:10+07', NULL),
        (76, 57, 34, 3, 'Tháp Chăm Pô Sah Inư - di tích lịch sử Chăm. Tuy không lớn nhưng có giá trị văn hóa.', '2025-09-01 15:25:25+07', NULL),
        (77, 58, 35, 5, 'Chợ nổi Cái Răng - nét văn hóa độc đáo của miền Tây. Dậy sớm để thấy chợ tấp nập nhất.', '2025-09-01 05:40:40+07', NULL),
        (78, 59, 36, 4, 'Nhà cổ Bình Thủy - kiến trúc Âu Á độc đáo. Được bảo tồn tốt, có giá trị lịch sử cao.', '2025-09-01 14:15:15+07', NULL),
        (79, 60, 37, 4, 'Thiền viện Trúc Lâm Phương Nam - không gian thanh tịnh. Kiến trúc đẹp, phù hợp tu tâm.', '2025-09-01 07:30:30+07', NULL),
        (80, 61, 38, 5, 'Miếu Bà Chúa Xứ Núi Sam - nơi linh thiêng của An Giang. Lễ hội rất đặc sắc.', '2025-09-01 09:45:45+07', NULL),
        (81, 62, 19, 4, 'Tượng Chúa Kitô Vua Vũng Tàu - tượng Chúa cao nhất châu Á. Leo lên được view toàn cảnh thành phố.', '2025-09-01 16:20:20+07', NULL),
        (82, 64, 20, 4, 'Eo Gió Quy Nhơn - điểm ngắm cảnh tuyệt đẹp. Sóng vỗ vào bờ đá, cảnh hoang sơ hùng vĩ.', '2025-09-01 17:35:35+07', NULL),
        (83, 65, 21, 3, 'Làng Cà phê Trung Nguyên - tìm hiểu về văn hóa cà phê Việt Nam. Hơi thương mại hóa.', '2025-09-01 13:50:10+07', NULL),
        (84, 66, 22, 4, 'Di tích Đồi A1 Điện Biên - nơi ghi dấu chiến thắng lịch sử. Có ý nghĩa giáo dục cao.', '2025-09-01 10:05:25+07', NULL),
        (85, 67, 23, 5, 'Vườn quốc gia Tràm Chim - thiên đường của các loài chim. Mùa nước nổi rất đẹp.', '2025-09-01 06:20:40+07', NULL),
        (86, 68, 24, 4, 'Cột cờ Lũng Cú - điểm cực Bắc của Tổ quốc. Cảm giác tự hào khi đứng ở đây.', '2025-09-01 11:35:15+07', NULL),
        (87, 69, 25, 3, 'Biển Đồ Sơn khá đông đúc vào mùa hè. Tuy nhiên có nhiều hoạt động giải trí.', '2025-09-01 14:50:30+07', NULL),
        (88, 70, 26, 5, 'Quần đảo Cát Bà - viên ngọc của vịnh Lan Hạ. Biển đẹp, rừng nguyên sinh phong phú.', '2025-09-01 08:05:45+07', NULL),
        (89, 71, 27, 3, 'Thủy điện Hòa Bình - công trình thủy lợi quan trọng. Tuy nhiên không có nhiều điểm tham quan.', '2025-09-01 15:20:20+07', NULL),
        (90, 72, 28, 5, 'Làng Sen - quê hương Bác Hồ. Không gian giản dị, bình yên. Rất có ý nghĩa giáo dục.', '2025-09-01 09:35:35+07', NULL),
        (91, 73, 29, 4, 'Ghềnh Đá Đĩa - kỳ quan địa chất độc đáo. Những cột đá basalt tự nhiên rất ấn tượng.', '2025-09-01 12:50:10+07', NULL),
        (92, 74, 30, 4, 'Đảo Lý Sơn - "Maldives của Việt Nam". Biển xanh, cát trắng, tỏi Lý Sơn thơm ngon.', '2025-09-01 10:25:25+07', NULL),
        (93, 75, 31, 5, 'Địa đạo Vĩnh Mốc - minh chứng sức mạnh của ý chí. Hệ thống đường hầm phức tạp.', '2025-09-01 13:40:40+07', NULL),
        (94, 76, 32, 4, 'Tòa thánh Cao Đài - tìm hiểu tôn giáo Cao Đài độc đáo. Kiến trúc đặc biệt.', '2025-09-01 11:15:15+07', NULL),
        (95, 77, 33, 4, 'Thành nhà Hồ - di sản thế giới. Kiến trúc đá độc đáo thời nhà Hồ.', '2025-09-01 16:30:30+07', NULL),
        (96, 78, 34, 4, 'Chùa Vĩnh Tràng - ngôi chùa cổ kính ở Mỹ Tho. Kiến trúc Khmer độc đáo, không gian yên tĩnh.', '2025-09-01 14:45:45+07', NULL),
        (97, 79, 35, 5, 'Tam Đảo - "Đà Lạt của miền Bắc". Khí hậu mát mẻ, cảnh núi non hùng vĩ, thích hợp nghỉ dưỡng.', '2025-09-01 08:20:20+07', NULL),
        (98, 80, 36, 4, 'Hồ Ba Bể - hồ nước ngọt tự nhiên lớn nhất Việt Nam. Cảnh đẹp hoang sơ, chèo thuyền thú vị.', '2025-09-01 12:35:35+07', NULL),
        (99, 81, 37, 4, 'Làng gốm Bát Tràng - làng nghề truyền thống 700 năm tuổi. Được xem thợ làm gốm và mua sản phẩm.', '2025-09-01 15:50:10+07', NULL),
        (100, 82, 38, 3, 'Chợ Lớn - khu người Hoa lớn nhất TP.HCM. Đông đúc, ồn ào nhưng có nhiều món ăn ngon.', '2025-09-01 18:25:25+07', NULL),
        (101, 84, 19, 5, 'Bãi biển An Bàng - bãi biển đẹp nhất Hội An. Cát trắng mịn, nước trong xanh, sóng nhẹ.', '2025-09-01 11:40:40+07', NULL),
        (102, 85, 20, 4, 'Cầu Trường Tiền - biểu tượng của Huế. Đi bộ trên cầu ngắm sông Hương rất thơ mộng.', '2025-09-01 17:15:15+07', NULL),
        (103, 86, 21, 4, 'Mũi Cà Mau - cực Nam Tổ quốc. Cảnh hoang sơ, có ý nghĩa đặc biệt về mặt địa lý.', '2025-09-01 14:30:30+07', NULL),
        (104, 87, 22, 4, 'Dinh Bảo Đại - cung điện mùa hè của vua cuối cùng. Kiến trúc Pháp, nội thất cổ điển.', '2025-09-01 13:45:45+07', NULL),
        (105, 88, 23, 3, 'Cửa khẩu Móng Cái - cửa ngõ ra Trung Quốc. Khá đông đúc, thích hợp mua sắm.', '2025-09-01 10:20:20+07', NULL),
        (106, 89, 24, 5, 'Cao nguyên đá Đồng Văn - di sản địa chất thế giới. Cảnh quan độc đáo, văn hóa dân tộc đặc sắc.', '2025-09-01 07:35:35+07', NULL),
        (107, 90, 25, 4, 'Đèo Ô Quy Hồ - một trong tứ đại đỉnh đèo. Cảnh núi non hùng vĩ, đường đi khá khó khăn.', '2025-09-01 09:50:10+07', NULL),
        (108, 91, 26, 5, 'Thác Bản Giốc - thác nước biên giới đẹp nhất Việt Nam. Nước đổ hùng vĩ, cảnh quan tuyệt đẹp.', '2025-09-01 12:25:25+07', NULL),
        (109, 92, 27, 4, 'Nhà hát Lớn Hà Nội - kiến trúc Pháp cổ điển tuyệt đẹp. Biểu diễn nghệ thuật chất lượng cao.', '2025-09-01 19:40:40+07', NULL),
        (110, 93, 28, 4, 'Chùa Thiên Hậu - ngôi chùa của người Hoa ở Chợ Lớn. Kiến trúc đặc trưng, nhiều tượng thần.', '2025-09-01 16:15:15+07', NULL),
        (111, 94, 29, 3, 'Asia Park - công viên giải trí với cầu Vàng mini. Vui nhưng không bằng cầu Vàng thật ở Bà Nà.', '2025-09-01 14:50:30+07', NULL),
        (112, 96, 30, 4, 'Viện Hải dương học - tìm hiểu về đời sống biển. Trưng bày phong phú, có ý nghĩa khoa học.', '2025-09-01 11:05:45+07', NULL),
        (113, 97, 31, 5, 'Cố đô Hoa Lư - kinh đô đầu tiên của Việt Nam. Di tích lịch sử quan trọng, cảnh đẹp.', '2025-09-01 15:20:20+07', NULL),
        (114, 98, 32, 4, 'Chùa Dơi - ngôi chùa độc đáo với hàng nghìn con dơi. Kiến trúc Khmer đặc sắc.', '2025-09-01 08:35:35+07', NULL),
        (115, 99, 33, 5, 'Hoàng thành Thăng Long - di sản thế giới ở Hà Nội. Khảo cổ học quan trọng, giá trị lịch sử cao.', '2025-09-01 13:10:10+07', NULL),
        (116, 100, 34, 4, 'Hồ Ba Bể - hồ nước ngọt tự nhiên lớn nhất VN. Cảnh đẹp hoang sơ, thích hợp nghỉ dưỡng.', '2025-09-01 10:45:25+07', NULL);
    """)

    # Set sequence for feedbacks table
    op.execute("SELECT setval('feedbacks_id_seq', 117, false);")


def downgrade() -> None:
    # Delete the inserted feedbacks
    op.execute("DELETE FROM feedbacks WHERE id BETWEEN 1 AND 116;")
    # Reset sequence to the maximum ID or 1 if no records remain
    op.execute("SELECT setval('feedbacks_id_seq', (SELECT COALESCE(MAX(id), 1) FROM feedbacks), false);")
