
# import streamlit as st
# import os
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# import io
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet

# from pypdf import PdfReader
# from PIL import Image
# import easyocr
# import numpy as np

# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.vectorstores import FAISS
# from langchain.embeddings import HuggingFaceEmbeddings

# @st.cache_resource(show_spinner=False)
# def load_ocr():
#     return easyocr.Reader(['en'])

# reader = load_ocr()

# st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

# st.markdown("""
# <style>
# .stApp {
#     background: linear-gradient(135deg, #1a102a, #2a1b3d, #3b2a5a);
#     color: #f5f3ff;
# }

# [data-testid="stSidebar"] {
#     background: #1a102a !important;
# }

# section[data-testid="stChatInput"] textarea {
#     background: #2a1b3d !important;
#     color: #f5f3ff !important;
#     border: 1px solid #6b5ca5 !important;
# }
# </style>
# """, unsafe_allow_html=True)


# load_dotenv()
# api_key = os.getenv("GROQ_API_KEY")

# if not api_key:
#     st.error("Missing API key")
#     st.stop()

# def generate_pdf(history):
#     buffer = io.BytesIO()
#     doc = SimpleDocTemplate(buffer)
#     styles = getSampleStyleSheet()
#     elements = []

#     for chat in history:
#         elements.append(Paragraph(f"<b>User:</b> {chat['question']}", styles["Normal"]))
#         elements.append(Spacer(1, 8))
#         elements.append(Paragraph(f"<b>Assistant:</b> {chat['answer']}", styles["Normal"]))
#         elements.append(Spacer(1, 12))

#     doc.build(elements)
#     buffer.seek(0)
#     return buffer

# def extract_text(file):
#     text = ""
#     if file.type == "application/pdf":
#         pdf = PdfReader(file)
#         for page in pdf.pages:
#             text += page.extract_text() or ""
#     elif "image" in file.type:
#         image = Image.open(file)
#         result = reader.readtext(np.array(image))
#         text = " ".join([r[1] for r in result])
#     return text

# def create_vector_store(text):
#     splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
#     chunks = splitter.split_text(text)
#     embeddings = HuggingFaceEmbeddings()
#     return FAISS.from_texts(chunks, embeddings)

# @st.cache_resource(show_spinner=False)
# def cached_vector_store(text):
#     return create_vector_store(text)

# if "history" not in st.session_state:
#     st.session_state.history = []
# if "current_chat" not in st.session_state:
#     st.session_state.current_chat = []
# if "vector_store" not in st.session_state:
#     st.session_state.vector_store = None
# if "last_file" not in st.session_state:
#     st.session_state.last_file = None

# llm = ChatGroq(
#     temperature=0.7,
#     model="llama-3.1-8b-instant",
#     api_key=api_key
# )

# user_input = st.chat_input("Ask something...")

# if user_input:
#     question = user_input.lower()

#     if any(word in question for word in ["short", "brief", "briefly"]):
#         style_instruction = "Answer in very short 2-3 lines."
#     elif any(word in question for word in ["detailed", "explain", "in detail", "deep"]):
#         style_instruction = "Give a detailed and well-explained answer."
#     else:
#         style_instruction = "Answer normally in a balanced way."

#     if st.session_state.vector_store:
#         docs = st.session_state.vector_store.similarity_search(question, k=3)
#         context = "\n".join([d.page_content for d in docs])
#     else:
#         context = ""

#     prompt = f"""
# You are a helpful AI assistant.

# {style_instruction}

# Context:
# {context}

# Question:
# {question}
# """

#     answer = llm.invoke(prompt).content

#     st.session_state.history.append({"question": question, "answer": answer})
#     st.session_state.current_chat = [{"question": question, "answer": answer}]

# st.markdown("<h1 style='text-align:center;'>🤖 Nexa AI</h1>", unsafe_allow_html=True)

# for chat in st.session_state.current_chat:
#     st.chat_message("user").write(chat["question"])
#     st.chat_message("assistant").write(chat["answer"])

# with st.sidebar:
#     st.title("📜 Chat History")
#     st.markdown("---")

#     uploaded_file = st.file_uploader("📄 Upload file")

#     if uploaded_file:
#         if st.session_state.last_file != uploaded_file.name:
#             st.session_state.last_file = uploaded_file.name

#             # ✅ NEW CLEAN LOADING UI
#             progress = st.progress(0)
#             status_text = st.empty()

#             status_text.markdown("📄 **Processing your document...**")

#             progress.progress(30)
#             text = extract_text(uploaded_file)

#             progress.progress(70)
#             st.session_state.vector_store = cached_vector_store(text)

#             progress.progress(100)
#             status_text.markdown("✅ **Document ready!**")

#             progress.empty()
#             status_text.empty()

#     st.markdown("---")

#     for i, item in enumerate(reversed(st.session_state.history)):
#         if st.button(item["question"][:40], key=f"hist_{i}"):
#             st.session_state.current_chat = [item]
#             st.rerun()

#     st.markdown("---")

#     if st.button("🧹 Clear Chat"):
#         st.session_state.history = []
#         st.session_state.current_chat = []
#         st.session_state.vector_store = None
#         st.session_state.last_file = None
#         st.cache_resource.clear()
#         st.rerun()

#     st.download_button("📥 Download Chat", generate_pdf(st.session_state.history), "chat.pdf")

