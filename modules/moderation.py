from telegram import Update
from telegram.ext import ContextTypes

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text("Responda a mensagem do usuário para banir.")
        return

    user = update.message.reply_to_message.from_user.id

    await update.effective_chat.ban_member(user)

    await update.message.reply_text("🚫 Usuário banido.")
