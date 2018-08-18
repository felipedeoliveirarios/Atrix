import telegram
import os
import logging
import database

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, CallbackQueryHandler

# Inicialização de parâmetros
token = os.environ['TOKEN']
support_chat_id = int(os.environ['SUP_CHAT_ID'])

# Inicialização do logger
logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
                    datefmt='%d/%m/%Y, %H:%M:%S', level=logging.DEBUG)

# Conectando à API do Telegram
# O Updater recupera informações e o Dispatcher conecta comandos
updater = Updater(token=token)
dispatcher = updater.dispatcher

"""#########################################################################"""
# FUNÇÕES GERAIS

# Função que retorna se um usuário é administrador de um grupo.
def is_group_admin(bot, user_id, group_id):
    is_admin = False
    for chat_member in bot.get_chat_administrators(group_id):
        if chat_member.user.id == user_id:
            is_admin = True
            break
    return is_admin

# Função que remove um InlineKeyboardMarkup de uma mensagem.
def rmv_inline_keyboard(bot, query):
    bot.edit_message_reply_markup(query.message.chat_id, query.message.message_id, reply_markup = None)

# Função que retorna a id do usuário, independente da update ser
# um callback_query ou mensagem.
def get_usr_id(bot, update):
    try:
        str(update.callback_query.message.from_user.id)
        return update.callback_query.message.from_user.id
    except:
        return update.message.from_user.id

# Função que retorna a id do chat, independente da update ser um
# callback_query ou uma mensagem.
def get_chat_id(bot, update):
    try:
        str(update.callback_query.message.chat_id)
        return update.callback_query.message.chat_id
    except:
        return update.message.chat_id
"""#########################################################################"""

# Trata comandos desconhecidos.
def desconhecido(bot, update):
    chat_id = get_chat_id(bot, update)
    msg = "Desculpe, não consigo entender esse comando."
    bot.send_message(chat_id=update.message.chat_id, text=msg)
    msg = "Utilize o comando /ajuda para exibir a lista de comandos."
    bot.send_message(chat_id=update.message.chat_id, text=msg)

"""-------------------------------------------------------------------------"""

# Inicia o tratamento de uma requisição de suporte.
def suporte(bot, update):
    msg = "Qual é o problema?\n(Descreva da forma mais clara que puder)"
    bot.send_message(chat_id=update.message.chat_id, text=msg)
    msg = "(Utilize o comando /cancelar para cancelar o pedido de suporte)"
    bot.send_message(chat_id=update.message.chat_id, text=msg)
    return SUPORTE_PERGUNTA_DUVIDA

"""-------------------------------------------------------------------------"""

