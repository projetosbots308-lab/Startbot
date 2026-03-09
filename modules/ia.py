import requests
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from modules.anime import format_anime
from modules.manga import format_manga

# busca anime pelo nome
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

# busca recomendações
def get_animes_parecidos(mal_id):
    try:
        r = requests.get(f"https://api.jikan.moe/v4/anime/{mal_id}/recommendations")
        data = r.json().get("data", [])
        return [x["entry"]["title"] for x in data][:5]
    except:
        return []

# busca personagem pelo nome
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

# pega lista da temporada atual
def get_temporada_atual():
    try:
        r = requests.get("https://api.jikan.moe/v4/seasons/now")
        return r.json().get("data", [])
    except:
        return []

# comando principal
async def ia(update: Update, context: ContextTypes.DEFAULT_TYPE):

    pergunta = " ".join(context.args).lower().strip()

    if not pergunta:
        await update.message.reply_text("❗ Use: /ia sua pergunta")
        return

    try:

        ####################
        #  Animes parecidos #
        ####################
        if "parecido" in pergunta or "semelhante" in pergunta:
            # extrai nome depois da expressão
            nome = pergunta.replace("animes parecidos com", "").replace("parecido com", "").strip()
            anime_data = get_anime(nome)

            if anime_data:
                mal_id = anime_data["mal_id"]
                lista = get_animes_parecidos(mal_id)

                if lista:
                    texto = f"🎬 Animes parecidos com **{anime_data['title']}**:\n"
                    texto += "\n".join([f"• {a}" for a in lista])
                    await update.message.reply_text(texto)
                    return

            await update.message.reply_text("😅 Não encontrei animes parecidos.")
            return

        ####################
        #  Lançamentos da temporada #
        ####################
        if any(x in pergunta for x in ["lançamentos", "animes da temporada", "próximos episódios"]):
            season_list = get_temporada_atual()

            if season_list:
                texto = "📅 Animes na temporada atual:\n"
                for a in season_list[:10]:
                    texto += f"• {a['title']}\n"
                await update.message.reply_text(texto)
                return
            else:
                await update.message.reply_text("😅 Não consegui obter a temporada.")
                return

        ####################
        #  Personagem
        ####################
        if "quem é" in pergunta or "personagem" in pergunta:
            nome = pergunta.replace("quem é", "").replace("personagem", "").strip()
            char = get_personagem(nome)

            if char:
                about = char.get("about") or "Sem descrição."
                texto = f"👤 {char['name']}\n\n{about[:400]}..."
                await update.message.reply_text(texto)
                return
            else:
                await update.message.reply_text("😅 Personagem não encontrado.")
                return

        ####################
        #  Anime específico #
        ####################
        anime_data = get_anime(pergunta)
        if anime_data:
            texto = format_anime(anime_data)
            await update.message.reply_text(texto)
            return

        ####################
        #  Mangá específico #
        ####################
        manga_data = get_manga(pergunta)
        if manga_data:
            texto = format_manga(manga_data)
            await update.message.reply_text(texto)
            return

        ####################
        #  Fallback
        ####################
        fallback = (
            "🤔 Não encontrei resposta para isso.\n"
            "Posso ajudar com:\n"
            "- Animes parecidos (ex: ‘quais são animes parecidos com Naruto’)\n"
            "- Lançamentos da temporada atual\n"
            "- Informações de anime/mangá\n"
            "- Personagens"
        )
        await update.message.reply_text(fallback)

    except Exception as e:
        print(e)
        await update.message.reply_text("⚠️ Erro ao processar a pergunta.")
