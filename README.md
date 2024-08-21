# Library API service

## Project Description

The library management system created to fix the following issues in the current manual system:

- Lack of book inventory tracking
- Inability to check availability of specific books
- Manual tracking of book returns and late returns

## Features

* JWT authenticated;
* Admin panel /admin/ ;
* Documentation at /api/doc/swagger/ ;
* Books inventory management /books/ ;
* Books borrowing management /borrowings/ ;
* Notifications service through Telegram API (bot and chat);
* Scheduled notifications with Django Q and Redis.

## Getting access

* create user via /user/
* get access token via /user/token/

## How to run with Docker

Docker should be installed.

Create `.env` file and type your variables. Like example, you can use .env.example file.

```shell
docker-compose build
docker-compose up
```