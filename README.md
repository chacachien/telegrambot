# Telegram Bot 

## Overview

This repository contains the source code for a Telegram bot developed in Python. The bot leverages the Telegram Bot API and performs various tasks based on user commands. It is designed to be easily extendable and customizable for different use cases.

## Features

- **Command Handling:** The bot responds to specific commands provided by users.
- **Scheduled Jobs:** Implements scheduled tasks using the schedule library.
- **Web Scraping:** Utilizes Selenium for web scraping tasks.
- **Modular Structure:** The code is organized into modular components for better maintainability.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python packages: `python-telegram-bot`, `schedule`, `selenium`


# Setting Up Your Telegram Bot

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/chacachien/telegrambot.git
    cd telegrambot
    ```

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Your Telegram Bot Token:**
   Obtain a token from the BotFather on Telegram and add it to the `.env` file.

4. **Run the Bot:**
   ```bash
   python main.py
    ```

