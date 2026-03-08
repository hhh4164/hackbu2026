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
from util import redact_text, parse_ai

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
        summarizer = LsaSummarizer()
        summary_sentences = summarizer(parser.document, 50)
        final = "".join([str(sentence) for sentence in summary_sentences])
        print(final)

        #gemini
        prompt = ("You are a neutral legal auditor focusing on contract risks. Analyze the following summary "
                  "and identify major red flags. First, generate a concise and short summary in a couple sentences of the costs and purpose of the contract. Append this summary with '~'"
                  "Secondly, For each risk, you MUST find direct, verbatim quote from text"
                  "to serve as evidence."
                  "STRICT OUTPUT FORMAT:"
                  "Problem ; Recommended Solution ; Direct Quote \n"
                  "Separate each risk block with pipe '|'"
                  "EXAMPLE: \n"
                  "This is a standard agreement for consulting. It is fair on payment terms ~ Automatic Renewal ; Negotiate 30-day notice ; This agreement automatically renews"
                  f"Summary to analyze:{final}")
        response = client.models.generate_content(
            model = "gemini-3-flash-preview",
            contents = prompt)
        
        final_summary, parsed = parse_ai(response.text)

        return {
            "filename": file.filename,
            "summary": final_summary,
            "gemini_response": parsed
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(path):
            os.remove(path)

