import discord
import os
from configs import bot_config
from discord.ext import commands
from datetime import datetime
from modules import getter


class core(commands.Cog):

    # ◄███▓▒░░ SYSTEM ░░▒▓███►#

    def __init__(self,client):
        self.client = client;
        self.name = bot_config.CLIENT_NAME;
        self.version = bot_config.CLIENT_VERSION;

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.guild != None:
            INFORMATION = [];
            currentTime = datetime.now();

            sql = "SELECT {},{},{},{},{},{} FROM {} WHERE {}={}".format(
            bot_config.MYSQL_KK["bot_id"],bot_config.MYSQL_KK["discord_zahl"],
            bot_config.MYSQL_KK["discord_ereignisse"],bot_config.MYSQL_KK["discord_beobachter"],
            bot_config.MYSQL_KK["discord_moderation"],bot_config.MYSQL_KK["discord_global"],
            bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],bot_config.MYSQL_KK["kanal_id"],
            message.guild.id);
            data = getter.getData(sql);

            for value in data:
                INFORMATION.append(value[0]);  # BOT_ID
                INFORMATION.append(value[1]);  # DISCORD_ZAHL
                INFORMATION.append(value[2]);  # DISCORD_EREIGNISSE
                INFORMATION.append(value[3]);  # DISCORD_BEOBACHTER
                INFORMATION.append(value[4]);  # DISCORD_MODERATION
                INFORMATION.append(value[5]);  # DISCORD_GLOBAL

            if len(INFORMATION) != 0:
                if INFORMATION[0] != None and INFORMATION[2] != None and message.channel.id == INFORMATION[2]:  # DISCORD_EREIGNISSE
                    if message.author.id == INFORMATION[0]:    # BOT_ID
                        await message.add_reaction(bot_config.DISCORD_EMOJIS["positiv"]);

                if INFORMATION[3] != None and message.channel.id == INFORMATION[3]:  # DISCORD_BEOBACHTER
                    if message.author.bot:
                        pass;
                    else:
                        await message.delete();

                if INFORMATION[1] != None and message.channel.id == INFORMATION[1]:
                    INFORMATION = [];
                    sql = "SELECT {},{} FROM {}".format(bot_config.MYSQL_MOD["kanal_id"],
                    bot_config.MYSQL_MOD["discord_mod"],
                    bot_config.MYSQL_CONFIGURATION["mysql_kanal_mod"]);
                    data = getter.getData(sql);

                    if message.author.bot != True:
                        await message.add_reaction(bot_config.DISCORD_EMOJIS["positiv"]);

                    for value in data:
                        INFORMATION.append(value[0]);
                        INFORMATION.append(value[1]);

                    if data != []:
                        GLOBAL_KANAL = self.client.get_guild(INFORMATION[0]);
                        GLOBAL_CHANNEL = GLOBAL_KANAL.get_channel(INFORMATION[1]);
                        if message.attachments != []:
                            win = discord.Embed(
                                title="✙ Beobachter - valdymo pultas".format(message.author.mention),
                                description="✙ {} laukia {}.".format(message.author.mention, "dropo patvirtinimo"),
                                color=discord.Color.purple(),
                            );
                            win.set_author(name="{}".format(message.guild.name),icon_url=bot_config.DISCORD_MODULE_IMAGES["gp"]);
                            win.set_thumbnail(url="https://cdn.discordapp.com/attachments/594153281169653760/595574430948655117/gp.png");
                            win.add_field(name="Patvirtinkite žaidėjus",value="**Kontentas:** *{}* **✉** *{}*.".format(message.author.mention,message.content),inline=True);
                            win.add_field(name="Papildoma informacija",value="`Kanalo pavadinimas: {}`\n`Kanalo id: {}`\n`Žinutės id: {}`\n`Žinutės nuoroda:` {}".format(message.author.guild,message.author.guild.id,message.id,message.jump_url),inline=True);
                            win.set_image(url=message.attachments[0].url);
                            win.set_footer(text="✙ Beobachter {} versija.".format(bot_config.CLIENT_VERSION));
                            await GLOBAL_CHANNEL.send(embed=win);
                        else:
                            if not message.author.bot:
                                win = discord.Embed(
                                    title="✙ Beobachter - valdymo pultas".format(message.author.mention),
                                    description="✙ {} laukia {}.".format(message.author.mention, "dropo patvirtinimo"),
                                    color=discord.Color.purple(),
                                );
                                win.set_author(name="{}".format(message.guild.name), icon_url=bot_config.DISCORD_MODULE_IMAGES["gp"]);
                                win.set_thumbnail(url="https://cdn.discordapp.com/attachments/594153281169653760/595574430948655117/gp.png");
                                win.add_field(name="Patvirtinkite žaidėjus",value="**Kontentas:** *{}* **✉** *{}*.".format(message.author.mention,message.content),inline=True);
                                win.add_field(name="Papildoma informacija",value="`Kanalo pavadinimas: {}`\n`Kanalo id: {}`\n`Žinutės id: {}`\n`Žinutės nuoroda:` {}".format(
                                message.author.guild,message.author.guild.id,message.id,message.jump_url
                                ), inline=True);
                                win.set_footer(text="✙ Beobachter {} versija.".format(bot_config.CLIENT_VERSION));
                                await GLOBAL_CHANNEL.send(embed=win);
                            else:
                                pass;

                if len(INFORMATION) == 6:
                    if INFORMATION[5] != None and message.channel.id == INFORMATION[5]:
                        KANAL = []; DISCORD_GLOBAL = []; USER = [];
                        sql = "SELECT {},{} FROM {}".format(bot_config.MYSQL_KK["kanal_id"],
                        bot_config.MYSQL_KK["discord_global"],
                        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"]);
                        data = getter.getData(sql);

                        sql2 = "SELECT {},{} FROM {} WHERE {}={} AND {}={}".format(
                        bot_config.MYSQL_KMK["global_status"], bot_config.MYSQL_KMK["global_ban_status"],
                        bot_config.MYSQL_CONFIGURATION["mysql_kanal_mitglied_konten"],
                        bot_config.MYSQL_KMK["kanal_id"],message.guild.id,
                        bot_config.MYSQL_KMK["benutzer_id"],message.author.id);
                        data2 = getter.getData(sql2);

                        for value in data:
                            KANAL.append(value[0]);         # KANAL_ID
                            DISCORD_GLOBAL.append(value[1]); # DISCORD_GLOBAL

                        for value in data2:
                            USER.append(value[0]);
                            USER.append(value[1]);

                        if USER != []:
                            if USER[1] != bot_config.GLOBAL_BAN_STATUS:
                                for server,channel in zip(KANAL,DISCORD_GLOBAL):
                                    if channel != None and message.author.bot == False:
                                        SERVER = self.client.get_guild(server);
                                        if SERVER != None:
                                            CHANNEL = SERVER.get_channel(channel);
                                            await CHANNEL.send("`{}` **{}** *{}* {}".format(message.guild.name,message.author.display_name,message.content,message.attachments[0].url if message.attachments != [] else ""));
                                        else:
                                            try:
                                                if os.path.exists("./data/"):
                                                    file = open("./data/{}.txt".format("server_problem"),"a");
                                                    encodet = textData.encode('utf-8');
                                                    file.write("{}\n".format(encodet));
                                                else:
                                                    os.mkdir("./data/{}".format(before.guild));
                                                    file = open("./data/{}.txt".format("server_problem"), "a");
                                                    encodet = textData.encode('utf-8');
                                                    file.write("{}\n".format(encodet));
                                            except Exception as error:
                                                print("Exception: (server_problem): {}.".format(error));
                                            finally:
                                                file.close();
                            else:
                                await user.send("**{}** *Jūs esate užbanintas Beobachter-Global pokalbio kanale.*".format(message.guild.name));

                            if message.author.bot == False and INFORMATION[5] == message.channel.id:
                                await message.delete();
                        else:
                            if message.author.bot == False and INFORMATION[5] == message.channel.id:
                                await message.delete();
            else:
                pass;

            if message.attachments == []:
                printText = "Record: {} - Server: {} - Action: {} - Channel: {} - User: {} - Content: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), message.guild,bot_config.CLIENT_MESSAGES["on_message"], str(message.channel.mention), message.author.mention, message.content);
                textData = "Record: {} - Action: {} - User: {} - Content: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),bot_config.CLIENT_MESSAGES["on_message"], message.author.mention, message.content);
                print(printText);
            else:
                printText = "Record: {} - Server: {} - Action: {} - Channel: {} - User: {} - Content: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), message.guild,bot_config.CLIENT_MESSAGES["image_upload"], str(message.channel.mention), message.author.mention, message.attachments);
                textData = "Record: {} - Action: {} - User: {} - Content: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),bot_config.CLIENT_MESSAGES["image_upload"], message.author.mention, message.attachments);
                print(printText);
            try:
                if os.path.exists("./data/{}".format(message.guild)):
                    file = open("./data/{}/{}.txt".format(message.guild,message.channel),"a");
                    encodet = textData.encode('utf-8');
                    file.write("{}\n".format(encodet));
                else:
                    os.mkdir("./data/{}".format(message.guild));
                    file = open("./data/{}/{}.txt".format(message.guild,message.channel),"a");
                    encodet = textData.encode('utf-8');
                    file.write("{}\n".format(encodet));
            except Exception as error:
                print("Exception: (on_message): {}.".format(error));
            finally:
                file.close();

    @commands.Cog.listener()
    async def on_message_edit(self,before,after):
        currentTime = datetime.now();
        printTextAfter = "Record: {} - Server: {} - Action: {} - Channel: {} - User: {} - Before: {} - After: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), before.guild,bot_config.CLIENT_MESSAGES["on_message_edit"], str(before.channel.mention), before.author.mention, before.content, after.content);
        textDataAfter = "Record: {} - Action: {} - Channel: {} - User: {} - Before: {} - After: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),bot_config.CLIENT_MESSAGES["on_message_edit"], str(before.channel.mention), before.author.mention, before.content, after.content);
        print(printTextAfter);

        try:
            if os.path.exists("./data/{}".format(before.guild)):
                file = open("./data/{}/{}.txt".format(before.guild,"edited_messages"), "a");
                encodet = textDataAfter.encode('utf-8');
                file.write("{}\n".format(encodet));
            else:
                os.mkdir("./data/{}".format(before.guild));
                file = open("./data/{}/{}.txt".format(before.guild,"edited_messages"), "a");
                encodet = textDataAfter.encode('utf-8');
                file.write("{}\n".format(encodet));
        except Exception as error:
            print("Exception: (on_message_edit): {}.".format(error));
        finally:
            file.close();

    @commands.Cog.listener()
    async def on_message_delete(self,message):
        currentTime = datetime.now();

        if message.attachments == []:
            printText = "Record: {} - Server: {} - Action: {} - Channel: {} - User: {} - Content: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), message.guild,bot_config.CLIENT_MESSAGES["on_message_delete"], str(message.channel.mention), message.author.mention, message.content);
            textData = "Record: {} - Action: {} - Channel: {} - User: {} - Content: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),bot_config.CLIENT_MESSAGES["on_message_delete"], str(message.channel.mention), message.author.mention, message.content);
            print(printText);
        else:
            printText = "Record: {} - Server: {} - Action: {} - Channel: {} - User: {} - Content: {} - Attachments: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), message.guild,bot_config.CLIENT_MESSAGES["on_message_delete"], str(message.channel.mention), message.author.mention, message.content, message.attachments);
            textData = "Record: {} - Action: {} - Channel: {} - User: {} - Content: {} - Attachments: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),bot_config.CLIENT_MESSAGES["on_message_delete"], str(message.channel.mention), message.author.mention, message.content, message.attachments);
            print(printText);

        try:
            if os.path.exists("./data/{}".format(message.guild)):
                file = open("./data/{}/{}.txt".format(message.guild,"deleted_messages"), "a");
                encodet = textData.encode('utf-8');
                file.write("{}\n".format(encodet));
            else:
                os.mkdir("./data/{}".format(message.guild));
                file = open("./data/{}/{}.txt".format(message.guild,"deleted_messages"), "a");
                encodet = textData.encode('utf-8');
                file.write("{}\n".format(encodet));
        except Exception as error:
            print("Exception: (on_message_delete): {}.".format(error));
        finally:
            file.close();

    @commands.Cog.listener()
    async def on_user_update(self,before,after):
        currentTime = datetime.now();
        if before.display_name != after.display_name:
            printText = "Record: {} - Action: {} - User: {} - Content: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),bot_config.CLIENT_MESSAGES["on_user_update"], before.display_name, after.display_name);
            textData = "Record: {} - Action: {} - User: {} - Content: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),bot_config.CLIENT_MESSAGES["on_user_update"], before.display_name, after.display_name);
            print(printText);
        elif before.avatar_url != after.avatar_url:
            printText = "Record: {} - Action: {} - User: {} - Before: {} - After: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),bot_config.CLIENT_MESSAGES["on_user_update"], before.display_name, before.avatar_url, after.avatar_url);
            textData = "Record: {} - Action: {} - User: {} - Before: {} - After: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),bot_config.CLIENT_MESSAGES["on_user_update"], before.display_name, before.avatar_url, after.avatar_url);
            print(printText);

        try:
            file = open("./data/{}.txt".format("user_update"), "a");
            encodet = textData.encode('utf-8');
            file.write("{}\n".format(encodet));
        except Exception as error:
            print("Exception: (on_user_update): {}.".format(error));
        finally:
            file.close();

        if before.display_name != after.display_name:
            sql = "SELECT {},{} FROM {}".format(bot_config.MYSQL_NV["benutzer_id"],
            bot_config.MYSQL_NV["benutzer_name"],
            bot_config.MYSQL_CONFIGURATION["mysql_name_verbot"]);
            data = getter.getData(sql);

            if data != []:
                for value in data:
                    if value[0] != after.id and value[1] == str(after.display_name).lower():
                        member = self.client.get_member(after.id);
                        await member.ban(reason="{}".format(bot_config.DISCORD_MESSAGES["ban_reason"]));
                        try:
                            printText = "Record: {} - Server: {} - Action: {} - User: {} - Uerd ID: {} - Reason: {}".format(
                                currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), after.guild,
                                bot_config.CLIENT_MESSAGES["client_banned"], after.display_name, after.id,
                                bot_config.DISCORD_MESSAGES["ban_reason"]);
                            textData = "Record: {} - Action: {} - User: {} - Uerd ID: {} - Reason: {}".format(
                                currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), bot_config.CLIENT_MESSAGES["client_banned"],
                                after.display_name, after.id, bot_config.DISCORD_MESSAGES["ban_reason"]);
                            print(printText);
                            if os.path.exists("./data/{}".format(after.guild)):
                                file = open("./data/{}/{}.txt".format(after.guild, "member_banned"), "a");
                                encodet = textData.encode('utf-8');
                                file.write("{}\n".format(encodet));
                            else:
                                os.mkdir("./data/{}".format(after.guild));
                                file = open("./data/{}/{}.txt".format(after.guild, "member_banned"), "a");
                                encodet = textData.encode('utf-8');
                                file.write("{}\n".format(encodet));
                        except Exception as error:
                            print("Exception: (on_user_update/member_banned/name_verbot): {}.".format(error));
                        finally:
                            file.close();

    @commands.Cog.listener()
    async def on_member_update(self,before,after):
        currentTime = datetime.now();
        if before.display_name != after.display_name:
            sql = "SELECT {},{} FROM {}".format(bot_config.MYSQL_NV["benutzer_id"],
            bot_config.MYSQL_NV["benutzer_name"],
            bot_config.MYSQL_CONFIGURATION["mysql_name_verbot"]);
            data = getter.getData(sql);

            if data != []:
                for value in data:
                    if value[0] != after.id and value[1] == str(after.display_name).lower():
                        await after.ban(reason="{}".format(bot_config.DISCORD_MESSAGES["ban_reason"]));
                        try:
                            printText = "Record: {} - Server: {} - Action: {} - User: {} - Uerd ID: {} - Reason: {}".format(
                                currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), after.guild,
                                bot_config.CLIENT_MESSAGES["client_banned"], after.display_name, after.id,
                                bot_config.DISCORD_MESSAGES["ban_reason"]);
                            textData = "Record: {} - Action: {} - User: {} - Uerd ID: {} - Reason: {}".format(
                                currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), bot_config.CLIENT_MESSAGES["client_banned"],
                                after.display_name, after.id, bot_config.DISCORD_MESSAGES["ban_reason"]);
                            print(printText);
                            if os.path.exists("./data/{}".format(after.guild)):
                                file = open("./data/{}/{}.txt".format(after.guild, "member_banned"), "a");
                                encodet = textData.encode('utf-8');
                                file.write("{}\n".format(encodet));
                            else:
                                os.mkdir("./data/{}".format(after.guild));
                                file = open("./data/{}/{}.txt".format(after.guild, "member_banned"), "a");
                                encodet = textData.encode('utf-8');
                                file.write("{}\n".format(encodet));
                        except Exception as error:
                            print("Exception: (on_member_update/member_banned/name_verbot): {}.".format(error));
                        finally:
                            file.close();

            elif before.avatar_url != after.avatar_url:
                printText = "Record: {} - Server: {} - Action: {} - User: {} - Before: {} - After: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), before.guild,bot_config.CLIENT_MESSAGES["on_user_update"], before.display_name, before.avatar_url, after.avatar_url);
                textData = "Record: {} - Action: {} - User: {} - Before: {} - After: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),bot_config.CLIENT_MESSAGES["on_user_update"], before.display_name, before.avatar_url, after.avatar_url);
                print(printText);

                try:
                    if os.path.exists("./data/{}".format(before.guild)):
                        file = open("./data/{}/{}.txt".format(before.guild, "member_update"), "a");
                        encodet = textData.encode('utf-8');
                        file.write("{}\n".format(encodet));
                    else:
                        os.mkdir("./data/{}".format(before.guild));
                        file = open("./data/{}/{}.txt".format(before.guild, "member_update"), "a");
                        encodet = textData.encode('utf-8');
                        file.write("{}\n".format(encodet));
                except Exception as error:
                    print("Exception: (on_member_update): {}.".format(error));
                finally:
                    file.close();

                sql = "SELECT {},{} FROM {}".format(bot_config.MYSQL_NV["benutzer_id"],
                bot_config.MYSQL_NV["benutzer_name"],
                bot_config.MYSQL_CONFIGURATION["mysql_name_verbot"]);
                data = getter.getData(sql);

                for value in data:
                    if value[0] != after.id and value[1] == str(after.display_name).lower():
                        await after.ban(reason="{}".format(bot_config.DISCORD_MESSAGES["ban_reason"]));
                        try:
                            printText = "Record: {} - Server: {} - Action: {} - User: {} - Uerd ID: {} - Reason: {}".format(
                                currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), after.guild,
                                bot_config.CLIENT_MESSAGES["client_banned"], after.display_name, after.id,
                                bot_config.DISCORD_MESSAGES["ban_reason"]);
                            textData = "Record: {} - Action: {} - User: {} - Uerd ID: {} - Reason: {}".format(
                                currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), bot_config.CLIENT_MESSAGES["client_banned"],
                                after.display_name, after.id, bot_config.DISCORD_MESSAGES["ban_reason"]);
                            print(printText);
                            if os.path.exists("./data/{}".format(after.guild)):
                                file = open("./data/{}/{}.txt".format(after.guild, "member_banned"), "a");
                                encodet = textData.encode('utf-8');
                                file.write("{}\n".format(encodet));
                            else:
                                os.mkdir("./data/{}".format(after.guild));
                                file = open("./data/{}/{}.txt".format(after.guild, "member_banned"), "a");
                                encodet = textData.encode('utf-8');
                                file.write("{}\n".format(encodet));
                        except Exception as error:
                            print("Exception: (on_member_update/member_banned/name_verbot): {}.".format(error));
                        finally:
                            file.close();
            else:
                pass

    @commands.Cog.listener()
    async def on_member_join(self,member):
        INFORMATION = []; BAN = False;
        sql = "SELECT {} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["discord_registration"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
        bot_config.MYSQL_KK["kanal_id"], member.guild.id);
        data = getter.getData(sql);

        for value in data:
            INFORMATION.append(value[0]);

        currentTime = datetime.now();
        printText = "Record: {} - Server: {} - Action: {} - User: {} - Uerd ID: {} - Created at: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), member.guild,bot_config.CLIENT_MESSAGES["client_joined"], member.display_name, member.id, member.created_at);
        textData = "Record: {} - Action: {} - User: {} - Uerd ID: {} - Created at: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),bot_config.CLIENT_MESSAGES["client_joined"], member.display_name, member.id, member.created_at);
        print(printText);

        try:
            if os.path.exists("./data/{}".format(member.guild)):
                file = open("./data/{}/{}.txt".format(member.guild,"member_join"), "a");
                encodet = textData.encode('utf-8');
                file.write("{}\n".format(encodet));
            else:
                os.mkdir("./data/{}".format(member.guild));
                file = open("./data/{}/{}.txt".format(member.guild,"member_join"), "a");
                encodet = textData.encode('utf-8');
                file.write("{}\n".format(encodet));
        except Exception as error:
            print("Exception: (on_member_join): {}.".format(error));
        finally:
            file.close();

        sql = "SELECT {},{},{} FROM {} WHERE {}={}".format(bot_config.MYSQL_KB["benutzer_id"],
        bot_config.MYSQL_KB["benutzer_name"],
        bot_config.MYSQL_KB["benutzer_ban_grund"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_ban"],
        bot_config.MYSQL_KB["kanal_id"],
        member.guild.id);
        data = getter.getData(sql);

        for value in data:
            if value[0] == member.id:
                await member.ban(reason="{}".format(value[2]));
                BAN = True;
                try:
                    printText = "Record: {} - Server: {} - Action: {} - User: {} - Uerd ID: {} - Reason: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), member.guild,bot_config.CLIENT_MESSAGES["client_banned"], member.display_name, member.id, value[2]);
                    textData = "Record: {} - Action: {} - User: {} - Uerd ID: {} - Reason: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),bot_config.CLIENT_MESSAGES["client_banned"], member.display_name, member.id, value[2]);
                    print(printText);
                    if os.path.exists("./data/{}".format(member.guild)):
                        file = open("./data/{}/{}.txt".format(member.guild, "member_banned"), "a");
                        encodet = textData.encode('utf-8');
                        file.write("{}\n".format(encodet));
                    else:
                        os.mkdir("./data/{}".format(member.guild));
                        file = open("./data/{}/{}.txt".format(member.guild, "member_banned"), "a");
                        encodet = textData.encode('utf-8');
                        file.write("{}\n".format(encodet));
                except Exception as error:
                    print("Exception: (on_member_join/member_banned): {}.".format(error));
                finally:
                    file.close();
            if value[1] == str(member.display_name).lower():
                await member.ban(reason="{}".format(value[2]));
                BAN = True;
                try:
                    printText = "Record: {} - Server: {} - Action: {} - User: {} - Uerd ID: {} - Reason: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), member.guild,bot_config.CLIENT_MESSAGES["client_banned"], member.display_name, member.id, value[2]);
                    textData = "Record: {} - Action: {} - User: {} - Uerd ID: {} - Reason: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),bot_config.CLIENT_MESSAGES["client_banned"], member.display_name, member.id, value[2]);
                    print(printText);
                    if os.path.exists("./data/{}".format(member.guild)):
                        file = open("./data/{}/{}.txt".format(member.guild, "member_banned"), "a");
                        encodet = textData.encode('utf-8');
                        file.write("{}\n".format(encodet));
                    else:
                        os.mkdir("./data/{}".format(member.guild));
                        file = open("./data/{}/{}.txt".format(member.guild, "member_banned"), "a");
                        encodet = textData.encode('utf-8');
                        file.write("{}\n".format(encodet));
                except Exception as error:
                    print("Exception: (on_member_join/member_banned): {}.".format(error));
                finally:
                    file.close();

        sql = "SELECT {},{},{} FROM {}".format(bot_config.MYSQL_GB["benutzer_id"], bot_config.MYSQL_GB["benutzer_name"],
        bot_config.MYSQL_GB["benutzer_ban_grund"],
        bot_config.MYSQL_CONFIGURATION["mysql_global_ban"]);
        data = getter.getData(sql);

        for value in data:
            if value[0] == member.id:
                await member.ban(reason="Global-{}".format(value[2]));
                BAN = True;
                try:
                    printText = "Record: {} - Server: {} - Action: {} - User: {} - Uerd ID: {} - Reason: Global-{}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), member.guild,bot_config.CLIENT_MESSAGES["client_banned"], member.display_name, member.id, value[2]);
                    textData = "Record: {} - Action: {} - User: {} - Uerd ID: {} - Reason: Global-{}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),bot_config.CLIENT_MESSAGES["client_banned"], member.display_name, member.id, value[2]);
                    print(printText);
                    if os.path.exists("./data/{}".format(member.guild)):
                        file = open("./data/{}/{}.txt".format(member.guild, "member_banned"), "a");
                        encodet = textData.encode('utf-8');
                        file.write("{}\n".format(encodet));
                    else:
                        os.mkdir("./data/{}".format(member.guild));
                        file = open("./data/{}/{}.txt".format(member.guild, "member_banned"), "a");
                        encodet = textData.encode('utf-8');
                        file.write("{}\n".format(encodet));
                except Exception as error:
                    print("Exception: (on_member_join/member_banned): {}.".format(error));
                finally:
                    file.close();
            if value[1] == member.display_name:
                await member.ban(reason="Global-{}".format(value[2]));
                BAN = True;
                try:
                    printText = "Record: {} - Server: {} - Action: {} - User: {} - Uerd ID: {} - Reason: Global-{}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), member.guild,bot_config.CLIENT_MESSAGES["client_banned"], member.display_name, member.id, value[2]);
                    textData = "Record: {} - Action: {} - User: {} - Uerd ID: {} - Reason: Global-{}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),bot_config.CLIENT_MESSAGES["client_banned"], member.display_name, member.id, value[2]);
                    print(printText);
                    if os.path.exists("./data/{}".format(member.guild)):
                        file = open("./data/{}/{}.txt".format(member.guild, "member_banned"), "a");
                        encodet = textData.encode('utf-8');
                        file.write("{}\n".format(encodet));
                    else:
                        os.mkdir("./data/{}".format(member.guild));
                        file = open("./data/{}/{}.txt".format(member.guild, "member_banned"), "a");
                        encodet = textData.encode('utf-8');
                        file.write("{}\n".format(encodet));
                except Exception as error:
                    print("Exception: (on_member_join/member_banned): {}.".format(error));
                finally:
                    file.close();

        sql = "SELECT {},{} FROM {}".format(bot_config.MYSQL_NV["benutzer_id"], bot_config.MYSQL_NV["benutzer_name"],
        bot_config.MYSQL_CONFIGURATION["mysql_name_verbot"]);
        data = getter.getData(sql);

        for value in data:
            if value[0] != member.id and value[1] == str(member.display_name).lower():
                await member.ban(reason="{}".format(bot_config.DISCORD_MESSAGES["ban_reason"]));
                BAN = True;
                try:
                    printText = "Record: {} - Server: {} - Action: {} - User: {} - Uerd ID: {} - Reason: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), member.guild,
                    bot_config.CLIENT_MESSAGES["client_banned"], member.display_name, member.id,
                    bot_config.DISCORD_MESSAGES["ban_reason"]);
                    textData = "Record: {} - Action: {} - User: {} - Uerd ID: {} - Reason: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),
                    bot_config.CLIENT_MESSAGES["client_banned"], member.display_name, member.id,
                    bot_config.DISCORD_MESSAGES["ban_reason"]);
                    print(printText);
                    if os.path.exists("./data/{}".format(member.guild)):
                        file = open("./data/{}/{}.txt".format(member.guild, "member_banned"), "a");
                        encodet = textData.encode('utf-8');
                        file.write("{}\n".format(encodet));
                    else:
                        os.mkdir("./data/{}".format(member.guild));
                        file = open("./data/{}/{}.txt".format(member.guild, "member_banned"), "a");
                        encodet = textData.encode('utf-8');
                        file.write("{}\n".format(encodet));
                except Exception as error:
                    print("Exception: (on_member_join/member_banned/name_verbot): {}.".format(error));
                finally:
                    file.close();

        sql = "SELECT {} FROM {} WHERE {}={}".format(bot_config.MYSQL_KK["discord_random"],
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
        bot_config.MYSQL_KK["kanal_id"], member.guild.id);
        data = getter.getData(sql);

        for value in data:
            if value[0] != None and BAN != True:
                channel = self.client.get_channel(value[0]);
                await channel.send("*{} {} {} {}:* **{}**.".format(member.mention,
                bot_config.DISCORD_MESSAGES["member_joined"], "PvM registracija vyksta <#{}> skiltyje.".format(INFORMATION[0]) if len(INFORMATION) != 0 else "",
                bot_config.DISCORD_MESSAGES["member_created_at"], member.created_at.strftime("%m/%d/%y  %H:%M:%S")));

    @commands.Cog.listener()
    async def on_error(self,event,*args,**kwargs):
        try:
            printText = "Record: {} - Event: {} - Args: {} - Kwargs: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),event,args,kwargs);
            textData = "Record: {} - Event: {} - Args: {} - Kwargs: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),event,args,kwargs);
            print(printText);
            if os.path.exists("./data/"):
                file = open("./data/{}.txt".format("discord_error_log"), "a");
                encodet = textData.encode('utf-8');
                file.write("{}\n".format(encodet));
            else:
                os.mkdir("./data/");
                file = open("./data/{}.txt".format("discord_error_log"), "a");
                encodet = textData.encode('utf-8');
                file.write("{}\n".format(encodet));
        except Exception as error:
            print("Exception: (on_error): {}.".format(error));
        finally:
            file.close();

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error,discord.ext.commands.CommandError):
            return error;
        raise error

def setup(client):
    client.add_cog(core(client));