# -----------------------------------------------------
# The Imposter - An Among Us Discord bot
# Created by Patrick Brennan(AM2i9)
# https://github.com/AM2i9/the-imposter
#------------------------------------------------------
import discord
from discord.ext import commands

class Music(commands.Cog):

    #Alrght, this Cog is a bit experimental. Evan challenged me to make a bot that would play an attached mp3 filename,and here it is.
    #This is the buggiest thing that ever existed. If you can fix it up so that it don't break when people do bad things with
    #the command, please do

    def __init__(self,bot):
        self.client = bot
        self.VoiceClient = None

    @commands.command(pass_context=True)
    async def play(self,ctx):

        message = ctx.message
        vc = message.author.voice.channel

        if vc is not None:
            attachments = message.attachments

            #gets the first attachment on the message with the command
            att = attachments[0]

            #If the voicelcient is existent, i needed to get stop it first to get it to transition from song to song fluidly
            if self.VoiceClient:
                self.VoiceClient.stop()
            else:
                #Connects to vc
                self.VoiceClient = await vc.connect()

            #checks if its an mp3. currently, it only plays mp3
            if '.mp3' in att.filename:

                #saves the mp3 as a file, in the same directory this is being run in
                #gonna want a .gitignore
                await att.save('np.mp3',seek_begin=True)

                #display message
                await message.channel.send("Now playing {}".format(att.filename))

                #plays song
                #ya gonna need FFmpeg
                self.VoiceClient.play(discord.FFmpegPCMAudio('np.mp3'))
        else:
            await message.channel.send("You are not in a voice channel.")

    @commands.command(pass_context=True)
    async def leave(self,ctx):

        # Makes the bot leave the voice channel
        message = ctx.message
        vc = message.author.voice.channel

        if vc is None:

            await ctx.message.channel.send("You are not in a voice channel.")
        else:
            #Makes the client stop playing first before disconnecting, because, once again, this is super buggy
            if self.VoiceClient.is_playing():
                self.VoiceClient.stop()
            await self.VoiceClient.disconnect()
