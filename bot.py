# -----------------------------------------------------
# The Imposter - An Among Us Discord bot
# Created by Patrick Brennan(AM2i9)
# https://github.com/AM2i9/the-imposter
#------------------------------------------------------
# So this is a discord bot I created for one of my
# friends discord servers, named Among Us ft. Niranth,
# mostly because they would not shut up when we were
# playing Among Us. And I may have added a few little
# things to it here and there, just to have a little
# more fun.
#------------------------------------------------------
import discord
from discord.ext import commands
from games import Games
from studyhall import StudyHall
from music import Music
import json

bot = commands.Bot(command_prefix='i!')

bot.add_cog(Games(bot))
bot.add_cog(StudyHall(bot))
bot.add_cog(Music(bot))
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as {}'.format(bot.user))

@bot.command(pass_context=True)
async def help(ctx):

    # So the basic discord help command is absolute GARBAGE, so here we are
    # making a rich embed so that it looks nicer

    embed = discord.Embed(type="rich")
    embed.title = "Among Us"
    embed.colour = discord.Color(0x9e0500)
    embed.description = "Hello there! I am the impost- a fellow crewmate. I am a bot to help you manage your games, making it easier for people to join and play."
    embed.add_field(name="How to start game",value="Start a game by typing the following command:\n\n    i!start <Game Server> <Game Code>\n\nThe game server can be one of the following:\nNA - North America\nEU - Europe\nA - Asia\n\n The game code must be a six letter code given to you by the game.")
    embed.add_field(name="Game controls",value="The game controls are in the form of reactions, as such:\n\n🔇 Mute and Unmute the voice channel\n🎙️ This button allows you to mute everyone in the channel when you mute yourself in discord\n❌ End the game")
    embed.add_field(name="Transfering Host",value="In the event the host needs to leave, they can transfer the host controls to another user in the voice channel by typing the command:\n\ni!transfer <user>\n\nOtherwise, the game will end when the host leaves the channel.",inline=False)
    await ctx.message.channel.send(embed=embed)


@bot.event
async def on_message(message):

    #Ok, so these are some random shit things that people have asked me to do

    #catJAM gif
    if message.content.upper() == "CATJAM":
        await message.channel.send("https://cdn.discordapp.com/attachments/665640365528842241/741114065987960863/3x.gif")
        await message.delete()

    # Julia
    if message.content == "cool":
      await message.channel.send("<@{}> is the coolest".format(message.author.id))

    await bot.process_commands(message)

with open('key.json') as keyfile:

    #Opens a keyfile, which is a json file with a structure looking a bit like this:
    #{
    #  "key":"<YOUR DISCORD BOT TOKEN HERE>"
    #}

    key = json.load(keyfile)["key"]

bot.run(key)
