import re 
import scrubadub

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

        (r"\d{3,5}\s+[A-Za-z09\s\.]+?\s+(?:Street|St|Ave|Avenue|Road|Rd|Boulevard|Blvd|Drive|Dr|Parkway|Pwky)\.?,?\s+[A-Za-z0-9\s\.]+,?\s+[A-Z]{2}\s+\d{5}", r"[REDACTED ADDRESS]"),
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
