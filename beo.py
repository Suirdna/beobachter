import discord
import os
from configs import bot_config
from discord.ext import commands
from datetime import datetime
from modules import getter

#◄███▓▒░░ SYSTEM ░░▒▓███►#

client = commands.Bot(command_prefix=bot_config.CLIENT_PREFIX);

@client.event
async def on_ready():
    currentTime = datetime.now();
    for string in bot_config.CLIENT_LOGO:
        print(string);
    print(bot_config.CLIENT_SPLIT);
    print("{}{}{}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), bot_config.CLIENT_NAME,bot_config.CLIENT_MESSAGES["client_online"]));
    print("{}{}{}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"), bot_config.CLIENT_NAME,bot_config.CLIENT_MESSAGES["client_recording"]));
    print(bot_config.CLIENT_SPLIT);

@client.event
async def on_guild_join(guild):
    INFORMATION = [];
    sql = "SELECT {} FROM {} WHERE {}={}".format(bot_config.MYSQL_KMK["kanal_id"],bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
    bot_config.MYSQL_KMK["kanal_id"], guild.id
    );
    data = getter.getData(sql);

    if data == []:
        sql = "INSERT INTO {} ({},{},{},{},{},{},{},{},{}) VALUES ({},{},'{}','{}','{}',{},{},{},'{}')".format(
            bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
            bot_config.MYSQL_KK["status"], bot_config.MYSQL_KK["kanal_id"],
            bot_config.MYSQL_KK["kanal_name"], bot_config.MYSQL_KK["kanal_symbol"],
            bot_config.MYSQL_KK["kanal_region"], bot_config.MYSQL_KK["bot_id"],
            bot_config.MYSQL_KK["kanal_besitzer_id"], bot_config.MYSQL_KK["bot_administration_id"],
            bot_config.MYSQL_KK["erstellung_datum"],
            bot_config.CLIENT_ACTIVE, guild.id,
            guild.name, guild.icon_url if guild.icon_url != None else guild.icon,
            guild.region, bot_config.CLIENT_ID,
            guild.owner_id, bot_config.CLIENT_ADMNISTRATION,
            guild.created_at
            );
        getter.setData(sql);
    else:
        sql = "UPDATE {} SET {}={},{}='{}',{}='{}',{}='{}',{}={},{}={},{}={},{}='{}' WHERE {}={}".format(
        bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
        bot_config.MYSQL_KK["status"], bot_config.CLIENT_ACTIVE,
        bot_config.MYSQL_KK["kanal_name"],guild.name,
        bot_config.MYSQL_KK["kanal_symbol"],guild.icon_url if guild.icon_url != None else guild.icon,
        bot_config.MYSQL_KK["kanal_region"],guild.region,
        bot_config.MYSQL_KK["bot_id"], bot_config.CLIENT_ID,
        bot_config.MYSQL_KK["kanal_besitzer_id"],guild.owner_id,
        bot_config.MYSQL_KK["bot_administration_id"], bot_config.CLIENT_ADMNISTRATION,
        bot_config.MYSQL_KK["erstellung_datum"],guild.created_at,
        bot_config.MYSQL_KK["kanal_id"],guild.id
        );
        getter.setData(sql);

    currentTime = datetime.now();
    printText = "Record: {} - Action: {} - Server: {} - Server Icon: {} - Server Owner: {} - Created at: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),bot_config.CLIENT_MESSAGES["on_guild_joined"], guild.name, guild.icon_url, guild.owner, guild.created_at);
    textData = "Record: {} - Action: {} - Server: {} - Server Icon: {} - Server Owner: {} - Created at: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),bot_config.CLIENT_MESSAGES["on_guild_joined"], guild.name, guild.icon_url, guild.owner, guild.created_at);
    print(printText);
    try:
        if os.path.exists("./data/{}".format(guild.name)):
            file = open("./data/{}/{}.txt".format(guild.name,"server_history"), "a");
            encodet = textData.encode('utf-8');
            file.write("{}\n".format(encodet));
        else:
            os.mkdir("./data/{}".format(guild.name));
            file = open("./data/{}/{}.txt".format(guild.name,"server_history"), "a");
            encodet = textData.encode('utf-8');
            file.write("{}\n".format(encodet));
    except Exception as error:
        print("Exception: (on_guild_join): {}.".format(error));
    finally:
        file.close();

    INFORMATION.append("DATE: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]")));
    INFORMATION.append("SERVER CONFIGURATION LOG");
    INFORMATION.append("---------------------------------------------------------------------------");
    INFORMATION.append("SERVER NAME = {}".format(guild.name));
    INFORMATION.append("SERVER ID = {}".format(guild.id));
    INFORMATION.append("SERVER REGION = {}".format(guild.region));
    INFORMATION.append("SERVER OWNER_NAME = {}".format(guild.owner.name));
    INFORMATION.append("SERVER OWNER_ID = {}".format(guild.owner_id));
    INFORMATION.append("SERVER VERIFICATION_LEVEL = {}".format(guild.verification_level));
    INFORMATION.append("---------------------------------------------------------------------------");
    INFORMATION.append("SERVER INVITE_LIST = {}".format(await guild.invites()));
    INFORMATION.append("---------------------------------------------------------------------------");
    INFORMATION.append("SERVER TEXT_CHANNEL_LIST = {}".format(guild.text_channels));
    INFORMATION.append("---------------------------------------------------------------------------");
    INFORMATION.append("SERVER VOICE_CHANNEL_LIST = {}".format(guild.voice_channels));
    INFORMATION.append("---------------------------------------------------------------------------");
    INFORMATION.append("SERVER CATEGORY_LIST = {}".format(guild.categories));
    INFORMATION.append("---------------------------------------------------------------------------");
    INFORMATION.append("SERVER MEMBER_LIST = {}".format(guild.members));
    INFORMATION.append("---------------------------------------------------------------------------");
    INFORMATION.append("SERVER ROLE_LIST = {}".format(guild.roles));
    INFORMATION.append("---------------------------------------------------------------------------");
    INFORMATION.append("SERVER AUDIT LOG");
    async for entry in guild.audit_logs(limit=500):
        INFORMATION.append("AUDIT LOG = {}".format(entry));
    try:
        if os.path.exists("./data/{}".format(guild.name)):
            file = open("./data/{}/{}.txt".format(guild.name,"server_history"), "a");
            for value in INFORMATION:
                encodet = value.encode('utf-8');
                file.write("{}\n".format(encodet));
        else:
            os.mkdir("./data/{}".format(guild.name));
            file = open("./data/{}/{}.txt".format(guild.name,"server_history"), "a");
            for value in INFORMATION:
                encodet = value.encode('utf-8');
                file.write("{}\n".format(encodet));
    except Exception as error:
        print("Exception: (on_guild_join/data_recording): {}.".format(error));
    finally:
        file.close();

    owner = guild.owner;
    logo = open(bot_config.IMAGES["logo"], 'rb');
    split_1 = open(bot_config.IMAGES["split"], 'rb');
    split_2 = open(bot_config.IMAGES["split"], 'rb');
    split_3 = open(bot_config.IMAGES["split"], 'rb');
    split_4 = open(bot_config.IMAGES["split"], 'rb');
    split_5 = open(bot_config.IMAGES["split"], 'rb');
    split_6 = open(bot_config.IMAGES["split"], 'rb');
    example_id = open(bot_config.IMAGES["id"], 'rb');
    example_emoji = open(bot_config.IMAGES["emoji"], 'rb');

    text_1 = "{}\n\n{}".format("*Dėkojame, kad užsiregistravote prie Beobachter statistikos ir analizavimo sistemos.*\n*Jūsų discordo kanalas yra užregistruotas Beobachter sistemoje, tačiau nėra tinkamai sukonfigūruotas. Tam, kad Beobachter botas galėtų teisingai veikti jūsų discordo kanale, būtina atlikti apačioje nurodytus veiksmus.*",
    "**Pastaba!** *Discordo kanalų Beobachter struktūros sukurtų skilčių ar rolių trynimas, pavadinimų keitimas gali neigiamai paveikti Beobachter botą!*\n*Apačioje aprašytus veikmus gali atlikti tik Discordo kanalo arba Beobachter boto savininkas.*");

    text_2 = "__**Rs-Justice boto pridėjimas**__\n\n**Instrukcija:** *Pridėkite Rs-Justice botą paspausdami ant nuorodos ir patvirtinkite jo prisijungimą pasirinke savo discordo kanalą*.\n*https://discordapp.com/oauth2/authorize?&client_id=349014426067927040&scope=bot&permissions=0*";

    text_3 = "__**1. Įdiegimas**__ `.setup init`\n\n**Komanda:** `.setup init`\n**Aprašymas:** *Šios komandos pagalba, Beobachter botas sukurs jūsų discordo kanale reikalingą (struktūrą/roles) ir automatiškai sukonfigūruos botą tinkamui veikimui.*\n**Instrukcija:** *Paspauskite ant bet kurios skilties jūsų discordo kanale ir parašykite komandą* `.setup init`.";
    text_4 = "__**2. Papildomos kanalo nuostatos**__ `.setup config`\n\n**Komanda:** `.setup config`\n**Aprašymas:** *Šios komandos pagalba, Beobachter botas parodys discordo kanalo konfigūracijos nuostatas, kurias galite sukonfigūruoti rankiniu būdu.*\n**Instrukcija:** *Paspauskite ant bet kurios skilties jūsų discordo kanale ir parašykite komandą* `.setup config`."
    text_5 = "__**3. Papildomų kanalo nuostatų konfigūracija**__ `.setup cfg` `[argumentas] ir [id]` arba `[emoji]`\n\n**Pastaba!** *Be papildomų kanalo nuostatų konfigūracijos, Beobachter botas vistiek atliks būtinas funkcijas!*\n**Komanda:** `.setup cfg` `[argumentas] ir [id]` arba `[emoji]`\n**Aprašymas:** *Komanda leidžianti rankiniu būdu sukonfigūruoti papildomas discordo kanalo nuostatas Beobachter sistemoje.*\n**Instrukcija:** *Paspauskite ant bet kurios skilties jūsų discordo kanale ir parašykite komandą* `.server cfg [argumentas] ir [id] arba [emoji]`.\n\n**Pavyzdys su** `id`:";
    text_5_1 = "**Pavyzdys su** `emoji`: ";
    text_6 = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format("__**Argumentų paaiškinimas**__\n\n",
    "[argumentas] - Argumentus rasite aprašioje ⤋ arba kanalo papildomų konfigūracijų nuostatų langelyje parašydami komandą `.setup config`.\n",
    "[id] - Discordo kanalo skilties id. Pavyzdys: \\#taisyklės ir jame esantys skaičiai yra id.\n",
    "[emoji] - Discordo kanalo emoji. Pavyzdys: \\:attack:.\n\n",
    "[id] `kanal_besitzer_id` - Discordo kanalo savininkas.\n",
    "[id] `bot_id` - Beobachter botas.\n",
    "[id] `bot_administration_id` - Beobachter boto administratorius.\n",
    "[id] `discord_registration` - Discordo kanalo registracijos skiltis.\n",
    "[id] `discord_uberprufung` - Discordo kanalo check-rsn skiltis.\n",
    "[id] `discord_zahl` - Discordo kanalo uždarbio skiltis.\n",
    "[id] `discord_global` - Discordo kanalo globalus pokalbio skiltis.\n",
    "[id] `discord_beobachter` - Discordo kanalo Beobachter valdymo pulto skiltis.\n",
    "[id] `discord_moderation` - Discordo kanalo Boebachter moderacijos skiltis. `[Nenaudojama]`\n",
    "[id] `discord_beschreibung` - Discordo kanalo aprašymo skiltis.\n",
    "[id] `discord_regeln` - Discordo kanalo taisyklių skiltis.\n",
    "[id] `discord_ereignisse` - Discordo kanalo eventų skiltis.\n",
    "[id] `discord_random` - Discordo kanalo random žaidėjų pokalbių skiltis.\n",
    "[id] `discord_mitglied` - Discordo kanalo Beobachter narių pokalbių skiltis.\n",
    "[id] `discord_cox_beschreibung` - Discordo kanalo Cox aprašymo skiltis.\n",
    "[emoji]`emoji_olm` - Discordo kanalo olm emoji.\n",
    "[emoji]`emoji_attack` - Discordo kanalo attack emoji.\n",
    "[emoji]`emoji_strength` - Discordo kanalo strength emoji.\n",
    "[emoji]`emoji_defence` - Discordo kanalo defence emoji.\n",
    "[emoji]`emoji_magic` - Discordo kanalo magic emoji.\n",
    "[emoji]`emoji_range` - Discordo kanalo range emoji.\n",
    "[emoji]`emoji_prayer` - Discordo kanalo prayer emoji.\n",
    "[emoji]`emoji_herblore` - Discordo kanalo herblore emoji.\n",
    "[emoji]`emoji_farming` - Discordo kanalo farming emoji.\n",
    "[emoji]`emoji_gp` - Discordo kanalo gp emoji.\n",
    );

    text_7 = "**✙ PROGRAMUOTOJAS:** *Andrius Lizunovas*.\n**✙ FBN:** *https://www.facebook.com/amiraarima.liz*.\n**✙ DCN:** *FaustRecht#5546*.";

    await owner.send(file=discord.File(logo));
    await owner.send(content=text_1);
    await owner.send(file=discord.File(split_1));
    await owner.send(content=text_2);
    await owner.send(file=discord.File(split_2));
    await owner.send(content=text_3);
    await owner.send(file=discord.File(split_3));
    await owner.send(content=text_4);
    await owner.send(file=discord.File(split_4));
    await owner.send(content=text_5);
    await owner.send(file=discord.File(example_id));
    await owner.send(content=text_5_1);
    await owner.send(file=discord.File(example_emoji));
    await owner.send(file=discord.File(split_5));
    await owner.send(content=text_6);
    await owner.send(file=discord.File(split_6));
    await owner.send(content=text_7);

