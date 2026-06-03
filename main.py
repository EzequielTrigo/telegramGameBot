from typing import Final
from dotenv import load_dotenv
import os
# pip install python-telegram-bot
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from queue import Queue
from partida import Partida
from globales import partidas

debugMode=False

print('Bot is now starting up...')

load_dotenv()

API_TOKEN: Final = os.getenv('API_BOT_TOKEN')
BOT_HANDLE: Final = os.getenv('BOT_HANDLE')


# Command to start the bot
async def initiate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Greetings! I am your bot. How can I assist you today?')


# Command to provide help information
async def assist_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Here comes the help')


# Command for custom functionality
async def personalize_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command, you can put whatever you want here.')


def generate_response(user_input: str) -> str:
    # Custom logic for response generation
    normalized_input: str = user_input.lower()

    if 'hi' in normalized_input:
        return 'Hello!'

    if 'how are you doing' in normalized_input:
        return 'I am functioning properly!'

    if 'i would like to subscribe' in normalized_input:
        return 'Sure go ahead!'

    return 'I didn’t catch that, could you please rephrase?'


async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Extract details of the incoming message
    chat_type: str = update.message.chat.type
    text: str = update.message.text
    print("usuario: " + str(update.effective_user))
    # Logging for troubleshooting
    print(f'User ({update.message.chat.id}) in {chat_type}: "{text}"')

    # Handle group messages only if bot is mentioned
    if chat_type == 'group':
        if BOT_HANDLE in text:
            cleaned_text: str = text.replace(BOT_HANDLE, '').strip()
            response: str = generate_response(cleaned_text)
        else:
            return  # Ignore messages where bot is not mentioned in a group
    else:
        response: str = generate_response(text)

    # Reply to the user
    print('Bot response:', response)
    await update.message.reply_text(response+". I know who you are, " + update.effective_user.first_name + "!")

async def menu(update, context):
    keyboard = [
        [InlineKeyboardButton("Jugar", callback_data="jugar")],
        [InlineKeyboardButton("Salir", callback_data="salir")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)   

    await update.message.reply_text(
        "Elegí una opción:",
        reply_markup=reply_markup
    )

async def boton(update, context):
    query = update.callback_query  

    print(query.data)

    if query.data == "jugar":
        print(query.from_user.username)
        print(query.message.reply_to_message.from_user.username)
        print("debug: " + str(debugMode))
        if (query.from_user.id == query.message.reply_to_message.from_user.id) and (not debugMode):
            await query.answer("No puedes jugar contra ti mismo!") 
            return
        partidas[query.chat_instance] = Partida(query)
        await partidas[query.chat_instance].updateKeyboard(query)
        await query.answer()  
        
        #await updateKeyboard(query, partidas[query.chat_instance])
    elif query.data == "salir":
        await query.answer()  
        await query.edit_message_text("Saliendo...")
    else: 
        await partidas[query.chat_instance].keyboardBottonPress(query, context, query.data)
        await query.answer() 

# Log errors
async def log_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

async def bienvenida(update, context):
    print("Me agregaron a un grupo!")

async def debug(update, context):
    print("debug: " + str(update))

# Start the bot
if __name__ == '__main__':
    app = Application.builder().token(API_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler('start', initiate_command))
    app.add_handler(CommandHandler('help', assist_command))
    app.add_handler(CommandHandler('custom', personalize_command))

    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(boton))
    # Register message handler
    #app.add_handler(MessageHandler(filters.TEXT, process_message))

    # Register error handler
    app.add_error_handler(log_error)

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, bienvenida))

    #app.add_handler(MessageHandler(filters.ALL, debug))
    #print("debug handler added")
    print('Starting polling...')
    # Run the bot
    app.run_polling(poll_interval=0.5)