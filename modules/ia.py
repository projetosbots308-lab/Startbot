import requests
from telegram import Update
from telegram.ext import ContextTypes


async def ia(update: Update, context: ContextTypes.DEFAULT_TYPE):

    pergunta = " ".join(context.args).lower()

    if not pergunta:
        await update.message.reply_text("Use: /ia sua pergunta")
        return


    try:

        # pergunta sobre temporada
        if "temporada" in pergunta or "season" in pergunta:

            r = requests.get("https://api.jikan.moe/v4/seasons/now")
            data = r.json()["data"][:10]

            texto = "📺 Animes da temporada:\n\n"

            for a in data:
                texto += f"• {a['title']}\n"

            await update.message.reply_text(texto)
            return


        # pergunta sobre personagem
        if "quem é" in pergunta:

            nome = pergunta.replace("quem é", "").strip()

            url = f"https://api.jikan.moe/v4/characters?q={nome}&limit=1"

            r = requests.get(url)
            data = r.json()

            if data["data"]:

                char = data["data"][0]

                nome = char["name"]
                about = char["about"]

                texto = f"""
👤 {nome}

{about[:400]}...
"""

                await update.message.reply_text(texto)
                return


        # pergunta sobre anime
        url = f"https://api.jikan.moe/v4/anime?q={pergunta}&limit=1"

        r = requests.get(url)

        data = r.json()

        if data["data"]:

            anime = data["data"][0]

            titulo = anime["title"]
            episodios = anime["episodes"]
            score = anime["score"]
            status = anime["status"]

            texto = f"""
🎬 {titulo}

📺 Episódios: {episodios}
⭐ Nota: {score}
📡 Status: {status}

Use /anime {titulo} para ver detalhes.
"""

            await update.message.reply_text(texto)
            return


        await update.message.reply_text(
            "🤔 Não encontrei resposta. Tente perguntar sobre animes ou personagens."
        )

    except Exception as e:

        print(e)

        await update.message.reply_text("⚠️ Erro ao processar a pergunta.")
