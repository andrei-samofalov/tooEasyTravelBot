## Too Easy Travel BOT
Это простой Телеграм бот, с помощью него можно 
получать информацию об отелях, расположенных по 
всему миру, в работе использует Rapid Api.

### Основные технологии и библиотеки
* Python (3.10);
* pyTelegramBotAPI;
* requests;
* python-dotenv.

### Установка
1. Скопируйте все содержимое репозитория в отдельный 
каталог.

2. Установите все библиотеки из [requirements.txt](requirements.txt).
Вы можете использовать команду 
> pip install -r requirements.txt

3. Файл .env.template переименуйте в .env. Откройте 
его и заполните необходимые данные (токен бота 
необходимо получить у [BotFather](https://t.me/BotFather), токен 
RapidAPI получить на сайте [RapidAPI](https://rapidapi.com/hub)).

4. Запустите файл [main.py](main.py).