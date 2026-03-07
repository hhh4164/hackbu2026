import pymupdf
from google import genai

def get_text(file):
    try:
        doc = pymupdf.open(file)
        text = ""
        for page in doc:
            text+=page.get_text()
        doc.close()
        return text
    except Exception as e:
        return f"Error: {e}"

extracted = get_text("backend/sample.pdf")


client = genai.Client()

response = client.models.generate_content(
    model = "gemini-3-flash-preview",
   contents = "test"
)

