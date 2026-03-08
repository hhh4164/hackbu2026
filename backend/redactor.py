import re 
import scrubadub

def redact_text(text):

    scrubber = scrubadub.Scrubber()
    scrubber.add_detector(scrubadub.detectors.DateOfBirthDetector)
    text = scrubber.clean(text)

    patterns = [
        (r"(Name:\s*)(.+)", r"\1[REDACTED NAME]"),
        (r"(Address:\s*)([\s\S]{1,70})", r"\1[REDACTED ADDRESS]"),
        (r"(Billing Address:\s*)([\s\S]{1,70})", r"\1[REDACTED ADDRESS]")

    ]

    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text