# Encaminha uma mensagem do usuário para o grupo de suporte.
def contato_com_suporte(bot, update):
    bot.forward_message(chat_id=support_chat_id, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
    
    msg = "Encaminhei sua mensagem para o suporte. Te aviso assim que tiver uma resposta."
    bot.send_message(chat_id=update.message.chat_id, text=msg)
    msg = "Desde já, peço desculpas pelo transtorno"
    bot.send_message(chat_id=update.message.chat_id, text=msg)
    return SUPORTE_ENCAMINHA_RESPOSTA
    
"""-------------------------------------------------------------------------"""

# Encaminha uma resposta vinda do grupo de suporte de volta para o usuário.
def resposta_do_suporte(bot, update):
    if update.message.reply_to_message and update.message.reply_to_message.forward_from:
        msg = "O suporte enviou uma resposta:"
        bot.send_message(chat_id=update.message.reply_to_message.forward_from.id, text=msg)
        bot.forward_message(chat_id=update.message.reply_to_message.forward_from.id, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        return ConversationHandler.END

"""-------------------------------------------------------------------------"""

# Finaliza a execução de um ConversationHandler
def cancelar(bot, update):
    msg = "Tudo bem. Estarei aqui se precisar de mim."
    bot.send_message(chat_id=update.message.chat_id, text=msg)
    return ConversationHandler.END

"""-------------------------------------------------------------------------"""

# Inicia o setup básico.
def setup(bot, update):
    # Se o setup for iniciado em um grupo
    if update.message.chat.type == 'group':
        # Se já houver uma entrada desse grupo na base de dados
        if database.confere_grupo(update.message.chat_id):
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

# Função que trata a resposta do setup de grupo
def setup_resposta(bot, update):
    # Cria um alias para a resposta do teclado, para melhorar a legibilidade.
    query = update.callback_query
    if query.data == "Sim":
        resp = True
    else:
        resp = False
    rmv_inline_keyboard(bot, query)
    database.cria_grupo(int(query.message.chat_id), int(query.from_user.id), resp)
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

# A princípio, exibe uma mensagem de boas vindas e mostra os comandos.
# Em seguida, inicia o setup do banco de dados.
def start(bot, update):
    me = bot.get_me()

    # Mensagem de boas vindas
    msg = "Olá!\n"
    msg += "Meu nome é {0}!\n".format(me.first_name)
    msg += "Fui criada para gerenciar fichas de RPG do sistema Mutantes & Malfeitores.\n"
    msg += "Use o comando /ajuda para exibir a lista de comandos."
    bot.send_message(chat_id=update.message.chat_id, text=msg)
    msg = "Agora, estou iniciando o setup básico do banco de dados."
    bot.send_message(chat_id=update.message.chat_id, text=msg)
    
    database.carregar_bd()

    return setup(bot, update)

"""-------------------------------------------------------------------------"""

def ficha(bot, update):
    # Caso já exista uma entrada da combinação de usuário e grupo no BD...
    if database.confere_usuario(update.message.chat_id, update.message.from_user.id):
        # Recupera e envia as informações básicas do personagem.
        pers = database.get_informação_basica(update.message.chat_id, update.message.from_user.id)
        msg = "{}, Nv. {}\n{} {}, {}".format(pers.nome, pers.nivel, pers.ident, pers.sexo, pers.idade)
        bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup = inline_kb_markup)
        
        msg = "E então, o que tem em mente?"
        
        keyboard = [[telegram.InlineKeyboardButton("Editar Ficha", callback_data = "Editar")],
                    [telegram.InlineKeyboardButton("Excluir Ficha", callback_data = "Excluir")],
                    [telegram.InlineKeyboardButton("Importar/Exportar Ficha", callback_data = "Imp/Exp")],
                    [telegram.InlineKeyboardButton("Sair", callback_data = "Sair")]]
        inline_kb_markup = telegram.InlineKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        # Envia a pergunta e o menu de opções de operações relacionadas à ficha
        bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup = inline_kb_markup)
        # Passa para o próximo estado, que irá tratar a resposta.
        return FICHA_MENU

    # Caso não exista uma entrada da combinação de usuário e grupo no BD...
    else:
        msg = "Não encontrei nenhuma ficha sua nos meus arquivos..."
        bot.send_message(chat_id=update.message.chat_id, text=msg)
        msg = "Que tal criar uma?"
        
        keyboard = [[telegram.InlineKeyboardButton("Sim", callback_data = "Sim")],
                    [telegram.InlineKeyboardButton("Não", callback_data = "Não")]]
        inline_kb_markup = telegram.InlineKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        # Envia a pergunta e um teclado anexo com sim/não.
        bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup = inline_kb_markup)
        # Passa para o próximo estado, que irá conduzir a outro
        # ConversationHandler para acompanhar o usuário na criação de ficha.
        return FICHA_CRIAR

"""-------------------------------------------------------------------------"""

# Trata a resposta enviada pelo menu exibido em /ficha quando o usuário
# já possúi uma ficha.
def ficha_menu(bot, update):
    query = update.callback_query
    # Remove o teclado após receber a resposta.
    rmv_inline_keyboard(bot, query)

    # Trata a resposta do usuário via menu.
    if query.data == "Editar":
        # Inicia o ConversationHandler de edição de fichas
        ficha_editar(bot, update)
        return FICHA_RESET

    elif query.data == "Excluir":
        msg = "Uau. Essa é uma decisão bem séria. Tem certeza?"
        keyboard = [[telegram.InlineKeyboardButton("Sim", callback_data = "Sim")],
                    [telegram.InlineKeyboardButton("Não", callback_data = "Não")]]
        inline_kb_markup = telegram.InlineKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        bot.send_message(chat_id=query.message.chat_id, text=msg, reply_markup = inline_kb_markup)
        return FICHA_EXCLUIR

    elif query.data == "Imp/Exp":
        msg = "Importar ou exportar?"
        keyboard = [[telegram.InlineKeyboardButton("Importar", callback_data = "IMP")],
                    [telegram.InlineKeyboardButton("Exportar", callback_data = "EXP")]]
        inline_kb_markup = telegram.InlineKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        bot.send_message(chat_id=query.message.chat_id, text=msg, reply_markup = inline_kb_markup)
        return FICHA_IMP/EXP
        
    elif query.data == "Sair":
        msg = "Ok! Me chame de novo se precisar de algo."
        bot.send_message(chat_id=query.message.chat_id, text=msg)
        return ConversationHandler.END

    else:
        return FICHA_MENU

