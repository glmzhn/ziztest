Deploy/

1 step - clone repo

2 step - create .env file with "DB_NAME", DB_USER" and "DB_PASSWORD" settings

3 step - run command `docker-compose build`

4 step - run command `docker-compose run --rm web sh -c "python manage.py migrate"`

5 step - run command `docker-compose run --rm web sh -c "python manage.py createsuperuser"`

6 step - after creating super user run command `docker-compose up`


API Work/

Get JWT Bearer token, path: /api/token/, if it's expired get the new access token via refresh token, path: /api/token/refresh/

The whole API Documentation is available on the path: /api/v1/schema/docs/

The admin panel is available on the path: /admin

Filtration by the status - GET /api/v1/tasks/?status=pending

Filtration by the date = GET /api/v1/tasks/?due_date=2024-10-24

Filtration by the status and date - GET /api/v1/tasks/?status=overdue&due_date__lt=2024-10-24

Filtration by the title or description = GET /api/v1/tasks/?search=Task N1


Tests/

run command -  `docker-compose exec web sh`, and then run - `pytest test_tasks.py`

--------------------------------------------------------------------------------------------------------------------------------------------------------|

Good luck ;)
