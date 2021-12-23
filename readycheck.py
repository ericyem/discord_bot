
   
from discord.client import Client
from discord import Member, Embed
from stopwatch import Timer
import asyncio
class ReadyChecker:
    def __init__(self, author, game) -> None:
        self.author = author
        data = initReadyData()
        self.game = game
        self.reactEmojis = data["reactEmojis"]
        self.msg_id = data["messageId"]
        
    def createReadyMsg(self):
        self.embed = Embed()
        self.embed.add_field(name=(self.game + " check"), 
                        value = ("{name} has started a ready check for {game}".format(name=self.author, game=self.game)),
                        inline=False)
        self.embed.add_field(name = "Players Ready",
                        value = formatListString(self.reactEmojis['✅']),
                        inline=True)
        self.embed.add_field(name = "Players Coming Next Game",
                        value = formatListString(self.reactEmojis['🕐']),
                        inline=True) 
        self.embed.add_field(name = "Players Not Coming",
                        value = formatListString(self.reactEmojis['❌']),
                        inline=True)
        self.embed.add_field(name = "Total",
                        value = "Players coming: {yes} \n Players not coming: {no}".format(yes=len(self.reactEmojis['✅']),
                                                                                           no = len(self.reactEmojis['❌'])),
                        inline=False)
        return self.embed
    
    def add_data(self, emoji, player: Member):
        try:
            self.reactEmojis[emoji].append(player.display_name)
        except KeyError:
            print("error adding data")
            
    def remove_data(self, emoji, player: Member):
        try:
            self.reactEmojis[emoji].remove(player.display_name)
        except KeyError:
            print("error removing data")
    def updateEmbed(self):
        self.embed.set_field_at(index=1,name = "Players Ready",
                        value = formatListString(self.reactEmojis['✅']),
                        inline=True)
        self.embed.set_field_at(index=2,name = "Players Coming Next Game",
                        value = formatListString(self.reactEmojis['🕐']),
                        inline=True) 
        self.embed.set_field_at(index=3,name = "Players Not Coming",
                        value = formatListString(self.reactEmojis['❌']),
                        inline=True)
        return self.embed
    
    def get_msg_id(self):
        return self.msg_id
    
def initReadyData():
    return {"messageId" : None,
        "reactEmojis" : {
        '✅' : [],
        '🕐' : [],
        '❌' : []
            }
        }

def formatListString(list):
    if len(list) == 0:
        return None
    string_output = ""
    for i in range(len(list)):
        elem = "{num}. {elem}\n".format(num = i+1, elem = list[i])
        string_output += elem
    return string_output

async def ready_actions_add(readyChecker: ReadyChecker, botMessage):      
    for emoji in readyChecker.reactEmojis:
        await botMessage.add_reaction(emoji)
        
        
async def runReadyCheck(ctx, game, client):
    try:
        author = ctx.author.display_name
        gameStr = client.gameIds[game]
        client.readyData = ReadyChecker(author, gameStr)
    except asyncio.TimeoutError:    
        await ctx.send("```bruh you took too long to type something.```")
    except IndexError:
        await ctx.send("```that's not a tag...```")
    else:
        readyMessage = await ctx.send(embed=client.readyData.createReadyMsg())
        client.readyData.msg_id = readyMessage.id
        await ready_actions_add(client.readyData, readyMessage)
        timer = Timer(120)
        while True:
            await timer.run()
            if timer.seconds_remaining() == 0:
                await ctx.send("```The ready check for {game} has ended```".format(game=client.readyData.game))
                client.readyData = None
                break