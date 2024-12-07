import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler

# Importando os handlers do bot
from botTelegram.bot import handle_location, handle_audio, cancel, start, LOCATION, AUDIO

TOKEN = '7621244735:AAHYyFa1QI99bSLDl9jpwkB2L0QX10kQzwY'

# Configure o Flask
app = Flask(__name__)

# Configuração do bot do Telegram
application = Application.builder().token(TOKEN).build()

# Configuração do ConversationHandler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        LOCATION: [MessageHandler(filters.LOCATION, handle_location)],
        AUDIO: [MessageHandler(filters.VOICE, handle_audio)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

application.add_handler(conv_handler)

# Logger para erros
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Rota do webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """Endpoint que será chamado pelo Telegram para entregar mensagens."""
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "OK", 200


@app.route("/")
def index():
    """Rota principal para verificar se o serviço está funcionando."""
    return "Bot do Telegram está ativo!", 200


if __name__ == "__main__":
    # Configurando o webhook
    webhook_url = f"https://<SEU_DOMÍNIO>.pythonanywhere.com/{TOKEN}"  # Substitua <SEU_DOMÍNIO> pelo domínio fornecido pelo PythonAnywhere
    application.bot.set_webhook(url=webhook_url)
    app.run()
