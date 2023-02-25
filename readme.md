## Too Easy Travel BOT

Телеграм бот, с помощью которого можно
получать информацию об отелях, расположенных по
всему миру, в работе использует [Hotels Api](https://rapidapi.com/apidojo/api/hotels4/).

### Основные технологии и библиотеки

* Python (3.10);
* pyTelegramBotAPI;
* sqlite3;
* requests;
* jsonpointer;
* multiprocessing;
* logging;
* python-dotenv;
* Docker.

### Установка на локальном сервере:

1. Скопируйте все содержимое репозитория в отдельный
   каталог.

2. Установите все библиотеки из [requirements.txt](requirements.txt).
   Вы можете использовать команду

   `pip install -r requirements.txt`

3. Файл .env.template переименуйте в .env. Откройте
   его и заполните необходимые данные (токен бота
   необходимо получить у [BotFather](https://t.me/BotFather), токен
   RapidAPI получить на сайте [RapidAPI](https://rapidapi.com/hub)).

4. Запустите файл [main.py](main.py).

### Установка на удаленном сервере Linux:

1. [Установите Docker](https://docs.docker.com/engine/install/ubuntu/) на удаленном сервере
2. Вы должны быть зарегистрированы на сайте [Dockerhub](https://hub.docker.com/), также необходимо пройти
   аутентификацию (`$ docker login`) на удаленном сервере
3. Введите команды

   `$ docker build -t <image_name> <path>` где `<image_name>` - название образа, а `<path>` - путь, где необходимо искать
   докерфайл (точка, если Вы находитесь в нужном каталоге)

   `$ docker tag <image_name> <your_login>/<image_rep>` где `<your_login>` - Ваш логин на DockerHub, `<image_rep>` -
   название репозитория на DockerHub

   `$ docker push <your_login/image_rep>`

4. Теперь Вы можете запустить приложение, используя свой 
собственный образ docker:

   `$ docker run <your_login/image_rep>`