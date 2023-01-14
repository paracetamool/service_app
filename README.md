<h1 align="center">Пример сервиса с основными фичами по оптимизации</h1>


---
<h3>Для запуска системы необходимо выполнить следующие операции</h3> 

---
1. Склонировать проект на локальный компьютер

    `git clone https://..`

2. Выполнить миграции с помощью самоудаляемого образа:

    `docker-compose run --rm web-app sh -c "./manage.py makemigrations"`

    `docker-compose run --rm web-app sh -c "./manage.py migrate"`

3. забилдить и запустить docker

    `docker-compose build`


    `docker-compose up`