@client.event
async def on_guild_remove(guild):
    INFORMATION = [];
    sql = "UPDATE {} SET {}={},{}='{}',{}='{}',{}='{}',{}={},{}={},{}={},{}='{}',{}={} WHERE {}={}".format(
    bot_config.MYSQL_CONFIGURATION["mysql_kanal_konfiguration"],
    bot_config.MYSQL_KK["status"], bot_config.CLIENT_ACTIVE,
    bot_config.MYSQL_KK["kanal_name"],guild.name,
    bot_config.MYSQL_KK["kanal_symbol"],guild.icon_url if guild.icon_url != None else guild.icon,
    bot_config.MYSQL_KK["kanal_region"],guild.region,
    bot_config.MYSQL_KK["bot_id"], bot_config.CLIENT_ID,
    bot_config.MYSQL_KK["kanal_besitzer_id"],guild.owner_id,
    bot_config.MYSQL_KK["bot_administration_id"], bot_config.CLIENT_ADMNISTRATION,
    bot_config.MYSQL_KK["erstellung_datum"],guild.created_at,
    bot_config.MYSQL_KK["status"], bot_config.CLIENT_DISABLE,
    bot_config.MYSQL_KK["kanal_id"],guild.id
    );
    getter.setData(sql);

    currentTime = datetime.now();
    printText = "Record: {} - Action: {} - Server: {} - Server Icon: {} - Server Owner: {} - Created at: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),bot_config.CLIENT_MESSAGES["on_guild_removed"], guild.name, guild.icon_url, guild.owner, guild.created_at);
    textData = "Record: {} - Action: {} - Server: {} - Server Icon: {} - Server Owner: {} - Created at: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),bot_config.CLIENT_MESSAGES["on_guild_removed"], guild.name, guild.icon_url, guild.owner, guild.created_at);
    print(printText);
    try:
        if os.path.exists("./data/{}".format(guild.name)):
            file = open("./data/{}/{}.txt".format(guild.name,"server_history"), "a");
            encodet = textData.encode('utf-8');
            file.write("{}\n".format(encodet));
        else:
            os.mkdir("./data/{}".format(guild.name));
            file = open("./data/{}/{}.txt".format(guild.name,"server_history"), "a");
            encodet = textData.encode('utf-8');
            file.write("{}\n".format(encodet));
    except Exception as error:
        print("Exception: (on_guild_remove): {}.".format(error));
    finally:
        file.close();

    INFORMATION.append("DATE: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]")));
    INFORMATION.append("SERVER CONFIGURATION LOG");
    INFORMATION.append("---------------------------------------------------------------------------");
    INFORMATION.append("SERVER NAME = {}".format(guild.name));
    INFORMATION.append("SERVER ID = {}".format(guild.id));
    INFORMATION.append("SERVER REGION = {}".format(guild.region));
    INFORMATION.append("SERVER OWNER_NAME = {}".format(guild.owner.name));
    INFORMATION.append("SERVER OWNER_ID = {}".format(guild.owner_id));
    INFORMATION.append("SERVER VERIFICATION_LEVEL = {}".format(guild.verification_level));
    INFORMATION.append("---------------------------------------------------------------------------");
    INFORMATION.append("SERVER TEXT_CHANNEL_LIST = {}".format(guild.text_channels));
    INFORMATION.append("---------------------------------------------------------------------------");
    INFORMATION.append("SERVER VOICE_CHANNEL_LIST = {}".format(guild.voice_channels));
    INFORMATION.append("---------------------------------------------------------------------------");
    INFORMATION.append("SERVER CATEGORY_LIST = {}".format(guild.categories));
    INFORMATION.append("---------------------------------------------------------------------------");
    INFORMATION.append("SERVER MEMBER_LIST = {}".format(guild.members));
    INFORMATION.append("---------------------------------------------------------------------------");
    INFORMATION.append("SERVER ROLE_LIST = {}".format(guild.roles));
    try:
        if os.path.exists("./data/{}".format(guild.name)):
            file = open("./data/{}/{}.txt".format(guild.name,"server_history"), "a");
            for value in INFORMATION:
                encodet = value.encode('utf-8');
                file.write("{}\n".format(encodet));
        else:
            os.mkdir("./data/{}".format(guild.name));
            file = open("./data/{}/{}.txt".format(guild.name,"server_history"), "a");
            for value in INFORMATION:
                encodet = value.encode('utf-8');
                file.write("{}\n".format(encodet));
    except Exception as error:
        print("Exception: (on_guild_remove/data_recording): {}.".format(error));
    finally:
        file.close();

