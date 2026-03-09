import requests
from telegram import Update
from telegram.ext import ContextTypes


async def ia(update: Update, context: ContextTypes.DEFAULT_TYPE):

    pergunta = " ".join(context.args)

    if not pergunta:
        await update.message.reply_text("Use: /ia sua pergunta")
        return

    try:

        r = requests.get(
            "https://api.affiliateplus.xyz/api/chatbot",
            params={
                "message": pergunta,
                "botname": "Senpai",
                "ownername": "Otaku"
            },
            timeout=10
        )

        resposta = r.json().get("message", "Não consegui responder 😅")

        await update.message.reply_text(resposta)

    except:
        await update.message.reply_text("Erro ao acessar IA.")
