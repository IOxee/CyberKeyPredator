from telethon.sync import TelegramClient, events
from telethon.tl.types import InputPeerChannel
import asyncio
import datetime
import re, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Telegram API credentials: https://my.telegram.org/auth?to=apps
api_id = ''  # ADD HERE YOUR API ID 
api_hash = ''  # ADD HERE YOUR API HASH
phone = ''  # PUT HERE THE TOKEN OF BOT OR PUT YOUR PHONE WITH CODE OF COUNTRY LIKE +34123123123 IF CHANNEL PRIVATED
channel_username = ''  # Channel username

language = 'ESP'  # Options: 'ESP', 'EN'
user_data_dir = r"C:\Users\YOUR USER NAME HERE!!!\AppData\Local\Google\Chrome\User Data"  # The 'r' before the string indicates a raw string

message_params = {
    'Game': {
        'ESP': 'Juego: ',
        'EN': 'Game: '
    },
    'Key': {
        'ESP': 'Clave: ',
        'EN': 'Key: '
    }
}

# I18N - Internationalization 
messages = {
    'ErrorClaimed': {
        'ESP': "La clave de producto ya ha sido activada en otra cuenta de Steam.",
        'EN': "The product key has already been activated on another Steam account."
    },
    'ErrorOccurred': {
        'ESP': "Ha ocurrido un error: ",
        'EN': "An error occurred: "
    },
    'UnclaimedGameDetected': {
        'ESP': "Juego no reclamado detectado: ",
        'EN': "Unclaimed game detected: "
    },
    'ActivationURI': {
        'ESP': "URI de activación: ",
        'EN': "Activation URI: "
    },
    'WaitingForNewMessages': {
        'ESP': "Esperando nuevos mensajes...",
        'EN': "Waiting for new messages..."
    },
    'GameAlreadyClaimedOrInvalidMessage': {
        'ESP': "Juego ya reclamado o mensaje inválido.",
        'EN': "Game already claimed or invalid message."
    },
    'StartingMessageWaitingProgram': {
        'ESP': "Iniciando programa de espera de mensajes...",
        'EN': "Starting message waiting program..."
    }
}

error_patterns = {
    'ESP': "ya ha sido activada por otra cuenta de Steam",
    'EN': "has already been activated on another Steam account"
}


def is_game_already_claimed(game):
    """Checks if a game has already been claimed."""
    # if claimed_games.txt doesn't exist, create it
    if not os.path.exists('claimed_games.txt'):
        with open('claimed_games.txt', 'w'): pass

    with open('claimed_games.txt', 'r') as file:
        claimed_games = file.readlines()
    return game in [g.strip() for g in claimed_games]

def add_claimed_game(game):
    """Adds a game to the list of claimed games."""
    with open('claimed_games.txt', 'a') as file:
        file.write(game + '\n')

def extract_message_data(message):
    """Extracts the game name and key from the message."""
    ## i neeed get the game_match checking the message_params dictionary and the language variable to get the correct paramGame value and re.search it in the message
    gameString = message_params['Game'][language]
    keyString = message_params['Key'][language]

    game_match = re.search(gameString + r'(.+?) -', message)
    key_match = re.search(keyString + r'(.+)', message)

    if game_match and key_match:
        return game_match.group(1), key_match.group(1)
    return None, None

def open_uri_in_browser(uri, game):
    """Opens the provided URI in the browser and performs automatic actions."""
    options = Options()
    
    # Ensure the path to the user profile is correct and properly escaped
    options.add_argument(f"user-data-dir={user_data_dir}")

    # Ensure the ChromeDriver installation is appropriate
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(uri)

    try:
        # Wait until the subscriber agreement checkbox is clickable and click
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='checkbox'][name='accept_ssa']"))
        ).click()

        # Wait until the "Continue" button is clickable and click
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "register_btn"))
        ).click()

        # Wait to see if an error message appears after clicking Continue
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "error_display"))
        )

        # Check if the error message indicates that the key has already been activated
        if error_patterns[language] in error_message.text:
            print(messages['ErrorClaimed'][language])
            print(messages['WaitingForNewMessages'][language])
        else:
            add_claimed_game(game)

    except Exception as e:
        print(f"{messages['ErrorOccurred'][language]}{e}")
    finally:
        driver.quit()

async def main():
    """Main function to start the Telegram client and wait for messages."""
    async with TelegramClient(phone, api_id, api_hash) as client:

        @client.on(events.NewMessage(chats=channel_username))
        async def new_message_listener(event):
            """Function triggered with each new message in the channel."""
            game, key = extract_message_data(event.message.text)
            if game and key and not is_game_already_claimed(game):
                uri = f"https://store.steampowered.com/account/registerkey?key={key}"
                print(f"{messages['UnclaimedGameDetected'][language]}{game}")
                print(f"{messages['ActivationURI'][language]}{uri}")
                open_uri_in_browser(uri, game)
            else:
                print(messages['GameAlreadyClaimedOrInvalidMessage'][language])

        print(messages['WaitingForNewMessages'][language])
        await client.run_until_disconnected()

print(messages['StartingMessageWaitingProgram'][language])
asyncio.run(main())
