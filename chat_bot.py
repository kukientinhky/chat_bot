from openai import OpenAI
import gradio as gr
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import PyPDF2

load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key = os.getenv("OPENROUTER_API_KEY")
    )
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_article_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        selectors = [
            'article',                          # Ưu tiên 1: thẻ <article>
            'div.entry-content',                # WordPress
            'div.fck_detail',                   # VnExpress
            'div.article-body',                 # Forbes
            'div.post-content',                 # Blog cá nhân
            {'name': 'div', 'class': 'content'} # Class chung
        ]

        article = None
        for selector in selectors:
            if isinstance(selector, dict):
                article = soup.find(**selector)
            else:
                article = soup.select_one(selector)
            if article:
                break
            
        paragraphs = article.find_all('p') if article else []
        return "\n".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
    except Exception as e:
        return f"⚠️ Lỗi khi đọc URL: {str(e)}"

def ask_bot(input_text, history, url = None, pdf_file = None):
    print(f"Input: {input_text}, History: {history}, URL: {url}", f"PDF: {pdf_file}")
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for human, ai in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": ai})
    if pdf_file:
        pdf_text = extract_text_from_pdf(pdf_file.name)
        messages.append({
            "role": "user",
            "content": f"This is PDF content:\n{pdf_text}\n\n {messages}"
        })
    elif url and url.strip():
        article_content = extract_article_content(url)
        messages.append({
            "role": "user",
            "content": f"This is url content:\n{article_content}\n\n {messages}"
        })
    else:
        messages.append({"role": "user", "content": input_text})
    response = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
            },
        model="openai/gpt-3.5-turbo",
        messages=messages,
        stream=True
        )
    partial_message = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            partial_message += chunk.choices[0].delta.content
            yield partial_message

with gr.Blocks() as demo:
    url_input = gr.Textbox(label="URL", placeholder="https://...")
    clear_url_btn = gr.Button("🗑️ Xóa URL", variant="secondary", scale=1)
    chat_interface = gr.ChatInterface(
        ask_bot,
        additional_inputs=[url_input, gr.File(
            label="📤 Tải lên PDF (tùy chọn)",
            type="file",
            file_types=[".pdf"],
            height=100
        )]
        
    )
    clear_url_btn.click(
        lambda: "",  
        inputs=None,
        outputs=url_input
    )
demo.queue().launch()