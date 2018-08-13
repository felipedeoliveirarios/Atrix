import telegram
import os
import logging
import database

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, CallbackQueryHandler

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
    msg = "(Utilize o comando /cancelar para cancelar o pedido de suporte)"
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

def is_group_admin(bot, user_id, group_id):
    is_admin = False
    for chat_member in bot.get_chat_administrators(group_id):
        if chat_member.user.id == user_id:
            is_admin = True
            break
    return is_admin

"""-------------------------------------------------------------------------"""

def setup(bot, update):
    # Se o setup for iniciado em um grupo
    if update.message.chat.type == 'group':
        # Se já houver uma entrada desse grupo na base de dados
        if database.confereGrupo(update.message.chat_id):
            msg = "Ops! Parece que esse grupo já possui uma entrada na base de dados..."
            bot.send_message(chat_id=update.message.chat_id, text=msg)
            msg = "Não se preocupe. A não ser que esse grupo seja recém-criado, não é um problema."
            bot.send_message(chat_id=update.message.chat_id, text=msg)
            msg = "Caso esse grupo seja recém-criado, use o comando /suporte, e resolveremos seu problema em breve."
            bot.send_message(chat_id=update.message.chat_id, text=msg)
            return ConversationHandler.END
        
        # Se o usuário for um administrador do grupo...
        if is_group_admin(bot, update.message.from_user.id, update.message.chat.id):
            msg = "As fichas de personagem associadas a esse grupo devem ficar abertas para edições?\n"
            # Cria um teclado para a resposta
            keyboard = [[telegram.InlineKeyboardButton("Sim", callback_data = "Sim")],
                        [telegram.InlineKeyboardButton("Não", callback_data = "Não")]]
            inline_kb_markup = telegram.InlineKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            # Exibe o teclado
            bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=inline_kb_markup)
            return SETUP_RESPOSTA
        # Se o setup não for iniciado/respondido por um usuário na lista de administradores.
        else:
            msg = "Desculpe, mas é preciso ser um administrador do grupo para concluir o setup."
            bot.send_message(chat_id=update.message.chat_id, text=msg)
    # Se o setup não for iniciado em um grupo
    else:
        msg = "Já que esse é um chat privado, não precisamos configurar nada relacionado a um grupo."
        bot.send_message(chat_id=update.message.chat_id, text=msg)
        return ConversationHandler.END
"""-------------------------------------------------------------------------"""

def setup_resposta(bot, update):
    # Trata a resposta do setup de grupo
    query = update.callback_query
    if query.data == "Sim":
        resp = True
    else:
        resp = False
    bot.edit_message_reply_markup(query.message.chat_id, query.message.message_id, reply_markup = None)
    database.criaGrupo(int(query.message.chat_id), int(query.from_user.id), resp)
    msg = "Tudo certo!"
    bot.send_message(chat_id=query.message.chat_id, text=msg)
    msg = "À partir de agora, sinta-se à vontade para utilizar o sistema."
    bot.send_message(chat_id=query.message.chat_id, text=msg)
    
"""-------------------------------------------------------------------------"""

def setup_cancelar(bot, update):
    msg = "Ok, vamos deixar o setup pra outra hora."
    bot.send_message(chat_id=update.message.chat_id, text=msg)
    msg = "Use o comando /start para tentar novamente depois."
    bot.send_message(chat_id=update.message.chat_id, text=msg)
    msg = "(Lembrando que, sem o setup apropriado, não serei capaz de gerenciar as fichas de personagem...)"
    bot.send_message(chat_id=update.message.chat_id, text=msg)

    return ConversationHandler.END

"""-------------------------------------------------------------------------"""

def start(bot, update):
    #A princípio, exibe uma mensagem de boas vindas e mostra os comandos.
    #Em seguida, 
    me = bot.get_me()

    # Mensagem de boas vindas
    msg = "Olá!\n"
    msg += "Meu nome é {0}!\n".format(me.first_name)
    msg += "Fui criada para gerenciar fichas de RPG do sistema Mutantes & Malfeitores.\n"
    msg += "Use o comando /ajuda para exibir a lista de comandos."
    bot.send_message(chat_id=update.message.chat_id, text=msg)
    msg = "Agora, estou iniciando o setup básico do banco de dados."
    bot.send_message(chat_id=update.message.chat_id, text=msg)
    
    database.carregarBD()

    return setup(bot, update)

"""#########################################################################"""

# Cada CommandHandler liga um comando a uma função.

# Os ConversationHandler criam um handler com estrutura de máquina de estados
# que é utilizada para coleta de mais de um dado, ou execuções que exigem
# que o bot mantenha uma "conversação" com o usuário.

# Os CallbackQueryHandler reagem quando há uma resposta vinda de um teclado inline.

"""-------------------------------------------------------------------------"""

# Esse handler trata das requisições de suporte.

SUPORTE_PERGUNTA_DUVIDA, SUPORTE_ENCAMINHA_RESPOSTA = range(2)
# Inicializa uma enumeração dos estados para o ConversationHandler.
# É possível usar inteiros diretamente, mas afeta a legibilidade.

support_handler = ConversationHandler(
    entry_points=[CommandHandler('suporte', suporte)],

    states={
        SUPORTE_PERGUNTA_DUVIDA: [RegexHandler('$[^/].*', contato_com_suporte)],
        SUPORTE_ENCAMINHA_RESPOSTA: [RegexHandler('$[^/].*', resposta_do_suporte)],
        },
    
    fallbacks=[CommandHandler('cancelar', cancelar)]
    )

dispatcher.add_handler(support_handler)

"""-------------------------------------------------------------------------"""

# Esse handler trata do setup inicial quando executado o comando /start.

SETUP_RESPOSTA = range(1)
# Inicializa uma enumeração dos estados para o ConversationHandler.
# É possível usar inteiros diretamente, mas afeta a legibilidade.

setup_handler = ConversationHandler(
    entry_points = [CommandHandler('start', start)],
    states={
        SETUP_RESPOSTA: [CallbackQueryHandler(setup_resposta)],
    },
    fallbacks=[CommandHandler('cancelar', setup_cancelar)],
    per_chat = True
    )

dispatcher.add_handler(setup_handler)

"""-------------------------------------------------------------------------"""

unknown_handler = RegexHandler(r'/.*', desconhecido)
dispatcher.add_handler(unknown_handler)

"""-------------------------------------------------------------------------"""
