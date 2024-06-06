from typing import Final
from telegram import Update
from telegram.ext import  Application,CommandHandler,filters,ContextTypes,MessageHandler
from dotenv import load_dotenv
import os
from pydub import AudioSegment
from utilities.transcripter import transcripter
from chattest import Chat
from utilities.redis_test import RedisTest

red = RedisTest()
#load env
load_dotenv()

token:Final = os.getenv('BOT_PASSKEY')
bot_username:Final = os.getenv('USER_NAME')
open_ai_key:Final = os.getenv('OPENAI_API_KEY')

#init all
transcripter =transcripter(key=open_ai_key)
chat = Chat()

#start bot code 

async def start_command (Update:Update,context:ContextTypes.DEFAULT_TYPE):
     red.delete_key(Update.effective_chat.id)
     await Update.message.reply_text("hello back ...")      



async def help_command (Update:Update,context:ContextTypes.DEFAULT_TYPE):
     
     await Update.message.reply_text("hello back ...")      




async def teach_command (Update:Update,context:ContextTypes.DEFAULT_TYPE):
    
     await Update.message.reply_text("hello back ...")      



#---handel response
     
async  def handel_respons(text:str,context:ContextTypes.DEFAULT_TYPE) -> str:
  await Update.message.reply_text ("we are happy to recive you  here")     



async def error_handler (update:Update,context:ContextTypes.DEFAULT_TYPE):
    try:
        # Attempt to notify the user
        print(context.error)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="An unexpected error occurred.")
    except Exception as exc:
        # Log the new exception if the message failed to send
        print(f"An error occurred while handling another error: {exc}")


#---handel response

async def handel_message(update:Update,context:ContextTypes.DEFAULT_TYPE) -> str:
    user_id = update.effective_user.id
    await update.message.reply_text( f"we are happy to recive you  here {user_id}")     

    


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice_file = update.message.voice
    # Retrieve the file from Telegram's servers
    new_file = await context.bot.get_file(voice_file.file_id)
    # Download the file
    file_path_oog = f'./{voice_file.file_id}.ogg'  # Define a custom path if needed
    await new_file.download_to_drive(custom_path=file_path_oog)  # Ensure this matches the library's API
    # Load your existing OGG file
    audio = AudioSegment.from_ogg(file_path_oog)
    # Export the loaded audio into MP3 format
    file_path_mp3 = f'./{voice_file.file_id}.mp3'
    audio.export(file_path_mp3, format='mp3')
    # Delete the original .ogg file after conversion
    os.remove(file_path_oog)
    #transcript 
    print("from bot!!---> voice recived")
    transcripted_text=  transcripter.transcribe(file_path_mp3)
    print(f"from bot!!---> voice transcripted Id  {update.message.chat_id}")
    chat_respond =  chat.chat(transcripted_text,chatId = update.effective_chat.id)
    print(f" from bot !!---> final res recived Id  {update.message.chat_id} ")
    # Respond to the user
    await context.bot.send_message(chat_id=update.effective_chat.id,text=chat_respond)
 
    #writing to txt file
    # with open('transcribed_text.txt', 'a', encoding='utf-8') as text_file:
    #     text_file.write(f"{transcripted_text} ----->respond = {chat_respond}")
    
    
     
 









if __name__ == '__main__':
    print("program Started")
    
    app = Application.builder().token(token).build()
    # commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('teach',teach_command))
    # Message 
    app.add_handler(MessageHandler(filters.TEXT,handel_message))
    #voice
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    #erro 
    app.add_error_handler(error_handler)
    #
    print("polling ")
    app.run_polling(poll_interval=2)