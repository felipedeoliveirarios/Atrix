from main import updater
updater.start_polling()
comm = ''
while comm != 'quit':
    comm = input('Atrix >> ')
updater.stop()
quit()
