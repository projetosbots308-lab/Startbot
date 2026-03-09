from deep_translator import GoogleTranslator


def traduzir(texto):
    try:
        return GoogleTranslator(source="auto", target="pt").translate(texto)
    except:
        return texto


def cortar(texto, tamanho=300):
    if not texto:
        return "Sem sinopse."
    return texto[:tamanho] + "..."


def format_anime(anime):

    titulo = anime["title"]
    episodios = anime["episodes"]
    score = anime["score"]

    synopsis = traduzir(anime["synopsis"])
    synopsis = cortar(synopsis)

    generos = [g["name"] for g in anime["genres"]]
    generos = " | ".join([f"#{g}" for g in generos])

    studio = "Desconhecido"
    if anime["studios"]:
        studio = anime["studios"][0]["name"]

    estreia = anime["aired"]["from"][:10]

    texto = f"""
⭐ {titulo}

📚 GÊNEROS: {generos}

🎬 EPISÓDIOS: {episodios}
📅 ESTREIA: {estreia}
🏢 ESTÚDIO: #{studio}

⭐ NOTA: {score}

📝 SINOPSE:
{synopsis}
"""

    return texto
