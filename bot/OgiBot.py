import discord, discord.ext, discord.utils
from discord.ext import commands
from data.database import data
from actions.casesinfo import CovidCases
from actions.roles import initRoles, assign_role, remove_role
from actions.readycheck import initReadyData, runReadyCheck
import random
class Ogikubot(commands.Bot):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        self.rolesMsgId = data['roles']['messageId']
        self.rolesIds = data['roles']['roleEmojis']
        self.gameIds = data['gameIds']
        self.readyData = None
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

    def add_commands(self):
        @self.command(pass_context = True)
        async def hello(ctx):
            await ctx.send("```Hello {}```".format(ctx.message.author))

        @self.command(pass_context = True)
        async def bad(ctx):
            await ctx.send("```No you```")

        @self.command(pass_context = True)
        async def gay(ctx):
            await ctx.send("```{} is gay```".format(ctx.message.author))

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
        
