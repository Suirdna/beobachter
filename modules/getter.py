import mysql.connector
from configs import bot_config


def getData(sql):
    try:
        database = mysql.connector.connect(
            host=bot_config.MYSQL_CONFIGURATION["server"],
            user=bot_config.MYSQL_CONFIGURATION["username"],
            passwd=bot_config.MYSQL_CONFIGURATION["password"],
            database=bot_config.MYSQL_CONFIGURATION["database"],
            port=bot_config.MYSQL_CONFIGURATION["port"],
        );
        control = database.cursor();
        control.execute(sql);
        data = control.fetchall();
        return data;
    except Exception as error:
        print(error);
    finally:
        control.close();

def setData(sql):
    database = mysql.connector.connect(
        host=bot_config.MYSQL_CONFIGURATION["server"],
        user=bot_config.MYSQL_CONFIGURATION["username"],
        passwd=bot_config.MYSQL_CONFIGURATION["password"],
        database=bot_config.MYSQL_CONFIGURATION["database"],
        port=bot_config.MYSQL_CONFIGURATION["port"],
    );
    control = database.cursor();
    control.execute(sql);
    database.commit();