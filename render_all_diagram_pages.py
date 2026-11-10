import os, sys, pymupdf

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = "downloads/ReadMath_2025수능킬러_변형24제_N제.pdf"
out_dir = "rendered_pages"
os.makedirs(out_dir, exist_ok=True)

doc = pymupdf.open(pdf_path)
print(f"Total pages: {len(doc)}")

# Solution pages are 7 through 18 (Solutions 1 to 24)
for pno in range(7, 19):
    page = doc[pno - 1]
    pix = page.get_pixmap(dpi=150)
    out_path = os.path.join(out_dir, f"page_{pno}.png")
    pix.save(out_path)
    print(f"Rendered Page {pno} (Solutions { (pno-7)*2 + 1 } ~ { (pno-7)*2 + 2 }) -> {out_path} ({os.path.getsize(out_path)} bytes)")

print("\nAll 12 solution pages (24 diagrams) successfully rendered to PNG.")
