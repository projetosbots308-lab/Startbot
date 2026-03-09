import os
import requests
from telegram import Update
from telegram.ext import ContextTypes


HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}


async def ia(update: Update, context: ContextTypes.DEFAULT_TYPE):

    pergunta = " ".join(context.args)

    if not pergunta:
        await update.message.reply_text("Use: /ia sua pergunta")
        return

    try:

        payload = {
            "inputs": f"Responda em português: {pergunta}",
            "options": {"wait_for_model": True}
        }

        r = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        data = r.json()

        if isinstance(data, list):
            resposta = data[0]["generated_text"]
        else:
            resposta = "Não consegui gerar resposta agora."

        await update.message.reply_text(resposta)

    except Exception as e:

        print(e)

        await update.message.reply_text(
            "⚠️ A IA demorou muito para responder."
        )
