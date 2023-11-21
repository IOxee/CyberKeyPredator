<h1 align="center">Cyber Key Predator - Unleash the Game Hunter Within</h1>

![Header Image](https://github.com/IOxee/CyberKeyPredator/assets/48241519/e7431e6d-cd9f-4f7b-af5e-063fe04a0e8c)


This script uses the `telethon` library to interact with Telegram and `selenium` for automating actions in a web browser. Its goal is to monitor messages in a Telegram channel, extract game keys, and then attempt to claim them automatically on a Steam account.

## 🚀 Getting Started

### 📋 Prerequisites

1. **Python 3**: You must have Python 3 installed on your machine.
2. **Python Libraries**: You will need `telethon`, `selenium`, and `asyncio`. Install them using pip:
   ```bash
   pip install telethon selenium asyncio webdriver_manager
   ```
3. **Google Chrome and ChromeDriver**: You must have Google Chrome and ChromeDriver installed.

### 🔑 Telegram API Configuration

- Obtain your `api_id`, `api_hash`, and `phone` from [Telegram Apps](https://my.telegram.org/auth?to=apps).
- Replace these values in the script accordingly.

### 📝 Script Configuration

- **Telegram Channel**: Define the `channel_username` of the channel that the bot should monitor.
- **Language**: The script supports Spanish (`ESP`) and English (`EN`). Configure the `language` according to your preference.
- **Chrome User Data Directory**: Adjust `user_data_dir` to the path of your Chrome user profile directory.

### ⚙ How the Script Works

The script performs the following actions:

1. **Message Monitoring**: Listens for messages in the specified Telegram channel.
2. **Message Data Extraction**: Extracts the name of the game and the key from the message.
3. **Claimed Games Verification**: Checks if the game has already been claimed before.
4. **Browser Automation**: Opens the activation URI in Chrome and performs automatic actions to claim the game.
5. **Error Handling**: Detects and manages errors, such as keys already activated on another account.

## 🛠️ Execution

To run the script, follow these steps:

1. Make sure you have all dependencies installed and the environment set up as described above.
2. Run the script in your Python environment:
   ```bash
   python hunter.py
   ```

## 📄 License

This script is open source and distributed under the MIT license.
