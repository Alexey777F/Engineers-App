 # CRM-sys
 ![CRM-sys](https://github.com/Alexey777F/Engineers-App/blob/main/eng_app2.png)
 * Система распределения задач для сотруников.
 * Система назначает сотрудника в зависимости от его направления деятельности, отпуска, количества текущих задач и даты последней переданной ему задачи. 
 ___
 * 

## Технологии - Technologies
 * Docker-compose
 * Python(image): 3.9.18-bullseye
 * Postgresql(image): postgres:14.8-alpine3.18ут
 * Flask(v. 2.3.2)
 * Sqlalchemy(v. 2.0.23)
 * psycopg2-binary(v. 2.9.9)
 * WTForms(v. 3.1.2)
 * Flask-WTF(v. 1.2.1)
 
## Установка с помощью Docker-compose - Install with Docker-compose
 * Установите Docker Desktop под вашу ОС
 * Необходимо скопировать все содержимое репозитория в отдельный каталог.
 * Установите виртуальное окружение на вашей ОС, на Mac OS python3 -m venv my_env
 * Активируйте виртуальное окружение на вашей ОС, на Mac OS source my_env/bin/activate
 * Откройте файл docker-compose.yml и заполните необходимыми данными(секретный ключ, хост, порт и настройки базы данных).
 * Запустите сборку образа и создания контейнера с помощью команды: docker-compose up --build
 * Приложение запущено в контейнере 
 ___
 * Install Docker Desktop on your OS
 * It is necessary to copy all important repositories to a separate directory.
 * Install a virtual environment on your OS, on Mac OS python3 -m venv my_env
 * Activate the virtual environment in your OS, in the Mac OS source my_env/bin/activate.
 * Open the docker-compose.yml file and fill in the necessary data (secret key, host, port and database settings).
 * Start building the image and creating the container using the command: docker-compose up --build
 * The application is running
   
## Как работает - How does it works
  * Примеры работы приложения
  * Application examples
  ![CRM-sys](https://github.com/Alexey777F/Engineers-App/blob/main/eng_app1.png)
  ![CRM-sys](https://github.com/Alexey777F/Engineers-App/blob/main/eng_app2.png)
  ![CRM-sys](https://github.com/Alexey777F/Engineers-App/blob/main/eng_app3.png)
  ![CRM-sys](https://github.com/Alexey777F/Engineers-App/blob/main/eng_app4.png)
  ![CRM-sys](https://github.com/Alexey777F/Engineers-App/blob/main/eng_app5.png)

