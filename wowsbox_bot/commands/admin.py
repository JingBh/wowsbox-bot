import logging

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from ..env import env

DEVELOPER_ID = env.int('DEVELOPER_ID', None)

if DEVELOPER_ID is None:
    logging.warning('Developer ID not set, no one will get admin privilege.')


def admin_command(update: Update, context: CallbackContext):
    if DEVELOPER_ID and update.effective_user.id == DEVELOPER_ID:
        if ' '.join(context.args) == '':
            return

        command = context.args[0]
        if command == 'give':
            if len(context.args) < 2:
                update.effective_message.reply_text('指令参数不足')

            user_id = update.effective_user.id
            if update.effective_message.reply_to_message is not None:
                user_id = update.effective_message.reply_to_message.from_user.id

            if 'containers' not in context.dispatcher.user_data[user_id]:
                context.dispatcher.user_data[user_id]['containers'] = {}
            if context.args[1] not in context.dispatcher.user_data[user_id]['containers']:
                context.dispatcher.user_data[user_id]['containers'][context.args[1]] = 0
            context.dispatcher.user_data[user_id]['containers'][context.args[1]] += int(context.args[2])
            if context.dispatcher.user_data[user_id]['containers'][context.args[1]] <= 0:
                del context.dispatcher.user_data[user_id]['containers'][context.args[1]]

            update.effective_message.reply_text('指令执行成功')
        else:
            update.effective_message.reply_text('此指令不存在')
    else:
        update.effective_message.reply_text('你寄吧谁啊，爬')


admin_handler = CommandHandler('admin', admin_command, run_async=True)
