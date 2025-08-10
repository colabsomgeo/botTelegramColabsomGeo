import requests
import nest_asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
from botTelegram.bot import handle_location, handle_audio, cancel, start, LOCATION, AUDIO

TOKEN = ''


#Aquiri o IP do servidor e Configurar no MongoDB Atlas
def get_public_ip():
    try:
        # Consulta o IP público usando uma API pública
        response = requests.get("https://ifconfig.me")
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Erro ao obter o IP público: {e}")
        return None


def main():
    # Obtém o IP público da instância Railway
    public_ip = get_public_ip()
    if public_ip:
        print(f"IP público do Railway: {public_ip}")
    else:
        print("Não foi possível obter o IP público.")

    nest_asyncio.apply()
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LOCATION: [MessageHandler(filters.LOCATION, handle_location)],
            AUDIO: [MessageHandler(filters.VOICE, handle_audio)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
