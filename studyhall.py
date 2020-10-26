# -----------------------------------------------------
# The Imposter - An Among Us Discord bot
# Created by Patrick Brennan(AM2i9)
# https://github.com/AM2i9/the-imposter
#------------------------------------------------------
import discord
from discord.ext import commands

class StudyHall(commands.Cog):

    #So this is a special COG for Among Us ft.Niranth discord server, which has a channel named Study Hall.
    #The idea is that only one human person can be in the channel at a time, but we couldn't use the user limit on channels because alot
    # of the people who like to join and earrape people have admin. So, this bot kicks whoevers joining if there is already a person in the vc.
    def __init__(self,bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):

        #Fetches the voice channel
        sh_channel = discord.utils.get(member.guild.voice_channels, id=768639430013091860)

        #The bot keeps a count of real users IN MEMORY because im too lazy
        real_users = 0

        if member.voice is not None:
            if member.voice.channel == sh_channel:

                for user in sh_channel.members:

                    #Checks to make sure the user is not a bot. As many bots as you want can join
                    if not user.bot:
                        real_users = real_users + 1

                if real_users > 1:

                    #funny enough, I think i may have almost kicked some people from the server while testing this because i used .kick by accident
                    await member.edit(voice_channel=None)
