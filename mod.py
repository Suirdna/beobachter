import discord
import locale
import requests
import random
from configs import bot_config
from modules import getter
from discord.ext import commands
from discord.utils import get
from datetime import datetime
from bs4 import BeautifulSoup

class functions(commands.Cog):

    # ◄███▓▒░░ SYSTEM ░░▒▓███►#

    async def calculate_drop(self,ctx,arg,users,item_id,server_id):
        locale.setlocale(locale.LC_ALL,"german");
        currentTime = datetime.now();
        INFORMATION = []; USERS = users; FORMAT = ""; ITEM_ID = 0; DATA_SPLIT = []; DATA = "";

        DATA = str(arg);
        DATA_SPLIT = DATA.split(" ");
        for value in DATA_SPLIT[:-2]:
            FORMAT += "<@{}> ".format(value);

        index = len(DATA_SPLIT)-2;
        format = DATA_SPLIT[index];
        format = format.replace("<","");
        format = format.replace(">", "");
        format = format.replace("#", "");

        item = discord.Client.get_channel(self.client,int(format));

        sql = "SELECT {},{},{},{},{},{},{},{},{},{},{},{},{},{} FROM {} WHERE {}={}".format(
            bot_config.MYSQL_KK["discord_mitglied"], bot_config.MYSQL_KK["discord_zahl"],
            bot_config.MYSQL_KK["emoji_gp"], bot_config.MYSQL_KK["role_zahl_2"],
            bot_config.MYSQL_KK["role_zahl_3"], bot_config.MYSQL_KK["role_zahl_4"],
            bot_config.MYSQL_KK["role_zahl_5"],
            bot_config.MYSQL_KK["role_name_2"], bot_config.MYSQL_KK["role_name_3"],
            bot_config.MYSQL_KK["role_name_4"], bot_config.MYSQL_KK["role_name_5"],
            bot_config.MYSQL_KK["kanal_id"], bot_config.MYSQL_KK["discord_random"],
            bot_config.MYSQL_KK["discord_registration"],
            bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"], bot_config.MYSQL_KK["kanal_id"],server_id);

        data = getter.getData(sql);
        for value in data:
            INFORMATION.append(value[0]);  # DISCORD_MITGLIED
            INFORMATION.append(value[1]);  # DISCORD_ZAHL
            INFORMATION.append(value[2]);  # EMOJI_GP
            INFORMATION.append(value[3]);  # role_zahl_2
            INFORMATION.append(value[4]);  # role_zahl_3
            INFORMATION.append(value[5]);  # role_zahl_4
            INFORMATION.append(value[6]);  # role_zahl_5
            INFORMATION.append(value[7]);  # role_name_2
            INFORMATION.append(value[8]);  # role_name_3
            INFORMATION.append(value[9]);  # role_name_4
            INFORMATION.append(value[10]);  # role_name_5
            INFORMATION.append(value[11]);  # KANAL_ID
            INFORMATION.append(value[12]);  # DISCORD_RANDOM
            INFORMATION.append(value[13]);  # DISCORD_REGISTRATION

        COUNT = 0; VALUE = 0; SUM = 0; GP = 0; MESSAGE_COUNT = 0;
        TEXT = []; SEARCH = [];
        VALUE_STR = ""; DATA = "";
        STATUS = False;

        url = "http://services.runescape.com/m=itemdb_oldschool/Twisted_bow/viewitem?obj={}".format(item_id);
        source_code = requests.get(url);
        plain_text = source_code.text;
        crawler = BeautifulSoup(plain_text,"html.parser");

        for link in crawler.findAll("h3"):
            TEXT.append(str(link));

        SEARCH.append(TEXT[0].find('"'));
        SEARCH.append(TEXT[0].find('"',SEARCH[0]+1));
        VALUE_STR = TEXT[0][SEARCH[0]+1:SEARCH[1]];
        VALUE = int(VALUE_STR.replace(",", ""));
        SUM = (VALUE/len(USERS)) + random.randint(1,10);

        if VALUE != 0:
            for value in USERS:
                USER = value.replace("<","");
                USER = USER.replace("@", "");
                USER = USER.replace("!", "");
                USER = int(USER.replace(">", ""));
                sql1 = "SELECT * FROM {} WHERE {}={}".format(
                bot_config.MYSQL_CONFIGURATION["mysql_allgemein_statistik"], bot_config.MYSQL_AS["benutzer_id"], USER);
                data = getter.getData(sql1);

                EXTERN_KANAL = self.client.get_guild(server_id);
                EXTERN_CHANNEL = EXTERN_KANAL.get_channel(INFORMATION[1]);
                user = EXTERN_KANAL.get_member(USER);

                if data != []:
                    for result in data:
                        GP += int(result[6] + SUM);
                else:
                    GP = int(SUM);

                if data != []:
                    Text = "Record: {} - Server: {} - Action: {} -  Channel: {} - User: {} - Sum: {} - BeforeSum: {}\n".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), EXTERN_KANAL.name,
                    bot_config.CLIENT_MESSAGES["on_command_drop_succ"], INFORMATION[1], user.display_name, GP, result[6]);

                    sql = "UPDATE {} SET {}='{}',{}={} WHERE {}={}".format(
                        bot_config.MYSQL_CONFIGURATION["mysql_allgemein_statistik"], bot_config.MYSQL_AS["kanal_name"], EXTERN_KANAL.name,
                        bot_config.MYSQL_AS["zahl"], GP,
                        bot_config.MYSQL_AS["benutzer_id"], user.id);
                    getter.setData(sql);

                    if MESSAGE_COUNT == 0:
                        MESSAGE_COUNT += 1;
                        if INFORMATION[0] != None: # DISCORD_MITGLIED
                            """CHANNEL1 = EXTERN_KANAL.get_channel(INFORMATION[0]);
                            await CHANNEL1.send("**{}** *Komanda:* *{}{}.*\n**{}** *Splitas:* {} *{}.*\n{}".format(
                            EXTERN_KANAL.name,FORMAT,item.name,EXTERN_KANAL.name,INFORMATION[2] if INFORMATION[2] != None else "💰",locale.format_string("%d",SUM,grouping=True),
                            "**{}** *Informacija:* *Daugiau informacijos <#{}> skiltyje.*".format(EXTERN_KANAL.name,INFORMATION[1]) if INFORMATION[1] != None else ""));"""

                        if INFORMATION[1] != None: #DISCORD_ZAHL
                            CHANNEL2 = EXTERN_KANAL.get_channel(INFORMATION[1]);
                            await CHANNEL2.send("**{}** *Komanda:* *{}{}.*\n**{}** *Splitas:* {} *{}.*\n**{}** *Patvirtino:* **{}**.".format(
                            EXTERN_KANAL.name,FORMAT,item.name,EXTERN_KANAL.name,INFORMATION[2] if INFORMATION[2] != None else "💰",locale.format_string("%d",SUM,grouping=True),
                            EXTERN_KANAL.name,ctx.author.display_name));

                        if INFORMATION[12] != None: #DISCORD_RANDOM
                            CHANNEL3 = EXTERN_KANAL.get_channel(INFORMATION[12]);
                            await CHANNEL3.send("**{}** *Komanda:* *{}{}.*\n**{}** *Splitas:* {} *{}.*\n{} {}".format(
                            EXTERN_KANAL.name,FORMAT,item.name,EXTERN_KANAL.name,INFORMATION[2] if INFORMATION[2] != None else "💰",locale.format_string("%d",SUM,grouping=True),
                            "**{}** *Informacija:* *Daugiau informacijos <#{}> skiltyje.*".format(EXTERN_KANAL.name,INFORMATION[1]) if INFORMATION[1] != None else "",
                            "PvM narių registracija vyksta <#{}> skiltyje.".format(INFORMATION[13] if INFORMATION[13] != None else "")));

                else:
                    Text = "Record: {} - Server: {} - Action: {} -  Channel: {} - User: {} - Sum: {}\n".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), EXTERN_KANAL.name,
                    bot_config.CLIENT_MESSAGES["on_command_drop_added"], INFORMATION[1], user.display_name, SUM);

                    if MESSAGE_COUNT == 0:
                        MESSAGE_COUNT += 1;
                        if INFORMATION[0] != None: # DISCORD_MITGLIED
                            """CHANNEL1 = EXTERN_KANAL.get_channel(INFORMATION[0]);
                            await CHANNEL1.send("**{}** *Komanda:* *{}{}.*\n**{}** *Splitas:* {} *{}.*\n{}".format(
                            EXTERN_KANAL.name,FORMAT,item.name,EXTERN_KANAL.name,INFORMATION[2] if INFORMATION[2] != None else "💰",locale.format_string("%d",SUM,grouping=True),
                            "**{}** *Informacija:* *Daugiau informacijos <#{}> skiltyje.*".format(EXTERN_KANAL.name,INFORMATION[1]) if INFORMATION[1] != None else ""));"""

                        if INFORMATION[1] != None: #DISCORD_ZAHL
                            CHANNEL2 = EXTERN_KANAL.get_channel(INFORMATION[1]);
                            await CHANNEL2.send("**{}** *Komanda:* *{}{}.*\n**{}** *Splitas:* {} *{}.*\n**{}** *Patvirtino:* **{}**.".format(
                            EXTERN_KANAL.name,FORMAT,item.name,EXTERN_KANAL.name,INFORMATION[2] if INFORMATION[2] != None else "💰",locale.format_string("%d",SUM,grouping=True),
                            EXTERN_KANAL.name,ctx.author.display_name));

                        if INFORMATION[12] != None: #DISCORD_RANDOM
                            CHANNEL3 = EXTERN_KANAL.get_channel(INFORMATION[12]);
                            await CHANNEL3.send("**{}** *Komanda:* *{}{}.*\n**{}** *Splitas:* {} *{}.*\n{} {}".format(
                            EXTERN_KANAL.name,FORMAT,item.name,EXTERN_KANAL.name,INFORMATION[2] if INFORMATION[2] != None else "💰",locale.format_string("%d",SUM,grouping=True),
                            "**{}** *Informacija:* *Daugiau informacijos <#{}> skiltyje.*".format(EXTERN_KANAL.name,INFORMATION[1]) if INFORMATION[1] != None else "",
                            "PvM narių registracija vyksta <#{}> skiltyje.".format(INFORMATION[13] if INFORMATION[13] != None else "")));

                    SUM = SUM+random.randint(0,50);
                    sql2 = "INSERT INTO {} ({},{},{},{},{},{}) VALUES ({},'{}',{},'{}','{}',{})".format(
                        bot_config.MYSQL_CONFIGURATION["mysql_allgemein_statistik"],
                        bot_config.MYSQL_AS["kanal_id"], bot_config.MYSQL_AS["kanal_name"],
                        bot_config.MYSQL_AS["benutzer_id"], bot_config.MYSQL_AS["benutzer_name"],
                        bot_config.MYSQL_AS["benutzer_symbol"], bot_config.MYSQL_AS["zahl"],
                        EXTERN_KANAL.id, EXTERN_KANAL.name,
                        user.id, user.display_name,
                        user.avatar_url if user.avatar_url != None else user.avatar, SUM);
                    data = getter.setData(sql2);

                if GP >= INFORMATION[6]:  # role_value_5
                    role_set = get(EXTERN_KANAL.roles, name=INFORMATION[10]);  # discord_role_5
                    role_del = get(EXTERN_KANAL.roles, name=INFORMATION[9]);  # discord_role_4
                    await user.add_roles(role_set, reason="Beobachter level up.", atomic=True);
                    await user.remove_roles(role_del, reason="Beobachter role deleted.", atomic=True);
                elif GP >= INFORMATION[5]:  # role_value_4
                    role_set = get(EXTERN_KANAL.roles, name=INFORMATION[9]);  # discord_role_4
                    role_del = get(EXTERN_KANAL.roles, name=INFORMATION[8]);  # discord_role_3
                    await user.add_roles(role_set, reason="Beobachter level up.", atomic=True);
                    await user.remove_roles(role_del, reason="Beobachter role deleted.", atomic=True);
                elif GP >= INFORMATION[4]:  # role_value_3
                    role_set = get(EXTERN_KANAL.roles, name=INFORMATION[8]);  # discord_role_3
                    role_del = get(EXTERN_KANAL.roles, name=INFORMATION[7]);  # discord_role_2
                    await user.add_roles(role_set, reason="Beobachter level up.", atomic=True);
                    await user.remove_roles(role_del, reason="Beobachter role deleted.", atomic=True);
                elif GP >= INFORMATION[3]:  # role_value_2
                    role_set = get(EXTERN_KANAL.roles, name=INFORMATION[7]);  # discord_role_2
                    await user.add_roles(role_set, reason="Beobachter level up.", atomic=True);

                try:
                    file = open("./data/statistic.txt", "a");
                    file.write(Text);
                except Exception as error:
                    encodet = textData.encode('utf-8');
                    file.write("{}\n".format(encodet));
                finally:
                    file.close();
                    GP = 0;

    def __init__(self,client):
        self.client = client;
        self.name = bot_config.CLIENT_VERSION;
        self.version = bot_config.CLIENT_VERSION

    # ◄███▓▒░░ ADMINISTRATION ░░▒▓███►#

    @commands.command()
    async def drop(self,ctx,*,arg):
        INFORMATION = [];
        sql = "SELECT {},{},{} FROM {} WHERE {}={}".format(bot_config.MYSQL_MOD["kanal_id"],
        bot_config.MYSQL_MOD["discord_mod"],
        bot_config.MYSQL_MOD["kanal_besitzer_id"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_mod"],
        bot_config.MYSQL_MOD["kanal_id"], ctx.guild.id);
        data = getter.getData(sql);

        for value in data:
            INFORMATION.append(value[0]);  # KANAL_ID
            INFORMATION.append(value[1]);  # DISCORD_MOD
            INFORMATION.append(value[2]);  # KANAL_BESITZER_ID

        if INFORMATION[0] == ctx.guild.id:
            if INFORMATION[1] == ctx.channel.id:
                CONTEXT = str(arg);
                NEW_CONTEXT = CONTEXT.split(" ");

                ITEM_CHANNEL = NEW_CONTEXT[len(NEW_CONTEXT)-2];
                ITEM_CHANNEL = ITEM_CHANNEL.replace("<","");
                ITEM_CHANNEL = ITEM_CHANNEL.replace(">", "");
                ITEM_CHANNEL = ITEM_CHANNEL.replace("#", "");
                ITEM_CHANNEL = ITEM_CHANNEL.replace("@", "");
                CHANNEL = self.client.get_channel(int(ITEM_CHANNEL));
                ITEM_ID = int(CHANNEL.topic);

                USERS = NEW_CONTEXT[0:len(NEW_CONTEXT)-2];
                SERVER_ID = int(NEW_CONTEXT[len(NEW_CONTEXT)-1]);
                await self.calculate_drop(ctx,arg,USERS,ITEM_ID,SERVER_ID);
            else:
                await ctx.send("**{}** *Jūs neturite privilegijos naudotis šia komanda.*".format(ctx.guild.name));

    @commands.command()
    async def dcdrop(self,ctx,*,arg):
        DATA = str(arg).split(" ");
        sql = "SELECT {} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["discord_zahl"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
        bot_config.MYSQL_KK["kanal_id"],
        int(DATA[0]));
        data = getter.getData(sql);

        SERVER = self.client.get_guild(int(DATA[0]));
        CHANNEL = SERVER.get_channel(data[0][0]);
        await CHANNEL.send("**{}** *Komanda:* *<@{}>.*\n**{}** *Dropas nepriimtas*. **Priežastis:** *{}*.\n**{}** *Atmėtė:* **{}**.".format(SERVER.name,DATA[1],SERVER.name,DATA[2],SERVER.name,ctx.author.display_name));


    @commands.command()
    async def ban(self,ctx,*,arg):
        currentTime = datetime.now();
        sql = "SELECT {},{} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["kanal_besitzer_id"],
        bot_config.MYSQL_KK["bot_administration_id"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
        bot_config.MYSQL_KK["kanal_id"],
        ctx.guild.id);
        data = getter.getData(sql);

        if ctx.guild.owner.id == data[0][0] or data[0][1] == bot_config.CLIENT_ADMNISTRATION:
            STRING = str(arg); DATA = [];
            DATA = STRING.split(" ");
            USER = DATA[0];
            USER = USER.replace("<", "");
            USER = USER.replace(">", "");
            USER = USER.replace("@", "");
            USER = int(USER.replace("!", ""));

            sql = "SELECT {},{} FROM {} WHERE {}={} AND {}={}".format(bot_config.MYSQL_KB["benutzer_id"],
            bot_config.MYSQL_KB["benutzer_ban_grund"],
            bot_config.MYSQL_CONFIGURATION["mysql_kanal_ban"],
            bot_config.MYSQL_KB["benutzer_id"],USER,
            bot_config.MYSQL_KB["kanal_id"],ctx.guild.id);
            data = getter.getData(sql);

            if data != []:
                await ctx.send("**{}** *Žaidėjas jau yra užbanintas.* **Priežastis:** *{}*.".format(ctx.guild.name,value[0][2]));
            else:
                user = ctx.guild.get_member(USER);
                sql = "INSERT INTO {} ({},{},{},{},{},{}) VALUES ({},'{}',{},'{}','{}','{}')".format(
                bot_config.MYSQL_CONFIGURATION["mysql_kanal_ban"],
                bot_config.MYSQL_KB["kanal_id"], bot_config.MYSQL_KB["kanal_name"],
                bot_config.MYSQL_KB["benutzer_id"], bot_config.MYSQL_KB["benutzer_name"],
                bot_config.MYSQL_KB["benutzer_ban_grund"], bot_config.MYSQL_KB["benutzer_ban_datum"],
                ctx.guild.id, ctx.guild.name, user.id, user.display_name, DATA[1], currentTime.strftime("%d/%m/%y  %H:%M:%S"));
                await ctx.send("**{}** *Žaidėjas {} yra užbanintas.* **Priežastis:** *{}*.".format(ctx.guild.name,user.display_name,DATA[1]));
                await ctx.guild.ban(user,reason=None);
        await ctx.message.delete();

    @commands.command()
    async def unban(self,ctx,*,arg):
        currentTime = datetime.now();
        sql = "SELECT {},{} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["kanal_besitzer_id"],
        bot_config.MYSQL_KK["bot_administration_id"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
        bot_config.MYSQL_KK["kanal_id"],
        ctx.guild.id);
        data = getter.getData(sql);

        if ctx.guild.owner.id == data[0][0] or data[0][1] == bot_config.CLIENT_ADMNISTRATION:
            STRING = str(arg);  DATA = [];
            DATA = STRING.split(" ");
            USER = DATA[0];
            USER = USER.replace("<", "");
            USER = USER.replace(">", "");
            USER = USER.replace("@", "");
            USER = int(USER.replace("!", ""));

            sql = "SELECT {},{} FROM {} WHERE {}={} AND {}={}".format(bot_config.MYSQL_KB["benutzer_id"],
            bot_config.MYSQL_KB["benutzer_ban_grund"],
            bot_config.MYSQL_CONFIGURATION["mysql_kanal_ban"],
            bot_config.MYSQL_KB["benutzer_id"], USER,
            bot_config.MYSQL_KB["kanal_id"], ctx.guild.id);
            data = getter.getData(sql);

            print(USER);

            await ctx.guild.unban(USER, reason=None);

            if data != []:
                bans = await ctx.guild.bans();
                sql = "DELETE FROM {} WHERE {}={} AND {}={}".format(bot_config.MYSQL_CONFIGURATION["mysql_kanal_ban"],
                bot_config.MYSQL_KB["benutzer_id"],
                USER, bot_config.MYSQL_KB["kanal_id"], ctx.guild.id);
                getter.setData(sql);
                for value in bans:
                    if value[1].id == USER:
                        await ctx.guild.unban(value[1],reason=None);

                await ctx.send("**{}** *Žaidėjas yra atbanintas*.".format(ctx.guild.name));
            else:
                await ctx.send("**{}** *Žaidėjas nėra užbanintas.*".format(ctx.guild.name));

        await ctx.message.delete();

    @commands.command()
    async def organizator(self,ctx,*,arg):
        INFORMATION = []; STRING = [];
        STRING = str(arg).split(" ");

        sql = "SELECT {},{} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["kanal_besitzer_id"],
        bot_config.MYSQL_KK["bot_administration_id"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
        bot_config.MYSQL_KK["kanal_id"], ctx.guild.id);
        data = getter.getData(sql);

        for value in data:
            INFORMATION.append(value[0]);
            INFORMATION.append(value[1]);

        if INFORMATION[0] == ctx.author.id or INFORMATION[1] == ctx.author.id:
            USER = STRING[0];
            USER = USER.replace("<","");
            USER = USER.replace(">", "");
            USER = USER.replace("@", "");
            USER = int(USER.replace("!", ""));

            sql = "SELECT {} FROM {} WHERE {}={} AND {}={}".format(bot_config.MYSQL_KMK["benutzer_id"], bot_config.MYSQL_CONFIGURATION["mysql_kanal_mitglied_konten"],
            bot_config.MYSQL_KMK["benutzer_id"], USER,
            bot_config.MYSQL_KMK["kanal_id"], ctx.guild.id);
            data = getter.getData(sql);

            if data != []:
                sql = "UPDATE {} SET {}={} WHERE {}={} AND {}={}".format(
                bot_config.MYSQL_CONFIGURATION["mysql_kanal_mitglied_konten"],
                bot_config.MYSQL_KMK["spezial_status"], 1,
                bot_config.MYSQL_KMK["benutzer_id"], USER,
                bot_config.MYSQL_KMK["kanal_id"], ctx.guild.id);
                getter.setData(sql);
                user = get(ctx.guild.members,id=USER);
                role = get(ctx.guild.roles, name=bot_config.DISCORD_EVENT_ORGANIZER);
                await user.add_roles(role,reason="Event - Organizer added.",atomic=True);
            else:
                await ctx.send("**{}** *Žaidėjas {} nėra užsiregistravęs prie PvM grupės.*".format(ctx.guild.name,STRING[0]));
        await ctx.message.delete();

    @commands.command()
    async def rorganizator(self,ctx,*,arg):
        STRING = [];
        STRING = str(arg).split(" ");
        USER = STRING[0];
        USER = USER.replace("<","");
        USER = USER.replace(">", "");
        USER = USER.replace("@", "");
        USER = int(USER.replace("!", ""));

        sql = "SELECT {} FROM {} WHERE {}={} AND {}={}".format(bot_config.MYSQL_KMK["benutzer_id"], bot_config.MYSQL_CONFIGURATION["mysql_kanal_mitglied_konten"],
        bot_config.MYSQL_KMK["benutzer_id"], USER,
        bot_config.MYSQL_KMK["kanal_id"], ctx.guild.id);
        data = getter.getData(sql);

        if data != []:
            sql = "UPDATE {} SET {}={} WHERE {}={} AND {}={}".format(
            bot_config.MYSQL_CONFIGURATION["mysql_kanal_mitglied_konten"],
            bot_config.MYSQL_KMK["spezial_status"], 0,
            bot_config.MYSQL_KMK["benutzer_id"], USER,
            bot_config.MYSQL_KMK["kanal_id"], ctx.guild.id);
            getter.setData(sql);
            user = get(ctx.guild.members,id=USER);
            role = get(ctx.guild.roles,name=bot_config.DISCORD_EVENT_ORGANIZER);
            await user.remove_roles(role,reason="Event - Organizer remove.",atomic=True);
        else:
            await ctx.send("**{}** *Žaidėjas {} nėra užsiregistravęs prie PvM grupės.*".format(ctx.guild.name,STRING[0]));
        await ctx.message.delete();

    """"@commands.command()
    async def setup(self,ctx,*,arg):
        INFORMATION = []; CMD = []; STRING = arg; failSafe = True;
        sql = "SELECT {},{} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["kanal_besitzer_id"],
        bot_config.MYSQL_KK["bot_administration_id"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
        bot_config.MYSQL_KK["kanal_id"], ctx.guild.id);
        data = getter.getData(sql);

        for value in data:
            INFORMATION.append(value[0]);
            INFORMATION.append(value[1]);

        if arg[:6] == "config":
            sql1 = "SELECT * FROM {} WHERE {}={}".format(bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
            bot_config.MYSQL_KK["kanal_id"], ctx.guild.id);
            data2 = getter.getData(sql1);

            config = discord.Embed(
                title="✙ Beobachter - Serverio konfigūracija",
                description="Pilnai sukonfigūruotas discordo kanalas leidžia naudotis visomis boto funkcijomis. Komanda .setup leidžia rankiniu būdu sukonfigūruoti discordo kanalą. Argumentai apačioje. Pavyzdys: .setup cfg discord_registration [id].",
                color=discord.Color.purple(),
            );
            config.set_author(name="{}".format(ctx.guild.name), icon_url=bot_config.CLIENT_ICON);
            config.set_thumbnail(url=bot_config.CLIENT_ICON);
            for index,value in enumerate(data2[0]):
                if index >= 6:
                    if isinstance(value,int):
                        if index >= 6 and index <=8:
                            config.add_field(name="`.setup cfg {}`".format(list(bot_config.MYSQL_KK.items())[index - 1][0]), value="<@!{}> - `{}`".format(value, value), inline=False);
                        else:
                            config.add_field(name="`.setup cfg {}`".format(list(bot_config.MYSQL_KK.items())[index - 1][0]), value="<#{}> - `{}`".format(value, value), inline=False);
                    else:
                        config.add_field(name="`.setup cfg {}`".format(list(bot_config.MYSQL_KK.items())[index - 1][0]), value="{} - `{}`".format(value, value), inline=False);
            config.set_footer(text="✙ Beobachter {} versija. ✙ Programuotojas: {}.\n".format(bot_config.CLIENT_VERSION,bot_config.CLIENT_AUTHOR));
            await ctx.send(embed=config);

        if arg[:3] == "cfg":
            CMD.append(STRING.split(" "));
            LEN = len(CMD[0][0])+1
            value = arg[LEN:];

            if ctx.author.id == INFORMATION[0] or ctx.author.id == INFORMATION[1]:
                for argument in bot_config.MYSQL_KK.keys():
                    if argument == CMD[0][1] or argument == CMD[0][1]:
                        pass;

                    if argument == CMD[0][1]:
                        sql = "UPDATE {} SET {}='{}' WHERE {}={}".format(
                        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
                        argument, CMD[0][2], bot_config.MYSQL_KK["kanal_id"], ctx.guild.id);
                        getter.setData(sql);
                        await ctx.send("**{}** *{}* sukonfigūruota.".format(ctx.guild.name,argument))
            else:
                await ctx.send("**{}** *Jūs neturite privilegijos naudotis šia komanda.*".format(ctx.guild.name));

        if arg[:4] == "init" and (ctx.author.id == INFORMATION[0] or ctx.author.id == INFORMATION[1]):
            permissions = discord.Permissions(37084224); # 37084224 - standart
            await ctx.guild.create_role(name=bot_config.DISCORD_LOYAL_SPLITTER, permissions=permissions, color=discord.Colour.green(), hoist=True, mentionable=True, reason="Beobachter Initialization");
            await ctx.guild.create_role(name=bot_config.DISCORD_TRUSTED_SPLITTER, permissions=permissions, color=discord.Colour.purple(), hoist=True, mentionable=True, reason="Beobachter Initialization");
            await ctx.guild.create_role(name=bot_config.DISCORD_AVERAGE_SPLITTER, permissions=permissions, color=discord.Colour.magenta(), hoist=True, mentionable=True, reason="Beobachter Initialization");
            await ctx.guild.create_role(name=bot_config.DISCORD_NOVICE_SPLITTER, permissions=permissions, color=discord.Colour.orange(), hoist=True, mentionable=True, reason="Beobachter Initialization");
            await ctx.guild.create_role(name=bot_config.DISCORD_EVENT_ORGANIZER,permissions=permissions,color=discord.Colour.blue(),hoist=True,mentionable=True,reason="Beobachter Initialization");
            await ctx.guild.create_role(name=bot_config.DISCORD_GLOBALS, permissions=permissions, color=discord.Colour.blue(), hoist=True, mentionable=True, reason="Beobachter Initialization");
            await ctx.guild.create_role(name=bot_config.DISCORD_MEMBERS, permissions=permissions, color=discord.Colour.red(), hoist=True, mentionable=True, reason="Beobachter Initialization");
            role_default = get(ctx.guild.roles, name=bot_config.DISCORD_EVERYONES);
            role_event_org = get(ctx.guild.roles, name=bot_config.DISCORD_EVENT_ORGANIZER);
            role_global = get(ctx.guild.roles, name=bot_config.DISCORD_GLOBALS);

            overwrite = discord.PermissionOverwrite()
            overwrite.kick_members = False;
            overwrite.ban_members = False;
            overwrite.administrator = False;
            overwrite.manage_channels = False;
            overwrite.manage_guild = False;
            overwrite.view_audit_log = False;
            overwrite.priority_speaker = False;
            overwrite.manage_messages = False;
            overwrite.mention_everyone = False;
            overwrite.mute_members = False;
            overwrite.deafen_members = False;
            overwrite.move_members = False;
            overwrite.change_nickname = False;
            overwrite.manage_nicknames = False;
            overwrite.manage_roles = False;
            overwrite.manage_webhooks = False;
            overwrite.manage_emojis = False;
            overwrite.create_instant_invite = False;
            overwrite.add_reactions = False;
            overwrite.stream = False;
            overwrite.read_messages = False;
            overwrite.send_messages = False;
            overwrite.send_tts_messages = False;
            overwrite.embed_links = False;
            overwrite.attach_files = False;
            overwrite.read_message_history = False;
            overwrite.external_emojis = False;
            overwrite.speak = False;
            overwrite.use_voice_activation = False;

            overwrite2 = discord.PermissionOverwrite()
            overwrite2.kick_members = False;
            overwrite2.ban_members = False;
            overwrite2.administrator = False;
            overwrite2.manage_channels = False;
            overwrite2.manage_guild = False;
            overwrite2.view_audit_log = False;
            overwrite2.priority_speaker = False;
            overwrite2.manage_messages = False;
            overwrite2.mention_everyone = False;
            overwrite2.mute_members = False;
            overwrite2.deafen_members = False;
            overwrite2.move_members = False;
            overwrite2.change_nickname = False;
            overwrite2.manage_nicknames = False;
            overwrite2.manage_roles = False;
            overwrite2.manage_webhooks = False;
            overwrite2.manage_emojis = False;
            overwrite2.create_instant_invite = True;
            overwrite2.add_reactions = True;
            overwrite2.stream = True;
            overwrite2.read_messages = True;
            overwrite2.send_messages = True;
            overwrite2.send_tts_messages = True;
            overwrite2.embed_links = True;
            overwrite2.attach_files = True;
            overwrite2.read_message_history = True;
            overwrite2.external_emojis = True;
            overwrite2.speak = True;
            overwrite2.use_voice_activation = True;

            overwrite3 = discord.PermissionOverwrite()
            overwrite3.kick_members = False;
            overwrite3.ban_members = False;
            overwrite3.administrator = False;
            overwrite3.manage_channels = False;
            overwrite3.manage_guild = False;
            overwrite3.view_audit_log = False;
            overwrite3.priority_speaker = False;
            overwrite3.manage_messages = False;
            overwrite3.mention_everyone = False;
            overwrite3.mute_members = False;
            overwrite3.deafen_members = False;
            overwrite3.move_members = False;
            overwrite3.change_nickname = False;
            overwrite3.manage_nicknames = False;
            overwrite3.manage_roles = False;
            overwrite3.manage_webhooks = False;
            overwrite3.manage_emojis = False;
            overwrite3.create_instant_invite = True;
            overwrite3.add_reactions = True;
            overwrite3.stream = True;
            overwrite3.read_messages = True;
            overwrite3.send_messages = False;
            overwrite3.send_tts_messages = False;
            overwrite3.embed_links = False;
            overwrite3.attach_files = False;
            overwrite3.read_message_history = True;
            overwrite3.external_emojis = True;
            overwrite3.speak = True;
            overwrite3.use_voice_activation = True;

            await ctx.guild.create_category(bot_config.DISCORD_GROUP, overwrites=None, reason="Beobachter Initialization");
            category = get(ctx.guild.categories, name=bot_config.DISCORD_GROUP);

            await category.create_text_channel(bot_config.DISCORD_REGISTRATION, overwrites=None, reason="Beobachter Initialization", topic=bot_config.DISCORD_REGISTRATION_T);
            await category.create_text_channel(bot_config.DISCORD_COUNT, overwrites=None, reason="Beobachter Initialization", topic=bot_config.DISCORD_COUNT_T, slowmode_delay=600);
            await category.create_text_channel(bot_config.DISCORD_CHECK, overwrites=None, reason="Beobachter Initialization", topic=bot_config.DISCORD_CHECK_T);
            await category.create_text_channel(bot_config.DISCORD_EVENT, overwrites=None, reason="Beobachter Initialization", topic=bot_config.DISCORD_EVENT_T);
            await category.create_text_channel(bot_config.DISCORD_GLOBAL, overwrites=None, reason="Beobachter Initialization", topic=bot_config.DISCORD_GLOBAL_T);
            await category.create_text_channel(bot_config.DISCORD_MEMBER, overwrites=None, reason="Beobachter Initialization", topic=bot_config.DISCORD_MEMBER_T);
            await category.create_text_channel(bot_config.DISCORD_BEOBACHTER, overwrites=None, reason="Beobachter Initialization", topic=bot_config.DISCORD_BEOBACHTER_T);

            registration = get(category.channels, name=bot_config.DISCORD_REGISTRATION);
            count = get(category.channels, name=bot_config.DISCORD_COUNT);
            check = get(category.channels, name=bot_config.DISCORD_CHECK);
            event = get(category.channels, name=bot_config.DISCORD_EVENT);
            globals = get(category.channels, name=bot_config.DISCORD_GLOBAL);
            member = get(category.channels, name=bot_config.DISCORD_MEMBER);
            beobachter = get(category.channels, name=bot_config.DISCORD_BEOBACHTER);

            role_member = get(ctx.guild.roles, name=bot_config.DISCORD_MEMBERS);

            sql = "UPDATE {} SET {}={},{}={},{}={},{}={},{}={},{}={},{}='{}',{}='{}',{}='{}',{}='{}',{}='{}',{}='{}',{}='{}',{}={},{}={},{}={},{}={} WHERE {}={}".format(
                bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
                bot_config.MYSQL_KK["discord_registration"], registration.id,
                bot_config.MYSQL_KK["discord_zahl"], count.id,
                bot_config.MYSQL_KK["discord_uberprufung"], check.id,
                bot_config.MYSQL_KK["discord_global"], globals.id,
                bot_config.MYSQL_KK["discord_mitglied"], member.id,
                bot_config.MYSQL_KK["discord_beobachter"], beobachter.id,
                bot_config.MYSQL_KK["role_name_1"], bot_config.DISCORD_MEMBERS,
                bot_config.MYSQL_KK["role_name_2"], bot_config.DISCORD_NOVICE_SPLITTER,
                bot_config.MYSQL_KK["role_name_3"], bot_config.DISCORD_AVERAGE_SPLITTER,
                bot_config.MYSQL_KK["role_name_4"], bot_config.DISCORD_TRUSTED_SPLITTER,
                bot_config.MYSQL_KK["role_name_5"], bot_config.DISCORD_LOYAL_SPLITTER,
                bot_config.MYSQL_KK["spezial_role_1"], bot_config.DISCORD_EVENT_ORGANIZER,
                bot_config.MYSQL_KK["role_name_global"], bot_config.DISCORD_GLOBALS,
                bot_config.MYSQL_KK["role_zahl_2"], bot_config.DISCORD_ZAHL_2,
                bot_config.MYSQL_KK["role_zahl_3"], bot_config.DISCORD_ZAHL_3,
                bot_config.MYSQL_KK["role_zahl_4"], bot_config.DISCORD_ZAHL_4,
                bot_config.MYSQL_KK["role_zahl_5"], bot_config.DISCORD_ZAHL_5,
                bot_config.MYSQL_KK["kanal_id"], ctx.guild.id);
            getter.setData(sql);

            await registration.set_permissions(role_default,overwrite=overwrite2,reason="Beobachter Initialization");
            await registration.set_permissions(role_member,overwrite=overwrite,reason="Beobachter Initialization");
            await count.set_permissions(role_default,overwrite=overwrite3,reason="Beobachter Initialization");
            await count.set_permissions(role_member,overwrite=overwrite2,reason="Beobachter Initialization");
            await check.set_permissions(role_default,overwrite=overwrite,reason="Beobachter Initialization");
            await check.set_permissions(role_member,overwrite=overwrite2,reason="Beobachter Initialization");
            await event.set_permissions(role_event_org, overwrite=overwrite2, reason="Beobachter Initialization");
            await event.set_permissions(role_default,overwrite=overwrite3,reason="Beobachter Initialization");
            await event.set_permissions(role_member,overwrite=overwrite3,reason="Beobachter Initialization");
            await globals.set_permissions(role_default,overwrite=overwrite,reason="Beobachter Initialization");
            await globals.set_permissions(role_member,overwrite=overwrite,reason="Beobachter Initialization");
            await globals.set_permissions(role_global,overwrite=overwrite2,reason="Beobachter Initialization");
            await member.set_permissions(role_default,overwrite=overwrite,reason="Beobachter Initialization");
            await member.set_permissions(role_member,overwrite=overwrite2,reason="Beobachter Initialization");
            await beobachter.set_permissions(role_default,overwrite=overwrite,reason="Beobachter Initialization");
            await beobachter.set_permissions(role_member,overwrite=overwrite2,reason="Beobachter Initialization");

            INFORMATION2 = [];
            sql1 = "SELECT {},{} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["discord_regeln"],
            bot_config.MYSQL_KK["discord_zahl"],
            bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
            bot_config.MYSQL_KK["kanal_id"], ctx.guild.id);
            data = getter.getData(sql1);

            for value in data:
                INFORMATION2.append(value[0]);
                INFORMATION2.append(value[1]);

            registration_content = "*Prisijungdami prie OSRS Lietuva PvM grupės, jūs sutinkate su joje galiojančiomis taisyklėmis {}.*\n{}\n{}".format("<#{}>".format(INFORMATION2[0]) if INFORMATION2[0] != None else "",
            "*Prieš registruodamiesi, būtinai patikrinkite ar discordo botas <@{}> nėra offline.*".format(
                bot_config.CLIENT_ID),
            "*Norėdami užregistruoti savo* **RSN** *(Runescape nickname), įvekite komandą* **.rsn ir savo tikslų RSN**. *Pavyzdys apačioje.* **⤋**");

            count_content_1 = "*Uždarbis skaičiuojamas skiltyje: <#{}>.*\n{}\n{}".format(INFORMATION2[1] if INFORMATION2[1] != None else "",
            "*Uždirbtų gp suma neraidinimo ar bossinimo metu, neįskaičiuojama į nario uždarbį.*",
            "*Gautas dropas nesu Beobachter nariais, įskaičiuojamas į nario uždarbį.*");

            count_content_2 = "*Paveiksliuke turi būti atvaizduota laikas ir data.*\n{}\n{}\n{}".format(
                "*Žaidėjas turi įrašyti visų dalyvavusių žaidėjų nickus.*",
                "*Žaidėjo FFA dropas neįskaičiuojamas į statistiką.*",
                "**Pastaba!** *Napaisant šių taisyklių, moderacija nepatvirtins žaidėjo dropo rezultatų.* *Taisyklingo dropo rezultato publikavimas apačioje.* **⤋**");

            event_content = "*Prieš publikuojant eventą, būtinai patikrinkite ar discordo botas <@{}> nėra offline.*\n{}".format(
                bot_config.CLIENT_ID,
                "*Norėdami publikuoti Chambers of Xeric mass eventą, įveskite komandą* **.post** argumentą **mass** ir **papildomą informaciją**. *Pavyzdys apačioje.* **⤋**");

            beobachter_content = "*<@{}> tai specifinis discordo botas, kuris atlieka žaidėjų slapyvardžių registravimo, duomenų įrašinėjimo, statistikos saugojimo, analyzavimo bei abdorojimo funkcijas.* *Prieš naudojant komandą, būtinai patikrinkite ar discordo botas @Beobachter nėra offline.* **Pastaba!** *Žinutės išsitrina automatiškai.*".format(
                bot_config.CLIENT_ID
                );

            logo = open(bot_config.IMAGES["logo"], 'rb');
            logo2 = open(bot_config.IMAGES["logo"], 'rb');
            logo3 = open(bot_config.IMAGES["logo"], 'rb');
            logo4 = open(bot_config.IMAGES["logo"], 'rb');
            reg_example = open(bot_config.IMAGES["reg_example"], 'rb');
            zahl_example = open(bot_config.IMAGES["zahl_example"], 'rb');
            ereignisse_example = open(bot_config.IMAGES["ereignisse_example"], 'rb');
            split = open(bot_config.IMAGES["split"], 'rb');

            await registration.send(file=discord.File(logo));
            await registration.send(content="{}".format(registration_content));
            await registration.send(file=discord.File(reg_example));

            await count.send(file=discord.File(logo2));
            await count.send(content="{}".format(count_content_1));
            await count.send(file=discord.File(split));
            await count.send(content="{}".format(count_content_2));
            await count.send(file=discord.File(zahl_example));

            await event.send(file=discord.File(logo3));
            await event.send(content="{}".format(event_content));
            await event.send(file=discord.File(ereignisse_example));

            sql2 = "UPDATE {} SET {}={} WHERE {}={}".format(bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
            bot_config.MYSQL_KK["discord_ereignisse"], event.id,
            bot_config.MYSQL_KK["kanal_id"], ctx.guild.id);
            getter.setData(sql2);

            await beobachter.send(file=discord.File(logo4));
            await beobachter.send(content="{}".format(beobachter_content));

            win = discord.Embed(
                title="✙ Beobachter komandos",
                color=discord.Color.purple(),
            );

            win.set_author(name="{}".format(ctx.guild.name), icon_url=bot_config.CLIENT_ICON);
            win.set_thumbnail(url=bot_config.CLIENT_ICON);
            for index, value in enumerate(bot_config.DISCORD_COMMANDS):
                win.add_field(name=":gear: {}".format(value[0]), value=" {}".format(value[1]), inline=False);
            win.set_footer(text="✙ Beobachter {} versija.".format(bot_config.CLIENT_VERSION));

            await beobachter.send(embed=win);
        else:
            pass;

        if ctx.author.bot == True:
            pass;
        else:
            await ctx.message.delete();"""

def setup(client):
    client.add_cog(functions(client));