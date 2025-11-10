import fitz  # PyMuPDF
import docx2txt
import requests
from bs4 import BeautifulSoup
import yt_dlp
import pandas as pd

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        text = ""
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text

    elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        return docx2txt.process(uploaded_file)

    elif uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")

    elif uploaded_file.type in [
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ]:
        try:
            df = pd.read_excel(uploaded_file, dtype=str)
            text = "\n".join(df.fillna("").apply(lambda row: " ".join(row), axis=1))
            return text
        except Exception as e:
            return f"⚠️ Error reading Excel file: {str(e)}"

    return ""


def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = [p.get_text() for p in soup.find_all("p")]
    return "\n".join(paragraphs)


def extract_text_from_youtube(url):
    ydl_opts = {"skip_download": True, "writeinfojson": False}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    transcript = info.get("description", "")
    return transcript
