import requests
from discord.ext import commands

def read_token():
    with open('token.txt', 'r') as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

bot = commands.Bot(command_prefix="!")

def getCandleLightingTime(city, ashkenaz=True):
  try:
    if (ashkenaz==True):
        url = f"https://www.hebcal.com/shabbat?cfg=json&city={city}&M=on&a=on"
        res = requests.get(url).json()
        reply = f"**🕯Shabbos information for: __{res['location']['title']}__🕯**\n__Date:__ {res['items'][0]['date']}\n{res['items'][2]['hebrew']} {res['items'][2]['title']}\n**{res['items'][1]['title']}**\n**{res['items'][3]['title']}**\n\nTimes from https://www.hebcal.com"
    else:
        url = f"https://www.hebcal.com/shabbat?cfg=json&city={city}&M=on&a=off"
        res = requests.get(url).json()
        reply = f"**🕯Shabbat information for: __{res['location']['title']}__🕯**\n__Date:__ {res['items'][0]['date']}\n{res['items'][2]['hebrew']} {res['items'][2]['title']}\n**{res['items'][1]['title']}**\n**{res['items'][3]['title']}**\n\nTimes from https://www.hebcal.com"
    return reply

  except:
    reply="Unable find times for that location.\n\nMake sure your location is in the right form.\ntype `!cities` for more information"
    
    return reply

@bot.command()
async def ShabbosTimes(ctx, area):
    await ctx.send(getCandleLightingTime(area))

@bot.command()
async def shabbostimes(ctx, area):
    await ctx.send(getCandleLightingTime(area))

@bot.command()
async def ShabbatTimes(ctx, area):
    await ctx.send(getCandleLightingTime(area,False))

@bot.command()
async def shabbattimes(ctx, area):
    await ctx.send(getCandleLightingTime(area,False))

@bot.command()
async def cities(ctx):
    await ctx.author.send("The list of available cities can be found here: https://github.com/hebcal/dotcom/blob/master/hebcal.com/dist/cities2.txt")
    
bot.run(token)
