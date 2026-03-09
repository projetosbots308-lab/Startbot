import requests
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from modules.anime import format_anime
from modules.manga import format_manga

# Pega todos os animes da temporada atual
def get_animes_temporada():
    try:
        r = requests.get("https://api.jikan.moe/v4/seasons/now")
        data = r.json()["data"]
        return data
    except:
        return []

# Pega próximo episódio de um anime e filtra pelo dia de hoje
def get_proximo_episodio_mal(mal_id):
    try:
        r = requests.get(f"https://api.jikan.moe/v4/anime/{mal_id}/episodes")
        data = r.json()["data"]
        for ep in data:
            if ep["aired"] is not None:
                dt = datetime.fromisoformat(ep["aired"].replace("Z",""))
                if dt.date() == datetime.today().date():
                    return ep["episode"], dt
        return None, None
    except:
        return None, None

# Busca personagem
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

# Busca anime
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

# Busca mangá
def get_manga(nome):
    try:
        url = f"https://api.jikan.moe/v4/manga?q={nome}&limit=1"
        r = requests.get(url)
        data = r.json()
        if data["data"]:
            return data["data"][0]
        return None
    except:
        return None

# Comando principal /ia
async def ia(update: Update, context: ContextTypes.DEFAULT_TYPE):

    pergunta = " ".join(context.args).lower().strip()

    if not pergunta:
        await update.message.reply_text("Use: /ia sua pergunta")
        return

    try:

        # 1️⃣ Lançamentos de hoje
        if any(x in pergunta for x in ["lançamento", "episódio hoje", "hoje"]):
            animes = get_animes_temporada()
            texto = f"📅 Lançamentos de hoje ({datetime.today().date()}):\n\n"
            count = 0
            for anime in animes:
                ep_num, ep_dt = get_proximo_episodio_mal(anime["mal_id"])
                if ep_num is not None:
                    texto += f"• {anime['title']} - Ep {ep_num}\n"
                    count += 1
            if count == 0:
                texto += "Nenhum lançamento hoje 😅"
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
        anime_data = get_anime(pergunta)
        if anime_data:
            texto = format_anime(anime_data)
            image = anime_data["images"]["jpg"]["large_image_url"]
            await update.message.reply_photo(photo=image, caption=texto)
            return

        # 4️⃣ Mangá específico
        manga_data = get_manga(pergunta)
        if manga_data:
            texto = format_manga(manga_data)
            image = manga_data["images"]["jpg"]["large_image_url"]
            await update.message.reply_photo(photo=image, caption=texto)
            return

        # 5️⃣ Pergunta geral do mundo otaku
        fallback = (
            "🤔 Ainda não sei a resposta, mas posso ajudar com:\n"
            "- Lançamentos de animes\n"
            "- Detalhes de animes\n"
            "- Mangás\n"
            "- Personagens\n\n"
            "Use /anime ou /manga para buscas específicas."
        )
        await update.message.reply_text(fallback)

    except Exception as e:
        print(e)
        await update.message.reply_text("⚠️ Erro ao processar a pergunta.")
