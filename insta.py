import requests
import json
import base64
import time
import random
import uuid
import string
import threading
import asyncio
import aiohttp
import os
from datetime import datetime
import pytz
from urllib.parse import quote
# Ajuste de compatibilidade para diferentes ambientes (Termux/Cloud)
try:
    from Cryptodome.Cipher import AES, PKCS1_v1_5
    from Cryptodome.PublicKey import RSA
    from Cryptodome.Random import get_random_bytes
except ImportError:
    from Crypto.Cipher import AES, PKCS1_v1_5
    from Crypto.PublicKey import RSA
    from Crypto.Random import get_random_bytes
from http.server import BaseHTTPRequestHandler, HTTPServer

# =================================================================
# 🔥 SISTEMA SUPREMO THAYSON - V10 FULL MULTI-THREAD 🔥
# =================================================================

# --- SERVIDOR PARA MANTER ONLINE (RENDER/RAILWAY) ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'SISTEMA THAYSON V10 ONLINE')
    def log_message(self, format, *args): return

def run_health_check():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# --- CONFIGURAÇÕES SEVENTV ---
IPTV_API = "https://seventvpainel.top"
IPTV_USER = "thaysonsilvacavalcante@gmail.com"
IPTV_PASS = "Thayson13.@"
APP_LINK = "https://www.mediafire.com/file/ngjeya72jutqgti/thayson+tv_1.0.apk/file"
ZAP_NUM = "1 438 942 3427"

IPTV_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
    "Locale": "pt"
}

# --- CONFIGURAÇÕES INSTAGRAM ---
USER_DEFAULT = "7p_thayson"
PASS_DEFAULT = "7p_thayson11"
THREAD_RELATORIO = "17845851594176556"
COOKIE_STRING = 'datr=vozQaZ9FTfSuYSDOh8c3S56v; ig_did=0A7CD33E-D3EC-401D-9761-77259A2493C3; ps_l=1; ps_n=1; dpr=2.206249952316284; csrftoken=tRKyNCkXz6AvTYmfdFyPWdjskwyH4ArO; mid=adFo6AABAAG5tAitm_wsuvQy4hMH; ds_user_id=80209457261; sessionid=80209457261%3Anq7JkMhXWVecM5%3A0%3AAYgEIsTcdLwF_8GRLQUSnaoP34MoBNBWH-VybWDGBg; wd=489x920; rur="NHA\\05480209457261\\0541806868880:01fe0ebf18749c15d5abf3b87108fb18cbfb8a23125333139c16cd2c95d7412164beddbe"'

contas_ativas = {} 

MENU_BOT = (
    "✨ *SISTEMA THAYSON AUTOMATIONS* ✨\n\n"
    "1️⃣ *FALAR COM O THAYSON* 👨‍💻\n"
    "2️⃣ *DEIXAR MENSAGEM AGENDADA* 📝\n"
    "3️⃣ *GERAR TESTE IPTV (SEVENTV)* 📺\n"
    "4️⃣ *GERENCIAR BOTS / ADICIONAR* 🚀\n"
    "5️⃣ *CONTATOS / APP* 🌐\n"
    "0️⃣ *REINICIAR* 🔄"
)

def fonte_pequena(texto):
    mapa = str.maketrans("abcdefghijklmnopqrstuvwxyz0123456789", "ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹")
    return texto.lower().translate(mapa)

