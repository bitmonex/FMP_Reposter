import time
import asyncio
import os
from telethon.sync import TelegramClient
from telethon import types, errors

# Определение пути к файлу лога
LOG_FILE = 'log.txt'

# Определение API_ID и API_HASH
API_ID = ''
API_HASH = ''

# Определение DESTINATION_CHANNEL_ID
DESTINATION_CHANNEL_ID = 'name_channel'
source_channels = ['1','2','3']

async def main():
    # Проверка существования файла лога и создание, если его нет
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w'):
            pass

    # Определение клиента Telethon
    client = TelegramClient('session_name', API_ID, API_HASH)

    async with client:
        for source_channel_name in source_channels:
            # Получение доступа к каналу и пересылка сообщений
            source_channel = await client.get_entity(source_channel_name)
            async for message in client.iter_messages(source_channel, limit=10):
                if not isinstance(message, types.MessageService):
                    if not message_exists_in_log(message.id):
                        try:
                            await client.forward_messages(DESTINATION_CHANNEL_ID, message)
                            log_message(message.id, message.text)
                            print(f"Repost x {source_channel.title}")
                        except errors.FloodWaitError as e:
                            print(f"Error forwarding message: {e}")
                        except errors.MessageIdInvalidError as e:
                            print(f"Error forwarding message: {e}")
                        except Exception as e:
                            print(f"Error forwarding message: {e}")

def message_exists_in_log(message_id):
    with open(LOG_FILE, 'r') as file:
        for line in file:
            if str(message_id) in line:
                return True
    return False

def log_message(message_id, message_text):
    with open(LOG_FILE, 'a') as file:
        file.write(f"{message_id} | {message_text}\n")

# Запуск основного цикла asyncio
async def run_main_periodically():
    while True:
        await main()
        await asyncio.sleep(10)

# Запуск основной функции
asyncio.run(run_main_periodically())
