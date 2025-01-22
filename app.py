from src.prompts import MAIN_PROMPT, NEW_QUESTION_PROMPT
# print(MAIN_PROMPT)
import gradio as gr
from src.database import DatabaseManager
from src.embeddings import setup_embeddings
from src.chat_model import setup_chat_model
# app.py continued
from src.utils import (
    build_history, 
    format_image_links, 
    process_question_with_history,
    build_final_context
)

# Setup
db_manager = DatabaseManager()
# retriever = setup_embeddings()
llm = setup_chat_model()

def get_context(question, history):
    new_question = question
    all_question = question
    
    if history != '':
        new_question = process_question_with_history(
            question, 
            history, 
            llm, 
            NEW_QUESTION_PROMPT
        )
        all_question = f"{new_question}\n{question}"
    
    # Get SQL context
    sql_context = db_manager.get_context_sql(all_question, llm)
    
    return build_final_context(sql_context)

def predict(message, history):
    history_str = build_history(history) if history else ""
    context = get_context(message, history_str)
    
    messages = [{
        "role": "user",
        "content": MAIN_PROMPT.format(
            context=context,
            question=message,
            history=history_str
        )
    }]
    
    response = llm.stream(messages)
    partial_message = ""
    
    for chunk in response:
        if chunk.content is not None:
            partial_message = partial_message + chunk.content
            yield format_image_links(partial_message)

if __name__ == "__main__":
    gr.ChatInterface(predict).launch(
        server_name="0.0.0.0",
        server_port=7860,
        debug=True,
        share=True
    )
