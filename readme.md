To use this bot you will need to create a bot with telegram bot maker, <br>
then you must make a .env file with the api key and the bot name, like this:<br>

API_BOT_TOKEN= api key<br>
BOT_HANDLE= @bot name<br>

To start the bot in a terminal you will need to create a python venv and install<br>
the requierements using pip install -r "requirements.txt", the write in the terminal:<br>
python3 main.py<br>

To start the docker you need to use; <br>
docker build -t botsname <br>
docker run --env-file .env telegram-gamebot<br>

To start the docker and have access to the docker terminal, you need to use;<br>
sudo docker run -it --env-file .env telegram-gamebot sh <br>
and then you will start the bot like in the normal terminal<br>