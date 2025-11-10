import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

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
