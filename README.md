Here's a **README.md** template for the project based on the code you provided. It includes sections for setup, description, and instructions on how to run the bot. You can customize it as needed.

---

# Telegram Chat Bot

This is a Telegram bot built using the `aiogram` library. The bot provides several functionalities such as user profile management, chat interactions, friend requests, media handling, tipping system, and referral code system. The bot is designed to work in private chats and processes a variety of commands, messages, and media.

## Features

- **User Profiles**: Users can register, enter referral codes, and manage their profiles.
- **Friendship System**: Users can send, accept, or reject friend requests.
- **Chat Matching**: Users can search for partners, connect, and chat.
- **Tip System**: Users can send tips to other users.
- **Media Handling**: The bot can process various types of media (photos, videos, stickers, etc.).
- **Referral System**: Users can join via referral codes, which can track user connections.

## Requirements

- Python 3.8+
- `aiogram` library
- Database connection (SQLite, PostgreSQL, etc.)
- Telegram Bot Token (Create your bot with [BotFather](https://core.telegram.org/bots#botfather))

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/your-repository.git
   ```

2. Navigate to the project directory:

   ```bash
   cd your-repository
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your **Telegram Bot Token** and database configuration in the `config.py` file:

   - **`TOKEN`**: Add your Telegram bot token.
   - **Database Configuration**: Ensure the database is correctly set up for storing user profiles, chats, and balances.

5. (Optional) Customize any other settings or bot messages according to your needs.

## Usage

1. **Start the Bot**: Once everything is set up, you can run the bot by executing:

   ```bash
   python bot.py
   ```

2. **Commands**:
   - `/start`: Initialize the bot and begin interaction.
   - **Friendship System**:
     - **Add Friends**: Use the "➕ Add" button to send friend requests.
     - **Accept/Reject Requests**: Partner receives buttons to accept or reject friendship requests.
   - **Find Partner**: Use the "🔍 Find a partner" button to search for a chat partner.
   - **Disconnect**: Use the "🚫 Disconnect 🚫" button to leave a chat.
   - **Kiss**: Send a tip using the "💋 Kiss" button.
   - **Stop Searching**: Stop looking for a partner with the "🚫 Stop searching" button.

3. **Media Handling**:
   - Users can send different types of media (voice, photo, video, stickers), and the bot will forward these to the partner in the chat.
   - The bot handles media types including: `voice`, `photo`, `video`, `sticker`, `audio`, `document`, and `video_note`.

4. **Referral System**:
   - Users can enter a referral code to register. If the code is valid, they are registered with the system and a profile is created.


## Key Components

- **Bot Handlers**:
  - `add_friend_request`: Handles the logic for sending and processing friend requests.
  - `find_partner`: Matches users with a partner based on the queue system.
  - `process_greetings`: Recognizes greetings and sends welcome messages.
  - `process_text_commands`: Processes commands like "Add", "Find a partner", and "Disconnect".
  - `process_message_count`: Keeps track of user messages in the chat.
  
- **Profile Management**:
  - Users can register and update their profiles using referral codes.
  - Profile data is saved in the database for future interactions.
  
- **Friendship Logic**:
  - Manages adding and removing friends, as well as limiting the number of friends a user can have.

- **Balance and Tip System**:
  - Users can send tips (💋 Kiss) to their partners.
  - The bot deducts the amount from the sender's balance and adds it to the receiver's balance.

## Configuration

1. **Bot Token**: You can get your token from [BotFather](https://core.telegram.org/bots#botfather) and place it in `config.py`.

2. **Database Setup**: Configure your database in `database.py`. The bot assumes that there is a `Database` class that handles profile creation, friend management, balance tracking, etc.

3. **Keyboard Customization**: The bot uses a custom keyboard setup for inline and reply buttons, defined in `app.keyboards.keyboards`. You can modify these buttons based on your needs.

## Contributing

Feel free to fork this project and submit pull requests if you want to contribute improvements or new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Tips

- Make sure you have a Telegram bot token ready and ensure the bot has proper permissions to interact with users and manage messages.
- Test the bot in a development environment before deploying it to production.
- The bot's functionality can be extended easily by adding new handlers, commands, or media types.

---

This README provides an overview of the bot, setup instructions, key components, and usage guidelines for your Telegram bot project. You can adjust the details as necessary depending on your actual code and requirements.