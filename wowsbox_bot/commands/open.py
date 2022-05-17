import time
from typing import Optional

from telegram import Update, ParseMode, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters

from ..utils import is_group, encode_data
from ..wows import Container, i18n_containers


def open_command(update: Update, context: CallbackContext):
    if context.user_data is None:
        return

    message = ''
    if is_group(update):
        message += f'{update.effective_user.mention_html()}，'

    containers = context.user_data.get('containers', {})
    if len(containers) == 0:
        message += '你还没有任何补给箱'
    else:
        message += '请在键盘选择你要打开的补给箱'

    update.effective_message.reply_text(message,
                                        reply_markup=ReplyKeyboardMarkup.from_column([
                                            KeyboardButton(Container(id=container_id).get_localized_name())
                                            for container_id in containers.keys()
                                        ], one_time_keyboard=True, selective=True),
                                        parse_mode=ParseMode.HTML,
                                        quote=False)


def open_callback(update: Update, context: CallbackContext):
    open_command(update, context)


def open_message(update: Update, context: CallbackContext):
    if context.user_data is None:
        return

    requested_container_name = update.effective_message.text.strip()
    requested_container: Optional[Container] = None
    for container_id, container_name in i18n_containers.items():
        if container_name == requested_container_name:
            requested_container = Container(id=container_id)
            break

    containers = context.user_data.get('containers', {})
    if containers.get(requested_container.id, 0) == 0:
        update.effective_message.reply_text('你还没有这个补给箱，快输入 /get 获取一个吧',
                                            reply_markup=ReplyKeyboardRemove(),
                                            quote=True)
        return
    else:
        context.user_data['containers'][requested_container.id] -= 1
        if context.user_data['containers'][requested_container.id] == 0:
            del context.user_data['containers'][requested_container.id]

    update.effective_message.reply_text('好，马上给你打开这个补给箱',
                                        reply_markup=ReplyKeyboardRemove(),
                                        quote=True)

    message_sent = update.effective_chat.send_message('‎\n📦\n‎')
    time.sleep(0.2)
    message_sent.edit_text('🪝\n📦\n\n\n         🚢')
    time.sleep(0.2)
    message_sent.edit_text('‎\n  🪝\n  📦\n\n        🚢')
    time.sleep(0.2)
    message_sent.edit_text('‎\n\n    🪝\n    📦\n       🚢')
    time.sleep(0.2)
    message_sent.edit_text('‎\n\n\n      📦\n      🚢')
    time.sleep(0.1)

    drops = requested_container.get_pack().get_drops()

    message = ''
    if is_group(update):
        message += f'{update.effective_user.mention_html()}，'
    message += '你开出了：\n\n'
    message += '\n'.join([drop.render() for drop in drops])
    message += '\n‎'

    message_sent.edit_text(message,
                           reply_markup=InlineKeyboardMarkup.from_column([
                               InlineKeyboardButton('再开一箱', callback_data=encode_data('open')),
                               # InlineKeyboardButton('历史记录', callback_data=encode_data('history')),
                           ]),
                           parse_mode=ParseMode.HTML)


open_handler = CommandHandler('open', open_command, run_async=True)
open_message_handler = MessageHandler(Filters.text(i18n_containers.values()), open_message)
