from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, ConversationHandler
import nest_asyncio
nest_asyncio.apply()
from mongDB.mongoDB import salvarUser,acharUser,salvarInfoAudio
from datetime import datetime
import os
from processamento.processamento import extrair_informacoes_audio

captura_som ={}
LOCATION, AUDIO = range(2)

async def handle_location(update: Update, context: CallbackContext) -> int:
    location = update.message.location
    if location:
        await update.message.reply_text(
            f"Localização recebida: Latitude {location.latitude}, Longitude {location.longitude}."
        )
        captura_som["latitude"] = location.latitude
        captura_som["longitude"] = location.longitude
        captura_som["data_criacao"] = datetime.now().date().strftime("%Y-%m-%d") + " " + datetime.now().time().strftime("%H:%M:%S")

        await update.message.reply_text("Agora envie um áudio de 10 segundos.")
        print(f"Localização recebida: Latitude {location.latitude}, Longitude {location.longitude}.")
        return AUDIO
    else:
        await update.message.reply_text("Isso não parece ser uma localização. Por favor, envie sua localização.")
        return LOCATION
    
async def handle_audio(update: Update, context: CallbackContext) -> int:
    audio_file = update.message.voice
    if audio_file:
        audio_file = await audio_file.get_file()
        file_path = await audio_file.download_to_drive(custom_path='audio.ogg')

        # Simulação de processamento do áudio
        captura_som.update(extrair_informacoes_audio(file_path))
        print(captura_som)
        salvarInfoAudio(captura_som)
        os.remove(file_path)  # Remover arquivo temporário
        captura_som.clear()

        await update.message.reply_text("Áudio processado! Dados salvos no banco de dados.")
        print("Áudio processado! Dados salvos no banco de dados.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Por favor, envie um áudio válido.")
        return AUDIO

async def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    user_id = user.id
    first_name = user.first_name

    if acharUser(user_id) != None:
        await update.message.reply_text("Notei que você já contribuiu antes! Bem-vindo!")
        captura_som["id_user_object"] = acharUser(user_id) 
    else:
        await update.message.reply_text(
            "Opa! Você é novo. Fiz um cadastro automático com seu ID e Nome de usuário!"
        )
        
        captura_som["id_user_object"] = salvarUser(user_id, first_name)

    await update.message.reply_text("Por favor, envie sua localização.")
    return LOCATION

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Operação cancelada. Use /start para tentar novamente.")
    return ConversationHandler.END