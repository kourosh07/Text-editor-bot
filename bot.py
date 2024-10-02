import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, CallbackContext, Filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a few command handlers
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Send me a sentence and I will transform it into different font styles.')

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Send me a sentence, then choose a font style.')

def choose_font(update: Update, context: CallbackContext) -> None:
    """Prompt the user to choose a font style."""
    user_message = update.message.text
    context.user_data['user_message'] = user_message

    keyboard = [
        [
            InlineKeyboardButton("Font 1", callback_data='1'),
            InlineKeyboardButton("Font 2", callback_data='2'),
        ],
        [
            InlineKeyboardButton("Font 3", callback_data='3'),
            InlineKeyboardButton("Font 4", callback_data='4'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose a font style:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    """Handle font style selection."""
    query = update.callback_query
    query.answer()

    font_choice = query.data
    user_message = context.user_data.get('user_message', '')

    if font_choice == '1':
        styled_message = to_tiny_font(user_message)
    elif font_choice == '2':
        styled_message = to_bold(user_message)
    elif font_choice == '3':
        styled_message = to_italic(user_message)
    elif font_choice == '4':
        styled_message = to_monospace(user_message)
    else:
        styled_message = user_message

    query.edit_message_text(text=styled_message)

def to_tiny_font(text):
    """Convert text to a tiny font (using Unicode subscript characters)."""
    tiny_font_map = str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖᑫʳˢᵗᵘᵛʷˣʸᶻᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᑫᴿˢᵀᵁⱽᵂˣʸᶻ"
    )
    return text.translate(tiny_font_map)

def to_bold(text):
    """Convert text to bold (using Unicode characters)."""
    bold_font_map = str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"
    )
    return text.translate(bold_font_map)

def to_italic(text):
    """Convert text to italic (using Unicode characters)."""
    italic_font_map = str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡"
    )
    return text.translate(italic_font_map)

def to_monospace(text):
    """Convert text to monospace (using Unicode characters)."""
    monospace_font_map = str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉"
    )
    return text.translate(monospace_font_map)

def main() -> None:
    """Start the bot."""
    # Your bot token
    token = ' your token place '

    # Create the Updater and pass it your bot's token.
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e. message - present font options
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, choose_font))

    # Handle button presses
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
