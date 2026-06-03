To use this bot you will need to create a bot with telegram bot maker, 
then you must make a .env file with the api key and the bot name, like this:
API_BOT_TOKEN=<api key>
BOT_HANDLE=@<bot name>
To start the bot in a terminal you will need to create a python venv and install
the requierements using pip install -r "requirements.txt", the write in the terminal:
python3 main.py

To start the docker you need to use; docker run --env-file .env telegram-gamebot
To start the docker and have access to the docker terminal, you need to use;
sudo docker run -it --env-file .env telegram-gamebot sh 
and then you will start the bot like in the normal terminal