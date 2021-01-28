import telebot
import datetime
import Operations as op
from Alumno import Alumno

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)
print("""
                    ___                         ___                         ___           ___     
     _____         /\  \                       /\__\                       /\  \         /\  \    
    /::\  \       /::\  \         ___         /:/ _/_                     /::\  \       /::\  \   
   /:/\:\  \     /:/\:\  \       /\__\       /:/ /\__\                   /:/\:\  \     /:/\:\__\  
  /:/ /::\__\   /:/  \:\  \     /:/  /      /:/ /:/  /    ___     ___   /:/  \:\  \   /:/ /:/  /  
 /:/_/:/\:|__| /:/__/ \:\__\   /:/__/      /:/_/:/  /    /\  \   /\__\ /:/__/ \:\__\ /:/_/:/__/___
 \:\/:/ /:/  / \:\  \ /:/  /  /::\  \      \:\/:/  /     \:\  \ /:/  / \:\  \ /:/  / \:\/:::::/  /
  \::/_/:/  /   \:\  /:/  /  /:/\:\  \      \::/__/       \:\  /:/  /   \:\  /:/  /   \::/~~/~~~~ 
   \:\/:/  /     \:\/:/  /   \/__\:\  \      \:\  \        \:\/:/  /     \:\/:/  /     \:\~~\     
    \::/  /       \::/  /         \:\__\      \:\__\        \::/  /       \::/  /       \:\__\    
     \/__/         \/__/           \/__/       \/__/         \/__/         \/__/         \/__/    
""")

# MENSAJE BIENVEIDA
@bot.message_handler(commands=['start'])
def send_bienvenida(message):
    with open('bienvenida.txt','r', encoding="UTF-8") as f:
        msg_bienvenida = f.read()
    bot.reply_to(message,msg_bienvenida)

# Handle all other messages with content_type 'text'
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    text = op.strip_accents(message.text)
    if op.validar_mensaje(text):
        bot.send_message(message.chat.id, "Debes seguir esta estructura:\n\nNombres ApellidoMaterno ApellidoPaterno Materia",parse_mode="MARKDOWN")
        with open('Images/giphy.gif', 'rb') as gif:
            bot.send_sticker(message.chat.id, gif)
    else:
        # La materia son las ultimas dos palabras
        materia = ' '.join(text.split(' ')[-2:])
        archivo = op.regresa_archivo(materia)
        if archivo == None:
            bot.send_message(message.chat.id, f"La materia: ___{materia}___ no existe, prueba cambiando el numero a romano o viceversa",parse_mode="MARKDOWN")
            with open('Images/fallout.webp', 'rb') as gif:
                bot.send_sticker(message.chat.id, gif)
        else:
            nombre = text.split(' ')[:-2]
            alumno = op.bitacora_alumno(archivo, nombre)
            if alumno == None:
                bot.send_message(message.chat.id, f"El nombre: ___{' '.join(nombre)}___ no esta en mi base de datos",parse_mode="MARKDOWN")
                with open('Images/mario.webp', 'rb') as gif:
                    bot.send_sticker(message.chat.id, gif)
            else:
                try:
                    bot.send_message(message.chat.id, f"```{alumno.get_table()}```",parse_mode="MARKDOWN")
                except telebot.apihelper.ApiTelegramException as ex:
                    if ex.error_code == 400:
                        with open('temp.html', 'w', encoding="UTF-8") as f:
                            f.write(f"{alumno.nombre}\n\n{alumno.get_html()}")
                        with open('temp.html', 'rb') as f:
                            bot.send_document(message.chat.id, f)
                bot.send_message(message.chat.id, f"___{alumno.nombre} - {materia.upper()}___ [👨🏼‍🎓]\n\nTienes {alumno.promedio} [📝]\n\nDado tu puntaje eres el numero {alumno.ranking} [🌟]",parse_mode="MARKDOWN")
                with open('log.txt', 'a', encoding="UTF-8") as f:
                    f.write(f"{message.from_user.username} | {alumno.nombre} | {materia} | {datetime.datetime.now()}\n")
bot.polling()
