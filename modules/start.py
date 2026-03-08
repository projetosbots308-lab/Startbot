from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user.first_name

    text = f"""
👋 Olá {user}!

Eu sou um bot assistente otaku 🤖

Comandos principais:

/anime nome
/manga nome
/season

Use /help para mais comandos
"""

    await update.message.reply_text(text)
