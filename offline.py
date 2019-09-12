import discord
from configs import bot_config
import asyncio
from modules import getter
from discord.ext import commands, tasks
import commands as cmd


class offline(commands.Cog):

    # ◄███▓▒░░ SYSTEM ░░▒▓███►#

    @tasks.loop(hours=24)
    async def get_statistic(self):
        await asyncio.sleep(5);
        try:
            sql1 = "SELECT {},{} FROM {}".format(bot_config.MYSQL_KK["kanal_id"],bot_config.MYSQL_KK["discord_zahl"],
            bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"]);
            data1 = getter.getData(sql1);

            sql2 = "SELECT {},{} FROM {}".format(bot_config.MYSQL_MOD["kanal_id"],bot_config.MYSQL_MOD["discord_mod"],bot_config.MYSQL_CONFIGURATION["mysql_kanal_mod"]);
            data2 = getter.getData(sql2);

            if data2 != []:
                SERVER = self.client.get_guild(int(data2[0][0]));
                if SERVER != None:
                    SERVER_MOD = SERVER.get_channel(int(data2[0][1]));

            for value in data1:
                if value[1] != None:
                    SERVER = self.client.get_guild(value[0]);
                    if SERVER != None:
                        CHANNEL = SERVER.get_channel(value[1]);
                        if CHANNEL != None:
                            async for message in CHANNEL.history(limit=20):
                                if (message.author.bot != True and message.reactions == []) or (message.author.bot != True and message.reactions[0].emoji != bot_config.DISCORD_EMOJIS["positiv"]):
                                    if message.attachments != []:
                                        win = discord.Embed(
                                            title="✙ Beobachter - valdymo pultas".format(message.author.mention),
                                            description="✙ {} laukia {}.".format(message.author.mention,"dropo patvirtinimo"),
                                            color=discord.Color.purple(),
                                        );
                                        win.set_author(name="{} - {}".format(message.guild.name,message.guild.id), icon_url=
                                        bot_config.DISCORD_MODULE_IMAGES["gp"]);
                                        win.set_thumbnail(url="https://cdn.discordapp.com/attachments/594153281169653760/595574430948655117/gp.png");
                                        win.add_field(name="Patvirtinkite žaidėjus",value="**{}** **Kontentas:** *{}* **-** *{}*.".format(message.guild.name, message.author.mention, message.content),inline=True);
                                        win.set_image(url=message.attachments[0].url);
                                        win.set_footer(text="✙ Beobachter {} versija.".format(bot_config.CLIENT_VERSION));
                                        await SERVER_MOD.send(embed=win);
                                    else:
                                        if not message.author.bot:
                                            win = discord.Embed(
                                                title="✙ Beobachter - valdymo pultas".format(message.author.mention),
                                                description="✙ {} laukia {}.".format(message.author.mention,"dropo patvirtinimo"),
                                                color=discord.Color.purple(),
                                            );
                                            win.set_author(name="{}".format(message.guild.name), icon_url=bot_config.DISCORD_MODULE_IMAGES["gp"]);
                                            win.set_thumbnail(url="https://cdn.discordapp.com/attachments/594153281169653760/595574430948655117/gp.png");
                                            win.add_field(name="Patvirtinkite žaidėjus",value="**Kontentas:** *{}* **✉** *{}*.".format(message.author.mention, message.content), inline=True);
                                            win.add_field(name="Papildoma informacija",value="`Kanalo pavadinimas: {}`\n`Kanalo id: {}`\n`Žinutės id: {}`\n`Žinutės nuoroda:` {}".format(message.author.guild, message.author.guild.id, message.id,message.jump_url), inline=True);
                                            win.set_footer(text="✙ Beobachter {} versija.".format(
                                                bot_config.CLIENT_VERSION));
                                            await SERVER_MOD.send(embed=win);
                                        else:
                                            pass;

                                if message.author.bot != True:
                                    await message.add_reaction(bot_config.DISCORD_EMOJIS["positiv"]);

        except Exception as error:
            print(error);

    @tasks.loop(hours=24)
    async def clean(self):
        await asyncio.sleep(5);
        try:
            sql1 = "SELECT {},{},{} FROM {}".format(bot_config.MYSQL_KK["kanal_id"],bot_config.MYSQL_KK["discord_registration"],
            bot_config.MYSQL_KK["discord_beobachter"],bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"]);
            data1 = getter.getData(sql1);

            for value in data1:
                if value[1] != None:
                    SERVER = self.client.get_guild(value[0]);
                    if SERVER != None:
                        REGISTRATION = SERVER.get_channel(value[1]);
                        if REGISTRATION != None:
                            async for message in REGISTRATION.history(limit=20):
                                if message.author.bot != True or message.author.id != bot_config.CLIENT_ID:
                                    await message.author.send("**{}** *Sveikas {}, noriu pranešti, kad tavo RSN registracija nepavyko. Priežastys: Beobachter botas buvo offline. Bandyk dar kartą.*".format(message.guild.name,message.author.name));
                                    await message.delete();

            for value in data1:
                if value[2] != None:
                    SERVER = self.client.get_guild(value[0]);
                    if SERVER != None:
                        BEOBACHTER = SERVER.get_channel(value[2]);
                        if BEOBACHTER != None:
                            async for message in BEOBACHTER.history(limit=20):
                                if message.author.bot != True or message.author.id != bot_config.CLIENT_ID:
                                    await message.author.send("**{}** *Sveikas {}, noriu pranešti, kad Beobachter botas buvo offline. Dėl šios priežasties negalėjai naudotis Beobachter komandomis. Bandyk dar kartą.*".format(message.guild.name,message.author.name));
                                    await message.delete();

        except Exception as error:
            print(error);

    def __init__(self,client):
        self.client = client;
        self.name = bot_config.CLIENT_NAME;
        self.version = bot_config.CLIENT_VERSION;
        self.get_statistic.start();
        self.clean.start();

def setup(client):
    client.add_cog(offline(client));