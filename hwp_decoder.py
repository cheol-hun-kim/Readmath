import os
import re
import json
import pymupdf

# Full HWP Math Font Unicode (PUA: 0xE000 - 0xF8FF) to Standard LaTeX / Korean Mapping Table
PUA_MAP = {
    # Digits
    0xE030: '0', 0xE031: '1', 0xE032: '2', 0xE033: '3', 0xE034: '4',
    0xE035: '5', 0xE036: '6', 0xE037: '7', 0xE038: '8', 0xE039: '9',
    0xE03A: '7', 0xE03B: '8', 0xE03C: '9', 0xE03D: '0',
    # Operators & Delimiters
    0xE044: '(', 0xE045: ')', 0xE046: '-', 0xE047: '=', 0xE048: '+',
    0xE049: '[', 0xE04A: ']', 0xE04B: '{', 0xE04C: '}', 0xE04F: ':',
    0xE052: ',', 0xE055: '<', 0xE056: '>', 0xE05B: r'\int', 0xE05C: r'\sqrt',
    0xE067: r'\sum', 0xE06D: '/', 0xE101: '|',
    # Brackets
    0xE078: '{', 0xE079: '', 0xE07A: '', 0xE07B: '',
    # Greek letters
    0xE09D: r'\alpha', 0xE09E: r'\beta', 0xE0A4: r'\theta', 0xE0AC: r'\pi',
    # Latin uppercase
    0xE002: 'C', 0xE00C: 'M', 0xE00E: 'O', 0xE012: 'S', 0xE000: 'A', 0xE001: 'B',
    0xE003: 'D', 0xE004: 'E', 0xE005: 'F', 0xE006: 'G', 0xE007: 'H', 0xE00F: 'P', 0xE010: 'Q',
    # Latin lowercase variables
    0xE0E5: 'a', 0xE0E6: 'b', 0xE0E7: 'c', 0xE0E8: 'd', 0xE0EA: 'f',
    0xE0EB: 'g', 0xE0EC: 'h', 0xE0EF: 'k', 0xE0F0: 'l', 0xE0F1: 'm',
    0xE0F2: 'n', 0xE0F4: 'p', 0xE0F5: 'q', 0xE0F8: 't', 0xE0FA: 'v',
    0xE0FC: 'x', 0xE0FD: 'y', 0xE0FE: 'z',
    # Circle numbers
    0x2460: '(1)', 0x2461: '(2)', 0x2462: '(3)', 0x2463: '(4)', 0x2464: '(5)'
}

def clean_hwp_text(text: str) -> str:
    """Translates HWP PUA font characters into clean standard math characters."""
    chars = []
    for ch in text:
        cp = ord(ch)
        if cp in PUA_MAP:
            chars.append(PUA_MAP[cp])
        elif 0xE000 <= cp <= 0xF8FF:
            # Drop unknown PUA marks like overlines or baseline anchors
            continue
        else:
            chars.append(ch)
    
    res = "".join(chars)
    # Clean up double spaces & line breaks inside equations
    res = re.sub(r'[ \t]+', ' ', res)
    return res.strip()

print("Clean HWP module ready!")
