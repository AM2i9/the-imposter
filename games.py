# -----------------------------------------------------
# The Imposter - An Among Us Discord bot
# Created by Patrick Brennan(AM2i9)
# https://github.com/AM2i9/the-imposter
#------------------------------------------------------
import discord
import asyncio
from discord.ext import commands

class Game:

    # The structure of a game, which is stored in memory. All games are stored in memory becaues I'm too lazy to setup an sqlite database
    def __init__(self, message, channel, host):
        self.message = message
        self.channel = channel
        self.host = host
        self.self_mute_toggle = False


class Games(commands.Cog):

    # The Cog which contains all of the commands for creating and managing games

    def __init__(self, bot):
        self.client = bot
        self.games = [] # The frickin list where all of the games are stored

    @commands.command(pass_context=True)
    async def start(self, ctx, game_server="",game_code=""):

        # Command to start a game.
        # i!start <GAME_SERVER> <GAME_CODE>

        author = ctx.message.author

        #Check to see if user is in voice channel
        try:
            channel = author.voice.channel
        except:
            await ctx.message.channel.send("You are not in a voice channel!")
            return

        #Checking to see if user has entered a game server and code
        if game_server == "":
            await ctx.message.channel.send("Please supply a game server!")
            return
        else:
            if game_code == "":
                await ctx.message.channel.send("Please supply a game code!")
                return
            else:

                #Checks to see if server and code are valid
                servers = ["NA", "EU", "A"]
                servers_display = {"NA" : "North America", "EU" : "Europe", "A" : "Asia"}

                #Game servers must be equal to one of the servers in the list [servers]
                if game_server.upper() not in servers:
                    await ctx.message.channel.send("Please supply a valid gamer server. Valid servers are:\nNA - North America\nEU - Europe\nA - Asia")
                    return

                #The game code just has to be 6 digits. Not being too picky here
                if len(game_code) != 6:
                    await ctx.message.channel.send("Please supply a valid game code. A valid game code must be 6 digits.")
                    return

                #Checks if someone is already using the current vc for a game
                for game in self.games:
                    if game.channel == channel:
                        await ctx.message.channel.send("There is already a game running in {}! Join another VC, or end the game.".format(channel))
                        return

                #Creates a discord channel invite, so people can just click 'join'
                invite = await channel.create_invite()

                #The games embed, the result of the start command
                embed = discord.Embed(type="rich")
                embed.title = "Among Us"
                embed.colour = discord.Color(0x9e0500)
                embed.description = "Hosted by: {}".format(author)
                embed.add_field(name="🎮Game Code:",value = game_code.upper(),inline=False)
                embed.add_field(name="🌎Server:",value = "{0} - {1}".format(game_server.upper(),servers_display[game_server.upper()]),inline=False)
                embed.add_field(name="🔊Channel:",value = channel,inline=False)
                embed.add_field(name="Click to Join:", value = invite)

                await ctx.message.channel.send(embed=embed)
                await ctx.message.channel.send(invite)


                # GAME CONTROLS
                mute_embed = discord.Embed(type="rich")
                mute_embed.title = "Game Controls"
                mute_embed.description = "Only the Host of the game can use these"
                mute_embed.add_field(name="Reactions",value= "🔇 Mute and Unmute the voice channel\n🎙️Toggle to mute everyone when you self-mute\n❌ End the game",inline=True)
                mute_embed.colour = discord.Color(0x9e0500)

                mute_message = await ctx.message.channel.send(embed=mute_embed)
                await mute_message.add_reaction("🔇")
                await mute_message.add_reaction("🎙️")
                await mute_message.add_reaction("❌")

                #Stores the game in memory
                self.games.append(Game(mute_message, channel, author))

    @commands.command(pass_context=True)
    async def transfer(self,ctx,user):

        # Command to transfer hostage of the game from the host to another user in case the host has to leave

        if "<@" in user:
            user = self.client.get_user(int(user[3:len(user)-1]))

            #checks to see if user is sending host to themselves
            if user == ctx.message.author:
                await ctx.message.channel.send("You can't transfer host to yourself, you are already hosting a game.")
            for game in self.games:

                #checks if user is sending host to a player who is already hosting another game
                if game.host == user:
                    await ctx.message.channel.send("This user is already hosting a game. They cannot host two at once.")
                    return

            # Transfers host privledges
            for game in self.games:
                if game.host == ctx.message.author:
                    game.host = user
                    await ctx.message.channel.send("Host privledges have been transfered to {}".format(user))
                    return
        else:
            await ctx.message.channel.send("Please tag someone to transfer host to.")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        # Buttons being clicked under game controls
        if user != self.client.user:

            for game in self.games:

                if reaction.message.id == game.message.id:
                    if user == game.host:

                        if reaction.emoji == "🔇":

                            #Togglemute button
                            for user in game.channel.members:

                                await user.edit(mute=True)

                        if reaction.emoji == "❌":

                            #End game button
                            self.games.remove(game)
                            await reaction.message.channel.send("{} has ended their game.".format(user))

                        if reaction.emoji == "🎙️":

                            #togglemute on selfmute Button
                            game.self_mute_toggle = True


    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):

        #The same as the previous event, but to turn things off
        if user != self.client.user:

            for game in self.games:

                if reaction.message.id == game.message.id:
                    if user == game.host:

                        #togglemute button
                        if reaction.emoji == "🔇":
                            for user in game.channel.members:

                                await user.edit(mute=False)

                        #togglemute on selfmute button
                        if reaction.emoji == "🎙️":

                                game.self_mute_toggle = False

    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):

        # Executes whenever someone does SOMTHING in a voice Channel
        # be careful what you add, because it WILL start to loop if your not careful

        #When a user leaves a voice channel, it will end their game if they have one after 10 seconds
        if member.voice == None:
            for game in self.games:
                if game.host == member:
                    await asyncio.sleep(10)
                    if member.voice == None:
                        self.games.remove(game)
                        await game.message.channel.send("{} has ended their game because they left the vc for more than 10 seconds.".format(member))

        #togglemute on selfmute
        #Checks if the update event was someone muting, then checks if they are in a game
        #if they are, it toggles mute on the channel
        if member.voice and before.mute == after.mute:

            if member.voice.self_mute:
                for game in self.games:
                    if game.host == member and game.self_mute_toggle:
                            for user in game.channel.members:

                                    await user.edit(mute=True)
            else:
                for game in self.games:
                    if game.host == member and game.self_mute_toggle:
                        for user in game.channel.members:

                                await user.edit(mute=False)