class InstagramBot:
    def __init__(self, user=None, pw=None, is_main=False):
        self.session = requests.Session()
        self.username = user
        self.password = pw
        self.is_main = is_main
        self.auth_token = None
        self.iptv_token = None
        self.my_user_id = None
        self.device_id = str(uuid.uuid4())
        self.user_states = {}
        self.running = True
        self.fixed_msg = "Olá! Esta conta está sendo monitorada pelo Bot do Thayson."
        self.trigger = None
        self.response = None

    def animar(self, texto):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {texto}")

    def get_pks(self):
        try:
            resp = requests.get("https://i.instagram.com/api/v1/qe/sync/", timeout=10)
            return int(resp.headers.get("ig-set-password-encryption-key-id")), resp.headers.get("ig-set-password-encryption-pub-key")
        except: return None, None

    def encrypt_password(self, password):
        pki, pk = self.get_pks()
        if not pki: return None
        sk, iv, ts = get_random_bytes(32), get_random_bytes(12), str(int(time.time()))
        rk = RSA.import_key(base64.b64decode(pk.encode()))
        re = PKCS1_v1_5.new(rk).encrypt(sk)
        ca = AES.new(sk, AES.MODE_GCM, iv)
        ca.update(ts.encode())
        ae, tg = ca.encrypt_and_digest(password.encode("utf8"))
        pl = base64.b64encode(b"\x01" + pki.to_bytes(1, "big") + iv + len(re).to_bytes(2, "little") + re + tg + ae)
        return f"#PWD_INSTAGRAM:4:{ts}:{pl.decode()}"

    def login_iptv(self):
        url = f"{IPTV_API}/api/auth/login"
        payload = {"username": IPTV_USER, "password": IPTV_PASS}
        try:
            res = requests.post(url, json=payload, headers=IPTV_HEADERS)
            if res.status_code == 200:
                self.iptv_token = res.json().get('token')
                return True
        except: return False
        return False

    def gerar_iptv_real(self):
        if not self.login_iptv(): return "❌ Erro ao conectar ao painel SevenTV."
        h = IPTV_HEADERS.copy()
        h["Authorization"] = f"Bearer {self.iptv_token}"
        payload = {"server_id": "BV4D3rLaqZ", "package_id": "z2BDvoWrkj", "connection_type": "IPTV", "is_trial": "NO", "connections": 1}
        try:
            res = requests.post(f"{IPTV_API}/api/customers", json=payload, headers=h)
            if res.status_code in [200, 201]:
                d = res.json().get('data', {})
                u, p = d.get('username'), d.get('password')
                return (f"🚀 *ACESSO SEVENTV*\n👤 Usuário: `{u}`\n🔑 Senha: `{p}`\n🌐 DNS: http://cdnflash.top\n📥 APP: {APP_LINK}")
        except: pass
        return "⚠️ Erro ao gerar teste."

    def login_process(self, two_factor_code=None):
        self.animar(f"🔐 Logando @{self.username}...")
        enc_pw = self.encrypt_password(self.password)
        data = {"jazoest": "22565", "enc_password": enc_pw, "username": self.username, "device_id": self.device_id, "login_attempt_count": "0"}
        if two_factor_code: data["verification_code"] = two_factor_code
        headers = {"User-Agent": "Instagram 342.0.0.33.103 Android", "X-IG-App-ID": "567067343352427"}
        try:
            res = self.session.post("https://i.instagram.com/api/v1/accounts/login/", data=data, headers=headers)
            rj = res.json()
            if res.status_code == 200:
                self.auth_token = res.headers.get('ig-set-authorization')
                self.my_user_id = str(rj.get("logged_in_user", {}).get("pk"))
                return "SUCCESS"
            elif "checkpoint_url" in rj: return "CHECKPOINT"
            elif "two_factor_required" in rj: return "2FA"
            else: return rj.get("message", "Erro desconhecido")
        except: return "ERRO_CONEXAO"

    def enviar_msg(self, thread_id, texto, recipient_id):
        ts = int(time.time())
        headers = {
            "Authorization": self.auth_token if self.auth_token else "",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Instagram 342.0.0.33.103 Android",
            "X-IG-App-ID": "567067343352427",
            "X-CSRFToken": self.session.cookies.get("csrftoken", ""),
            "IG-U-DS-USER-ID": self.my_user_id
        }
        data = {"action": "send_item", "thread_id": thread_id, "text": texto, "client_context": str(ts), "offline_threading_id": str(ts), "device_id": self.device_id, "mutation_token": str(ts), "_uuid": self.device_id}
        if recipient_id: data["recipient_users"] = f"[[{recipient_id}]]"
        try:
            res = self.session.post("https://i.instagram.com/api/v1/direct_v2/threads/broadcast/text/", data=data, headers=headers)
            return res.status_code == 200
        except: return False

    async def monitorar(self):
        while self.running:
            try:
                headers = {"Authorization": self.auth_token if self.auth_token else "", "User-Agent": "Instagram 342.0.0.33.103 Android", "X-IG-App-ID": "567067343352427"}
                res = self.session.get("https://i.instagram.com/api/v1/direct_v2/inbox/", headers=headers)
                if res.status_code == 200:
                    threads = res.json().get("inbox", {}).get("threads", [])
                    for thread in threads:
                        items = thread.get("items", [])
                        if not items: continue
                        last = items[0]
                        sid, tid = str(last.get("user_id")), thread.get("thread_id")
                        msg = str(last.get("text", "")).strip().lower()
                        if sid == self.my_user_id: continue

                        if msg.startswith("stop"):
                            if not self.is_main:
                                self.enviar_msg(tid, "🔴 Bot finalizado.", sid)
                                self.running = False
                                if self.username in contas_ativas: del contas_ativas[self.username]
                            continue

                        if self.is_main:
                            if msg in ["oi", "menu", "0"]: self.user_states.pop(sid, None)
                            if sid not in self.user_states:
                                if self.enviar_msg(tid, MENU_BOT, sid): self.user_states[sid] = {"step": "MENU"}
                            else:
                                step = self.user_states[sid]["step"]
                                if step == "MENU":
                                    if msg == "1": self.enviar_msg(tid, "⚠️ Thayson está offline. Deixe recado na opção 2.", sid)
                                    elif msg == "2":
                                        self.enviar_msg(tid, "👤 Qual seu nome?", sid)
                                        self.user_states[sid]["step"] = "NOME"
                                    elif msg == "3":
                                        self.enviar_msg(tid, "⏳ Gerando acesso...", sid)
                                        self.enviar_msg(tid, self.gerar_iptv_real(), sid)
                                    elif msg == "4":
                                        self.enviar_msg(tid, f"🚀 Ativas: {len(contas_ativas)}\nEnvie `ATIVAR` para começar.", sid)
                                    elif msg == "5":
                                        self.enviar_msg(tid, f"📸 @{USER_DEFAULT}\n📥 {APP_LINK}", sid)
                                    
                                    if msg == "ativar":
                                        self.enviar_msg(tid, "🤖 Digite o USUÁRIO:", sid)
                                        self.user_states[sid]["step"] = "SET_USER"
                                
                                elif step == "SET_USER":
                                    self.user_states[sid]["new_u"] = msg
                                    self.enviar_msg(tid, "🔑 Digite a SENHA:", sid)
                                    self.user_states[sid]["step"] = "SET_PASS"
                                elif step == "SET_PASS":
                                    self.user_states[sid]["new_p"] = msg
                                    self.enviar_msg(tid, "🎁 Resposta para o gatilho:", sid)
                                    self.user_states[sid]["step"] = "SET_RESPONSE"
                                elif step == "SET_RESPONSE":
                                    self.user_states[sid]["new_r"] = msg
                                    self.enviar_msg(tid, "⏳ Ativando bot secundário...", sid)
                                    threading.Thread(target=self.init_worker, args=(self.user_states[sid]["new_u"], self.user_states[sid]["new_p"], self.user_states[sid]["new_r"], tid, sid)).start()
                                    self.user_states[sid]["step"] = "FIM"

                                elif step == "NOME":
                                    self.user_states[sid]["nome"] = msg
                                    self.enviar_msg(tid, "📝 Digite o recado:", sid)
                                    self.user_states[sid]["step"] = "RECADO"
                                elif step == "RECADO":
                                    self.enviar_msg(THREAD_RELATORIO, f"🔔 *RECADO:*\n👤 {self.user_states[sid]['nome']}\n💬 {msg}", None)
                                    self.enviar_msg(tid, "✅ Enviado!", sid)
                                    self.user_states[sid]["step"] = "FIM"
                        else:
                            txt_pequeno = fonte_pequena(f"bot by thayson zap {ZAP_NUM}")
                            self.enviar_msg(tid, f"{self.response}\n\n🤖 {txt_pequeno}", sid)
                await asyncio.sleep(8)
            except: await asyncio.sleep(15)

    def init_worker(self, u, p, r, tid, sid):
        bot = InstagramBot(u, p)
        bot.response = r
        if bot.login_process() == "SUCCESS":
            contas_ativas[u] = bot
            self.enviar_msg(tid, f"✅ @{u} Online!", sid)
            asyncio.run(bot.monitorar())

async def main_engine():
    main_bot = InstagramBot(USER_DEFAULT, PASS_DEFAULT, is_main=True)
    if main_bot.login_process() != "SUCCESS":
        for c in COOKIE_STRING.split(';'):
            if '=' in c:
                n, v = c.strip().split('=', 1)
                main_bot.session.cookies.set(n, v.replace('"', ''), domain=".instagram.com")
        main_bot.my_user_id = main_bot.session.cookies.get("ds_user_id", "80209457261")
        main_bot.auth_token = f"Ds-User-Id={main_bot.my_user_id}"
    await main_bot.monitorar()

if __name__ == "__main__":
    threading.Thread(target=run_health_check, daemon=True).start()
    print("🔥 THAYSON SUPREMO V10 CARREGADO 🔥")
    try: asyncio.run(main_engine())
    except KeyboardInterrupt: pass