@client.event
async def on_guild_update(before,after):
    currentTime = datetime.now();
    printText = "Record: {} - Action: {} - Server: {} - Server Owner: {}".format(currentTime.strftime("[ %d/%m/%y  %H:%M:%S ]"),bot_config.CLIENT_MESSAGES["on_guild_update"], before.name, before.owner, before.created_at);
    textData = "Old: {} New: {}".format(before,after);
    print(printText);
    try:
        if os.path.exists("./data/{}".format(before.name)):
            file = open("./data/{}/{}.txt".format(before.name,"server_history"), "a");
            encodet = textData.encode('utf-8');
            file.write("{}\n".format(encodet));
        else:
            os.mkdir("./data/{}".format(before.name));
            file = open("./data/{}/{}.txt".format(before.name,"server_history"), "a");
            encodet = textData.encode('utf-8');
            file.write("{}\n".format(encodet));
    except Exception as error:
        print("Exception: (on_guild_update): {}.".format(error));
    finally:
        file.close();

@client.command()
async def load(extension):
    try:
        client.load_extension(extension);
    except Exception as error:
        print("{} {} {}".format(bot_config.CLIENT_NAME, module, error));
    finally:
        pass;

if __name__ == "__main__":
    for module in bot_config.CLIENT_MODULES:

        client.load_extension(module);

client.run(bot_config.CLIENT_TOKEN);