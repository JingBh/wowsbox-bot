from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import CallbackContext, CommandHandler

from ..utils import encode_data, is_group
from ..wows import Container


def my_command(update: Update, context: CallbackContext):
    if context.user_data is None:
        return

    message = ''
    if is_group(update):
        message += f'{update.effective_user.mention_html()}，'

    containers = context.user_data.get('containers', {})
    if len(containers) == 0:
        message += '你还没有任何补给箱'
    else:
        message += '你现在拥有：\n\n'
        for container_id, count in containers.items():
            message += f'<strong>{Container(id=container_id).get_localized_name()}</strong> x{count}\n'

    update.effective_message.reply_text(message,
                                        reply_markup=InlineKeyboardMarkup.from_row([
                                            InlineKeyboardButton('获取补给箱',
                                                                 callback_data=encode_data('get')),
                                            InlineKeyboardButton('打开补给箱',
                                                                 callback_data=encode_data('open'))
                                        ]),
                                        parse_mode=ParseMode.HTML)


def my_callback(update: Update, context: CallbackContext):
    my_command(update, context)


my_handler = CommandHandler('my', my_command, run_async=True)
