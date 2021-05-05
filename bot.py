import requests
from discord.ext import commands
import re
import pandas as pd
import os
from keep_alive1 import keep_alive

# 1) need to have bot token for it to communicate with discord
# 2) Bot needs to be registered on your server
#    Link is of the form:
#    https://discordapp.com/oauth2/authorize?client_id=<BOT_ID>&scope=bot&permissions=0

def read_token():
  return os.environ['token.txt']


token = read_token()

bot = commands.Bot(command_prefix="!")


def getCandleLightingTime(text):

    def convertSpaces(text):
        return re.sub(' ','%20',text)

    def approxMatch(text):
        matchDf = pd.read_csv('https://raw.githubusercontent.com/hebcal/dotcom/master/hebcal.com/dist/cities2.txt', '\t',
                          header=None)
        selection = matchDf[0][matchDf[0].str.contains(text, case=False)]
        subSelection = re.split('\|',selection.to_string())[0]
        return re.sub(r"\d", "", subSelection).strip()
    try:
      url = f"https://www.hebcal.com/shabbat?cfg=json&city={convertSpaces(approxMatch(text))}&M=on&a=on"
      res = requests.get(url).json()
      reply = f"**🕯Shabbos information for: __{res['location']['title']}__🕯**\n__Date:__ {res['items'][1]['date']}\n{res['items'][1]['title_orig']}\n{res['items'][1]['hebrew']}\n**{res['items'][0]['title']}**\n**{res['items'][2]['title']}**\n\nTimes from https://www.hebcal.com"
    except:
      reply= "Unable find times for that location.\n\nMake sure your location is in the right form.\ntype `!cities` for more information"
    return reply




@bot.command()
async def ShabbosTimes(ctx, area):
  await ctx.send(getCandleLightingTime(area))
   
@bot.command()
async def shabbostimes(ctx, area):
  await ctx.send(getCandleLightingTime(area))

@bot.command()
async def ShabbatTimes(ctx, area):
  await ctx.send(getCandleLightingTime(area))

@bot.command()
async def shabbattimes(ctx, area):
    await ctx.send(getCandleLightingTime(area))


@bot.command()
async def cities(ctx):
    await ctx.author.send("The list of available cities can be found here: https://github.com/hebcal/dotcom/blob/master/hebcal.com/dist/cities2.txt")

bot.run(token)

keep_alive()
bot.run(token)
