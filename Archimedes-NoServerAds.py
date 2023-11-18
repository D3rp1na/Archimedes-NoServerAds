import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Dictionary to store muted users and their timers
muted_users = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if "https://discord.gg/" in message.content:
        # Check if the message contains a Discord invite link
        await mute_user(message.author)

    await bot.process_commands(message)

async def mute_user(user):
    # Mute the user for a specified duration (in seconds)
    mute_duration = 300  # 5 minutes, adjust as needed

    # Check if the user is already muted
    if user.id in muted_users:
        return

    # Mute the user
    await user.add_roles(discord.utils.get(user.guild.roles, name="Muted"))

    # Store the user and timer in the dictionary
    muted_users[user.id] = asyncio.get_event_loop().call_later(mute_duration, unmute_user, user)

async def unmute_user(user):
    # Unmute the user
    await user.remove_roles(discord.utils.get(user.guild.roles, name="Muted"))

    # Remove the user from the dictionary
    del muted_users[user.id]

# Command to manually unmute a user
@bot.command(name='unmute')
async def unmute(ctx, member: discord.Member):
    if member.id in muted_users:
        muted_users[member.id].cancel()  # Cancel the scheduled unmute
        await unmute_user(member)
        await ctx.send(f'{member.display_name} has been unmuted.')
    else:
      await ctx.send(f'{member.display_name} is not currently muted.')

bot.run("YOUR_BOT_TOKEN")

