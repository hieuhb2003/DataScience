import re
import json
# from prompts import TABLE_INFO
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
def string_to_json(string):
    string = string.replace('\n', '').replace('\r', '')
    matches_json = re.findall(r'\{.*?\}', string, re.DOTALL)
    for match_mini in matches_json:
        try:
            match_mini = json.loads(match_mini)
            return match_mini
        except:
            return match_mini

def build_history(history):
    if len(history) > 3:
        short_history = history[-3:]
    else:
        short_history = history
    history_str = ""
    for human, assistant in short_history:
        history_str += f"User: {human}\nAssistant: {assistant}\n"
    return history_str

def format_image_links(text):
    return re.sub(
        r'(!\[screenshot\]\(.*?\))',
        lambda m: m.group(1).replace(" ", "%20").replace("#","%23"),
        text
    )

def process_question_with_history(question, history, llm, new_question_prompt):
    response = llm.invoke(
        new_question_prompt.format(
            history=history,
            question=question
        )
    ).content
    
    new_question = string_to_json(response)
    return str(new_question["new_question"])

def build_final_context(sql_context):
    return (
        "Dưới đây là kết quả tìm kiếm của công cụ SQL: \n" +
        sql_context +
        "\n\n" +
        TABLE_INFO +
        "Có thể có một số sản phẩm trùng lặp không được phép giới thiệu 2 sản phẩm có thông số giống hệt nhau"
    )