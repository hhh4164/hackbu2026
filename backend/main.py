import pymupdf.layout
import pymupdf4llm
import ftfy
import os
import nltk
import shutil
import uuid
from dotenv import load_dotenv
from google import genai
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse, JSONResponse
from util import redact_text, parse_ai, highlight_points
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
nltk.download('punkt')
nltk.download('punkt_tab')

client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# configure cors
origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],          
    allow_headers=["*"], 
)

pdf_dict = {}

@app.post("/audit")
async def audit(file: UploadFile = File(...), type: str = Form(...)):
    original_pdf = await file.read()
    await file.seek(0)

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
        if type == "contract":
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
        else:
            prompt = (
                "You are a medical billing advocate and auditor. Analyze the following medical bill summary "
                "and identify errors, overcharges, or suspicious items that patients should dispute or question. "
                "First, generate a concise 2-sentence summary of the bill: what it is for and the total amount owed. Append this summary with '~' "
                "Secondly, for each issue found, you MUST find a direct, verbatim quote from the text as evidence. "
                "Look specifically for: duplicate charges, upcoded procedures, unbundled services, charges for services not rendered, "
                "inflated costs compared to standard rates, and unclear or missing itemization. "
                "STRICT OUTPUT FORMAT: "
                "Problem ; Recommended Action ; Direct Quote \n"
                "Separate each issue block with pipe '|' "
                "EXAMPLE: \n"
                "This is a bill for a routine ER visit totaling $4,200. Several charges appear inflated or duplicated. "
                "~ Duplicate Lab Fee ; Request itemized bill and dispute the repeated charge ; CBC Blood Test $220, CBC Blood Test $220 "
                "| Upcoded ER Visit Level ; Ask hospital to review visit complexity rating ; Emergency Room Level 5 - $3,200 "
                f"Summary to analyze: {final}"
            )
        response = client.models.generate_content(
            model = "gemini-3-flash-preview",
            contents = prompt)
        
        final_summary, parsed = parse_ai(response.text)

        highlighted_pdf = highlight_points(original_pdf, parsed)

        file_id = str(uuid.uuid4())
        pdf_dict[file_id] = highlighted_pdf

        return {
            "filename": file.filename,
            "summary": final_summary,
            "gemini_response": parsed,
            "pdf_url": f"/download/{file_id}"
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(path):
            os.remove(path)

@app.get("/download/{file_id}")
async def download_pdf(file_id: str):
    if file_id in pdf_dict:
        highlighted_pdf = pdf_dict[file_id]
        highlighted_pdf.seek(0)

        return StreamingResponse(
            highlighted_pdf,
            media_type="application/pdf",
            headers={"Content-Disposition": f'inline; filename="audit_{file_id}.pdf"'}
        )
    return JSONResponse(
        content={"message": "File not found"}
    )
