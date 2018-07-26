import telegram
import os
#import redis
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

# Inicialização de parâmetros
token = os.environ['TOKEN']
support_chat_id = os.environ['SUP_CHAT_ID']

# Inicialização do logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# Conectando à API do Telegram
# O Updater recupera informações e o Dispatcher conecta comandos
updater = Updater(token=token)
dispatcher = updater.dispatcher

"""#########################################################################"""

# Variáveis globais
support_flag = True

"""#########################################################################"""

def start(bot, update):
    """
        Exibe uma mensagem de boas vindas e mostra os comandos.
    """
    me = bot.get_me()

    # Mensagem de boas vindas
    msg = "Olá!\n"
    msg += "Eu sou {0} e estou aqui para ajudar.\n".format(me.first_name)
    msg += "O que você gostaria de fazer?\n\n"
    msg += "/suporte - Abre um novo ticket de suporte\n"

    # Commands menu
    main_menu_keyboard = [[telegram.KeyboardButton('/suporte')]]
    reply_kb_markup = telegram.ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True, one_time_keyboard=True)

    # Send the message with menu
    bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_kb_markup)

"""-------------------------------------------------------------------------"""

def desconhecido(bot, update):
    """
        Executado quando um comando desconhecido é chamado
    """

    msg = "Desculpe, não consigo entender esse comando."
    bot.send_message(chat_id=update.message.chat_id, text=msg)

"""-------------------------------------------------------------------------"""

def suporte(bot, update):
    """
        Responde ao pedido de suporte e ativa a flag para a comunicação com o suporte
    """
    bot.send_message(chat_id=update.message.chat_id,
                     text="Qual é o problema que você está tendo?")
    support_flag = True

"""-------------------------------------------------------------------------"""

def contato_com_suporte(bot, update):
    """
        Faz a ponte entre o grupo/chat de suporte e um local de uso.

        Se a mensagem é uma resposta do suporte ao usuário, o bot a envia ao usuário.
        Se a mensagem é do usuário, o bot a repassa para o grupo de suporte.
    """
    if support_flag:
        if update.message.reply_to_message and \
           update.message.reply_to_message.forward_from:
            # Se for uma resposta do suporte ao usuário, o bot responde ao usuário
            bot.send_message(chat_id=update.message.reply_to_message.forward_from.id, text=update.message.text)
        else:
            # Se for uma requisição do usuário, o bot a repassa para o
            # grupo de suporte
            bot.forward_message(chat_id=int(support_chat_id), from_chat_id=update.message.chat_id, message_id=update.message.message_id)
            
            bot.send_message(chat_id=update.message.chat_id, text="Me dá só um minuto.")

"""#########################################################################"""

# Cada CommandHadler liga um comando a uma função
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

support_handler = CommandHandler('suporte', suporte)
dispatcher.add_handler(support_handler)

unknown_handler = RegexHandler(r'/.*', desconhecido)
dispatcher.add_handler(unknown_handler)

support_contact_handler = MessageHandler(Filters.text, contato_com_suporte)
# O handler de mensagens deve ser o último
dispatcher.add_handler(support_contact_handler)
