import telegram
import os
import logging
import database

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler

# Inicialização de parâmetros
token = os.environ['TOKEN']
support_chat_id = os.environ['SUP_CHAT_ID']

# Inicialização do logger
logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
                    datefmt='%d/%m/%Y, %H:%M:%S', level=logging.DEBUG)

# Conectando à API do Telegram
# O Updater recupera informações e o Dispatcher conecta comandos
updater = Updater(token=token)
dispatcher = updater.dispatcher

"""#########################################################################"""

def desconhecido(bot, update):
    """
        Executado quando um comando desconhecido é chamado
    """

    msg = "Desculpe, não consigo entender esse comando."
    bot.send_message(chat_id=update.message.chat_id, text=msg)

"""-------------------------------------------------------------------------"""

def suporte(bot, update):
    # Inicia o estado de suporte.
    msg = "Qual é o problema que você está encontrando?"
    bot.send_message(chat_id=update.message.chat_id, text=msg)
    msg = "(Utilize o comando \"\\cancelar\" para cancelar o pedido de suporte)"
    bot.send_message(chat_id=update.message.chat_id, text=msg)
    return SUPORTE_PERGUNTA_DUVIDA

"""-------------------------------------------------------------------------"""

def contato_com_suporte(bot, update):
    # Encaminha uma mensagem do usuário para o grupo de suporte.
    bot.forward_message(chat_id=int(support_chat_id), from_chat_id=update.message.chat_id, message_id=update.message.message_id)            
    msg = "Encaminhei sua mensagem para o suporte. Te aviso assim que tiver uma resposta."
    bot.send_message(chat_id=update.message.chat_id, text=msg)
    msg = "Desde já, peço desculpas pelo transtorno"
    bot.send_message(chat_id=update.message.chat_id, text=msg)
    return SUPORTE_ENCAMINHA_RESPOSTA
    
"""-------------------------------------------------------------------------"""

def resposta_do_suporte(bot, update):
    # Encaminha uma resposta vinda do grupo de suporte de volta para o usuário.
    if update.message.reply_to_message and update.message.reply_to_message.forward_from:
        bot.send_message(chat_id=int(update.message.reply_to_message.forward_from.id), text="O suporte enviou uma resposta:")
        bot.forward_message(chat_id=int(update.message.reply_to_message.forward_from.id), from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        return ConversationHandler.END

"""-------------------------------------------------------------------------"""

def cancelar(bot, update):
    # Finaliza o ConversationHandler do suporte e avisa o cancelamento no grupo
    # de suporte.
    msg = "Tudo bem. Estarei aqui se precisar de mim."
    bot.send_message(chat_id=update.message.chat_id, text=msg)
    bot.forward_message(chat_id=int(support_chat_id), from_chat_id=update.message.message_id)
    return ConversationHandler.END

"""-------------------------------------------------------------------------"""
def criar_bd_grupo(bot, update):
    # Se o comando for utilizado em um grupo
    if update.message.chat.type == 'group':
        # Se o comando for utilizado por um usuário na lista de administradores
        if update['message']['from']['id'] in bot.get_chat_administrators(update.message.chat_id):
            bot.send_message(chat_id=update.message.chat_id, text=msg)
            msg = "A base de dados deve ficar aberta para edições?\n"
            msg += "(Selecionar essa opção permitirá que os jogadores alterem as fichas)"

            # Cria um teclado para a resposta
            keyboard = [[telegram.KeyboardButton('Sim')], [telegram.KeyboardButton('Não')]]
            reply_kb_markup = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            # Exibe o teclado
            bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_kb_markup)
        # Se o comando não for utilizado por um usuário na lista de administradores
        else:
            msg = "Desculpe, mas esse comando deve ser utilizado por um administrador."
    # Se o comando não for utilizado em um grupo
    else:
        msg = "Desculpe, mas esse comando deve ser utilizado em um grupo."
        bot.send_message(chat_id=update.message.chat_id, text=msg)

"""-------------------------------------------------------------------------"""

