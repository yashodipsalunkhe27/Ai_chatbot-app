import streamlit as st

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from pypdf import PdfReader
import requests

# ==============================
# UI (UNCHANGED)
# ==============================
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
# API KEY
# ==============================
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Missing API key")
    st.stop()

# ==============================
# SESSION STATE
# ==============================
if "history" not in st.session_state:
    st.session_state.history = []

if "current_chat" not in st.session_state:
    st.session_state.current_chat = []

if "doc_text" not in st.session_state:
    st.session_state.doc_text = ""

if "last_file" not in st.session_state:
    st.session_state.last_file = None

if "doc_loaded" not in st.session_state:
    st.session_state.doc_loaded = False

if "file_reset" not in st.session_state:
    st.session_state.file_reset = False

# ==============================
# TEXT EXTRACTION
# ==============================
def extract_text(file):
    text = ""

    if file.type == "application/pdf":
        pdf = PdfReader(file)
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    elif "image" in file.type:
        try:
            response = requests.post(
                "https://api.ocr.space/parse/image",
                files={"file": file},
                data={"apikey": "helloworld"}
            )
            result = response.json()

            if result.get("ParsedResults"):
                text = result["ParsedResults"][0]["ParsedText"]
        except Exception:
            text = ""

    return text.strip()

# ==============================
# RAG RETRIEVAL
# ==============================
def get_relevant_chunks(text, query, chunk_size=500, top_k=4):
    words = query.lower().split()

    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    scored = []
    for chunk in chunks:
        score = sum(1 for w in words if w in chunk.lower())
        scored.append((score, chunk))

    scored.sort(reverse=True, key=lambda x: x[0])

    return "\n".join([c[1] for c in scored[:top_k]])

# ==============================
# PDF GENERATOR
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
# LLM
# ==============================
llm = ChatGroq(
    temperature=0.7,
    model_name="llama-3.1-8b-instant",
    groq_api_key=api_key
)

# ==============================
# UI HEADER
# ==============================
st.markdown("<h1 style='text-align:center;'>🤖 Nexa AI</h1>", unsafe_allow_html=True)

for chat in st.session_state.current_chat:
    st.chat_message("user").write(chat["question"])
    st.chat_message("assistant").write(chat["answer"])

# ==============================
# SIDEBAR (FIXED - SINGLE BLOCK ONLY)
# ==============================
with st.sidebar:
    st.title("📜 Chat History")
    st.markdown("---")

    uploaded_file = st.file_uploader("📄 Upload file")

    if st.session_state.file_reset:
        uploaded_file = None
        st.session_state.file_reset = False

    if uploaded_file:
        if st.session_state.last_file != uploaded_file.name:
            st.session_state.last_file = uploaded_file.name
            st.session_state.doc_loaded = False
            st.session_state.doc_text = ""

        if not st.session_state.doc_loaded:
            with st.spinner("📄 Processing document..."):
                text = extract_text(uploaded_file)
                st.session_state.doc_text = text
                st.session_state.doc_loaded = True

            if text and len(text.strip()) > 20:
                st.success("✅ Document processed successfully")
            else:
                st.warning("⚠️ No readable text found")

    st.markdown("---")

    for i, item in enumerate(reversed(st.session_state.history)):
        if st.button(item["question"][:40], key=f"hist_{i}"):
            st.session_state.current_chat = [item]
            st.rerun()

    st.markdown("---")

    # ✅ ONLY ONE SET OF BUTTONS (FIX)
    if st.button("🧹 Clear Chat"):
        st.session_state.history = []
        st.session_state.current_chat = []
        st.session_state.doc_text = ""
        st.session_state.last_file = None
        st.session_state.doc_loaded = False
        st.rerun()

    st.download_button(
        "📥 Download Chat",
        generate_pdf(st.session_state.history),
        "chat.pdf"
    )

# ==============================
# CHAT INPUT
# ==============================
user_input = st.chat_input("Ask something...")

if user_input:
    question = user_input.lower()
    context = st.session_state.doc_text

    has_doc = context and len(context.strip()) > 50

    if "short" in question:
        style = "Answer in 2-3 lines."
    elif "detailed" in question:
        style = "Give detailed explanation."
    else:
        style = "Answer normally."

    doc_keywords = ["document", "file", "uploaded", "this document", "from document"]
    is_doc_question = any(word in question for word in doc_keywords)

    if has_doc and is_doc_question:
        relevant_context = get_relevant_chunks(context, question)

        prompt = f"""
You are a document QA assistant.

Use ONLY the document below.
If answer is not present say:
"This information is not available in the document."

{style}

DOCUMENT:
{relevant_context}

QUESTION:
{question}
"""
    else:
        prompt = f"""
You are a helpful AI assistant.

Answer using general knowledge.

{style}

QUESTION:
{question}
"""

    answer = llm.invoke(prompt).content

    st.session_state.history.append({"question": question, "answer": answer})
    st.session_state.current_chat.append({"question": question, "answer": answer})

    st.rerun()

# ==============================
# FOOTER
# ==============================
st.markdown("""
<hr>
<p style='text-align:center; font-size:14px;'>
Built with ❤️ using Streamlit | AI Chatbot
</p>
""", unsafe_allow_html=True)