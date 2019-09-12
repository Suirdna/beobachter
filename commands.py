import discord
import random
import os
import locale
import collections
import asyncio
from configs import bot_config
from discord.ext import commands, tasks
from discord.utils import get
from datetime import datetime
from modules import getter
from OSRS_Hiscores import Hiscores

class commands(commands.Cog):

    # ◄███▓▒░░ SYSTEM ░░▒▓███►#

    @tasks.loop(minutes=5)
    async def on_user_reg(self):
        await asyncio.sleep(5);
        sql = "SELECT COUNT({}) FROM {}".format(bot_config.MYSQL_KMK["benutzer_name"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_mitglied_konten"]);
        data = getter.getData(sql);
        online_count = int(data[0][0]);
        try:
            await self.client.change_presence(status=discord.Status.do_not_disturb,activity=discord.Game(name="{} Nariai".format(online_count)),afk=True);
        except Exception as error:
            print(error);

    async def check_username(self,ctx,message,status):
        INFORMATION = [];
        sql = "SELECT {},{},{},{},{},{},{},{},{} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["discord_uberprufung"],
        bot_config.MYSQL_KK["emoji_attack"],
        bot_config.MYSQL_KK["emoji_strength"],
        bot_config.MYSQL_KK["emoji_defence"],
        bot_config.MYSQL_KK["emoji_magic"],
        bot_config.MYSQL_KK["emoji_range"],
        bot_config.MYSQL_KK["emoji_prayer"],
        bot_config.MYSQL_KK["emoji_herblore"],
        bot_config.MYSQL_KK["emoji_farming"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
        bot_config.MYSQL_KK["kanal_id"], ctx.guild.id
        );
        data = getter.getData(sql);

        for value in data:
            INFORMATION.append(value[0]);  # DISCORD_UBERPRUFUNG
            INFORMATION.append(value[1]);  # EMOJI_ATTACK
            INFORMATION.append(value[2]);  # EMOJI_STRENGTH
            INFORMATION.append(value[3]);  # EMOJI_DEFENCE
            INFORMATION.append(value[4]);  # EMOJI_MAGIC
            INFORMATION.append(value[5]);  # EMOJI_RANGE
            INFORMATION.append(value[6]);  # EMOJI_PRAYER
            INFORMATION.append(value[7]);  # EMOJI_HERBLORE
            INFORMATION.append(value[8]);  # EMOJI_FARMING

        USER = True;
        TEXT = "";
        textData = "";

        if status == True:
            if INFORMATION[0] != None:
                CHANNEL = self.client.get_channel(INFORMATION[0]);
                await CHANNEL.send("{}{}".format(bot_config.CHECK_MODULE["rj-check"], message));
                USERNAME = message;
        else:
            if INFORMATION[0] != None:
                CHANNEL = self.client.get_channel(INFORMATION[0]);
                await CHANNEL.send("{}{}".format(bot_config.CHECK_MODULE["rj-check"], message[:]));
                USERNAME = message[:];
        try:
            USER = Hiscores(USERNAME, 'N');
            if bot_config.STATISTIC[1]["attack"] <= int(USER.stats["attack"]["level"]) and bot_config.STATISTIC[1]["strength"] <= int(
                USER.stats["strength"]["level"]) and bot_config.STATISTIC[1]["defence"] <= int(
                USER.stats["defense"]["level"]) and bot_config.STATISTIC[1]["magic"] <= int(
                USER.stats["magic"]["level"]) and bot_config.STATISTIC[1]["range"] <= int(
                USER.stats["ranged"]["level"]) and bot_config.STATISTIC[1]["prayer"] <= int(USER.stats["prayer"]["level"]):
                TEXT = "{}".format(bot_config.GWD_POSITIV);
                if bot_config.STATISTIC[0]["attack"] <= int(USER.stats["attack"]["level"]) and bot_config.STATISTIC[0]["strength"] <= int(
                    USER.stats["strength"]["level"]) and bot_config.STATISTIC[0]["defence"] <= int(
                    USER.stats["defense"]["level"]) and bot_config.STATISTIC[0]["magic"] <= int(
                    USER.stats["magic"]["level"]) and bot_config.STATISTIC[0]["range"] <= int(
                    USER.stats["ranged"]["level"]) and bot_config.STATISTIC[0]["prayer"] <= int(
                    USER.stats["prayer"]["level"]) and bot_config.STATISTIC[0]["herblore"] <= int(
                    USER.stats["herblore"]["level"]):
                    TEXT = "{}".format(bot_config.COX_POSITIV);
                else:
                    TEXT = "{}".format(bot_config.COX_NEGATIV);
            else:
                TEXT = "{}".format(bot_config.GWD_NEGATIV);
        except Exception as ERROR:
            print(ERROR);
            USER = False;
        finally:
            pass;

        if USER != False:
            try:
                file = open("./data/{}/{}.txt".format(ctx.guild.name,"error"), "a");
                encodet = textData.encode('utf-8');
                file.write("{}\n".format(encodet));
            except Exception as error:
                print("Exception: (check_username): {}.".format(error));
            finally:
                file.close();

            win = discord.Embed(
                title="✙ Beobachter - {} statistikos patikrinimas".format(USERNAME),
                description="{}".format(TEXT),
                color=discord.Color.purple(),
            );
            win.set_author(name="✙ Beobachter - Statistika", icon_url=bot_config.CLIENT_ICON);
            win.set_thumbnail(url=bot_config.CLIENT_ICON);
            win.add_field(name="{} {}".format(INFORMATION[1] if INFORMATION[1] != None else "","Attack"),value="{}{}".format("Lygis: ",USER.stats["attack"]["level"]),inline=True);
            win.add_field(name="{} {}".format(INFORMATION[2] if INFORMATION[2] != None else "","Strength"),value="{}{}".format("Lygis: ",USER.stats["strength"]["level"]),inline=True);
            win.add_field(name="{} {}".format(INFORMATION[3] if INFORMATION[3] != None else "","Defence"),value="{}{}".format("Lygis: ",USER.stats["defense"]["level"]),inline=True);
            win.add_field(name="{} {}".format(INFORMATION[4] if INFORMATION[4] != None else "","Magic"),value="{}{}".format("Lygis: ",USER.stats["magic"]["level"]),inline=True);
            win.add_field(name="{} {}".format(INFORMATION[5] if INFORMATION[5] != None else "","Range"),value="{}{}".format("Lygis: ",USER.stats["ranged"]["level"]),inline=True);
            win.add_field(name="{} {}".format(INFORMATION[6] if INFORMATION[6] != None else "","Prayer"),value="{}{}".format("Lygis: ",USER.stats["prayer"]["level"]),inline=True);
            win.add_field(name="{} {}".format(INFORMATION[7] if INFORMATION[7] != None else "","Herblore"),value="{}{}".format("Lygis: ",USER.stats["herblore"]["level"]),inline=True);
            win.add_field(name="{} {}".format(INFORMATION[8] if INFORMATION[8] != None else "","Farming"),value="{}{}".format("Lygis: ",USER.stats["farming"]["level"]),inline=True);
            win.set_footer(text="✙ {}.".format(ctx.guild.name));

            if INFORMATION[0] != None:
                CHANNEL = self.client.get_channel(INFORMATION[0]);
                await CHANNEL.send(embed=win);
            else:
                await ctx.send("**{}** *Beobachter negali rasti check-rsn skilties.*".format(ctx.guild.name));
                await ctx.send("**{}** *Prašome sukonfigūruokite check-rsn skiltį su Beobachter botu, naudodami .setup komandą.*".format(ctx.guild.name));
        else:
            if INFORMATION[0] != None:
                CHANNEL = self.client.get_channel(INFORMATION[0]);
                await CHANNEL.send("**{}** *Toks RSN neegzistuoja, bandykite dar kartą.*".format(ctx.guild.name));
            else:
                await ctx.send("**{}** *Beobachter negali rasti check-rsn skilties.*".format(ctx.guild.name));
                await ctx.send("**{}** *Prašome sukonfigūruokite check-rsn skiltį su Beobachter botu, naudodami .setup komandą.*".format(ctx.guild.name));

    def __init__(self,client):
        self.client = client;
        self.name = bot_config.CLIENT_NAME;
        self.version = bot_config.CLIENT_VERSION;
        self.on_user_reg.start();

    # ◄███▓▒░░ ADMINISTRATION ░░▒▓███►#

    @commands.command()
    async def post(self,ctx,*,arg):
        INFORMATION = []; STRING = [];
        STRING = str(arg).split(" ");
        sql = "SELECT {},{},{},{},{},{} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["kanal_besitzer_id"],
        bot_config.MYSQL_KK["discord_mitglied"],
        bot_config.MYSQL_KK["discord_random"],
        bot_config.MYSQL_KK["discord_ereignisse"],
        bot_config.MYSQL_KK["discord_cox_beschreibung"],
        bot_config.MYSQL_KK["bot_administration_id"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
        bot_config.MYSQL_KK["kanal_id"],
        ctx.guild.id);
        data = getter.getData(sql);

        for value in data:
            INFORMATION.append(value[0]);  # KANAL_BESITZER
            INFORMATION.append(value[1]);  # DISCORD_MITGLIED
            INFORMATION.append(value[2]);  # DISCORD_RANDOM
            INFORMATION.append(value[3]);  # DISCORD_EREIGNISSE
            INFORMATION.append(value[4]);  # DISCORD_COX_BESCHREIBUNG
            INFORMATION.append(value[5]);  # BOT_ADMINISTRATION_ID

        if ctx.author.id == INFORMATION[0] or ctx.author.id == INFORMATION[5]:
            if STRING[0] == "nar":
                if INFORMATION[1] != None:
                    CHANNEL = self.client.get_channel(INFORMATION[1]);
                    await CHANNEL.send("**{}** *{}*".format(ctx.guild.name,arg[len(STRING[0])+1:]));
                else:
                    await ctx.send("**{}** *Beobachter negali rasti narių pokalbio skilties.*".format(ctx.guild.name));
                    await ctx.send("**{}** *Prašome sukonfigūruokite narių pokalbio skiltį su Beobachter botu, naudodami .setup komandą.*".format(ctx.guild.name));
            elif STRING[0] == "ran":
                if INFORMATION[2] != None:
                    CHANNEL = self.client.get_channel(INFORMATION[2]);
                    await CHANNEL.send("**{}** *{}*".format(ctx.guild.name,arg[len(STRING[0])+1:]));
                else:
                    await ctx.send("**{}** *Beobachter negali rasti narių pokalbio skilties.*".format(ctx.guild.name));
                    await ctx.send("**{}** *Prašome sukonfigūruokite narių pokalbio skiltį su Beobachter botu, naudodami .setup komandą.*".format(ctx.guild.name));
            else:
                pass;

        await ctx.message.delete();

    # ◄███▓▒░░ USER ░░▒▓███►#

    @commands.command()
    async def rsn(self,ctx,*,arg):
        INFORMATION = []; MESSAGE_SPLIT = []; MESSAGE = "";
        sql = "SELECT {},{},{},{},{},{},{},{} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["discord_registration"],
        bot_config.MYSQL_KK["discord_mitglied"],
        bot_config.MYSQL_KK["role_name_1"],
        bot_config.MYSQL_KK["discord_zahl"],
        bot_config.MYSQL_KK["discord_beschreibung"],
        bot_config.MYSQL_KK["discord_regeln"],
        bot_config.MYSQL_KK["discord_cox_beschreibung"],
        bot_config.MYSQL_KK["discord_random"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
        bot_config.MYSQL_KK["kanal_id"],
        ctx.guild.id);
        data = getter.getData(sql);

        for value in data:
            INFORMATION.append(value[0]);  # DISCORD_REGISTRATION
            INFORMATION.append(value[1]);  # DISCORD_MITGLIED
            INFORMATION.append(value[2]);  # ROLE_NAME_1
            INFORMATION.append(value[3]);  # DISCORD_ZAHL
            INFORMATION.append(value[4]);  # DISCORD_BESCHREIBUNG
            INFORMATION.append(value[5]);  # DISCORD_REGELN
            INFORMATION.append(value[6]);  # DISCORD_COX_BESCHREIBUNG
            INFORMATION.append(value[7]);  # DISCORD_RANDOM

        sql = "SELECT * FROM {} WHERE {}={} AND {}={}".format(
            bot_config.MYSQL_CONFIGURATION["mysql_kanal_mitglied_konten"],
            bot_config.MYSQL_KMK["kanal_id"], ctx.guild.id,
            bot_config.MYSQL_KMK["benutzer_id"], ctx.author.id
            );
        data = getter.getData(sql);
        if INFORMATION[0] != None:
            if ctx.channel.id == INFORMATION[0]:
                if data == []:
                    currentTime = datetime.now(); USERNAME = arg[:]; STATUS = True; USER = Hiscores(USERNAME,'N');
                    if USER.status != 404:
                        if INFORMATION[3] != None:
                            MESSAGE_SPLIT.append(" Skiltyje <#{}> rasite informaciją, kiek, kas ir ką gavo mūsų {} nariai God Wars Dungeon, Chambers of Xeric ar Theatre of Blood raido metu.".format(INFORMATION[3],ctx.guild.name));
                        if INFORMATION[4] != None:
                            MESSAGE_SPLIT.append(" <#{}> skiltyje rasite aprašymą apie mus.".format(INFORMATION[4]));
                        if INFORMATION[5] != None:
                            MESSAGE_SPLIT.append(" Kiekvienam nariui patartina pasiskaityti <#{}>".format(INFORMATION[5]));
                        if INFORMATION[6] != None:
                            MESSAGE_SPLIT.append(" Jei esate naujokas Chambers of Xeric raiduose, prašome pasiskaityti esančią informaciją skiltyje <#{}>.".format(INFORMATION[6]));

                        sql = "INSERT INTO {} ({},{},{},{},{},{},{}) VALUES ({},'{}','{}',{},'{}','{}','{}')".format(
                            bot_config.MYSQL_CONFIGURATION["mysql_kanal_mitglied_konten"],
                            bot_config.MYSQL_KMK["kanal_id"],
                            bot_config.MYSQL_KMK["kanal_name"], bot_config.MYSQL_KMK["kanal_symbol"],
                            bot_config.MYSQL_KMK["benutzer_id"], bot_config.MYSQL_KMK["benutzer_name"],
                            bot_config.MYSQL_KMK["benutzer_symbol"], bot_config.MYSQL_KMK["registration_datum"],
                            ctx.guild.id,
                            ctx.guild.name, ctx.guild.icon_url if ctx.guild.icon_url != None else ctx.guild.icon,
                            ctx.author.id, arg,
                            ctx.author.avatar_url if ctx.author.avatar_url != None else ctx.author.avatar,
                            currentTime.strftime("%d/%m/%y %H:%M:%S"));
                        getter.setData(sql);

                        for message in MESSAGE_SPLIT:
                            MESSAGE += message;

                        if INFORMATION[1] != None:
                            CHANNEL = self.client.get_channel(INFORMATION[1]);
                            await CHANNEL.send("**{}** *{}, sveiki atvykę į {} PvM grupę.{}*".format(ctx.guild.name,ctx.author.mention,ctx.guild.name,MESSAGE));
                        if INFORMATION[7] != None:
                            CHANNEL1 = self.client.get_channel(INFORMATION[7]);
                            await CHANNEL1.send("**{}** *Žaidėjas {} prisijungė prie PvM grupės. PvM registracija vyksta <#{}> skiltyje.*".format(ctx.guild.name,ctx.author.mention,INFORMATION[0]));

                        role = get(ctx.guild.roles,name=INFORMATION[2]);
                        await discord.Member.edit(ctx.author,reason="Nickname registration",nick="{}".format(USERNAME));
                        await ctx.author.add_roles(ctx.author,role,reason="Rsn registracija",atomic=False);

                        try:
                            printText = "Record: {} - Server: {} - Action: {} - User: {} - Uerd ID: {} - Nickname: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), ctx.guild.name,bot_config.CLIENT_MESSAGES["on_command_rsn_succ"], ctx.author.name, ctx.author.id, arg);
                            textData = "Record: {} - Server: {} - Action: {} - User: {} - Uerd ID: {} - Nickname: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), ctx.guild.name,bot_config.CLIENT_MESSAGES["on_command_rsn_succ"], ctx.author.name, ctx.author.id, arg);
                            print(printText);
                            if os.path.exists("./data/{}".format(ctx.guild)):
                                file = open("./data/{}/{}.txt".format(ctx.guild,"member_reg_succ"), "a");
                                encodet = textData.encode('utf-8');
                                file.write("{}\n".format(encodet));
                            else:
                                os.mkdir("./data/{}".format(ctx.guild));
                                file = open("./data/{}/{}.txt".format(ctx.guild,"member_reg_succ"), "a");
                                encodet = textData.encode('utf-8');
                                file.write("{}\n".format(encodet));
                        except Exception as error:
                            print("Exception: (on_command_reg/member_reg_succ): {}.".format(error));
                        finally:
                            file.close();

                        await self.check_username(ctx,arg[:],True);
                        await ctx.message.delete();
                    else:
                        user = self.client.get_user(ctx.author.id);
                        await ctx.message.delete();
                        await user.send("**{}** *Jūs bandėte užregistruoti {} RSN.*".format(ctx.guild.name,arg));
                        await user.send("**{}** *Toks RSN neegzistuoja, įsitikinkite, kad RSN rašote tiksliai ir bandykite dar kartą.*".format(ctx.guild.name));
                else:
                    sql = "SELECT {},{} FROM {} WHERE ę{}={} AND {}={}".format(
                        bot_config.MYSQL_KMK["benutzer_id"], bot_config.MYSQL_KMK["benutzer_name"],
                        bot_config.MYSQL_CONFIGURATION["mysql_kanal_mitglied_konten"],
                        bot_config.MYSQL_KMK["benutzer_id"], ctx.author.id,
                        bot_config.MYSQL_KMK["kanal_id"], ctx.guild.id,
                        );
                    data2 = getter.getData(sql);

                    if data2 != []:
                        currentTime = datetime.now(); USERNAME = arg[:]; STATUS = True; USER = Hiscores(USERNAME, 'N');
                        if USER.status != 404:
                            if INFORMATION[3] != None:
                                MESSAGE_SPLIT.append(" Skiltyje <#{}> rasite informaciją, kiek, kas ir ką gavo mūsų {} nariai God Wars Dungeon, Chambers of Xeric ar Theatre of Blood raido metu.".format(INFORMATION[3], ctx.guild.name));
                            if INFORMATION[4] != None:
                                MESSAGE_SPLIT.append(" <#{}> skiltyje rasite aprašymą apie mus.".format(INFORMATION[4]));
                            if INFORMATION[5] != None:
                                MESSAGE_SPLIT.append(" Kiekvienam nariui patartina pasiskaityti <#{}>".format(INFORMATION[5]));
                            if INFORMATION[6] != None:
                                MESSAGE_SPLIT.append(" Jei esate naujokas Chambers of Xeric raiduose, prašome pasiskaityti esančią informaciją skiltyje <#{}>.".format(INFORMATION[6]));

                            for message in MESSAGE_SPLIT:
                                MESSAGE += message;

                            if INFORMATION[1] != None:
                                CHANNEL = self.client.get_channel(INFORMATION[1]);
                                await CHANNEL.send("**{}** *{}, sveiki sugrįžę į {} PvM grupę. {}*".format(ctx.guild.name,ctx.author.mention,ctx.guild.name,MESSAGE));
                            if INFORMATION[7] != None:
                                CHANNEL1 = self.client.get_channel(INFORMATION[7]);
                                await CHANNEL1.send("**{}** *Žaidėjas {} sugrįžo prie PvM grupės. PvM registracija vyksta <#{}> skiltyje.*".format(ctx.guild.name,ctx.author.mention,INFORMATION[0]));

                            sql = "UPDATE {} SET {}='{}',{}='{}',{}='{}',{}='{}',{}='{}' WHERE {}={} AND {}={}".format(
                            bot_config.MYSQL_CONFIGURATION["mysql_kanal_mitglied_konten"],
                            bot_config.MYSQL_KMK["kanal_name"],ctx.guild.name,
                            bot_config.MYSQL_KMK["kanal_symbol"],ctx.guild.icon_url if ctx.guild.icon_url != None else ctx.guild.icon,
                            bot_config.MYSQL_KMK["benutzer_name"],arg,
                            bot_config.MYSQL_KMK["benutzer_symbol"],ctx.author.avatar_url if ctx.author.avatar_url != None else ctx.author.avatar,
                            bot_config.MYSQL_KMK["registration_datum"],currentTime.strftime("%d/%m/%y %H:%M:%S"),
                            bot_config.MYSQL_KMK["kanal_id"],ctx.guild.id,
                            bot_config.MYSQL_KMK["benutzer_id"],ctx.author.id
                            );
                            getter.setData(sql);

                            role = get(ctx.guild.roles, name=INFORMATION[2]);
                            await discord.Member.edit(ctx.author, reason="Nickname registration",nick="{}".format(USERNAME));
                            await ctx.author.add_roles(ctx.author, role, reason="Rsn registracija", atomic=False);

                            try:
                                printText = "Record: {} - Server: {} - Action: {} - User: {} - Uerd ID: {} - Nickname: {}".format(
                                    currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), ctx.guild.name,
                                    bot_config.CLIENT_MESSAGES["on_command_rsn_succ"], ctx.author.name,
                                    ctx.author.id, arg);
                                textData = "Record: {} - Server: {} - Action: {} - User: {} - Uerd ID: {} - Nickname: {}".format(
                                    currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), ctx.guild.name,
                                    bot_config.CLIENT_MESSAGES["on_command_rsn_succ"], ctx.author.name,
                                    ctx.author.id, arg);
                                print(printText);
                                if os.path.exists("./data/{}".format(ctx.guild)):
                                    file = open("./data/{}/{}.txt".format(ctx.guild, "member_reg_succ"), "a");
                                    encodet = textData.encode('utf-8');
                                    file.write("{}\n".format(encodet));
                                else:
                                    os.mkdir("./data/{}".format(ctx.guild));
                                    file = open("./data/{}/{}.txt".format(ctx.guild, "member_reg_succ"), "a");
                                    encodet = textData.encode('utf-8');
                                    file.write("{}\n".format(encodet));
                            except Exception as error:
                                print("Exception: (on_command_reg/member_reg_succ): {}.".format(error));
                            finally:
                                file.close();

                            await self.check_username(ctx, arg[:], True);
                            await ctx.message.delete();
                        else:
                            user = self.client.get_user(ctx.author.id);
                            await ctx.message.delete();
                            await user.send("**{}** *Jūs bandėte užregistruoti {} RSN.*".format(ctx.guild.name, arg));
                            await user.send("**{}** *Toks RSN neegzistuoja, įsitikinkite, kad RSN rašote tiksliai ir bandykite dar kartą.*".format(ctx.guild.name));
        else:
            await ctx.send("**{}** *Beobachter negali rasti registracijos skilties.*".format(ctx.guild.name));
            await ctx.send("**{}** *Prašome sukonfigūruokite registracijos skiltį su Beobachter botu, naudodami .setup komandą.*".format(ctx.guild.name));

    @commands.command()
    async def reg(self,ctx,*,arg):
        INFORMATION = [];
        sql = "SELECT {} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["discord_beobachter"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
        bot_config.MYSQL_KK["kanal_id"], ctx.guild.id);
        data = getter.getData(sql);

        for value in data:
            INFORMATION.append(value[0]);  # DISCORD_BEOBACHTER

        if INFORMATION[0] != None:
            if ctx.channel.id == INFORMATION[0]:
                USERNAME = arg;
                CHANNEL = self.client.get_channel(INFORMATION[0]);
                USER = Hiscores(USERNAME, 'N');
                if USER.status != 404:
                    sql1 = "SELECT {} FROM {} WHERE {}={} AND {}='{}'".format(bot_config.MYSQL_KMK["benutzer_name"],
                    bot_config.MYSQL_CONFIGURATION["mysql_kanal_mitglied_konten"],
                    bot_config.MYSQL_KMK["kanal_id"], ctx.guild.id,
                    bot_config.MYSQL_KMK["benutzer_name"], arg);
                    data1 = getter.getData(sql1);
                    if data1 == []:
                        sql2 = "UPDATE {} SET {}='{}' WHERE {}={} AND {}={}".format(
                            bot_config.MYSQL_CONFIGURATION["mysql_kanal_mitglied_konten"],
                            bot_config.MYSQL_KMK["benutzer_name"], USERNAME,
                            bot_config.MYSQL_KMK["kanal_id"], ctx.guild.id,
                            bot_config.MYSQL_KMK["benutzer_id"], ctx.author.id
                            );
                        data2 = getter.setData(sql2);
                        await discord.Member.edit(ctx.author,reason="Nickname registration",nick="{}".format(USERNAME));
                        await self.check_username(ctx,arg,True);
                    else:
                        user = self.client.get_user(ctx.author.id);
                        await user.send("**{}** *Jūs bandėte užregistruoti {} RSN.*".format(ctx.guild.name,arg));
                        await user.send("**{}** *Toks RSN jau yra užregistruotas {} PvM grupėje. Dėl iškilusių nesklandumų prašome kreiptis pas {}.*".format(ctx.guild.name,ctx.guild.name,ctx.guild.owner.mention));
                else:
                    user = self.client.get_user(ctx.author.id);
                    await user.send("**{}** *Jūs bandėte užregistruoti {} RSN.*".format(ctx.guild.name,arg));
                    await user.send("**{}** *Toks RSN neegzistuoja, įsitikinkite, kad RSN rašote tiksliai ir bandykite dar kartą.*".format(ctx.guild.name));
            else:
                await ctx.send("**{}** *Šią komandą galima naudoti tik <#{}> skiltyje.*".format(ctx.guild.name,INFORMATION[0]));
        else:
            await ctx.send("**{}** *Beobachter negali rasti Beobachter valdymo pulto skilties.*".format(ctx.guild.name));
            await ctx.send("**{}** *Prašome sukonfigūruokite Beobachter valdymo pulto skiltį su Beobachter botu, naudodami .setup komandą.*".format(ctx.guild.name));

    @commands.command()
    async def tob(self,ctx,arg):
        INFORMATION = [];
        sql = "SELECT {} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["discord_beobachter"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
        bot_config.MYSQL_KK["kanal_id"], ctx.guild.id);
        data = getter.getData(sql);

        for value in data:
            INFORMATION.append(value[0]);  # DISCORD_BEOBACHTER

        if INFORMATION[0] != None:
            if ctx.channel.id == INFORMATION[0]:
                sql = "SELECT {} FROM {} WHERE {}={} AND {}={}".format(bot_config.MYSQL_KMK["benutzer_name"],
                bot_config.MYSQL_CONFIGURATION["mysql_kanal_mitglied_konten"],
                bot_config.MYSQL_KMK["kanal_id"], ctx.guild.id,
                bot_config.MYSQL_KMK["benutzer_id"], ctx.author.id);
                data = getter.getData(sql);

                for value in data:
                    INFORMATION.append(value[0]);
                COUNT = arg;
                try:
                    COUNT = int(COUNT);
                    await discord.Member.edit(ctx.author,reason="Cox kc registracija",nick="☠ {} - {}".format(INFORMATION[1],COUNT));
                except Exception as error:
                    print("Exception: (on_command_tob/not_int_type): {}.".format(error));
            else:
                await ctx.send("**{}** *Šią komandą galima naudoti tik <#{}> skiltyje.*".format(ctx.guild.name,INFORMATION[0]));
        else:
            await ctx.send("**{}** *Beobachter negali rasti Beobachter valdymo pulto skilties.*".format(ctx.guild.name));
            await ctx.send("**{}** *Prašome sukonfigūruokite Beobachter valdymo pulto skiltį su Beobachter botu, naudodami .setup komandą.*".format(ctx.guild.name));

    @commands.command()
    async def cox(self,ctx,arg):
        INFORMATION = [];
        sql = "SELECT {} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["discord_beobachter"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
        bot_config.MYSQL_KK["kanal_id"], ctx.guild.id);
        data = getter.getData(sql);

        for value in data:
            INFORMATION.append(value[0]);  # DISCORD_BEOBACHTER

        if INFORMATION[0] != None:
            if ctx.channel.id == INFORMATION[0]:
                sql = "SELECT {} FROM {} WHERE {}={} AND {}={}".format(bot_config.MYSQL_KMK["benutzer_name"],
                bot_config.MYSQL_CONFIGURATION["mysql_kanal_mitglied_konten"],
                bot_config.MYSQL_KMK["kanal_id"], ctx.guild.id,
                bot_config.MYSQL_KMK["benutzer_id"], ctx.author.id);
                data = getter.getData(sql);

                for value in data:
                    INFORMATION.append(value[0]);
                COUNT = arg;
                try:
                    COUNT = int(COUNT);
                    await discord.Member.edit(ctx.author,reason="Cox kc registracija",nick="⚔ {} - {}".format(INFORMATION[1],COUNT));
                except Exception as error:
                    print("Exception: (on_command_cox/not_int_type): {}.".format(error));
            else:
                await ctx.send("**{}** *Šią komandą galima naudoti tik <#{}> skiltyje.*".format(ctx.guild.name,INFORMATION[0]));
        else:
            await ctx.send("**{}** *Beobachter negali rasti Beobachter valdymo pulto skilties.*".format(ctx.guild.name));
            await ctx.send("**{}** *Prašome sukonfigūruokite Beobachter valdymo pulto skiltį su Beobachter botu, naudodami .setup komandą.*".format(ctx.guild.name));

    @commands.command()
    async def gstats(self,ctx):
        INFORMATION = [];
        count = 0; gp = 0;
        statistic = {};
        locale.setlocale(locale.LC_ALL,'german');

        sql1 = "SELECT * FROM {}".format(bot_config.MYSQL_CONFIGURATION["mysql_allgemein_statistik"]);
        myresult = getter.getData(sql1)

        sql2 = "SELECT {} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["emoji_gp"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
        bot_config.MYSQL_KK["kanal_id"], ctx.guild.id);
        data = getter.getData(sql2)

        for value in data:
            INFORMATION.append(value[0]);  # EMOJI_GP

        for index,result in enumerate(myresult):
            if result[4] != "random":
                gp += result[6];
                statistic[result[6]] = "{} **{}**".format(result[2],result[4]);

        procesed = collections.OrderedDict(sorted(statistic.items(), reverse=True))
        stats = discord.Embed(
            title="✙ Beobachter - Globali statistika",
            description="Statistika abdorojama {} svetainėje. Bendras uždarbis {} **{}**.".format(
                bot_config.CLIENT_WEBSITE, INFORMATION[0] if INFORMATION[0] != None else "💰", locale.format_string("%d", gp, grouping=True)),
            color=discord.Color.purple(),
        );

        stats.set_author(name="Beobachter statistika", icon_url=bot_config.CLIENT_ICON);
        stats.set_thumbnail(url=bot_config.CLIENT_ICON);
        for sum,id in procesed.items():
            if count != 10:
                stats.add_field(name="{}".format(bot_config.WORDS[count]), value="{} **-**{} *{}*.".format(id, INFORMATION[0] if INFORMATION[0] != None else "💰", locale.format_string("%d", sum, grouping=True)), inline=False);
                count += 1;
            else:
                pass;

        stats.add_field(name="Statistika", value="Daugiau informacijos rasite {} puslapyje.".format(
            bot_config.CLIENT_WEBSITE), inline=False);
        stats.set_footer(text="✙ Beobachter {} versija.".format(bot_config.CLIENT_VERSION));
        await ctx.send(embed=stats);

    @commands.command()
    async def stats(self,ctx):
        INFORMATION = [];
        count = 0; gp = 0;
        statistic = {};
        locale.setlocale(locale.LC_ALL,'german');

        sql1 = "SELECT * FROM {}".format(bot_config.MYSQL_CONFIGURATION["mysql_allgemein_statistik"]);
        myresult = getter.getData(sql1)

        sql2 = "SELECT {},{} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["discord_zahl"],
        bot_config.MYSQL_KK["emoji_gp"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
        bot_config.MYSQL_KK["kanal_id"], ctx.guild.id);
        data = getter.getData(sql2)

        for value in data:
            INFORMATION.append(value[0]);  # DISCORD_ZAHL
            INFORMATION.append(value[1]);  # EMOJI_GP

        if INFORMATION[0] != None:
            for index,result in enumerate(myresult):
                if result[1] == ctx.guild.id and result[4] != "random":
                    gp += result[6];
                    statistic[result[6]] = "**{}**".format(result[4]);

            procesed = collections.OrderedDict(sorted(statistic.items(), reverse=True))
            stats = discord.Embed(
                title="✙ Beobachter - {} statistika".format(ctx.guild.name),
                description="Statistika abdorojama ir analizuojama skiltyje <#{}>. Bendras grupės uždarbis {} **{}**.".format(INFORMATION[0],INFORMATION[1] if INFORMATION[1] != None else "💰", locale.format_string("%d", gp, grouping=True)),
                color=discord.Color.purple(),
            );

            stats.set_author(name="Beobachter Statistika", icon_url=bot_config.CLIENT_ICON);
            stats.set_thumbnail(url=bot_config.CLIENT_ICON);
            for sum,id in procesed.items():
                if count != 10:
                    stats.add_field(name="{}".format(bot_config.WORDS[count]), value="{} **-**{} *{}*.".format(id, INFORMATION[1] if INFORMATION[1] != None else "💰", locale.format_string("%d", sum, grouping=True)), inline=False);
                    count += 1;
                else:
                    pass;

            stats.add_field(name="Statistika", value="Daugiau informacijos rasite {} puslapyje.".format(
                bot_config.CLIENT_WEBSITE), inline=False);
            stats.set_footer(text="✙ Beobachter {} versija.".format(bot_config.CLIENT_VERSION));
            await ctx.send(embed=stats);
        else:
            await ctx.send("**{}** *Beobachter negali rasti uždarbio skilties.*".format(ctx.guild.name));
            await ctx.send("**{}** *Prašome sukonfigūruokite uždarbio skiltį su Beobachter botu, naudodami .setup komandą.*".format(ctx.guild.name));

    @commands.command()
    async def grank(self,ctx):
        INFORMATION = [];
        locale.setlocale(locale.LC_ALL,"german");
        STATUS = False;

        sql = "SELECT {},{},{} FROM {} ORDER BY {} DESC".format(bot_config.MYSQL_AS["benutzer_id"],
        bot_config.MYSQL_AS["benutzer_name"],
        bot_config.MYSQL_AS["zahl"], bot_config.MYSQL_CONFIGURATION["mysql_allgemein_statistik"],
        bot_config.MYSQL_AS["zahl"]);
        data = getter.getData(sql);

        for index, item in enumerate(data):
            if item[0] == ctx.author.id:
                win = discord.Embed(
                    description="✙ Daugiau informacijos {} puslapyje.".format(bot_config.CLIENT_WEBSITE),
                    color=discord.Color.purple(),
                );
                win.set_author(name="{}".format("✙ Beobachter - Global rangai"), icon_url=bot_config.CLIENT_ICON);
                win.add_field(name="```Mano RSN: {}```".format(item[1]),value="`Mano rangas: 👑 《 {} 》\n Uždirbau: ✨ 《 {} 》 m.`".format(index + 1,locale.format_string("%d",item[2],grouping=True)),inline=True);
                win.set_image(url=bot_config.DISCORD_RANK_IMAGES[random.randint(0, len(
                    bot_config.DISCORD_RANK_IMAGES) - 1)]);
                win.set_footer(text="✙ Beobachter {} versija.".format(bot_config.CLIENT_VERSION));
                STATUS = True;
                await ctx.send(embed=win);
            else:
                pass;

        if STATUS == False:
            sql = "SELECT {} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["discord_registration"],
            bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
            bot_config.MYSQL_KK["kanal_id"], ctx.guild.id);
            data = getter.getData(sql);

            for value in data:
                if value[0] != None:
                    await ctx.send("**{}** *Nėra splito? Nėra rango! Registruokis <#{}>.*".format(ctx.guild.name, value[0]));
                else:
                    await ctx.send("**{}** *Beobachter negali rasti registracijos skilties.*".format(ctx.guild.name));
                    await ctx.send("**{}** *Prašome sukonfigūruokite registracijos skiltį su Beobachter botu, naudodami .setup komandą.*".format(ctx.guild.name));

    @commands.command()
    async def rank(self,ctx):
        INFORMATION = [];
        locale.setlocale(locale.LC_ALL,"german");
        STATUS = False;

        sql = "SELECT {},{},{},{} FROM {} WHERE {}={} ORDER BY {} DESC".format(bot_config.MYSQL_AS["benutzer_id"], bot_config.MYSQL_AS["benutzer_name"],
        bot_config.MYSQL_AS["zahl"],
        bot_config.MYSQL_AS["kanal_id"],
        bot_config.MYSQL_CONFIGURATION["mysql_allgemein_statistik"],
        bot_config.MYSQL_AS["kanal_id"], ctx.guild.id,
        bot_config.MYSQL_AS["zahl"]
        );
        data = getter.getData(sql);

        for index, item in enumerate(data):
            if item[0] == ctx.author.id:
                win = discord.Embed(
                    description="✙ Daugiau informacijos {} puslapyje.".format(bot_config.CLIENT_WEBSITE),
                    color=discord.Color.purple(),
                );
                win.set_author(name="{}".format("✙ Beobachter - Rangai"), icon_url=bot_config.CLIENT_ICON);
                win.add_field(name="```Mano RSN: {}```".format(item[1]),value="`Mano rangas: 👑 《 {} 》\n Uždirbau: ✨ 《 {} 》 m.`".format(index + 1,locale.format_string("%d",item[2],grouping=True)),inline=True);
                win.set_image(url=bot_config.DISCORD_RANK_IMAGES[random.randint(0, len(
                    bot_config.DISCORD_RANK_IMAGES) - 1)]);
                win.set_footer(text="✙ Beobachter {} versija.".format(bot_config.CLIENT_VERSION));
                STATUS = True;
                await ctx.send(embed=win);
            else:
                pass;

        if STATUS == False:
            sql = "SELECT {} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["discord_registration"],
            bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
            bot_config.MYSQL_KK["kanal_id"], ctx.guild.id);
            data = getter.getData(sql);

            for value in data:
                if value[0] != None:
                    await ctx.send("**{}** *Nėra splito? Nėra rango! Registruokis <#{}>.*".format(ctx.guild.name, value[0]));
                else:
                    await ctx.send("**{}** *Beobachter negali rasti registracijos skilties.*".format(ctx.guild.name));
                    await ctx.send("**{}** *Prašome sukonfigūruokite registracijos skiltį su Beobachter botu, naudodami .setup komandą.*".format(ctx.guild.name));

    @commands.command()
    async def beobachter(self,ctx):
        INFORMATION = [];
        sql = "SELECT {},{},{} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["discord_beobachter"],
        bot_config.MYSQL_KK["kanal_besitzer_id"],
        bot_config.MYSQL_KK["bot_administration_id"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
        bot_config.MYSQL_KK["kanal_id"], ctx.guild.id
        );
        data = getter.getData(sql);

        for value in data:
            INFORMATION.append(value[0]);  # DISCORD_BEOBACHTER
            INFORMATION.append(value[1]);  # KANAL_BESITZER_ID
            INFORMATION.append(value[2]);  # BOT_ADMINISTRATION_ID

        if INFORMATION[0] != None:
            if ctx.author.id == INFORMATION[1] or ctx.author.id == INFORMATION[2] or ctx.author.id == bot_config.CLIENT_ID:
                CHANNEL = self.client.get_channel(INFORMATION[0]);
                win = discord.Embed(
                    title="✙ Beobachter komandos",
                    color=discord.Color.purple(),
                );

                win.set_author(name="{}".format(ctx.guild.name), icon_url=bot_config.CLIENT_ICON);
                win.set_thumbnail(url=bot_config.CLIENT_ICON);
                for index,value in enumerate(bot_config.DISCORD_COMMANDS):
                    win.add_field(name=":gear: {}".format(value[0]),value=" {}".format(value[1]), inline=False);
                win.set_footer(text="✙ Beobachter {} versija.".format(bot_config.CLIENT_VERSION));
                await CHANNEL.send(embed=win);
            else:
                await ctx.send("**{}** *Jūs ne esate kanalo savininkas.*".format(ctx.guild.name));
        else:
            await ctx.send("**{}** *Beobachter negali rasti beobachter skilties.*".format(ctx.guild.name));
            await ctx.send("**{}** *Prašome sukonfigūruokite beobachter skiltį su Beobachter botu, naudodami .setup komandą.*".format(ctx.guild.name));

    @commands.command()
    async def check(self,ctx,*,arg):
        await self.check_username(ctx,arg,False);

    @commands.command()
    async def dcn(self,ctx,*,arg):
        user_id = str(arg);
        user_id = user_id.replace("<","");
        user_id = user_id.replace(">","");
        user_id = user_id.replace("@","");
        user_id = user_id.replace("!","");

        user = ctx.guild.get_member(int(user_id));
        await ctx.send("**{}** *Žaidėjas {} prisijungė prie discordo* **{}**.".format(ctx.guild.name,user.mention,user.joined_at.strftime("%d/%m/%y  %H:%M:%S")));

    @commands.command()
    async def connect(self,ctx):
        INFORMATION = [];
        user = self.client.get_user(ctx.author.id);
        sql1 = "SELECT {},{} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["role_name_global"],
        bot_config.MYSQL_KK["discord_registration"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
        bot_config.MYSQL_KK["kanal_id"], ctx.guild.id);
        data = getter.getData(sql1);
        for value in data:
            INFORMATION.append(value[0]);
            INFORMATION.append(value[1]);

        sql2 = "SELECT {},{} FROM {} WHERE {}={} AND {}={}".format(bot_config.MYSQL_KMK["benutzer_id"],
        bot_config.MYSQL_KMK["global_ban_status"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_mitglied_konten"],
        bot_config.MYSQL_KMK["kanal_id"],ctx.guild.id,
        bot_config.MYSQL_KMK["benutzer_id"],ctx.author.id);
        data = getter.getData(sql2);
        for value in data:
            INFORMATION.append(value[0]);
            INFORMATION.append(value[1]);

        if len(INFORMATION) == 4:
            if ctx.author.id == INFORMATION[2]:
                if INFORMATION[3] != bot_config.GLOBAL_BAN_STATUS:
                    sql3 = "UPDATE {} SET {}={} WHERE {}={}".format(
                        bot_config.MYSQL_CONFIGURATION["mysql_kanal_mitglied_konten"],
                        bot_config.MYSQL_KMK["global_status"],
                        bot_config.GLOBAL_ACTIVE, bot_config.MYSQL_KMK["benutzer_id"], ctx.author.id);
                    getter.setData(sql3);

                    role = get(ctx.guild.roles,name=INFORMATION[0]);
                    await ctx.author.add_roles(role,reason="Beobachter Global-Connect",atomic=True)
                    await user.send("**{}** *Žaidėjas {} prisijungė prie Beobachter-Global pokalbio kanalo.*".format(ctx.guild.name,ctx.author.mention));
                else:
                    await user.send("**{}** *Jūs esate užbanintas Beobachter-Global pokalbio kanale.*".format(ctx.guild.name));
            else:
                await user.send("**{}** *Jūs neturite leidimo prisijungti prie Beobachter-Global pokalbio kanalo. Prašome užsiregistruoti prie Beobachter sistemos <#{}>.*".format(ctx.guild.name,INFORMATION[1]));
        else:
            await user.send("**{}** *{} prašome prisiregistruoti prie Beobachter sistemos <#{}> ir bandykite dar kartą.*".format(ctx.guild.name,ctx.author.mention,INFORMATION[1]));

    @commands.command()
    async def disconnect(self,ctx):
        INFORMATION = [];
        user = self.client.get_user(ctx.author.id);
        sql1 = "SELECT {},{} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["role_name_global"],
        bot_config.MYSQL_KK["discord_registration"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
        bot_config.MYSQL_KK["kanal_id"], ctx.guild.id);
        data = getter.getData(sql1);
        for value in data:
            INFORMATION.append(value[0]);
            INFORMATION.append(value[1]);

        sql2 = "SELECT {},{} FROM {} WHERE {}={} AND {}={}".format(bot_config.MYSQL_KMK["benutzer_id"],
        bot_config.MYSQL_KMK["global_status"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_mitglied_konten"],
        bot_config.MYSQL_KMK["kanal_id"],ctx.guild.id,
        bot_config.MYSQL_KMK["benutzer_id"],ctx.author.id);
        data = getter.getData(sql2);
        for value in data:
            INFORMATION.append(value[0]);
            INFORMATION.append(value[1]);

        if len(INFORMATION) == 4:
            if INFORMATION[3] == bot_config.GLOBAL_ACTIVE:
                if ctx.author.id == INFORMATION[2]:
                    sql3 = "UPDATE {} SET {}={} WHERE {}={} AND {}={}".format(
                        bot_config.MYSQL_CONFIGURATION["mysql_kanal_mitglied_konten"],
                        bot_config.MYSQL_KMK["global_status"],
                        bot_config.GLOBAL_DISABLE, bot_config.MYSQL_KMK["kanal_id"], ctx.guild.id,
                        bot_config.MYSQL_KMK["benutzer_id"], ctx.author.id);
                    getter.setData(sql3);

                    role = get(ctx.guild.roles,name=INFORMATION[0]);
                    await ctx.author.remove_roles(role,reason="Beobachter Global-Disconnect",atomic=True)
                    await ctx.send("**{}** *Žaidėjas {} atsijungė nuo Beobachter-Global pokalbio kanalo.*".format(ctx.guild.name,ctx.author.mention));
                else:
                    await user.send("**{}** *Jūs neturite leidimo atsijungti nuo Beobachter-Global pokalbio kanalo. Prašome užsiregistruoti prie Beobachter sistemos <#{}>.*".format(ctx.guild.name, INFORMATION[1]));
            else:
                await user.send("**{}** *Jūs neesate prisijungę prie Beobachter-Global pokalbio kanalo.*".format(ctx.guild.name,));
        else:
            await user.send("**{}** *{} prašome prisiregistruoti prie Beobachter sistemos <#{}> ir bandykite dar kartą.*".format(ctx.guild.name,ctx.author.mention,INFORMATION[1]));

def setup(client):
    client.add_cog(commands(client));