def setup(bot, update):
    # Se o comando for utilizado em um grupo
    if update.message.chat.type == 'group':
        # Se já houver uma entrada desse grupo na base de dados
        if database.confereGrupo(update.message.chat_id):
            msg = "Ops! Parece que esse grupo já possui https://www.youtube.com/watch?v=eQOkCQ6CQxAuma entrada na base de dados..."
            bot.send_message(chat_id=update.message.chat_id, text=msg)
            msg = "Não se preocupe. A não ser que esse grupo seja recém-criado, não é um problema."
            bot.send_message(chat_id=update.message.chat_id, text=msg)
            msg = "Caso esse grupo seja recém-criado, use o comando /suporte, e resolveremos seu problema em breve."
            bot.send_message(chat_id=update.message.chat_id, text=msg)
            return ConversationHandler.END
        
        # Se o comando for utilizado por um usuário na lista de administradores
        if update['message']['from']['id'] in bot.get_chat_administrators(update.message.chat_id):
            msg = "As fichas de personagem associadas a esse grupo devem ficar abertas para edições?\n"
            bot.send_message(chat_id=update.message.chat_id, text=msg)

            # Cria um teclado para a resposta
            keyboard = [[telegram.KeyboardButton('Sim')], [telegram.KeyboardButton('Não')]]
            reply_kb_markup = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            # Exibe o teclado
            bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_kb_markup)
            return SETUP_RESPOSTA
        # Se o comando não for utilizado por um usuário na lista de administradores
        else:
            msg = "Desculpe, mas essa resposta deve ser dada por um administrador."
    # Se o comando não for utilizado em um grupo
    else:
        msg = "Já que esse é um chat privado, não precisamos configurar nada relacionado a um grupo."
        return ConversationHandler.END
"""-------------------------------------------------------------------------"""

def setup_resposta(bot, update):
    # Trata a resposta do setup de grupo
    if update.message.text == 'Sim':
        resp = True
    elif update.message.text == 'Não':
        resp = False
    else:
        return ConversationHandler.END

    database.criaGrupo(int(update.message.chat_id), int(update['message']['from']['id']), resp)
    msg = "Tudo certo!"
    

"""-------------------------------------------------------------------------"""

def start(bot, update):
    #A princípio, exibe uma mensagem de boas vindas e mostra os comandos.
    #Em seguida, 
    me = bot.get_me()

    # Mensagem de boas vindas
    msg = "Olá!\n"
    msg += "Meu nome é {0}!\n".format(me.first_name)
    msg += "Fui criada para gerenciar fichas de RPG do sistema Mutantes & Malfeitores.\n"
    msg += "Estou fazendo todo o setup básico do banco de dados nesse momento.\n"
    msg += "Digite /ajuda para exibir os comandos."

    database.carregarBD()
    setup(bot, update)

    # Commands menu
    main_menu_keyboard = [[telegram.KeyboardButton('/suporte')]]
    reply_kb_markup = telegram.ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True, one_time_keyboard=True)

    # Send the message with menu
    bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_kb_markup)

"""#########################################################################"""

# Cada CommandHadler liga um comando a uma função
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

"""-------------------------------------------------------------------------"""

# Os ConversationHandler criam um handler com estrutura de máquina de estados
# que é utilizada para coleta de mais de um dado, ou execuções que exigem
# que o bot mantenha uma "conversação" com o usuário.
# Esse handler trata das requisições de suporte.

SUPORTE_PERGUNTA_DUVIDA, SUPORTE_ENCAMINHA_RESPOSTA = range(2)
# Inicializa uma enumeração dos estados para o ConversationHandler.
# É possível usar inteiros diretamente, mas afeta a legibilidade.
support_handler = ConversationHandler(
    entry_points=[CommandHandler('suporte', suporte)],

    states={
        SUPORTE_PERGUNTA_DUVIDA: [RegexHandler('.*', contato_com_suporte)],
        SUPORTE_ENCAMINHA_RESPOSTA: [RegexHandler('.*', resposta_do_suporte)],
        },
    
    fallbacks=[CommandHandler('cancelar', cancelar)]
    )

dispatcher.add_handler(support_handler)

"""-------------------------------------------------------------------------"""
SETUP_RESPOSTA = range(1)
# Handler do setup
setup_handler = ConversationHandler(
    entry_points = [CommandHandler('start', start)],
    states={
        SETUP_RESPOSTA: [RegexHandler('.*', setup_resposta)],
    }
    )

"""-------------------------------------------------------------------------"""

unknown_handler = RegexHandler(r'/.*', desconhecido)
dispatcher.add_handler(unknown_handler)

"""-------------------------------------------------------------------------"""
