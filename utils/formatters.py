from deep_translator import GoogleTranslator

def traduzir(texto):
    try:
        return GoogleTranslator(source='auto', target='pt').translate(texto)
    except:
        return texto


def format_anime(anime):

    titulo = anime["title"]
    episodios = anime["episodes"]
    score = anime["score"]
    synopsis = anime["synopsis"]

    generos = [g["name"] for g in anime["genres"]]
    generos = " | ".join([f"#{g}" for g in generos])

    studio = "Desconhecido"
    if anime["studios"]:
        studio = anime["studios"][0]["name"]

    temporada = anime["season"]
    ano = anime["year"]

    estreia = anime["aired"]["from"][:10]

    synopsis = traduzir(synopsis)

    texto = f"""
⭐ {titulo}

📚 GÊNEROS: {generos}

🎬 EPISÓDIOS: {episodios}
📺 TEMPORADA: {temporada} {ano}
📅 ESTREIA: {estreia}

🏢 ESTÚDIO: #{studio}

⭐ NOTA: {score}

📝 SINOPSE:
{synopsis[:500]}...
"""

    return texto
