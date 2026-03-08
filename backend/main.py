import pymupdf.layout
import pymupdf4llm
import ftfy
import os
import nltk
import shutil
from dotenv import load_dotenv
from google import genai
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from fastapi import FastAPI, UploadFile, File
from redactor import redact_text

load_dotenv()
nltk.download('punkt')
nltk.download('punkt_tab')

client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))

app = FastAPI()
@app.post("/audit")
async def audit(file: UploadFile = File(...)):
    path = f"temp_{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        #input -> md 
        md_text = pymupdf4llm.to_markdown(
        path, 
        show_progress = False, 
        write_images=False,
        use_ocr=False
        )
        #clean+summarize
        fixed = ftfy.fix_text(md_text)
        redacted_text = redact_text(fixed)
        parser = PlaintextParser.from_string(redacted_text, Tokenizer("english"))
        summarize = LsaSummarizer()
        summary_sentences = summarize(parser.document, 10)
        final = "".join([str(sentence) for sentence in summary_sentences])
        print(final)

        #gemini
        response = client.models.generate_content(
            model = "gemini-3-flash-preview",
            contents = "whats the weather like today?")
        
        return {
            "filename": file.filename,
            "summary": final,
            "gemini_response": response.text if response.text else "error failed"
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(path):
            os.remove(path)



