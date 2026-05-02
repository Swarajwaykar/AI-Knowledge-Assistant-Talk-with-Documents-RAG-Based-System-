import streamlit as st
import time
import tempfile
import os
from src.vectorstore import FaissVectorStore
from src.search import RAGSearch
from langchain_community.document_loaders import PyMuPDFLoader
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Page config (with branding)
st.set_page_config(page_title="AI Knowledge Assistant", page_icon="⚡", layout="wide")

# 🌌 ADVANCED UI + PARTICLES + HOVER
st.markdown("""
<style>

/* 🌌 Background */
html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 20% 20%, #0f172a, #020617);
    color: white;
    overflow: hidden;
}

/* 🌌 Particle container */
.particles {
    position: fixed;
    width: 100%;
    height: 100%;
    z-index: -1;
    top: 0;
    left: 0;
}

/* ✨ Particle */
.particle {
    position: absolute;
    border-radius: 50%;
    background: rgba(0, 245, 255, 0.7);
    box-shadow: 0 0 8px rgba(0, 245, 255, 0.8);
    animation: float ease-in-out infinite;
}

/* 🎞️ Floating motion */
@keyframes float {
    0%   { transform: translate(0px, 0px); }
    25%  { transform: translate(30px, -40px); }
    50%  { transform: translate(-20px, -80px); }
    75%  { transform: translate(40px, -120px); }
    100% { transform: translate(0px, -160px); }
}

/* 💬 Chat bubbles */
.user-bubble {
    background: linear-gradient(135deg, #00f5ff, #00c6ff);
    color: black;
    padding: 10px;
    border-radius: 12px;
    margin-bottom: 8px;
    animation: fadeIn 0.3s ease-in-out;
    transition: 0.3s;
}
.user-bubble:hover {
    transform: scale(1.02);
    box-shadow: 0 0 15px rgba(0,245,255,0.5);
}

.bot-bubble {
    background: rgba(255,255,255,0.08);
    padding: 10px;
    border-radius: 12px;
    margin-bottom: 8px;
    animation: fadeIn 0.3s ease-in-out;
    transition: 0.3s;
}
.bot-bubble:hover {
    transform: scale(1.02);
    box-shadow: 0 0 10px rgba(255,255,255,0.2);
}

/* 🌟 Title */
.title-glow {
    font-size: 36px;
    font-weight: bold;
    text-align: center;
    color: #00f5ff;
    text-shadow: 0px 0px 12px #00f5ff;
}

/* 📦 Feature cards */
.feature-card {
    background: rgba(255,255,255,0.05);
    padding: 8px 15px;
    border-radius: 10px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    transition: 0.3s;
}
.feature-card:hover {
    transform: scale(1.08);
    box-shadow: 0px 0px 20px rgba(0,255,255,0.3);
}

/* 🎞️ Fade animation */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

</style>

<div class="particles">
""" + "".join([
    f'''
    <div class="particle"
        style="
        left:{(i*7)%100}%;
        top:{(i*13)%100}%;
        width:{3 + (i%4)}px;
        height:{3 + (i%4)}px;
        animation-duration:{6 + (i%5)}s;
        animation-delay:{i*0.2}s;
        ">
    </div>
    '''
    for i in range(60)
]) + "</div>"
, unsafe_allow_html=True)

# 🌟 Branding Header
col1, col2 = st.columns([9, 1])

with col1:
    st.markdown('<div class="title-glow">⚡ AI Knowledge Assistant</div>', unsafe_allow_html=True)
    st.caption("Intelligent Document Understanding Engine 🚀")

with col2:
    if st.button("🗑️", help="Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# 🚀 3 SOLID FEATURES
st.markdown("""
<div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap; margin-top:10px;">

<div class="feature-card">🧠 Context-Aware AI</div>
<div class="feature-card">⚡ Semantic Search (FAISS)</div>
<div class="feature-card">📄 Dynamic Document Intelligence</div>

</div>
""", unsafe_allow_html=True)

# 🔥 Load system
@st.cache_resource
def load_system():
    store = FaissVectorStore("faiss_store")
    store.load()
    rag = RAGSearch()
    return store, rag

store, rag = load_system()

# 📤 Upload
uploaded_file = st.file_uploader("📤 Upload a PDF", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    loader = PyMuPDFLoader(tmp_path)
    docs = loader.load()

    st.info("Processing file...")
    store.build_from_documents(docs)
    st.success("✅ File added!")

# 💬 Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# 💬 Display chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

# ⚡ Typing animation
def stream_response(text):
    response = ""
    placeholder = st.empty()

    for word in text.split():
        response += word + " "
        placeholder.markdown(
            f'<div class="bot-bubble">{response}▌</div>',
            unsafe_allow_html=True
        )
        time.sleep(0.02)

    placeholder.markdown(
        f'<div class="bot-bubble">{response}</div>',
        unsafe_allow_html=True
    )

# 💬 Input
query = st.chat_input("Ask something futuristic... 🚀")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    st.markdown(f'<div class="user-bubble">{query}</div>', unsafe_allow_html=True)

    with st.spinner("Thinking... ⚡"):
        answer = rag.search_and_summarize(query)

    stream_response(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

# 🔻 Footer Branding
st.markdown("""
<hr style="border:1px solid rgba(255,255,255,0.1);">

<center>
Built with ❤️ by Swaraj Waykar  
⚡ Powered by RAG + FAISS + LLM
</center>
""", unsafe_allow_html=True)