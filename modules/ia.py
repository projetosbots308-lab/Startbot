import requests
from telegram import Update
from telegram.ext import ContextTypes


async def ia(update: Update, context: ContextTypes.DEFAULT_TYPE):

    pergunta = " ".join(context.args)

    if not pergunta:
        await update.message.reply_text("Use: /ia sua pergunta")
        return

    try:

        url = "https://api.popcat.xyz/chatbot"

        r = requests.get(
            url,
            params={
                "msg": pergunta,
                "owner": "Otaku",
                "botname": "Senpai"
            },
            timeout=15
        )

        data = r.json()

        resposta = data.get("response")

        if not resposta:
            resposta = "Não consegui responder 😅"

        await update.message.reply_text(resposta)

    except Exception as e:

        print(e)

        await update.message.reply_text(
            "⚠️ Não consegui acessar a IA agora."
        )
