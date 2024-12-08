import nest_asyncio
nest_asyncio.apply()
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
from botTelegram.bot import handle_location, handle_audio, cancel, start, LOCATION, AUDIO
import requests
TOKEN = '7621244735:AAHYyFa1QI99bSLDl9jpwkB2L0QX10kQzwY'

def get_public_ip():
    response = requests.get("https://api64.ipify.org?format=json")
    return response.json()["ip"]

def main():
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
    print("IP público:", get_public_ip())