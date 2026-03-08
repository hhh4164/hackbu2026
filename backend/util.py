import re 
import scrubadub
import pymupdf.layout
import pymupdf4llm
import io

def redact_text(text):

    scrubber = scrubadub.Scrubber()
    scrubber.add_detector(scrubadub.detectors.DateOfBirthDetector)
    text = scrubber.clean(text)

    patterns = [
        (r"(Name:\s*)(.+)", r"\1[REDACTED NAME]"),
        (r"(Patient Name:\s*)(.+)", r"\1[REDACTED NAME]"),
        (r"(Patient:\s*)(.+)", r"\1[REDACTED NAME]"),
        (r"(Address:\s*)([\s\S]{1,70})", r"\1[REDACTED ADDRESS]"),
        (r"(Billing Address:\s*)([\s\S]{1,70})", r"\1[REDACTED ADDRESS]"),

        (r"\d{1,5}\s+[A-Za-z0-9\s\.]+?\s+(?:Street|St|Ave|Avenue|Road|Rd|Boulevard|Blvd|Drive|Dr|Parkway|Pkwy)\.?,?\s+[A-Za-z0-9\s\.]+,?\s+[A-Z]{2}\s+\d{5}", "[REDACTED ADDRESS]"),
        (r"P\.?O\.?\s?Box\s\d+", "[REDACTED]")

    ]

    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text

def parse_ai(text):
    if "~" in text:
        summary, audit = text.split("~", 1)
    else:
        summary = ""
        audit = text

    results = []
    blocks = audit.strip().split("|")
    for block in blocks:
        parts = [p.strip() for p in block.split(";")]
        if len(parts)==3:
            results.append({
                "flag": parts[0],
                "solution": parts[1],
                "quote": parts[2]
            })
    return summary.strip(), results

def highlight_points(file, parse_results):
    doc = pymupdf.open(stream=file, filetype="pdf")
    for item in parse_results:
        quote = item.get("quote")
        if not quote:
            continue
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            rl = page.search_for(quote, quads=True)
            if rl:
                page.add_highlight_annot(rl)
    output_stream = io.BytesIO()
    doc.save(output_stream)
    doc.close()
    output_stream.seek(0)
    return output_stream


    
