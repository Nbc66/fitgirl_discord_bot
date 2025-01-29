import FitgirlAPI
import discord
from dotenv import load_dotenv
import os
import FitgirlAPI
import html


load_dotenv()

intents = discord.Intents.all()

fitgirl = FitgirlAPI.FitGirl()

bot = discord.Bot(intents=intents)

test_guild_id = [1224478474303963246]

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    print("we are inside theese servers")
    for guild in bot.guilds:
        print(guild.id)

# Error handler for slash commands
@bot.event
async def on_application_command_error(ctx, error):
    # Catch the error and prevent it from unregistering commands
    print(f"Error occurred in command {ctx.command}: {error}")

    if isinstance(error, discord.errors.HTTPException):
        await ctx.respond("An error occurred with Discord API.")
    elif isinstance(error, ZeroDivisionError):
        await ctx.respond("There was an issue with the command. Please try again later.")
    else:
        # Catching any other unexpected errors
        await ctx.respond(f"An unexpected error occurred: {error}")

@bot.command(description="Get the latest Post from the fitgirl Website",guild_ids=test_guild_id)
async def latest(ctx: discord.Interaction):

    latest_posts = fitgirl.new_posts()

    formated_posts = []

    embed = discord.Embed(
        title = "Latest Releases",
        color = discord.Colour.from_rgb(0, 0, 0)
    )


    for posts in latest_posts["results"]:
        fixed_title = html.unescape(f"{posts['title']}")
        embed.add_field(name=f"",value=f"[{fixed_title}]({posts['url']})",inline=False)


    await ctx.respond(f"latest post:",embed=embed)

@bot.command(description="Search for a game", guild_ids=test_guild_id)
async def search(ctx: discord.Interaction, querry: discord.Option(str)): # type: ignore
    embed:discord.Embed = discord.Embed(
        title="Search Result",
        color=discord.Colour.from_rgb(0,0,0)
    )
    
    querry_result = fitgirl.search(querry)

    if querry_result["status"] == "Error":
        return await ctx.respond("No results found")
    
    for result in querry_result["results"]:
        fixed_title = html.unescape(f"{result['title']}")
        embed.add_field(name="",value=f"[{fixed_title}]({result['url']})", inline=False)

    await ctx.respond(embed=embed)

@bot.command(description="Get all the download links for a specific Game", guild_ids=test_guild_id)
async def download(ctx: discord.Interaction, querry: discord.Option(str)): # type: ignore
    
    querry_result = fitgirl.download(querry)

    if querry_result["status"] == "Error":
        return await ctx.respond("No results found")
    
    embed:discord.Embed = discord.Embed(
        title=f"Download \"{html.unescape(querry_result['game'])}\"",
        description="Download links:",
        color=discord.Colour.from_rgb(0,0,0)
    )
    
    for result in querry_result["results"]:
        fixed_title = html.unescape(f"{result['title']}")
        embed.add_field(name="",value=f"[{fixed_title}]({result['url']})", inline=False)

    await ctx.respond(embed=embed)
    

if __name__ == "__main__":
    bot.run(os.getenv("BOT_TOKEN"))