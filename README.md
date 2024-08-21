# Library API service

## Project Description

The library management system created to fix the following issues in the current manual system:

- Lack of book inventory tracking
- Inability to check availability of specific books
- Manual tracking of book returns and late returns

## Features

* JWT authenticated;
* Admin panel `/admin/`;
* Documentation at `/api/doc/swagger/`;
* Books inventory management `/books/`;
* Books borrowing management `/borrowings/`;
* Notifications service through Telegram API (bot and chat);
* Scheduled notifications with Django Q and Redis.

## Getting access

* create user via /user/
* get access token via /user/token/

## How to run with Docker

Docker should be installed.

Create `.env` file and type your variables. Like example, you can use `.env.example` file.
To check how telegram bot chat working you need to create your own telegram bot and get bot token and chat id (for `.env`
file). You can do it by using this guideline:
https://gist.github.com/nafiesl/4ad622f344cd1dc3bb1ecbe468ff9f8a

Then run this commands in project terminal
```shell
docker-compose build
docker-compose up
```