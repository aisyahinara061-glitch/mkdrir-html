# bot_telegram.py - BOT ADMIN USER
import json
import base64
import requests
import os
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters

# ========== KONFIGURASI ==========
TOKEN = "8978270888:AAFixlzjmIDSSF4_6Gl8M13_o5Vn1_0KabU"
GITHUB_TOKEN = os.getenv("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")
GITHUB_REPO = "aisyahinara061-glitch/mkdrir-html"
GITHUB_FILE = "users.json"
ADMIN_ID = 8756879788  # Chat ID lu (admin)

# ========== FUNGSI GITHUB ==========
def get_users():
    """Ambil data user dari GitHub"""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        content = r.json()
        data = json.loads(base64.b64decode(content['content']).decode())
        return data, content['sha']
    return {"users": []}, None

def save_users(data, sha=None):
    """Simpen data user ke GitHub"""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    payload = {
        "message": f"Update users - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "content": base64.b64encode(json.dumps(data, indent=2).encode()).decode(),
    }
    
    if sha:
        payload["sha"] = sha
    
    r = requests.put(url, headers=headers, json=payload)
    return r.status_code in [200, 201]

# ========== CEK ADMIN ==========
def cek_admin(update: Update):
    if update.effective_user.id != ADMIN_ID:
        return False
    return True

# ========== COMMAND HANDLERS ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not cek_admin(update):
        await update.message.reply_text("❌ Lu bukan admin!")
        return
    
    await update.message.reply_text("""
🤖 *BOT ADMIN USER*

Command:
/add <nama> <password> - Tambah user
/remove <nama> - Hapus user
/list - Lihat semua user
/clear - Hapus semua user

Contoh:
/add azka 12345
/remove azka
    """, parse_mode="Markdown")

async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not cek_admin(update):
        return
    
    if len(context.args) < 2:
        await update.message.reply_text("Format: /add <nama> <password>")
        return
    
    nama = context.args[0].lower()
    password = context.args[1]
    
    data, sha = get_users()
    
    # Cek user udah ada
    for user in data['users']:
        if user['nama'] == nama:
            await update.message.reply_text(f"❌ User {nama} udah ada!")
            return
    
    # Tambah user baru
    data['users'].append({
        "nama": nama,
        "password": password,
        "created": datetime.now().isoformat()
    })
    
    if save_users(data, sha):
        await update.message.reply_text(f"✅ User {nama} berhasil ditambah!")
    else:
        await update.message.reply_text("❌ Gagal simpen ke GitHub!")

async def remove_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not cek_admin(update):
        return
    
    if not context.args:
        await update.message.reply_text("Format: /remove <nama>")
        return
    
    nama = context.args[0].lower()
    data, sha = get_users()
    
    # Filter user
    data['users'] = [u for u in data['users'] if u['nama'] != nama]
    
    if save_users(data, sha):
        await update.message.reply_text(f"✅ User {nama} dihapus!")
    else:
        await update.message.reply_text("❌ Gagal!")

async def list_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not cek_admin(update):
        return
    
    data, _ = get_users()
    
    if not data['users']:
        await update.message.reply_text("Belum ada user.")
        return
    
    pesan = "📋 *DAFTAR USER*\n\n"
    for i, u in enumerate(data['users'], 1):
        pesan += f"{i}. {u['nama']}\n"
    
    await update.message.reply_text(pesan, parse_mode="Markdown")

async def clear_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not cek_admin(update):
        return
    
    data, sha = get_users()
    data['users'] = []
    
    if save_users(data, sha):
        await update.message.reply_text("✅ Semua user dihapus!")
    else:
        await update.message.reply_text("❌ Gagal!")

# ========== MAIN ==========
def main():
    print("🤖 BOT ADMIN STARTING...")
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_user))
    app.add_handler(CommandHandler("remove", remove_user))
    app.add_handler(CommandHandler("list", list_user))
    app.add_handler(CommandHandler("clear", clear_user))
    
    print("✅ Bot siap!")
    app.run_polling()

if __name__ == "__main__":
    main()
