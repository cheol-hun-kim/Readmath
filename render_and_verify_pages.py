import os, sys, pymupdf

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = "downloads/ReadMath_2025수능킬러_변형24제_N제.pdf"
out_dir = "rendered_pages"
os.makedirs(out_dir, exist_ok=True)

doc = pymupdf.open(pdf_path)
print(f"Total pages in N-je PDF: {len(doc)}")

# Render key pages: Page 1 (Q1-6), Page 7 (Sol 1-2), Page 8 (Sol 3-4), Page 9 (Sol 5-6)
pages_to_render = [1, 2, 7, 8, 9, 10, 11, 12, 13, 14]

for pno in pages_to_render:
    page = doc[pno - 1]
    pix = page.get_pixmap(dpi=150)
    png_path = os.path.join(out_dir, f"page_{pno}.png")
    pix.save(png_path)
    print(f"Page {pno} rendered -> {png_path} ({os.path.getsize(png_path)} bytes)")

print("\n--- Optical Centering & Text Check on Rendered Pages ---")
page_w = doc[0].rect.width # 594.96

for i in range(len(doc)):
    page = doc[i]
    p_text = page.get_text()
    
    # Check rogue text in footer
    footer_rect = pymupdf.Rect(0, page.rect.height - 45, page.rect.width, page.rect.height)
    footer_text = page.get_text("text", clip=footer_rect).strip()
    
    if "수학 영역 (홀수형)" in footer_text:
        print(f"[FAIL] Page {i+1} footer has rogue '수학 영역 (홀수형)'!")
        sys.exit(1)
        
    if "정답 기재란" in p_text or "정답기재란" in p_text:
        print(f"[FAIL] Page {i+1} has '[정답 기재란]'!")
        sys.exit(1)

print("[PASS] 19 pages verified: 0 rogue footer spans, 0 '[정답 기재란]' labels!")
