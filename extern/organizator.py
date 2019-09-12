import discord
from configs import bot_config
from configs.extern import org_config
import asyncio
from modules import getter
from discord.ext import commands, tasks
from datetime import datetime

class organizator(commands.Cog):

    #◄███▓▒░░ SYSTEM ░░▒▓███►#

    @tasks.loop(minutes=40)
    async def check_event(self):
        await asyncio.sleep(5);
        TIME = 0;
        date = datetime.now();

        sql = "SELECT * FROM {}".format(bot_config.MYSQL_CONFIGURATION["mysql_kanal_ereignisse"]);
        data = getter.getData(sql);

        for value in data:
            if value[6] != 1:
                if value[4] == date.strftime("%d.%m"):
                    if int(date.strftime("%H"))+1 >= 12:
                        sql = "SELECT {},{},{} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["discord_random"],bot_config.MYSQL_KK["discord_mitglied"],
                        bot_config.MYSQL_KK["discord_ereignisse"],bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
                        bot_config.MYSQL_KK["kanal_id"],value[1]);
                        data = getter.getData(sql);

                        if data != []:
                            TIME = str(value[5]).replace(":", "");
                            SERVER = self.client.get_guild(value[1]);
                            CHANNEL1 = SERVER.get_channel(data[0][0]);
                            CHANNEL2 = SERVER.get_channel(data[0][1]);

                            if int(date.strftime("%H"))+1 == int(TIME[:2]):
                                await CHANNEL1.send("**{}** *Dėmesio! {} eventas prasidėjo. Daugiau informacijos <#{}> skiltyje arba parašę komandą `.events`.*".format(SERVER.name,value[3],data[0][2]));
                                await CHANNEL2.send("**{}** *Dėmesio! {} eventas prasidėjo. Daugiau informacijos <#{}> skiltyje arba parašę komandą `.events`.*".format(SERVER.name,value[3],data[0][2]));
                                sql3 = "UPDATE {} SET {}={} WHERE {}={}".format(
                                    bot_config.MYSQL_CONFIGURATION["mysql_kanal_ereignisse"],
                                    bot_config.MYSQL_E["ereignisse_status"],1,
                                    "id", value[0]);
                                getter.setData(sql3);
                            else:
                                pass;

                            if int(date.strftime("%H"))+2 == int(TIME[:2]):
                                await CHANNEL1.send("**{}** *Dėmesio! {} organizatorius <@{}> planuoja {} eventą. Daugiau informacijos <#{}> skiltyje arba parašę komandą `.events`.*".format(SERVER.name,value[5],value[2],value[3],data[0][2]));
                                await CHANNEL2.send("**{}** *Dėmesio! {} organizatorius <@{}> planuoja {} eventą. Daugiau informacijos <#{}> skiltyje arba parašę komandą `.events`.*".format(SERVER.name,value[5],value[2],value[3],data[0][2]));
                            else:
                                pass;

                            if ((int(date.strftime("%H")) + 2 != int(TIME[:2])) or (int(date.strftime("%H")) + 1 != int(TIME[:2]))) and value[6] != 1:
                                await CHANNEL1.send("**{}** *Dėmesio! {} GMT+1 Lietuvos laiku, organizatorius <@{}> planuoja {} eventą. Daugiau informacijos <#{}> skiltyje arba parašę komandą `.events`.*".format(SERVER.name,value[5],value[2],value[3],data[0][2]));
                                await CHANNEL2.send("**{}** *Dėmesio! {} GMT+1 Lietuvos laiku, organizatorius <@{}> planuoja {} eventą. Daugiau informacijos <#{}> skiltyje arba parašę komandą `.events`.*".format(SERVER.name,value[5],value[2],value[3],data[0][2]));
                            else:
                                pass;

            if value[6] == 1:
                TIME = str(value[5]).replace(":", "");
                if int(TIME[:2]) <= int(date.strftime("%H")):
                    sql = "DELETE FROM {} WHERE {}={}".format(bot_config.MYSQL_CONFIGURATION["mysql_kanal_ereignisse"], "id", value[0]);
                    getter.setData(sql);

    async def preprocessor(self,ctx,arg,data1,data2,option,extra):
        STRING = []; STRING = str(arg).split(" ");
        CHANNEL = self.client.get_channel(data2[0][0]);
        win = discord.Embed(
            title="✙ Beobachter - {} eventas".format(org_config.EVENT_NAME[option]),
            description="✙ {} organizuoja **{}** - **{}** Lietuvos laiku, {} eventą. Norintiems dalyvauti, prašome paspausti ant {} emoji.".format(
            ctx.author.mention,
            STRING[1],STRING[2], org_config.EVENT_NAME[option],bot_config.DISCORD_EMOJIS["positiv"]),
            color=discord.Color.purple(),
        );
        win.set_author(name="{} - Eventai".format(ctx.guild.name),icon_url=bot_config.CLIENT_ICON);
        win.set_thumbnail(url=org_config.EMBED_IMAGES[option]);
        if extra != "":
            win.add_field(name="Papildoma informacija",value="{}".format(extra),inline=True);
        win.set_footer(text="✙ Beobachter {} versija.".format(bot_config.CLIENT_VERSION));
        await CHANNEL.send(embed=win);

        sql3 = "INSERT INTO {} ({},{},{},{},{},{}) VALUES ({},{},'{}','{}','{}',{})".format(
            bot_config.MYSQL_CONFIGURATION["mysql_kanal_ereignisse"],
            bot_config.MYSQL_E["kanal_id"], bot_config.MYSQL_E["benutzer_id"],
            bot_config.MYSQL_E["ereignisse_name"], bot_config.MYSQL_E["ereignisse_datum"],
            bot_config.MYSQL_E["ereignisse_zeit"], bot_config.MYSQL_E["ereignisse_status"],
            ctx.guild.id,ctx.author.id,
            org_config.EVENT_NAME[option],STRING[1],
            STRING[2],0);
        data = getter.setData(sql3);
        await ctx.author.send("**{}** *Jūs sėkmingai užregistravote eventą.*".format(ctx.guild.name));

    def __init__(self,client):
        self.client = client;
        self.name = bot_config.CLIENT_NAME;
        self.author = bot_config.CLIENT_AUTHOR;
        self.check_event.start();

    #◄███▓▒░░ ADMINISTRATION ░░▒▓███►#

    @commands.command()
    async def add(self,ctx,*,arg):
        INFORMATION = []; STRING = []; EXTRA = "";
        STRING = str(arg).split(" ");

        sql = "SELECT {} FROM {} WHERE {}={} AND {}={}".format(bot_config.MYSQL_KMK["spezial_status"], bot_config.MYSQL_CONFIGURATION["mysql_kanal_mitglied_konten"],
        bot_config.MYSQL_KMK["benutzer_id"],ctx.author.id,
        bot_config.MYSQL_KMK["kanal_id"],ctx.guild.id);
        data1 = getter.getData(sql);

        sql2 = "SELECT {} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["discord_ereignisse"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
        bot_config.MYSQL_KMK["kanal_id"],ctx.guild.id);
        data2 = getter.getData(sql2);

        for value in STRING[3:]:
            EXTRA += "{} ".format(value);

        if data1 != [] and data2 != []:
            for event in org_config.EVENT_NAME:
                if STRING[0] == event:
                    await self.preprocessor(ctx,arg,data1,data2,STRING[0],EXTRA);
        else:
            if data1 == []:
                await ctx.author.send("**{}** *Jūs neturite privilegijos naudotis šia komanda.*".format(ctx.guild.name));
            elif data2 == []:
                await ctx.send("**{}** *Beobachter negali rasti eventų skilties.*".format(ctx.guild.name));
                await ctx.send("**{}** *Prašome sukonfigūruokite eventų skiltį su Beobachter botu, naudodami .setup komandą.*".format(ctx.guild.name));
        await ctx.message.delete();

    @commands.command()
    async def organize(self,ctx):
        sql = "SELECT {} FROM {} WHERE {}={} AND {}={}".format(bot_config.MYSQL_KMK["spezial_status"],bot_config.MYSQL_CONFIGURATION["mysql_kanal_mitglied_konten"],
        bot_config.MYSQL_KMK["benutzer_id"],ctx.author.id,
        bot_config.MYSQL_KMK["kanal_id"],ctx.guild.id);
        data = getter.getData(sql);

        if data != []:
            win = discord.Embed(
                color=discord.Color.purple(),
                description="**Pavyzdys:** *.add tob 01.08 20:00 Dėmesio @everyone! Eventas vyks 360w. Norintis dalyvauti evente, turi prisijungti prie voice kanalo!*"
            );
            win.set_thumbnail(url=bot_config.CLIENT_ICON);
            win.set_author(name="✙ Beobachter - Organizatoriaus komandos",icon_url=bot_config.CLIENT_ICON);
            for value in org_config.EVENT_NAME.items():
                win.add_field(name="{}".format(value[1]),value="`.add {} data laikas papildoma_informacija`".format(value[0]));
            win.set_footer(text="✙ Beobachter {} versija.".format(bot_config.CLIENT_VERSION));
            await ctx.author.send(embed=win);
        else:
            await ctx.author.send("**{}** *Jūs neturite privilegijos naudotis šia komanda.*".format(ctx.guild.name));

        await ctx.message.delete();

    # ◄███▓▒░░ USER ░░▒▓███►#

    @commands.command()
    async def events(self,ctx):
        sql = "SELECT * FROM {} WHERE {}={}".format(bot_config.MYSQL_CONFIGURATION["mysql_kanal_ereignisse"],bot_config.MYSQL_E["kanal_id"],ctx.guild.id);
        data = getter.getData(sql);

        if data != []:
            win = discord.Embed(
                title="✙ Beobachter - {} Eventai".format(ctx.guild.name),
                color=discord.Color.purple(),
            );
            win.set_thumbnail(url=bot_config.CLIENT_ICON);
            win.set_author(name="✙ Beobachter - Eventai",icon_url=bot_config.CLIENT_ICON);
            for value in data:
                win.add_field(name="{}".format(value[3]),value=":calendar: **Data:** *{}.*\n:stopwatch: **Laikas:** *{} Lietuvos laiku.*\n:spy: **Organizatorius:** *<@{}>.*".format(str(value[4]),str(value[5]),value[2]),inline=False);

            win.set_footer(text="✙ Beobachter {} versija.".format(bot_config.CLIENT_VERSION));
            await ctx.send(embed=win);
        else:
            await ctx.send("**{}** *Šiuo metu, nėra organizuojamų eventų.*".format(ctx.guild.name));

def setup(client):
    client.add_cog(organizator(client));