# Установка и запуск

1. Клонируйте репозиторий:

```bash
$ cd ~
$ git clone https://github.com/veeedmochka/fghj34.git
$ cd fghj34
```

2. Создайте базу данных:

```bash
CREATE DATABASE fghj34;
CREATE USER fghj_user WITH PASSWORD 'password';
ALTER ROLE fghj_user SET client_encoding TO 'utf8';
ALTER ROLE fghj_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE fghj_user SET timezone TO 'Europe/Minsk';
GRANT ALL PRIVILEGES ON DATABASE fghj34 TO fghj_user;
\c fghj34
GRANT ALL ON SCHEMA public TO ghjk_user;
GRANT ALL ON SCHEMA public TO public;
```

3. Добавьте `.env` файл с переменными окружения:

```bash
DEBUG=True
DB_URI=postgresql+psycopg2://ghjk_user:password@localhost/ghjk34
```

4. Создайте и активируйте виртуальное окружение:

```bash
$ python3 -m venv venv
$ . venv/bin/activate
```

5. Установите необходимые зависимости:

```bash
$ pip install -r requirements.txt
```


6. В каталоге `/etc/systemd/system/` создайте файлы `gunicorn.service` и `gunicorn.socket`:

gunicorn.service:

```bash                                                                                          
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=root
WorkingDirectory=/home/veeedmochka/fghj34
ExecStart=/home/veeedmochka/fghj34/venv/bin/gunicorn --workers 5 --bind unix:/run/gunicorn.sock wsgi:app

[Install]
WantedBy=multi-user.target
```

gunicorn.socket:
```bash
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

7. Копируем папку с статическими файлами:

```bash
$ cd /var/www/
$ sduo mkdir fghj34
$ cd fghj34 
$ sudo cp -r /home/veeedmochka/fghj34/static/ /var/www/fghj34/static/
```

8. В каталоге `/etc/nginx/sites-available/` создайте файл `fghj34`:

```bash
server {
    listen 80;
    server_name localhost;

    location /static/ {
        root /var/www/fghj34/;
    }

    location / {
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

9. Создайте символьную ссылку на этот файл в каталоге `/etc/nginx/site-enabled/`:

```bash
$ sudo ln -s /etc/nginx/sites-available/fghj34 /etc/nginx/sites-enabled/
```

10. Запустите службу gunicorn:

```bash
$ sudo systemctl enable gunicorn
$ sudo systemctl start gunicorn
```

11. Запустите nginx:

```bash
$ sudo service nginx start
```

Теперь приложение доустпно по адресу `http://localhost/`