# #=============================
#     # Footer
# #=============================
# st.markdown("""
# <hr>
# <p style='text-align:center; font-size:14px;'>
# Built with ❤️ using Streamlit | AI Chatbot
# </p>
# """, unsafe_allow_html=True)


#==========================================================================================================
                 #New code
#==========================================================================================================

import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from pypdf import PdfReader
from PIL import Image
import requests   # ✅ NEW (for OCR API)

# ==============================
# 🎨 UI CONFIG (SAME)
# ==============================
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1a102a, #2a1b3d, #3b2a5a);
    color: #f5f3ff;
}

[data-testid="stSidebar"] {
    background: #1a102a !important;
}

section[data-testid="stChatInput"] textarea {
    background: #2a1b3d !important;
    color: #f5f3ff !important;
    border: 1px solid #6b5ca5 !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# 🔐 API KEY
# ==============================
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Missing API key")
    st.stop()

# ==============================
# 📄 PDF GENERATOR (SAME)
# ==============================
def generate_pdf(history):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    for chat in history:
        elements.append(Paragraph(f"<b>User:</b> {chat['question']}", styles["Normal"]))
        elements.append(Spacer(1, 8))
        elements.append(Paragraph(f"<b>Assistant:</b> {chat['answer']}", styles["Normal"]))
        elements.append(Spacer(1, 12))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# ==============================
# 📄 TEXT EXTRACTION (UPDATED)
# ==============================
def extract_text(file):
    text = ""

    # ✅ PDF
    if file.type == "application/pdf":
        pdf = PdfReader(file)
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    # ✅ IMAGE / SCREENSHOT (OCR API)
    elif "image" in file.type:
        try:
            response = requests.post(
                "https://api.ocr.space/parse/image",
                files={"file": file},
                data={"apikey": "helloworld"}  # free demo key
            )

            result = response.json()

            if result.get("ParsedResults"):
                text = result["ParsedResults"][0]["ParsedText"]
            else:
                text = "No readable text found in image."

        except Exception as e:
            text = f"OCR failed: {str(e)}"

    # ✅ fallback
    if not text.strip():
        text = "No text could be extracted from the file."

    return text

# ==============================
# 🧠 SESSION STATE (SAME)
# ==============================
if "history" not in st.session_state:
    st.session_state.history = []
if "current_chat" not in st.session_state:
    st.session_state.current_chat = []
if "doc_text" not in st.session_state:
    st.session_state.doc_text = ""
if "last_file" not in st.session_state:
    st.session_state.last_file = None

# ==============================
# 🤖 LLM (SAME)
# ==============================
llm = ChatGroq(
    temperature=0.7,
    model_name="llama-3.1-8b-instant",
    groq_api_key=api_key
)

# ==============================
# 💬 CHAT INPUT
# ==============================
user_input = st.chat_input("Ask something...")

if user_input:
    question = user_input.lower()

    if any(word in question for word in ["short", "brief"]):
        style_instruction = "Answer in very short 2-3 lines."
    elif any(word in question for word in ["detailed", "explain", "deep"]):
        style_instruction = "Give a detailed and well-explained answer."
    else:
        style_instruction = "Answer normally."

    context = st.session_state.doc_text

    prompt = f"""
You are a helpful AI assistant.

{style_instruction}

Context:
{context}

Question:
{question}
"""

    answer = llm.invoke(prompt).content

    st.session_state.history.append({"question": question, "answer": answer})
    st.session_state.current_chat = [{"question": question, "answer": answer}]

# ==============================
# 🖥️ MAIN UI (SAME)
# ==============================
st.markdown("<h1 style='text-align:center;'>🤖 Nexa AI</h1>", unsafe_allow_html=True)

for chat in st.session_state.current_chat:
    st.chat_message("user").write(chat["question"])
    st.chat_message("assistant").write(chat["answer"])

# ==============================
# 📂 SIDEBAR (SAME STRUCTURE)
# ==============================
with st.sidebar:
    st.title("📜 Chat History")
    st.markdown("---")

    uploaded_file = st.file_uploader("📄 Upload file")

    if uploaded_file:
        if st.session_state.last_file != uploaded_file.name:
            st.session_state.last_file = uploaded_file.name

            progress = st.progress(0)
            status_text = st.empty()

            status_text.markdown("📄 **Processing your document...**")

            progress.progress(50)
            text = extract_text(uploaded_file)

            progress.progress(100)
            st.session_state.doc_text = text

            status_text.markdown("✅ **Document ready!**")

            progress.empty()
            status_text.empty()

    st.markdown("---")

    for i, item in enumerate(reversed(st.session_state.history)):
        if st.button(item["question"][:40], key=f"hist_{i}"):
            st.session_state.current_chat = [item]
            st.rerun()

    st.markdown("---")

    if st.button("🧹 Clear Chat"):
        st.session_state.history = []
        st.session_state.current_chat = []
        st.session_state.doc_text = ""
        st.session_state.last_file = None
        st.rerun()

    st.download_button("📥 Download Chat", generate_pdf(st.session_state.history), "chat.pdf")

# ==============================
# Footer (SAME)
# ==============================
st.markdown("""
<hr>
<p style='text-align:center; font-size:14px;'>
Built with ❤️ using Streamlit | AI Chatbot
</p>
""", unsafe_allow_html=True)