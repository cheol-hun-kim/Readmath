# -*- coding: utf-8 -*-
"""
ReadMath (리드매스) - 실시간 Gmail SMTP 이메일 인증 발송 서버
1286orbital21@gmail.com 전용 SMTP 브릿지 및 정적 파일 서버
"""

import os
import re
import sys
import time
import json
import smtplib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

PORT = 8765
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SMTP_USER = os.getenv("READMATH_SMTP_USER", "1286orbital21@gmail.com")
SMTP_PW = os.getenv("READMATH_SMTP_PW", "adiuvotwzlqhhmol")
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
FROM_NAME = "리드매스 (ReadMath)"

_OTP_RATE_STORE = {}
_OTP_WINDOW_SEC = 60
_OTP_MAX_REQ = 5
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_ALLOWED_ORIGIN_RE = re.compile(r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$|^https://.*\.(onrender\.com|vercel\.app|readmath\.kr)$")

def send_smtp_email(to_email: str, code: str) -> tuple[bool, str]:
    """
    Sends authentic 6-digit OTP verification email via Gmail SMTP.
    """
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "[ReadMath 리드매스] 학생 회원가입 본인확인 인증번호"
        msg["From"] = f"{FROM_NAME} <{SMTP_USER}>"
        msg["To"] = to_email

        html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>리드매스 본인인증 번호</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0b0f19; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Pretendard', sans-serif;">
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #0b0f19; padding: 36px 16px;">
        <tr>
            <td align="center">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 480px; background-color: #0f172a; border: 1.5px solid #4f46e5; border-radius: 16px; overflow: hidden; box-shadow: 0 12px 36px rgba(0,0,0,0.6);">
                    <tr>
                        <td style="padding: 30px 24px 20px 24px; text-align: center;">
                            <div style="font-size: 24px; font-weight: 900; color: #ffffff; letter-spacing: -0.5px; margin-bottom: 6px;">
                                ReadMath <span style="font-size: 13px; color: #818cf8; font-weight: 800;">리드매스</span>
                            </div>
                            <div style="font-size: 12.5px; color: #94a3b8; font-weight: 500;">
                                수학은 해석의 대상이다! 1:1 시각적 원리 튜터
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 0 24px 28px 24px;">
                            <div style="background-color: rgba(99, 102, 241, 0.12); border: 1px solid rgba(99, 102, 241, 0.4); border-radius: 12px; padding: 24px 16px; text-align: center;">
                                <div style="font-size: 13px; color: #c7d2fe; margin-bottom: 14px; font-weight: 600;">
                                    학생 회원가입 본인확인 6자리 인증번호
                                </div>
                                <div style="font-size: 34px; font-weight: 900; letter-spacing: 10px; color: #38bdf8; background-color: rgba(11, 15, 25, 0.85); border: 1.5px dashed #38bdf8; border-radius: 10px; padding: 14px 0; margin-bottom: 14px; font-family: monospace;">
                                    {code}
                                </div>
                                <div style="font-size: 12px; color: #f87171; font-weight: 700;">
                                    유효시간: 3분 (180초 이내 입력)
                                </div>
                            </div>
                            <div style="margin-top: 22px; font-size: 11px; color: #64748b; line-height: 1.5; text-align: center;">
                                * 본 인증번호는 리드매스 회원가입 및 본인 확인 목적으로만 사용됩니다.<br/>
                                * 본인이 요청하지 않은 경우 이 메일을 안전하게 무시하셔도 됩니다.
                            </div>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
        msg.attach(MIMEText(html, "html", "utf-8"))

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=12)
        server.starttls()
        server.login(SMTP_USER, SMTP_PW)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
        server.quit()
        print(f"[SMTP SUCCESS] Dispatched OTP code to {to_email}")
        return True, "이메일이 성공적으로 발송되었습니다."
    except Exception as e:
        err = str(e)
        print(f"[SMTP ERROR] Failed to send email to {to_email}: {err}")
        return False, err

class ReadMathHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        origin = self.headers.get("Origin", "") if hasattr(self, "headers") else ""
        if origin and _ALLOWED_ORIGIN_RE.match(origin):
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def _send_json(self, code: int, payload: dict):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))

    def do_POST(self):
        if self.path == "/api/send-email-otp":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                if content_length <= 0 or content_length > 16384:
                    self._send_json(400, {"success": False, "error": "유효하지 않은 요청 크기입니다."})
                    return

                body = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(body)
                email = str(data.get("email", "")).strip()
                code = str(data.get("code", "")).strip()

                if not _EMAIL_RE.match(email) or not re.match(r"^\d{4,8}$", code):
                    self._send_json(400, {"success": False, "error": "올바른 이메일과 숫자 인증번호 형식이 필요합니다."})
                    return

                # Rate limit per client IP + email (max 5 requests per 60s)
                client_ip = self.client_address[0] if self.client_address else "unknown"
                rate_key = f"{client_ip}:{email.lower()}"
                now = time.time()
                hits = [t for t in _OTP_RATE_STORE.get(rate_key, []) if now - t < _OTP_WINDOW_SEC]
                if len(hits) >= _OTP_MAX_REQ:
                    self._send_json(429, {"success": False, "error": "인증번호 요청이 너무 많습니다. 1분 후 다시 시도해 주세요."})
                    return
                hits.append(now)
                _OTP_RATE_STORE[rate_key] = hits

                ok, msg = send_smtp_email(email, code)
                if ok:
                    self._send_json(200, {"success": True, "message": msg})
                else:
                    self._send_json(500, {"success": False, "error": "이메일 발송 중 오류가 발생했습니다."})
            except Exception:
                self._send_json(500, {"success": False, "error": "요청 처리 중 오류가 발생했습니다."})
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        # Block sensitive config, source, and hidden files from static serving
        clean_path = self.path.split("?", 1)[0].lower()
        if (
            ".." in clean_path
            or "/." in clean_path
            or clean_path.endswith((".env", ".py", ".db", ".sqlite", ".sql", ".log", ".bak", ".bat", ".md", "package.json", "package-lock.json", "gemini_raw_out.json"))
        ):
            self.send_response(403)
            self.end_headers()
            return

        # Default root request to preview.html if index.html is requested or root
        if self.path == "/" or self.path == "/index.html":
            self.path = "/preview.html"
        return super().do_GET()

if __name__ == "__main__":
    print(f"==================================================")
    print(f"ReadMath Email & Web Server running on port {PORT}")
    print(f"Open: http://localhost:{PORT}")
    print(f"SMTP Dispatcher: {SMTP_USER} via {SMTP_HOST}")
    print(f"==================================================")
    server = ThreadingHTTPServer(("0.0.0.0", PORT), ReadMathHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer shutting down gracefully.")
        server.server_close()
