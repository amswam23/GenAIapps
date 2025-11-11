import streamlit as st
from langchain_openai import ChatOpenAI
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

try:
    from langchain_ollama import ChatOllama  # Ensure the library is installed and available
except ImportError:
    ChatOllama = None  # Fallback if the library is not available

def load_model(model_name):
    try:
        # Ensure the model is properly loaded
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        return model, tokenizer
    except Exception as e:
        raise RuntimeError(f"Error loading model '{model_name}': {str(e)}")

def chat_with_context(query, context_chunks, llm_choice="gpt-4-turbo"):
    context_text = "\n\n".join(context_chunks)
    prompt = f"""
Answer the user's question using the following context. Be concise and factual.

Context:
{context_text}

Question: {query}
Answer:
"""
    try:
        # Llama 3
        if "llama" in llm_choice.lower():
            if ChatOllama is None:
                raise RuntimeError("ChatOllama is not available. Please install the 'langchain-ollama' library.")
            model_used = "Llama 3 (Ollama)"
            llm = ChatOllama(model="llama3", temperature=0.3)
            response_text = llm.invoke(prompt)

        # OpenAI GPT
        else:
            model_used = llm_choice
            model_name_api = "gpt-4" if "4" in llm_choice else "gpt-3.5-turbo"
            llm = ChatOpenAI(model_name=model_name_api, temperature=0.3)
            response_text = llm.invoke(prompt)

        return response_text, model_used

    except Exception as e:
        st.error(f"LLM error: {str(e)}")
        return f"Error: {str(e)}", llm_choice
