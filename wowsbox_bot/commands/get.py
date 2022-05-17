from typing import Optional

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import CallbackContext, CommandHandler

from ..utils import encode_data, is_group
from ..wows import Container


def get_command(update: Update, _):
    if is_group(update):
        update.effective_message.reply_text('为防止刷屏，请和我私聊使用此命令~')
    else:
        update.effective_chat.send_message('拿，随便拿，反正你开不到船~')
        update.effective_message.reply_text('想要哪种补给箱？',
                                            reply_markup=InlineKeyboardMarkup.from_column([
                                                InlineKeyboardButton('💰 更多银币',
                                                                     callback_data=encode_data('get', ctype='mc')),
                                                InlineKeyboardButton('🚩 更多信号旗',
                                                                     callback_data=encode_data('get', ctype='ms')),
                                                InlineKeyboardButton('💎 更多资源',
                                                                     callback_data=encode_data('get', ctype='mr')),
                                                InlineKeyboardButton('🍀 试试你的运气',
                                                                     callback_data=encode_data('get', ctype='tyl'))
                                            ]))


def get_callback(update: Update, context: CallbackContext, ctype: Optional[str] = None):
    if context.user_data is not None and ctype is not None:
        container = Container.get_container(ctype)

        if 'containers' not in context.user_data:
            context.user_data['containers'] = {}
        if container.id not in context.user_data['containers']:
            context.user_data['containers'][container.id] = 1
        else:
            context.user_data['containers'][container.id] += 1

        message = ''
        if is_group(update):
            message += f'{update.effective_user.mention_html()}，'
        message += f'你获得了一个：\n\n' \
                   f'<strong>{container.get_localized_name()}</strong>\n‎'
        message_sent = update.effective_chat.send_message(message,
                                                          reply_markup=InlineKeyboardMarkup.from_row([
                                                              InlineKeyboardButton('查看我的补给箱',
                                                                                   callback_data=encode_data('my')),
                                                              InlineKeyboardButton('打开补给箱',
                                                                                   callback_data=encode_data('open'))
                                                          ]),
                                                          parse_mode=ParseMode.HTML)

        if container.id == 'super':
            message_sent.reply_text('这么牛？希望你在游戏里拿不到这个', quote=True)

    else:
        get_command(update, context)


get_handler = CommandHandler('get', get_command, run_async=True)
