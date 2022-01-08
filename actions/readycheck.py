from discord.client import Client
from discord import Member, Embed
from .timer import Timer
import asyncio


class ReadyChecker:
    def __init__(self, author, game) -> None:
        self.author = author
        data = initReadyData()
        self.game = game
        self.reactEmojis = data["reactEmojis"]
        self.msg_id = data["messageId"]

    def createReadyMsg(self):
        self.output = ["```prolog\n{name} has started a ready check for: {game} | additional notes: ".format(name=self.author.capitalize(), game=self.game.capitalize())]
        self.output.append("players ready: {}".format(formatListString(self.reactEmojis["✅"])))
        self.output.append("players coming next game: {}".format(formatListString(self.reactEmojis["🕐"])))
        self.output.append("players not coming: {}".format(formatListString(self.reactEmojis["❌"])))
        self.output.append("total number of players ready: {yes} \ntotal number of players not coming: {no}```".format(
                yes=len(self.reactEmojis["✅"]), no=len(self.reactEmojis["❌"])
            ))
        
        return "\n".join(self.output)

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

    def updateMessage(self):
        self.output[1] = "players ready: " + formatListString(self.reactEmojis["✅"])
        self.output[2] = "players coming next game: " + formatListString(self.reactEmojis["🕐"])
        self.output[3] = "players not coming: " + formatListString(self.reactEmojis["❌"])
        return "\n".join(self.output)

    def get_msg_id(self):
        return self.msg_id

def initReadyData():
    return {"messageId": None, "reactEmojis": {"✅": [], "🕐": [], "❌": []}}


def formatListString(list):
    if len(list) == 0:
        return ""
    string_output = ""
    for i in range(len(list)):
        if i == (len(list) - 1):  
            elem = "{num}. {elem}".format(num=i + 1, elem=list[i].capitalize())
        else:
            elem = "{num}. {elem}\n".format(num=i + 1, elem=list[i].capitalize())
        string_output += elem
    return string_output


async def ready_actions_add(readyChecker: ReadyChecker, botMessage):
    for emoji in readyChecker.reactEmojis:
        await botMessage.add_reaction(emoji)


async def runReadyCheck(ctx, author, client):
    try:
        botMessage = await ctx.channel.send("```I am ready. Tag a game and optionally write a note. For example: @Valorant quick we are starting in 2 minutes.```")
        message = await client.wait_for('message', check=lambda m: m.author == author, timeout=60)
        await botMessage.delete()
        gameStr = client.gameIds[message.content]
        await ctx.send(message.content)
        client.readyData = ReadyChecker(author.display_name, gameStr)
        client.readyData.reactEmojis['✅'].append(author.display_name)
    except asyncio.TimeoutError:
        await ctx.send("```bruh you took too long to type something.```")
    except IndexError:
        await ctx.send("```that's not a tag...```")
    else:
        readyMessage = await ctx.send(client.readyData.createReadyMsg())
        client.readyData.msg_id = readyMessage.id
        await ready_actions_add(client.readyData, readyMessage)
        timer = Timer(120)
        while True:
            await timer.run()
            if timer.seconds_remaining() == 0:
                await ctx.send(
                    "```prolog\nThe ready check for {game} has ended```".format(
                        game=client.readyData.game
                    )
                )
                client.readyData = None
                break
