def format_anime(anime):

    title = anime["title"]
    episodes = anime["episodes"]
    score = anime["score"]
    synopsis = anime["synopsis"]

    genres = [g["name"] for g in anime["genres"]]
    genres = " | ".join(genres)

    text = f"""
⭐ {title}

🎭 GÊNEROS: {genres}
📺 EPISÓDIOS: {episodes}
⭐ NOTA: {score}

📖 SINOPSE:
{synopsis[:400]}...
"""

    return text
