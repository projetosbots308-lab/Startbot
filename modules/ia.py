import requests
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

from modules.anime import format_anime
from modules.manga import format_manga


# -----------------------------
# BUSCAR ANIME
# -----------------------------
def get_anime(nome):
    try:
        r = requests.get(f"https://api.jikan.moe/v4/anime?q={nome}&limit=1")
        data = r.json()
        if data["data"]:
            return data["data"][0]
        return None
    except:
        return None


# -----------------------------
# BUSCAR MANGA
# -----------------------------
def get_manga(nome):
    try:
        r = requests.get(f"https://api.jikan.moe/v4/manga?q={nome}&limit=1")
        data = r.json()
        if data["data"]:
            return data["data"][0]
        return None
    except:
        return None


# -----------------------------
# PERSONAGEM
# -----------------------------
def get_personagem(nome):
    try:
        r = requests.get(f"https://api.jikan.moe/v4/characters?q={nome}&limit=1")
        data = r.json()

        if data["data"]:
            return data["data"][0]

        return None
    except:
        return None


# -----------------------------
# ANIMES PARECIDOS
# -----------------------------
def get_animes_parecidos(mal_id):
    try:
        r = requests.get(
            f"https://api.jikan.moe/v4/anime/{mal_id}/recommendations"
        )

        data = r.json()["data"]

        return [x["entry"]["title"] for x in data[:6]]

    except:
        return []


# -----------------------------
# PRÓXIMO EPISÓDIO
# -----------------------------
def get_proximo_ep(nome):

    anime = get_anime(nome)

    if not anime:
        return None

    mal_id = anime["mal_id"]

    try:
        r = requests.get(
            f"https://api.jikan.moe/v4/anime/{mal_id}"
        )

        data = r.json()["data"]

        ep = data.get("episodes")

        return ep

    except:
        return None


# -----------------------------
# LANÇAMENTOS HOJE
# -----------------------------
def get_lancamentos_hoje():

    dias = {
        0: "monday",
        1: "tuesday",
        2: "wednesday",
        3: "thursday",
        4: "friday",
        5: "saturday",
        6: "sunday",
    }

    hoje = dias[datetime.today().weekday()]

    try:
        r = requests.get(
            f"https://api.jikan.moe/v4/schedules?filter={hoje}"
        )

        data = r.json()["data"]

        lista = []

        for anime in data[:10]:
            lista.append(anime["title"])

        return lista

    except:
        return []


# =============================
# COMANDO /IA
# =============================
async def ia(update: Update, context: ContextTypes.DEFAULT_TYPE):

    pergunta = " ".join(context.args).lower().strip()

    if not pergunta:
        await update.message.reply_text(
            "Use: /ia sua pergunta"
        )
        return

    try:

        # -------------------------
        # LANÇAMENTOS HOJE
        # -------------------------
        if "lançamento" in pergunta or "hoje" in pergunta:

            lista = get_lancamentos_hoje()

            if lista:
                texto = "📅 Episódios que lançam hoje:\n\n"
                texto += "\n".join(
                    [f"• {a}" for a in lista]
                )
            else:
                texto = "😅 Não encontrei lançamentos hoje."

            await update.message.reply_text(texto)
            return

        # -------------------------
        # ANIMES PARECIDOS
        # -------------------------
        if "parecido" in pergunta or "semelhante" in pergunta:

            nome = (
                pergunta.replace("animes parecidos com", "")
                .replace("parecido com", "")
                .strip()
            )

            anime = get_anime(nome)

            if anime:

                lista = get_animes_parecidos(
                    anime["mal_id"]
                )

                if lista:

                    texto = (
                        f"🎬 Animes parecidos com {anime['title']}:\n\n"
                    )

                    texto += "\n".join(
                        [f"• {a}" for a in lista]
                    )

                    await update.message.reply_text(texto)

                    return

            await update.message.reply_text(
                "Não encontrei animes parecidos."
            )

            return

        # -------------------------
        # PRÓXIMO EPISÓDIO
        # -------------------------
        if "próximo episódio" in pergunta:

            nome = pergunta.replace(
                "quando sai o próximo episódio de", ""
            ).strip()

            ep = get_proximo_ep(nome)

            if ep:

                texto = (
                    f"📺 {nome}\n\n"
                    f"Episódios totais: {ep}"
                )

            else:

                texto = "Não consegui encontrar o anime."

            await update.message.reply_text(texto)

            return

        # -------------------------
        # PERSONAGEM
        # -------------------------
        if "quem é" in pergunta:

            nome = pergunta.replace("quem é", "").strip()

            char = get_personagem(nome)

            if char:

                about = char.get("about")

                if about:
                    about = about[:400] + "..."
                else:
                    about = "Sem descrição."

                texto = (
                    f"👤 {char['name']}\n\n{about}"
                )

                await update.message.reply_text(texto)

                return

            await update.message.reply_text(
                "Personagem não encontrado."
            )

            return

        # -------------------------
        # ANIME
        # -------------------------
        anime = get_anime(pergunta)

        if anime:

            texto = format_anime(anime)

            await update.message.reply_text(texto)

            return

        # -------------------------
        # MANGA
        # -------------------------
        manga = get_manga(pergunta)

        if manga:

            texto = format_manga(manga)

            await update.message.reply_text(texto)

            return

        # -------------------------
        # FALLBACK
        # -------------------------
        await update.message.reply_text(
            "🤔 Não entendi a pergunta.\n\n"
            "Exemplos:\n"
            "/ia quais são os lançamentos de hoje\n"
            "/ia animes parecidos com naruto\n"
            "/ia quem é gojo\n"
            "/ia frieren"
        )

    except Exception as e:

        print(e)

        await update.message.reply_text(
            "⚠️ Erro ao processar pergunta."
        )
