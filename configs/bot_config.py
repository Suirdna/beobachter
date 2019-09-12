from discord.ext import commands

#-----------------------------------------------------------------------------------------------------------------------
#BOT CONSOLE INTERFACE

CLIENT_LOGO = [
          " ____  ____  __  ____   __    ___  _  _  ____  ____  ____",
          "(  _ \(  __)/  \(  _ \ / _\  / __)/ )( \(_  _)(  __)(  _ \\",
          " ) _ ( ) _)(  O )) _ (/    \( (__ ) __ (  )(   ) _)  )   /",
          "(____/(____)\__/(____/\_/\_/ \___)\_)(_/ (__) (____)(__\_)",
];

CLIENT_SPLIT = "--------------------------------------------------------------";
CLIENT_NAME = "Beobachter: ";
DEVELOPER_MODE = True;

#-----------------------------------------------------------------------------------------------------------------------
#BOT CONFIGURATION

if DEVELOPER_MODE == True:
    CLIENT_TOKEN = "NjA0MjkyNjY2Njg3MDk0Nzg1.XUMNUQ.JY2uuo_7V8F6uzYkAKUzgBWWGlI";
else:
    CLIENT_TOKEN = "NTk5NjE1MTE2MDQ0MDA5NDc3.XUMNOA.l41v9AQe6rU1Ije_MeTj9xA8vr4";

CLIENT_PREFIX = ".";
CLIENT_ID = 599615116044009477;
CLIENT_ADMNISTRATION = 582600982916235290;
CLIENT_MODULES = ["offline","core","mod","commands","extern.organizator"];

CLIENT_VERSION = 2.2;
CLIENT_AUTHOR = "Andrius Lizunovas";
CLIENT_WEBSITE = "http://totenkopf.freevar.com/";
CLIENT_ICON = "https://cdn.discordapp.com/attachments/601499258767671321/601501912671453185/favicon.png";

CLIENT_ACTIVE = 1;
CLIENT_DISABLE = 0;
SPECIAL_ACTIVE = 1;
GLOBAL_ACTIVE = 1;
GLOBAL_DISABLE = 0;
GLOBAL_BAN_STATUS = 1;

#-----------------------------------------------------------------------------------------------------------------------
#MYSQL DATABASE CONFIGURATION

if DEVELOPER_MODE == True:
    MYSQL_CONFIGURATION = {
        "server":"localhost",
        "username":"admin",
        "password":"",
        "database":"beobachter_tabelle",
        "mysql_allgemein_statistik":"allgemein_statistik",
        "mysql_kanal_konfiguration":"kanal_konfiguration",
        "mysql_kanal_mitglied_konten":"kanal_mitglied_konten",
        "mysql_kanal_ban":"kanal_ban",
        "mysql_global_ban":"global_ban",
        "mysql_name_verbot":"name_verbot",
        "mysql_kanal_ereignisse": "kanal_ereignisse",
        "mysql_kanal_mod":"kanal_mod",
        "port":"3306",
    }
else:
    MYSQL_CONFIGURATION = {
        "server":"",
        "username":"",
        "password":"",
        "database":"",
        "mysql_allgemein_statistik":"allgemein_statistik",
        "mysql_kanal_konfiguration":"kanal_konfiguration",
        "mysql_kanal_mitglied_konten":"kanal_mitglied_konten",
        "mysql_kanal_ban":"kanal_ban",
        "mysql_global_ban":"global_ban",
        "mysql_name_verbot":"name_verbot",
        "mysql_kanal_ereignisse": "kanal_ereignisse",
        "mysql_kanal_mod":"kanal_mod",
        "port":"3306",
    }

MYSQL_KK = {"status":"status","kanal_id":"kanal_id","kanal_name":"kanal_name","kanal_symbol":"kanal_symbol","kanal_region":"kanal_region","kanal_besitzer_id":"kanal_besitzer_id","bot_id":"bot_id","bot_administration_id":"bot_administration_id",
"discord_registration":"discord_registration","discord_uberprufung":"discord_uberprufung","discord_zahl":"discord_zahl","discord_global":"discord_global","discord_beobachter":"discord_beobachter",
"discord_moderation":"discord_moderation","discord_beschreibung":"discord_beschreibung","discord_regeln":"discord_regeln",
"discord_ereignisse":"discord_ereignisse","discord_random":"discord_random","discord_mitglied":"discord_mitglied","discord_cox_beschreibung":"discord_cox_beschreibung","emoji_olm":"emoji_olm",
"emoji_attack":"emoji_attack","emoji_strength":"emoji_strength","emoji_defence":"emoji_defence","emoji_magic":"emoji_magic","emoji_range":"emoji_range","emoji_prayer":"emoji_prayer","emoji_herblore":"emoji_herblore",
"emoji_farming":"emoji_farming","emoji_gp":"emoji_gp","role_name_1":"role_name_1","role_name_2":"role_name_2","role_name_3":"role_name_3","role_name_4":"role_name_4",
"role_name_5":"role_name_5","spezial_role_1":"spezial_role_1","role_name_global":"role_name_global","role_zahl_2":"role_zahl_2","role_zahl_3":"role_zahl_3","role_zahl_4":"role_zahl_4","role_zahl_5":"role_zahl_5","erstellung_datum":"erstellung_datum"};

