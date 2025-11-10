import streamlit as st
import os
import tempfile
from utils.extractors import extract_text_from_file, extract_text_from_url, extract_text_from_youtube
from utils.rag_engine import build_vectorstore, retrieve_relevant_chunks
from utils.chat_model import chat_with_context
from utils.config import load_model_options
##os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "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")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("🧠 Universal RAG Chatbot")
st.caption("Chat with your documents, websites, YouTube videos, or Excel files")

# Sidebar options
model_choice = st.sidebar.selectbox("Choose LLM", load_model_options())
embedding_choice = st.sidebar.selectbox("Embedding Model", ["OpenAI", "HuggingFace"])
top_k = st.sidebar.slider("Number of relevant chunks", 2, 10, 4)

# File upload
st.markdown("### 📄 Upload or Provide Source")
uploaded_files = st.file_uploader(
    "Upload documents", type=["pdf", "docx", "txt", "xlsx", "xls"], accept_multiple_files=True
)
url_input = st.text_input("🌐 Enter Website or YouTube URL")
audio_file = st.file_uploader("🎧 Upload audio/video", type=["mp3", "wav", "mp4"])

source_text = ""

# Extract text from uploaded files
if uploaded_files:
    with st.spinner("Extracting text from documents..."):
        for file in uploaded_files:
            try:
                text = extract_text_from_file(file)
                if text.strip() == "":
                    st.warning(f"⚠️ Could not extract content from {file.name}")
                else:
                    source_text += text + "\n"
            except Exception as e:
                st.error(f"Error extracting {file.name}: {str(e)}")

# Extract from URL
elif url_input:
    try:
        if "youtube.com" in url_input or "youtu.be" in url_input:
            with st.spinner("Extracting transcript from YouTube..."):
                source_text = extract_text_from_youtube(url_input)
        else:
            with st.spinner("Extracting text from webpage..."):
                source_text = extract_text_from_url(url_input)
    except Exception as e:
        st.error(f"Error extracting from URL: {str(e)}")

# Transcribe audio/video
elif audio_file:
    try:
        with st.spinner("Transcribing audio/video..."):
            tmp_path = os.path.join(tempfile.gettempdir(), audio_file.name)
            with open(tmp_path, "wb") as f:
                f.write(audio_file.getbuffer())
            os.system(f"whisper '{tmp_path}' --model small --output_format txt")
            with open(tmp_path.replace(".mp3", ".txt"), "r") as t:
                source_text = t.read()
    except Exception as e:
        st.error(f"Error transcribing audio/video: {str(e)}")

# Build vectorstore if text extracted
if source_text.strip():
    try:
        st.success("✅ Source text extracted successfully!")
        vectorstore = build_vectorstore(source_text, embedding_choice)
        st.session_state["vectorstore"] = vectorstore
    except Exception as e:
        st.error(f"Error building vectorstore: {str(e)}")

st.divider()
st.markdown("### 💬 Chat Interface")

query = st.text_input("Ask your question:")

if query and "vectorstore" in st.session_state:
    try:
        with st.spinner("Retrieving and generating response..."):
            relevant_chunks = retrieve_relevant_chunks(st.session_state["vectorstore"], query, top_k)
            response, model_used = chat_with_context(query, relevant_chunks, model_choice)

            st.markdown(f"**Model used:** {model_used}")
            st.markdown("**Answer:**")
            st.write(response)

            st.markdown("#### 🔍 Sources")
            for i, s in enumerate(relevant_chunks, 1):
                st.markdown(f"**{i}.** {s[:200]}...")
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
