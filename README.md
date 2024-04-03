 # CRM-sys
 ![CRM-sys](https://github.com/Alexey777F/Engineers-App/blob/main/eng_app2.png)
 * Система распределения задач для сотруников.
 * Система назначает сотрудника в зависимости от его направления деятельности, отпуска, количества текущих задач и даты последней переданной ему задачи.
 * Алгоритм работы приложения:
 * Сначала программа получает на вход, из выпадающего списка всех направлений, направление на которое необходимо поставить задачу например DWH.
 * Далее программа выбирает всех потенциальных сотрудников у которых есть данное направление.
 * Следом идет отсеивание тех потенциальных сотрудников которые в отпуске, если оба сотрудника в отпуске, то задачу дать некому и появляется соответствующее уведомление, если один в отпуске то даем задачу второму, если оба не в отпуске, то фильтруем дальше по количеству задач.
 * Далее идет фильтрация по количеству задач и у кого меньше задач тому и даем новую, если задач поровну, то идем на следующий этап.
 * После фильтрации по количеству задач, мы фильруем по дате последней переданной задачи, даем задачу тому инженеру у которого дата последней задачи стоит раньше чем у второго, если даты равны то даем задачу первому инженеру.


 ___
 * System for distributing tasks for employees.
 * The system assigns an employee depending on his area of ​​activity, vacation, number of current tasks and the date of the last task transferred to him.
 * Application algorithm:
 * First, the program receives as input, from a drop-down list of all directions, the direction in which the task needs to be set, for example DWH.
 * Next, the program selects all potential employees who have this direction.
 * Next comes the screening of those potential employees who are on vacation, if both employees are on vacation, then there is no one to give the task and a corresponding notification appears, if one is on vacation, then we give the task to the second, if both are not on vacation, then we filter further by the number of tasks.
 * Next comes filtering by the number of tasks and whoever has fewer tasks is given a new one; if there are equal numbers of tasks, then we go to the next stage.
 * After filtering by the number of tasks, we filter by the date of the last transferred task, give the task to the engineer whose last task date is earlier than the second one, if the dates are equal, then we give the task to the first engineer.

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