MYSQL_KMK = {"kanal_id":"kanal_id","kanal_name":"kanal_name","kanal_symbol":"kanal_symbol","benutzer_id":"benutzer_id","benutzer_name":"benutzer_name","benutzer_symbol":"benutzer_symbol","global_status":"global_status","global_ban_status":"global_ban_status","spezial_status":"spezial_status","registration_datum":"registration_datum"};
MYSQL_AS = {"kanal_id":"kanal_id","kanal_name":"kanal_name","benutzer_id":"benutzer_id","benutzer_name":"benutzer_name","benutzer_symbol":"benutzer_symbol","zahl":"zahl"};
MYSQL_E = {"kanal_id":"kanal_id","benutzer_id":"benutzer_id","ereignisse_name":"ereignisse_name","ereignisse_datum":"ereignisse_datum","ereignisse_zeit":"ereignisse_zeit","ereignisse_status":"ereignisse_status"};
MYSQL_KB = {"kanal_id":"kanal_id","kanal_name":"kanal_name","benutzer_id":"benutzer_id","benutzer_name":"benutzer_name","benutzer_ban_grund":"benutzer_ban_grund","benutzer_ban_datum":"benutzer_ban_datum"};
MYSQL_GB = {"benutzer_id":"benutzer_id","benutzer_name":"benutzer_name","benutzer_ban_grund":"benutzer_ban_grund","benutzer_ban_status":"benutzer_ban_status"};
MYSQL_NV = {"benutzer_id":"benutzer_id","benutzer_name":"benutzer_name"};
MYSQL_MOD = {"kanal_id":"kanal_id","kanal_name":"kanal_name","kanal_symbol":"kanal_symbol","kanal_besitzer_id":"kanal_besitzer_id","bot_id":"bot_id","bot_administration_id":"bot_administration_id","discord_mod":"discord_mod"};
#-----------------------------------------------------------------------------------------------------------------------
#BOT INTERFACE MESSAGES

CLIENT_MESSAGES = {
    "client_online": "System ready.",
    "client_recording": "Data recording.",
    "client_mysql_connect_suc": "Mysql ready",
    "client_mysql_connect_uns": "Mysql offline",
    "server_joined": "Online",
    "on_message": "Writte",
    "on_message_delete": "Delete",
    "on_message_edit": "Edit",
    "on_user_update": "Update",
    "image_upload": "Upload",
    "client_joined": "Joined",
    "client_banned": "Banned",
    "on_guild_joined": "Guild Join",
    "on_guild_removed": "Guild Remove",
    "on_guild_update": "Guild Update",
    "on_command_rsn_succ": "Registration Confirmed",
    "on_command_rsn_fail": "Registration Failed",
    "on_command_drop_succ": "Statistic Updated",
    "on_command_drop_added": "Statistic Added",
};

#-----------------------------------------------------------------------------------------------------------------------
#DISCORD INTERFACE MESSAGES

DISCORD_MESSAGES = {
    "ban_reason":"Uždraustas nikas.",
    "member_joined":"prisijungė prie kanalo.",
    "member_created_at":"Vartotojo paskyra buvo sukurta",
};

DISCORD_COMMANDS = [
    [".reg","⬑ rsn registracija. Pavyzdys: **.reg FaustRecht**."],
    [".check","⬑ žaidėjo patikrinimas. Pavyzdys: **.check FaustRecht**."],
    [".cox","⬑ cox kc registracija. Pavyzdys: **.cox 150**."],
    [".tob","⬑ tob kc registracija. Pavyzdys: **.tob 150**."],
    [".gstats", "⬑ globali statistika."],
    [".stats", "⬑ serverio statistika."],
    [".grank", "⬑ globalus rangas."],
    [".rank", "⬑ serverio rangas."],
    [".dcn", "⬑ discordo acc registracijos data. Pavyzdys: **.dcn @FaustRecht**."],
    [".post mass","⬑ mass cox evento publikavimas. Pavyzdys: **.post mass 20:00**."],
    [".connect", "⬑ prisijungimas prie globalaus Beobachter pokalbio kanalo."],
    [".disconnect", "⬑ atsijungimas nuo globalaus Beobachter pokalbio kanalo."],
]

