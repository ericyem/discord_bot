import discord
from discord.channel import TextChannel
from discord.client import Client
from discord.message import Message

def createRolesMessage():
    embed=discord.Embed(title="Welcome to Ogikubois", 
                            url="https://www.youtube.com/watch?v=sxT5bnowzcU", 
                            description="Get roles by reacting below.", 
                            color=0xFF5733)
    embed.add_field(name="Roles:", 
                        value="✅ IG Alerts Channel\n🏐 Volleyball Channel\n☘️ Genshin Artifact Check Channel" , 
                        inline=False)
    embed.set_image(url = "https://cdn.discordapp.com/attachments/906689619205177415/909413127861465118/rolesImage.jpg")
    return embed

async def initRoles(client: Client):
        # id of the roles channel
        channel = client.get_channel(910706290760773662)
        messages = channel.history().filter(lambda x: x.author == client.user)
        botMessages = await messages.flatten()
        if len(botMessages) == 0:
            await role_add(client, channel, client.data)
        else:
            client.rolesMsgId = botMessages[0].id
            await retainedRoles(client, botMessages[0])

async def retainedRoles(client: Client, message: Message):
        reactionList = message.reactions
        # id of guild
        guild = await client.fetch_guild(910045653760102431)
        for reaction in reactionList:
            async for user in reaction.users():
                if message.author != user:
                    role = discord.utils.get(guild.roles, 
                                    name=client.rolesIds[reaction.emoji])
                    await user.add_roles(role)
                    
async def role_add(client: Client, channel: TextChannel, data: dict):      
        botMessage = await channel.send(embed=createRolesMessage())
        for emoji in client.rolesIds:
            await botMessage.add_reaction(emoji)
            data['roles']['messageId'] = botMessage.id
            client.rolesMsgId = botMessage.id

async def assign_role(client, payload):
    if payload.message_id != client.rolesMsgId:
                return
    guild = client.get_guild(payload.guild_id)
    try:
        role = discord.utils.get(guild.roles, 
                                name=client.rolesIds[payload.emoji.name])
                
        await payload.member.add_roles(role)
    except KeyError:
        print("Please react with correct emoji")

async def remove_role(client, payload):
        if payload.message_id != client.rolesMsgId:
            return
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = discord.utils.get(guild.roles, 
                                name=client.rolesIds[payload.emoji.name])
        await member.remove_roles(role)