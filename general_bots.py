from helpers import DiscordUserHelper, DiscordMessageHelper
import asyncio
import discord
import time
import os

time_limit = 1 # minutes
question_active = False
users_set = set() # active users answering the active question
client = discord.Client()

@client.event 
async def on_ready():
    print("Bot ready...")

@client.event 
async def on_message(msg):
    global question_active, time_limit, users_set

    if client.user == msg.author:
        return
    
    channel = msg.channel
    msg_content = msg.content

    if msg_content.startswith('$create problem'):
        if question_active:
            await channel.send("Ya hay un problema actualmente corriendo!")
            return

        question_active = True
        await channel.send("Obteniendo problema...")
        # fetch the problem from an API...

        await asyncio.sleep(60 * time_limit)

        # question finished
        question_active = False
        description = """
        El tiempo ha finalizado; la pregunta fue cerrada

        Las respuestas de todos los miembros se publicarán en #📋-qc-respuestas, esten atentos
        """

        await DiscordMessageHelper.send_message_embed(channel, "Tiempo finalizado", description)

    elif msg_content.startswith('$start time') and question_active:
        discord_user = DiscordUserHelper(msg.author.id, msg.author.display_name, msg.author.discriminator, time.time())
    
        if discord_user.username_complete in users_set:
            await channel.send(f"{msg.author}, tu tiempo esta corriendo actualmente para esta pregunta, no puedes iniciarla de nuevo!")
            return

        users_set.add(discord_user.username_complete)
        await channel.send(f'Tiempo iniciado para {msg.author}')

    elif msg_content.startswith('$solution') and question_active:
        # extra validation: is there a .py file attached or any image attached? is so the continue, otherwise dont execute
        discord_user = DiscordUserHelper(msg.author.id, msg.author.display_name, msg.author.discriminator, time.time())
        try:
            discord_user.solution_path = msg.attachments[0].url
        except IndexError:
            channel.send(f"{msg.author}, ninguna imagen fue encontrada en tu mensaje")
            return
        else:
            msg_error = ''
            if not discord_user.username_complete in users_set:
                msg_error = f"{msg.author}, no iniciaste el tiempo, por ende, no podemos procesar tu submisión"
            
            elif discord_user.is_time_question_expired():
                msg_error = f"{msg.author}, tu tiempo expiró, por ende no podemos procesar tu submisión"
            
            if msg_error:
                await channel.send(msg_error)
                return
        
            # process all the logic of the code submitted...
            discord_user.validate_solution()

            await channel.send("Validando script...")
            users_set.remove(discord_user.username_complete)

def execute_bot():
    client.run(os.getenv('BOT_TOKEN'))