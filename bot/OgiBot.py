import discord, discord.ext, discord.utils, random
from discord.ext import commands
from data.database import data
from actions.casesinfo import CovidCases
from actions.roles import initRoles, assign_role, remove_role
from actions.readycheck import initReadyData, runReadyCheck
import datetime as dt
class Ogikubot(commands.Bot):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        self.rolesMsgId = data['roles']['messageId']
        self.rolesIds = data['roles']['roleEmojis']
        self.gameIds = data['gameIds']
        self.readyData = None
        self.cachedDeletedMessage = None
        self.add_commands()
        
    async def on_ready(self):
        print("We have logged in as {0.user}".format(self))
        # id of the roles channel
        await initRoles(self)
            
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.user.id:
            if payload.channel_id == 910706290760773662:
                await assign_role(self, payload)
            
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        if user.id == self.user.id:
            return
        if reaction.message.id == self.readyData.get_msg_id():
            self.readyData.add_data(reaction.emoji, user)
            newEmbed = self.readyData.updateEmbed()
            await reaction.message.edit(embed=newEmbed)
            
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.Member):
        if user.id == self.user.id:
            return
        if reaction.message.id == self.readyData.get_msg_id():
            self.readyData.remove_data(reaction.emoji, user)
            newEmbed = self.readyData.updateEmbed()
            await reaction.message.edit(embed=newEmbed)
    
        
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id != self.user.id:
            if payload.channel_id == 910706290760773662:
                await remove_role(self, payload)

    async def on_raw_message_delete(self, payload):
        self.cachedDeletedMessage = payload.cached_message

    def add_commands(self):
        @self.command(pass_context = True)
        async def hello(ctx):
            await ctx.send("```Hello {}```".format(ctx.message.author))

        @self.command(pass_context=True)
        async def covid(ctx):
            botMessage = await ctx.send("Gathering results...")
            covidObj = CovidCases()
            result = covidObj.run()
            await botMessage.edit(content=("```" + result[0] +"\n" + result[1] + "\n" + result[2] + "```"))  

        @self.command(pass_context = True, help='Type $ready, then enter @<game> with an optional note')
        async def ready(ctx, game):
            self.readyData = initReadyData()
            await ctx.message.delete()
            await ctx.send(game)
            await runReadyCheck(ctx, game, self)
            
        @self.command(pass_context = True)
        async def roll(ctx):
            rngRoll = random.randrange(0,101)
            author = ctx.message.author.name
            await ctx.send("{name} rolled: {value}".format(name= author, value=rngRoll))
        
        @self.command(pass_context = True)
        async def coin(ctx):
            author = ctx.message.author.name
            rngCoin = random.randrange(0,2)
            res = "Heads" if rngCoin else "Tails"
            await ctx.send("{name} flipped a: {result}".format(name=author, result=res))
        
        @self.command(pass_context = True)
        async def summons(ctx, primos, intertwined):
            totalPrimos = int(primos) + int(intertwined)*160
            totalSummons = float(primos/160) + float(intertwined)
            await ctx.send("Total Primos: " + str(totalPrimos) + "\nTotal Summons: " + str(totalSummons)) 
            
        @self.command(pass_context = True)
        async def dmspam(ctx, user: discord.Member=None):
            authorName = ctx.author.name
            botMessage = await ctx.send("Currently spamming them in their DMs.")
            try:
                await user.send(authorName + " is spamming you")
                for i in range(1,6):
                    await user.send("spam")
                    await botMessage.edit("Currently spamming them in their DMs (" + str(i) + "/5)")  
            except:
                await ctx.send("Incorrect Syntax:\nUsage: `!dmspam [@user]`")
            await botMessage.edit("Finished spamming them.")
        
        @self.command(pass_context=True)
        async def snipe(ctx):
            if self.cachedDeletedMessage == None:
                await ctx.send("Nothing to snipe") 
            else:
                await ctx.send(self.cachedDeletedMessage.author.name + " sent: " + self.cachedDeletedMessage.content)
                await ctx.send(self.cachedDeletedMessage.attachments[0].url)
        @self.command(pass_context = True)
        async def talk(ctx, key, *, extra):
            await ctx.message.delete()
            if str(key) == "123":
                await ctx.send(str(extra))
            else:
                await ctx.send("Hey ya fkin gronk, don't even try again ya dog.")
        @self.command(pass_context = True)   
        async def pp(ctx):
            ppSize = random.randrange(0,16) * "="
            authorName = ctx.author.name
            await ctx.send("{}".format(authorName) + " pp: 8" + ppSize + "D")