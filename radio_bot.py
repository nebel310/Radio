import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.remove_command('help')

radio_stations = {
    'CapitalFM': 'https://icecast-vgtrk.cdnvideo.ru/capitalfmmp3',
    'ЮморFM' : 'https://ic5.101.ru:8000/v5_1',
}


@bot.event
async def on_ready():
    await update_status()

@bot.event
async def on_member_update(before, after):
    if before.id == bot.user.id and before.status != after.status:
        await update_status()

async def update_status():
    member = discord.utils.get(bot.get_all_members(), id=bot.user.id)
    if member.status == discord.Status.online:
        await bot.change_presence(activity=discord.Game(name="Играет в вашей мамке"))
    else:
        await bot.change_presence(activity=discord.Game(name="Разраб даун, забыл включить"))


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Список команд", description="Вот список доступных команд:", color=0x00ff00)
    
    # Add fields for each command
    embed.add_field(name="!play название станции", value="Воспроизводит радиостанцию по названию или ссылке.", inline=False)
    embed.add_field(name="!stop", value="Останавливает воспроизведение радиостанции и кикает бота. **Важно:** если соберешься менять станцию, то сначало впиши эту команду.", inline=False)
    embed.add_field(name='!list', value="Выдает список радиостанций, которые можно включить по названию. Радистанции, не входящие в этот список придется включать по ссылке. **Важно:** название нужно вписывать символ в символ.")
    
    await ctx.send(embed=embed)


@bot.command()
async def list(ctx):
    embed = discord.Embed(title="Список радиостанций", description="Вот список радиостанций, которые можно включить по названию", color=0x00ff00)
    
    # Add fields for each command
    radio_list = "\n".join([f"- {station}" for station in radio_stations.keys()])
    embed.add_field(name="Список радиостанций", value=radio_list, inline=False)
    embed.add_field(name="", value="Хотите видеть здесь вашу радиостанцию - пишите @vlados7529")
    embed.add_field(name="", value="**UPD:** *Какие-то станции работают хорошо, а какие-то плохо.*")
    embed.add_field(name="", value="*Если радиостанция лагает, то интернет ваш говно, а не бот*")
    
    await ctx.send(embed=embed)


@bot.command()
async def play(ctx, station_name):
    host = discord.utils.get(ctx.guild.members, id=714776610343092245)
    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.send("Вы не находитесь в голосовом канале.")
        return
    else:
        voice_client = await voice_channel.connect()

    if station_name not in radio_stations:
        await ctx.send("Такой радиостанции нет в списке.")
        await ctx.send("Проверяю на наличие ссылки...")
        
        if station_name.find("http") != -1:
            source = await discord.FFmpegOpusAudio.from_probe(station_name)
            voice_client.play(source)
            await ctx.send(f"Если хочешь находить это радио по названию, то пиши вот ему --->>> {host.mention}")
        else:
            await ctx.send(f"Попробуй вставить ссылку на **АУДИОПОТОК** (не на сайт с радио).")
            await ctx.send(f"Если не получилось с **2** попыток, то скажи разрабу, что он даун. UPD: его дс здесь --->>> {host.mention}")
            await voice_client.disconnect()
            
        return
    
    
    source = await discord.FFmpegOpusAudio.from_probe(radio_stations[station_name])
    voice_client.play(source)

@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()

bot.run('MTEzOTk0NDQ1ODMxODc3NDI3Mg.G_DTUd.k4C69GGN5sVN7xLk9Pcb6LkMM26YEkLfeDLHrE')