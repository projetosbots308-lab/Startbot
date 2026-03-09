import requests
from telegram import Update
from telegram.ext import ContextTypes
from datetime import date

# Função utilitária para pegar animes da temporada
def get_animes_temporada():
    try:
        r = requests.get("https://api.jikan.moe/v4/seasons/now")
        data = r.json()["data"]
        return data[:10]  # primeiros 10 animes da temporada
    except:
        return []

# Função utilitária para buscar personagem
def get_personagem(nome):
    try:
        url = f"https://api.jikan.moe/v4/characters?q={nome}&limit=1"
        r = requests.get(url)
        data = r.json()
        if data["data"]:
            return data["data"][0]
        return None
    except:
        return None

# Função utilitária para buscar anime
def get_anime(nome):
    try:
        url = f"https://api.jikan.moe/v4/anime?q={nome}&limit=1"
        r = requests.get(url)
        data = r.json()
        if data["data"]:
            return data["data"][0]
        return None
    except:
        return None

async def ia(update: Update, context: ContextTypes.DEFAULT_TYPE):

    pergunta = " ".join(context.args).lower().strip()

    if not pergunta:
        await update.message.reply_text("Use: /ia sua pergunta")
        return

    try:

        # 1️⃣ Lançamentos / temporada
        if any(x in pergunta for x in ["lançamento", "hoje", "temporada", "novos", "agora"]):
            animes = get_animes_temporada()
            if animes:
                texto = f"📅 Animes lançando agora ({date.today()}):\n\n"
                for a in animes:
                    texto += f"• {a['title']} ({a['status']})\n"
                await update.message.reply_text(texto)
                return

        # 2️⃣ Personagem
        if "quem é" in pergunta or "personagem" in pergunta:
            nome = pergunta.replace("quem é", "").replace("personagem", "").strip()
            char = get_personagem(nome)
            if char:
                about = char["about"] or "Sem descrição."
                texto = f"👤 {char['name']}\n\n{about[:400]}..."
                await update.message.reply_text(texto)
                return

        # 3️⃣ Anime específico
        anime = get_anime(pergunta)
        if anime:
            texto = f"🎬 {anime['title']}\n📺 Episódios: {anime['episodes']}\n⭐ Nota: {anime['score']}\n📡 Status: {anime['status']}\nUse /anime {anime['title']} para detalhes."
            await update.message.reply_text(texto)
            return

        # 4️⃣ Fallback
        await update.message.reply_text(
            "🤔 Não encontrei resposta. Tente perguntas sobre lançamentos, episódios ou personagens."
        )

    except Exception as e:
        print(e)
        await update.message.reply_text("⚠️ Erro ao processar a pergunta.")
