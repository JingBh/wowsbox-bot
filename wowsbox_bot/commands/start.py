from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from .help import help_command


def start_command(update: Update, context: CallbackContext):
    if not (context.args and ' '.join(context.args) == '_quiet'):
        update.effective_chat.send_message(text='有非洲人')
        update.effective_chat.send_message(text='游戏里开不出船')
        update.effective_chat.send_message(text='😅')

        help_command(update, context)


start_handler = CommandHandler('start', start_command, run_async=True)
