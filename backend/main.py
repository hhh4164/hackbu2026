import pymupdf.layout
import pymupdf4llm
import pathlib
import ftfy
import os
from dotenv import load_dotenv
from google import genai

from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser


input = "backend/sample.pdf"
#input -> md
md_text = pymupdf4llm.to_markdown(
    input, 
    show_progress = False, 
    write_images=False,
    use_ocr=False
)
#clean
fixed = ftfy.fix_text(md_text)

parser = PlaintextParser.from_string(fixed, Tokenizer("english"))
summarize = LsaSummarizer()
summary_sentences = summarize(parser.document, 10)
final = "".join([str(sentence) for sentence in summary_sentences])
print(final)


#gemini
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
#client = genai.Client(api_key = api_key)

#response = client.models.generate_content(
#    model = "gemini-3-flash-preview",
#   contents = "whats the weather like today?"
#)
#print(response.text)
