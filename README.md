# 🤖 AI Chat Assistant – Chat | Tóm tắt bài báo | Hỏi đáp file PDF

Ứng dụng web tích hợp 3 tính năng thông minh:
- 💬 Chatbot GPT-3.5 (qua OpenRouter)
- 📰 Đọc hỏi đáp trên nội dung từ đường dẫn bài báo (URL)
- 📄 Hỏi đáp dựa trên nội dung file PDF người dùng tải lên

> Xây dựng bằng Python + Gradio + OpenRouter API + OpenAI SDK + BeautifulSoup + PyPDF2

---

## 🚀 Demo tính năng

- **Chat bình thường với AI**: Chat với GPT-3.5 thông qua OpenRouter.
- **Gửi link bài báo (URL)**: AI sẽ tự động lấy nội dung bài viết và trả lời dựa trên câu hỏi của bạn.
- **Tải file PDF**: Trợ lý AI sẽ đọc toàn bộ nội dung PDF và giúp bạn trả lời các câu hỏi liên quan.

---

## 🧱 Công nghệ sử dụng

- 🐍 Python
- 🌐 [Gradio](https://www.gradio.app/) – giao diện web đơn giản
- 🧠 OpenRouter (thay OpenAI trực tiếp, không cần thẻ)
- 📄 `PyPDF2` – trích xuất nội dung từ file PDF
- 📰 `BeautifulSoup4` – đọc nội dung HTML bài báo/blog

---

## 📦 Cài đặt

### 1. Clone dự án hoặc tải dự án và tạo môi trường ảo:
```bash
git clone https://github.com/kukientinhky/chat_bot.git hoặc tải trưc tiếp.
cd CHAT_BOT
conda create --name my_env python==3.9
conda activate my_env
pip install -r requirement.txt
python chat_bot.py
click vào link: http://127.0.0.1:7860

```
link demo: 

