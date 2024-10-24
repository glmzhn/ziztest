test project

1 step - clone repo

2 step - run command `docker-compose build`

3 step - run command `docker-compose run --rm web sh -c "python manage.py makemigrations"`

4 step - run command `docker-compose run --rm web sh -c "python manage.py migrate"`

5 step - run command `docker-compose run --rm web sh -c "python manage.py createsuperuser"`

6 step - after creating super user run command `docker-compose up`

7 step - get JWT Bearer token, path: /api/token/, if it's expired get the new access token via refresh token, path: /api/token/refresh/

The whole API Documentation is available on the path: /api/v1/schema/docs/

The admin panel is available on the path: /admin

Filtration by the status - GET /api/v1/tasks/?status=pending

Filtration by the date = GET /api/v1/tasks/?due_date=2024-10-24

Filtration by the status and date - GET /api/v1/tasks/?status=overdue&due_date__lt=2024-10-24

Filtration by the title or description = GET /api/v1/tasks/?search=Task N1

Good luck ;)