CHECK_MODULE = {
    "rj-check":"!rw ",
};

GWD_POSITIV = "Žaidėjas gali dalyvauti God Wars Dungeon bossinime.";
COX_POSITIV = "Žaidėjas gali dalyvauti God Wars Dungeon bossinime ir Chambers of Xeric raiduose.";
GWD_NEGATIV = "Žaidėjas negali dalyvauti God Wars Dungeon bossinime ar Chambers of Xeric raiduose.";
COX_NEGATIV = "Žaidėjas gali bossinti God Wars Dungeone, tačiau neturėtu dalyvauti Chambers of Xeric raiduose.";

STATISTIC = [
    {"attack":90,"strength":90,"defence":90,"range":90,"magic":90,"prayer":70,"herblore":78,"farming":80},
    {"attack":80,"strength":80,"defence":80,"range":80,"magic":80,"prayer":70},
];

WORDS = [
    "Pirmoji vieta",
    "Antroji vieta",
    "Trečioji vieta",
    "Ketvirtoji vieta",
    "Penktoji vieta",
    "Šeštoji vieta",
    "Septintoji vieta",
    "Aštuntoji vieta",
    "Devintoji vieta",
    "Dešimta vieta",
];

DISCORD_EMOJIS = {
    "positiv":"✅",
};

DISCORD_MODULE_IMAGES = {
    "gp":"https://cdn.discordapp.com/attachments/601499258767671321/601501841154637845/gp.png",
};

DISCORD_RANK_IMAGES = [
    "https://cdn.discordapp.com/attachments/601499258767671321/601500942730395660/1.gif",
    "https://cdn.discordapp.com/attachments/601499258767671321/601500958354178073/0.gif",
    "https://cdn.discordapp.com/attachments/601499258767671321/601501008224321537/2.gif",
];

#-----------------------------------------------------------------------------------------------------------------------
#DISCORD STRUCTURE INITIALIZATION

DISCORD_GROUP = "BEOBACHTER - PVM";
DISCORD_REGISTRATION = "registracija";
DISCORD_COUNT = "uždarbis";
DISCORD_CHECK = "check-rsn";
DISCORD_EVENT = "eventai";
DISCORD_GLOBAL = "global-pokalbiai";
DISCORD_MEMBER = "narių-pokalbiai";
DISCORD_BEOBACHTER = "beobachter";
DISCORD_LOYAL_SPLITTER = "Loyal - Splitter";
DISCORD_TRUSTED_SPLITTER = "Trusted - Splitter";
DISCORD_AVERAGE_SPLITTER = "Average - Splitter";
DISCORD_NOVICE_SPLITTER = "Novice - Splitter";
DISCORD_EVENT_ORGANIZER = "Event - Organizer";
DISCORD_GLOBALS = "Beobachter - Global";
DISCORD_MEMBERS = "Narys";
DISCORD_EVERYONES = "@everyone";

DISCORD_REGISTRATION_T = "✙ Beobachter registracija.";
DISCORD_COUNT_T = "✙ Beobachter narių uždarbis.";
DISCORD_CHECK_T = "✙ Beobachter narių RSN patikrinimas.";
DISCORD_EVENT_T = "✙ Beobachter narių organizuojami eventai.";
DISCORD_GLOBAL_T = "✙ Beobachter globalus pokalbiai.";
DISCORD_MEMBER_T = "✙ Beobachter narių pokalbiai.";
DISCORD_BEOBACHTER_T = "✙ Beobachter valdymo pultas.";

DISCORD_ZAHL_2 = 100000000;
DISCORD_ZAHL_3 = 500000000;
DISCORD_ZAHL_4 = 1000000000;
DISCORD_ZAHL_5 = 2000000000;

IMAGES = {
    "logo":"./structure/logo.png",
    "reg_example":"./structure/reg_example.png",
    "zahl_example":"./structure/zahl_example.png",
    "ereignisse_example":"./structure/ereignisse_example.png",
    "split":"./structure/split.png",
    "id":"./structure/id.gif",
    "emoji":"./structure/emoji.gif",
};