"""-------------------------------------------------------------------------"""

def ficha_criar(bot, update):
    # Cria um alias para a resposta do teclado personalizado, para
    # melhorar a legibilidade.
    query = update.callback_query
    # Remove o teclado já utilizado.
    rmv_inline_keyboard(bot, query)
    
    if query.data == "Sim":
        # Caso o usuário decida por criar uma ficha, se iniciará um
        # ConversationHandler através da função para guiá-lo no processo
        ficha_criar_nome(bot, update)
        return FICHA_RESET
    else:
        # Caso o usuário não tenha uma ficha nem possua interesse em
        # criar uma no momento, não há nada a se fazer além de finalizar
        # a execução do módulo.
        return ConversationHandler.END

"""-------------------------------------------------------------------------"""

def ficha_excluir(bot, update):
    query = update.callback_query
    rmv_inline_keyboard(bot, query)

    if query.data == "Sim":
        # Caso o usuário decida por criar excluir a ficha...
        database.del_ficha(query.message.chat_id, query.from_user.id)
        msg = "Tá legal. Está feito."
        bot.send_message(chat_id=query.message.chat_id, text=msg)
        return FICHA_RESET
    else:
        # Caso o usuário decida não excluir a ficha...
        return FICHA_RESET

"""-------------------------------------------------------------------------"""

def ficha_impexp():
    query = update.callback_query
    rmv_inline_keyboard(bot, query)

    if query.data == "IMP":
        msg = "De qual chat quer importar uma ficha?"
        # TODO: Criar um teclado contendo os chats em comum entre Atrix
        # e o usuário
        bot.send_message(chat_id=query.message.chat_id, text=msg)
        return FICHA_IMP
    elif query.data == "EXP":
        msg = "Para qual chat quer exportar essa ficha?\n"
        msg += "(Lembre-se que, se houver uma ficha no chat de destino, ela será apagada.)"
        # TODO: Criar um teclado contendo os chats em comum entre Atrix
        # e o usuário
        bot.send_message(chat_id=query.message.chat_id, text=msg)
        return FICHA_EXP
    else:
        return FICHA_RESET

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

# Esse handler trata do menu de fichas e conduz às operações mais específicas
# do CRUD, e de importação e exportação.

FICHA_MENU, FICHA_CRIAR, FICHA_EXCLUIR, FICHA_IMP/EXP, FICHA_IMP, FICHA_EXP, FICHA_RESET = range(7)

sheet_handler = ConversationHandler(
    entry_points = [CommandHandler('ficha', ficha)],
    states = {
        FICHA_MENU: [CallbackQueryHandler(ficha_menu)]
        FICHA_CRIAR: [CallbackQueryHandler(ficha_criar)],
        FICHA_EXCLUIR: [CallbackQueryHandler(ficha_excluir)],
        FICHA_IMP/EXP: [CallbackQueryHandler(ficha_impexp)],
        FICHA_IMP: [CallbackQueryHandler()],
        FICHA_EXP: [CallbackQueryHandler()],
        FICHA_RESET:[],
    },
    fallbacks = [CallbackQueryHandler()],
    per_chat = True
    )

dispatcher.add_handler(sheet_handler)

"""-------------------------------------------------------------------------"""
# Esse handler trata da criação de fichas

sheet_create_handler = ConversationHandler(
    entry_points = [],
    states = {},
    fallbacks = [],
    per_chat = True
    )

dispatcher.add_handler(sheet_create_handler)

"""-------------------------------------------------------------------------"""# Esse handler trata da criação de fichas

sheet_edit_handler = ConversationHandler(
    entry_points = [],
    states = {},
    fallbacks = [],
    per_chat = True
    )

dispatcher.add_handler(sheet_edit_handler)

"""-------------------------------------------------------------------------"""

unknown_handler = RegexHandler(r'/.*', desconhecido)
dispatcher.add_handler(unknown_handler)

"""-------------------------------------------------------------------------"""
