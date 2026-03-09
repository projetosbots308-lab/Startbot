import requests
from telegram import Update
from telegram.ext import ContextTypes


async def ia(update: Update, context: ContextTypes.DEFAULT_TYPE):

    pergunta = " ".join(context.args)

    if not pergunta:
        await update.message.reply_text("Use: /ia sua pergunta")
        return

    url = "https://api.affiliateplus.xyz/api/chatbot"

    r = requests.get(url, params={
        "message": pergunta,
        "botname": "Senpai",
        "ownername": "Otaku"
    })

    resposta = r.json()["message"]

    await update.message.reply_text(resposta)
