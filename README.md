Simplified backend for X    [CI/CD github-actions](https://github.com/VladimerKhasia/fastapi_X/blob/main/.github/workflows/main.yml/badge.svg)

`fastapi` `pydantic` `sqlalchemy 2` `alembic` `postgresql` `pytest` `docker` `CI/CD github-actions` etc.

>TODO: X recently added grok to the application. To ensure learners with low-end devices can still benefit from this repository, we will liekly do the same but with a very small local model, likely Gemma-2b-it. 

Quick overview of current version:
![Capture](https://github.com/VladimerKhasia/fastapi_X/assets/56228503/f9c0d160-f737-4d26-8185-6fd88737c43d)


You need to add .env file in the root directory. Example .env file looks like this:
```
DB_USERNAME = postgres
DB_PASSWORD = your_password
DB_HOST = localhost     
DB_PORT = 5432
DB_NAME = postgres 
SECRET_KEY = "09d26myi889fmd0k49d8r0mm66b7a9563b93f7099f6njf78c9fmd88wnq88w9"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#### f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#### DB_NAME = #postgres #fastapi_X 
#### DB_HOST = #postgres #localhost #postgres instead of localhost - docker directly references to postgres
```
>To get a SECRET_KEY string run this command but use git bash terminal if you are on windows:  `openssl rand -hex 32` see [documentation](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/?h=jwt) 

Docker Image is uploaded here: [ladokhasia/fastapi_x](https://hub.docker.com/r/ladokhasia/fastapi_x)

REFERENCE: [Sanjeev Thiyagarajan](https://www.youtube.com/watch?v=0sOvCWFmrtA&t=44689s) and many thanks to him!

Deployment to the Ubuntu VM:

-------------------------------------------------------------------------- connect local postgres to remote Ubuntu

- `ssh root@IP of a host where your vm will live`  type yes, type your password
- `sudo apt update && sudo apt upgrade -y`
- check python version and install whatever version you need
- `sudo apt install python3-pip -y`
- `sudo apt install postgresql postrgesql-contrib -y`
- use cli tool psql to connect to postgres on from inside the VM requres to take a role of automatically created postgres user first via su postgres because peer authentication (check users with: `sudo cat /etc/passwd`)
- `su postgres`
- `psql -U postgres`
- `\password postgres` (to create a password as it trigers you to write a password you want)
- `\q`  (to exit postresql)
- `exit` (brings you back to root user from postgres user)
- `cd /etc/postgresql/12/main`  (12 is just whatever version of postgresql are you using)

- `sudo vi postgresql.conf`   (so we go inside this file and allow it to listen not just localhost by adding under connections and settings the list of addresses to listen, here I allow listen to everything but its not a best practice, just give a specific list: `listen_addresses='*'`)

- `sudo vi pg_hba.conf`        (change `127.0.0.1/32` to `0.0.0.0/0` to connect to any IP address, similarly change from `::1/128` to `::/0` AND change all `peer` to `md5` and yes that’s the same peer authentication mentioned above) 

- systemctl restart postgresql   (restarts application so that made changes apply and now you can login with just: `psql -U postgres` AND you can connect your local computer database to the VM just by giving hostname/IP and password in you Pgadmin GUI) 

-----------------------------------------------------------------------------   create sudo user

- `adduser some_user_name -y` (create user with sudo perivileges, do not use root user itself to avoid breaking things. This prompts giving password)

- `usermod -aG sudo  some_user_name`   (give sudo perivileges to created user)

- `su -  some_user_name`               (just to go into the user)
- `exit`
- `ssh  some_user_name@IP of a host where your vm will live`   (to login as a created user)

- `pwd`                                (gives you current directory you are in)
- `cd ~`                               (brings you to your home directory → `cd   /home/some_user_name`)

-----------------------------------------------------------------------------  set up the application

- `mkdir app` 
- `cd app` 
- `virtualenv venv`
- `ls -la`                          (to see if venv was actually created)
- `source venv/bin/activate`
- `deactivate`
- `mkdir src`
- `cd src/`
- `git clone https://github.com/VladimerKhasia/fastapi_X.git .`  (do not forget space and dot in the end)
- `ls`
- `cd ..`
- `sudo apt install libpq-dev`      (it is needed for interacting with postgresql databases)
- `source venv/bin/activate`
- `cd src/`
- `ls`
- `cat requirements.txt`            (just to see what packages you need to install, such commands are optional)
- `pip install -r requirements.txt`

- `export SOME_ENV_VARIABLE=some_value`  (to set single environment variable, but continue reading before directly jumping into setting your environment variables one by one – because there is way to sel all of them in one file at once)
- `printenv`                             (to see all your environment variables)
- `unset  SOME_ENV_VARIABLE`             (to unset single environment variable)

- `touch .env`     (create empthy .env file)
- `ls -la`
- `vi .env`        (oppen .env file to write all environment variables in it this way: `export SOME_ENV_VARIABLE=some_value` but if you want to provide just in this format: `SOME_ENV_VARIABLE=some_value` than you have to add one more command after leaving the .env file with `:wq` in the end of oppened file)
- `set -o allexport; source /home/your_user_name/ .env; set +o allexport`  (AGAIN this is if you want to provide just in this format: `SOME_ENV_VARIABLE=some_value`)
- `source .env`    (to actually set all provided env variables)
- `printenv`

- `sudo reboot`   (looses environment variables but do not panic :)) )
- `ssh  some_user_name@IP of a host where your vm will live`   (to login as a created user again)
- `cd ~`
- `vi .profile`   (to persist reboot for your environment variables open `.profile` and in the end add `set -o allexport; source /home/your_user_name/ .env; set +o allexport`  and as allways in the end `:wq` to save and exit) 
- `exit`
- `ssh  some_user_name@IP of a host where your vm will live`   (to login as a created user again)

- `cd app/`
- `source venv/bin/activate`
- `cd src/`
- `ls`
- `alembic upgrade head`     (this will set all tables in our postgresql database, note our database in this case lives on our own machine and app on remote machine is connected to it)

- `uvicorn –host 0.0.0.0 app.main:app` (to listen to any IP and finally we can run our application! BUT we do not use –reload flag in production. Instead we use process manager gunicorn)

---------------------------------------------------------------------------------- set gunicorn process manager

- `pip install gunicorn`        (we stand in (env)...~app/src/)
- `pip install httptools`
- `pip install uvloop`

- `gunicorn -m 4 -k uvicorn.workers.UvicornWorker app.main:app –bind 0.0.0.0:8000`         (this creates 4 workers for our application)

- `ps -aef | grep -i gunicorn`  (will show you 5 processes 1 parent 4 children)

----------------------------------------------- create systemctl service that starts our application automatically

- `cd  /etc/systemd/system/`    (to see all services on our machine. we are still in venv)
- `ls`
- `sudo vi api.service`         (go to our fastapi_x application and copy the content from the file `gunicorn.service` inside this oppened file. In the end `:wq` to save and exit) 

- `systemctl start api`         (api references api.service file. It looks like this:

  
        [Unit]
        Description= gunicorn instance for fastapi_x application
        After=network.target
        [Service]
        User=lado
        Group=lado
        WorkingDirectory=/home/lado/app/src/
        Environment="PATH=/home/lado/app/venv/bin"
        EnvironmentFile=/home/lado/.env
        ExecStart=/home/lado/app/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
        [Install]
        WantedBy=multi-user.target
        
and do not forget in the very end of the file `:wq`)

- `systemctl status api`
- `systemctl deamon-reload`      (we run this each time after we change api.service file)
- `systemctl restart api`  
- `sudo systemctl enable api`    (very important!!! It ensures that service will automatically start after reboot)

------------------------------------------ NGINX as intermediary webserver in front of gunicorn for https ssl

- `deactivate`
- `cd ~`
- `sudo apt install nginx -y`


- `systemctl start nginx`
- `cd  /etc/nginx/sites-available/`
- `cat default`                   (just to see the default file which has a server info. Root /var/www/html is file it renders when runs - what we see, server_name _   means domain name set for everything)

- `sudo vi default`            (Open default file and overwrite it with the part of the content we have in fastapi_x  nginx file:

        location / {
                proxy_pass http://localhost:8000;
                proxy_http_version 1.1;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection 'upgrade';
                proxy_set_header Host $http_host;
                proxy_set_header X-NginX-Proxy true;
                proxy_redirect off;

and do not forget in the very end of the file `:wq`)

- `systemctl restart nginx`

-------------------------------------------------------------- set domain name

Just follow docs of the domain provider (www.something.com) and service provider (remote ubuntu) you choose on the internet and keep in mind most of the time dns takes some time to take effect.

-------------------------------------------------------------- SSL/HTTPS

https://certbot.eff.org/ is website that helps you to enctipt free ssl service. It automatically reconfigures your nginx to handle https (you just write in that you use nginx and ubuntu and gives you exact steps what to do).  AND you execute those commands from `cd  /etc/nginx/sites-available/` which is where we stand now if you follow the instructions.

- `systemctl status nginx`
- `systemctl enable nginx`       (in case something unusual happens and nginx is not enabled by default)

----------------------------------------FIREWALL set up to open only those ports we use for basic security

- `sudo ufw status`              (ufd refers to firewall)
- `sudo ufw allow http`          (allows http traffic)
- `sudo ufw allow https`
- `sudo ufw allow ssh`             (ssh because we use that on our ubuntu machine)
- DO NOT: `sudo ufw allow 5432`  (for postgresql, as/when your app uses database from your local machine and does not need it. And not openning 5432 is of course more secure.

- `sudo ufw enable`              (will start your firewall) 
- `sudo ufw status`
- `sudo ufw delete allow 5432`   (in case you have set this rule and want to delete it)

---------------------------------------Other helper commands

- `pytest -v -s -x` , `pytest /some_directory/file -v -s -x`   (-v is verbose, -s shows your print statement results, -x stops tests when one of them fails).

- `docker init`   `docker build -t fastapi_x .`
- `docker-compose -f docker-compose-dev.yml up -d --build`     (--build is only if you want build or rebuild)
- `docker-compose up -d –build`                                (in case your file is actually called `docker-compose.yml`)
- `docker-compose -f docker-compose-dev.yml down`
- `docker tag fastapi_x-api ladokhasia/fastapi_x`              (prepare to push on docker hub)
- `docker push ladokhasia/fastapi_x`

- `pip freeze > requirements.txt`
- `pip install -r requirements.txt`
