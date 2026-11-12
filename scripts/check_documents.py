
from pathlib import Path
from pypdf import PdfReader

for folder in Path("data").iterdir():
    if not folder.is_dir():
        continue
    print(f"\n=== {folder.name} ===")
    for file in folder.glob("*.pdf"):
        reader = PdfReader(str(file))
        pages = len(reader.pages)
       
        text = "".join((p.extract_text() or "") for p in reader.pages[:5])
        status = "OK" if len(text) > 200 else "PROBLEM: little or no text (scanned?)"
        print(f"{file.name}: {pages} pages, {len(text)} chars in first 5 pages -> {status}")