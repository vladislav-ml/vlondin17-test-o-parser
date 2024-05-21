from dataclasses import dataclass

from dotenv import dotenv_values

from sitemain import settings


@dataclass
class Bot:
    bot_token: str
    admin_id: str


@dataclass
class Database:
    host: str
    port: str
    db_name: str
    user: str
    password: str


@dataclass
class Setting:
    bot: Bot
    database: Database


def get_settings(path: str):
    config = dotenv_values(path)
    return Setting(
        bot=Bot(
            bot_token=config['TOKEN'],
            admin_id=config['ADMIN_ID'],
        ),
        database=Database(
            host=config['DB_HOST'],
            port=config['DB_PORT'],
            db_name=config['DB_NAME'],
            user=config['DB_USER'],
            password=config['DB_PASSWORD'],
        )
    )


settings = get_settings(settings.NAME_ENV_FILE)
