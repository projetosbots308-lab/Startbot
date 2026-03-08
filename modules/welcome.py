from telegram import Update
from telegram.ext import ContextTypes

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):

    for member in update.message.new_chat_members:

        name = member.first_name

        text = f"""
🎉 Bem-vindo {name}!

Leia as regras do grupo 📜
e aproveite o conteúdo!

Use /anime para buscar animes 🎌
"""

        await update.message.reply_text(text)
