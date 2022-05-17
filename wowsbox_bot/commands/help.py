from telegram import Update
from telegram.ext import CommandHandler


def help_command(update: Update, _):
    update.effective_chat.send_message(text='使用帮助：\n\n'
                                            '/get 获取补给箱\n'
                                            '/my 查看我的补给箱\n'
                                            '/open 打开补给箱\n\n'
                                            '没有十连功能，只能一个一个开哦😋\n\n'
                                            '输入 /help 可再次查看此帮助')


help_handler = CommandHandler('help', help_command, run_async=True)
