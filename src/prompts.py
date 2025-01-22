MAIN_PROMPT = '''
Bạn là chuyên gia tư vấn bán hàng, Hãy trả lời một cách tự nhiên với vai trò như là một nhân viên bán hàng, Có đưa kèm link amazone của sản phẩm đó
Mỗi khi đưa ra sản phẩm phải có kèm hình ảnh trong một dòng mới
Dưới đây là một số thông tin có thể liên quan đến câu hỏi của người dùng
DATA:
{context}
-------------
{history}
User: {question}
Hãy tư vấn và trả lời cho bằng tiếng việt. Nếu DATA không có thông tin liên quan, trả lời người dùng là "Xin lỗi, tôi không có thông tin về sản phẩm này"
'''

NEW_QUESTION_PROMPT = '''
Bạn có nhiệm vụ viết lại câu hỏi của người dùng để tạo ra một câu hỏi mới có ý nghĩa đầy đủ mà không dựa vào lịch sử trò chuyện trước đó.
Câu hỏi mới cần được viết bằng tiếng Việt, rõ ràng, dễ hiểu và phải đảm bảo giữ nguyên ý nghĩa của câu hỏi gốc.
Trả về kết quả dưới dạng JSON với cấu trúc như sau:
{{
    "new_question": "<câu hỏi mới>"
}}
History: {history}
Question: {question}
'''

TABLE_INFO = """
Bảng `data_items` chứa thông tin về các laptop với các cột sau:
- BRAND (TEXT): Thương hiệu laptop (ví dụ: Lenovo, ASUS, Acer, Apple, Dell, HP).
- MODEL (TEXT): Mẫu laptop.
- SCREEN_SIZE (FLOAT): Kích thước màn hình tính bằng inch.
- CPU (TEXT): Bộ xử lý (ví dụ: Intel Core i7, M1, Ryzen 5).
- CPU_SPEED (FLOAT): Tốc độ CPU tính bằng GHz.
- RAM (FLOAT): Dung lượng RAM tính bằng GB.
- MEMORY (FLOAT): Dung lượng lưu trữ tính bằng GB.
- GPU (TEXT): Bộ xử lý đồ họa.
- GRAPHICS_CARD_DESCRIPTION (TEXT): Mô tả card đồ họa.
- OPERATING_SYSTEM (TEXT): Hệ điều hành.
- WEIGHT (TEXT): Trọng lượng của laptop.
- PRICE (FLOAT): Giá của laptop tính bằng USD.
- LINK_AMAZON (TEXT): Liên kết sản phẩm trên Amazon.
- WIDTH (FLOAT): Chiều rộng.
- HEIGHT (FLOAT): Chiều cao.
- IMAGE_LINK (TEXT): Liên kết hình ảnh.
"""