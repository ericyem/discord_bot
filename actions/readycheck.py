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
        self.output = ["{name} has started a ready check for: {game} | additional notes: ".format(name=self.author, game=self.game)]
        self.output.append("Players ready: " + formatListString(self.reactEmojis["✅"]))
        self.output.append("Players ready: " + formatListString(self.reactEmojis["🕐"]))
        self.output.append("Players ready: " + formatListString(self.reactEmojis["❌"]))
        self.output.append("Players coming: {yes} \n Players not coming: {no}".format(
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
        self.output[1] = "Players ready: " + formatListString(self.reactEmojis["✅"])
        self.output[2] = "Players ready: " + formatListString(self.reactEmojis["🕐"])
        self.output[3] = "Players ready: " + formatListString(self.reactEmojis["❌"])
        return "\n".join(self.output)

    def get_msg_id(self):
        return self.msg_id

def initReadyData():
    return {"messageId": None, "reactEmojis": {"✅": [], "🕐": [], "❌": []}}


def formatListString(list):
    if len(list) == 0:
        return None
    string_output = ""
    for i in range(len(list)):
        elem = "{num}. {elem}\n".format(num=i + 1, elem=list[i])
        string_output += elem
    return string_output


async def ready_actions_add(readyChecker: ReadyChecker, botMessage):
    for emoji in readyChecker.reactEmojis:
        await botMessage.add_reaction(emoji)


async def runReadyCheck(ctx, author, client):
    try:
        botMessage = await ctx.channel.send("```I am ready. Tag a game and optionally write a note. For example: @Valorant quick we are starting in 2 minutes.```")
        message = await client.wait_for('message', check=lambda m: m.author == author, timeout=60)
        await ctx.send(message)
        await botMessage.delete()
        gameStr = client.gameIds[message]
        await ctx.send(gameStr)
        client.readyData = ReadyChecker(author.display_name, gameStr)
    except asyncio.TimeoutError:
        await ctx.send("```bruh you took too long to type something.```")
    except IndexError:
        await ctx.send("```that's not a tag...```")
    except:
        await ctx.send("Didn't work")
    else:
        readyMessage = await ctx.send(client.readyData.createReadyMsg())
        client.readyData.msg_id = readyMessage.id
        await ready_actions_add(client.readyData, readyMessage)
        timer = Timer(120)
        while True:
            await timer.run()
            if timer.seconds_remaining() == 0:
                await ctx.send(
                    "```The ready check for {game} has ended```".format(
                        game=client.readyData.game
                    )
                )
                client.readyData = None
                break
