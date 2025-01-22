import ast
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.vectorstores import FAISS
from src.utils import string_to_json

# Các ví dụ SQL queries
SQL_EXAMPLES = [
    {
        "question": "MacBook Air M1 8GB giá bao nhiêu?",
        "query": "SELECT IMAGE_LINK, LINK_AMAZON, PRICE FROM data_items WHERE BRAND LIKE 'Apple' AND MODEL LIKE '%MacBook Air%' AND CPU LIKE '%M1%' AND RAM LIKE 8;"
    },
    {
        "question": "Laptop Dell có CPU i7 và RAM 16GB nào giá dưới 25 triệu?",
        "query": "SELECT IMAGE_LINK, LINK_AMAZON, BRAND, MODEL, PRICE FROM data_items WHERE BRAND LIKE 'Dell' AND CPU LIKE '%i7%' AND RAM LIKE 16 AND PRICE < 25000000;"
    },
    {
        "question": "Laptop nhẹ dưới 1.5kg có hệ điều hành Windows nào?",
        "query": "SELECT IMAGE_LINK, LINK_AMAZON, BRAND, MODEL, WEIGHT FROM data_items WHERE WEIGHT < 1.5 AND OPERATING_SYSTEM LIKE '%Windows%';"
    },
    {
        "question": "Laptop có màn hình 15.6 inch và GPU NVIDIA giá rẻ nhất?",
        "query": "SELECT IMAGE_LINK, LINK_AMAZON, BRAND, MODEL, PRICE FROM data_items WHERE SCREEN_SIZE LIKE 15.6 AND GPU LIKE '%NVIDIA%' ORDER BY PRICE ASC LIMIT 1;"
    },
    {
        "question": "MacBook nào có CPU M2 và RAM 16GB?",
        "query": "SELECT IMAGE_LINK, LINK_AMAZON, BRAND, MODEL FROM data_items WHERE BRAND LIKE 'Apple' AND CPU LIKE '%M2%' AND RAM LIKE 16;"
    },
    {
        "question": "Laptop ASUS nào có card đồ họa rời và RAM 8GB?",
        "query": "SELECT IMAGE_LINK, LINK_AMAZON, BRAND, MODEL FROM data_items WHERE BRAND LIKE 'ASUS' AND GRAPHICS_CARD_DESCRIPTION LIKE '%rời%' AND RAM LIKE 8;"
    },
    {
        "question": "Laptop Lenovo nào có màn hình 14 inch và CPU Ryzen 5?",
        "query": "SELECT IMAGE_LINK, LINK_AMAZON, BRAND, MODEL FROM data_items WHERE BRAND LIKE 'Lenovo' AND SCREEN_SIZE = 14 AND CPU LIKE '%Ryzen 5%';"
    },
    {
        "question": "Laptop HP với bộ nhớ 512GB và RAM 16GB giá bao nhiêu?",
        "query": "SELECT IMAGE_LINK, LINK_AMAZON, PRICE FROM data_items WHERE BRAND LIKE 'HP' AND MEMORY = 512 AND RAM = 16;"
    },
    {
        "question": "Có laptop nào giá dưới 10 triệu không?",
        "query": "SELECT IMAGE_LINK, LINK_AMAZON, BRAND, MODEL, PRICE FROM data_items WHERE PRICE < 10000000;"
    },
    {
        "question": "Laptop có CPU tốc độ trên 3.0GHz và RAM 32GB?",
        "query": "SELECT IMAGE_LINK, LINK_AMAZON, BRAND, MODEL FROM data_items WHERE CPU_SPEED > 3.0 AND RAM LIKE 32;"
    }

]

class SQLQueryGenerator:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        
        self.example_selector = SemanticSimilarityExampleSelector.from_examples(
            examples=SQL_EXAMPLES,
            embeddings=self.embedding_model,
            vectorstore_cls=FAISS,
            k=3
        )
        
        self.example_prompt = PromptTemplate(
            input_variables=["question", "query"],
            template="Câu hỏi: {question}\nTruy vấn SQL: {query}"
        )
        
        self.few_shot_prompt = FewShotPromptTemplate(
            example_selector=self.example_selector,
            example_prompt=self.example_prompt,
            prefix="Dựa trên các ví dụ dưới đây, hãy viết một truy vấn SQL phù hợp với câu hỏi.",
            suffix="Câu hỏi: {input}\nTruy vấn SQL:",
            input_variables=["input"]
        )
    
    def generate_sql_query(self, question, llm, db):
        formatted_prompt = self.few_shot_prompt.format(input=question)
        
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
    Đưa ra output dưới dạng json như sau:
    {{
        "sql": "<câu sql hoàn chỉnh để truy vấn thông tin theo mục đích câu hỏi>"
    }}
    Nếu câu hỏi không liên quan, trả ra như sau:
    {{
        "sql": "None"
    }}
    Lưu ý:
    - Có thể sẽ có một vài lỗi chính tả, vì vậy hãy sử dụng LIKE thay vì "=" và so sánh theo chữ in thường (LOWER) để truy vấn các trường là TEXT
    ví dụ:
    input: có laptop nào ram 16 gb, CPU Intel Core, giá dưới 600$ không
    output:
    {{
        "sql": "SELECT * FROM data_items WHERE RAM = 16 AND LOWER(CPU) LIKE '%i7%' AND PRICE < 600"
    }}
    -----
"""
        full_prompt = f"{formatted_prompt}\n\n{TABLE_INFO}"
        
        sql_response = llm.invoke(full_prompt).content
        sql_json = string_to_json(sql_response)
        sql = sql_json.get("sql", "None")
        
        if sql == "None":
            return "None"
            
        try:
            rs = db.run(sql)
            data_list = ast.literal_eval(rs)
            
            if len(data_list) > 3:
                data_list = data_list[:3]
                
            if len(data_list[0]) == 16:
                return f'Laptop hãng {data_list[0][0]}, model: {data_list[0][1]}, kích thước màn hình: {data_list[0][2]} Inches, cpu: {data_list[0][3]}, cpu speed: {data_list[0][4]} GHz, ram: {data_list[0][5]} GB, memory: {data_list[0][6]} GB, gpu: {data_list[0][7]}, hệ điều hành: {data_list[0][9]}, nặng: {data_list[0][10]}, giá tiền: {data_list[0][11]}$, link amazon: {data_list[0][12]}, chiều rộng: {data_list[0][13]}, chiều dài: {data_list[0][14]}, link ảnh: {data_list[0][15].replace(" ", "%20").replace("#", "%23")}'
            else:
                return f'SQL: {sql}\nSQL result: {rs}'
            
        except Exception as e:
            return f'Error: {str(e)}'
    