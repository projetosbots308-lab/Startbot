import os
import logging

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# módulos do bot
from modules.start import start
from modules.welcome import welcome
from modules.anime import anime
from modules.manga import manga
from modules.season import season
from modules.moderation import ban
from modules.ia import ia


# CONFIGURAÇÃO DE LOGS (importante no Railway)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


# TOKEN vindo das variáveis do Railway
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("⚠️ BOT_TOKEN não encontrado nas variáveis de ambiente")


# comando de teste
async def ping(update, context):
    await update.message.reply_text("🏓 Pong! Bot funcionando corretamente.")


def main():

    logger.info("🚀 Iniciando bot...")

    app = ApplicationBuilder().token(TOKEN).build()

    # comandos principais
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("anime", anime))
    app.add_handler(CommandHandler("manga", manga))
    app.add_handler(CommandHandler("season", season))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("ia", ia))

    # comando de teste
    app.add_handler(CommandHandler("ping", ping))

    # boas vindas
    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            welcome
        )
    )

    logger.info("✅ Bot iniciado com sucesso")

    app.run_polling()


if __name__ == "__main__":
    main()
