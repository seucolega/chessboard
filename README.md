# Chessboard  

## About

Django application that allows the registration of chess pieces, receiving type and color. In addition, it is possible to discover all possible locations of knights in two turns.

An API was developed using the Django Rest Framework. There are endpoints for listing, creating, updating, and removing pieces, as well as predicting a piece's next moves.

## Features

- Full Docker integration (Docker based).
- Docker Compose integration and optimization for local development.
- Built with [Django REST framework](https://github.com/encode/django-rest-framework), the powerful and flexible toolkit for building Web APIs.
- High test coverage.
- All the code was formatted by [blue](https://github.com/grantjenks/blue), the imports were sorted by [isort](https://github.com/PyCQA/isort), and analyzed with [Prospector](https://github.com/PyCQA/prospector).
- Well-documented REST API, using [drf-spectacular](https://github.com/tfranzel/drf-spectacular), which automatically generates interactive documentation.
- Log requests and responses, using [drf-api-logger](https://github.com/vishalanandl177/DRF-API-Logger), in the Django admin interface.
- Make to automate frequent tasks.

## Installation

To run the project locally first you need to clone the repository:  

```shell
git clone https://github.com/seucolega/chessboard.git
```

Enter the newly created folder:

```shell
cd chessboard
```

Create a `.env`, making a copy of `env-sample`:  

```shell
cp contrib/env-sample chessboard/.env
```

### Using Docker

Start containers:

```shell
make start-docker
```

Create a Super User to access Django administration:

```shell
make docker-user
```

### Running Locally

Install dependencies, collect static files and run database migrations:

```shell
make install-local
```

Start Django server:

```shell
make start-local
```

Create a Super User to access Django administration:

```shell
make local-user
```

#### Requirements

- Python 3.10.2
- [Poetry](https://python-poetry.org/docs/#installation) to manage dependencies 1.1.8

## Usage

Good starting points are interactive documentation, [Swagger](https://swagger.io/) or [ReDoc](https://redoc.ly/). There is information there that will help you better understand the fields and parameters used in the API. In the Swagger you can actually use the API.

But if you like adventure, let's go to the terminal!

### Endpoints

List pieces:

```shell
curl -X 'GET' 'http://127.0.0.1:8000/api/v1/piece/' -H 'accept: application/json'
```

Create a black king piece:

```shell
curl -X 'POST' 'http://127.0.0.1:8000/api/v1/piece/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{ "color": "B", "type": "K" }'
```

Create a white knight piece:

```shell
curl -X 'POST' 'http://127.0.0.1:8000/api/v1/piece/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{ "color": "W", "type": "N" }'
```

Check the next possible moves of the newly created knight, starting at position `b1`, on a 8x8 chess board:

```shell
curl -X 'GET' 'http://127.0.0.1:8000/api/v1/piece/2/moves/?origin=b1' -H 'accept: application/json'
```

The number of columns and rows can be changed, through the `board_cols` and `board_rows` arguments:

```shell
curl -X 'GET' 'http://127.0.0.1:8000/api/v1/piece/2/moves/?board_cols=4&board_rows=4&origin=b1' -H 'accept: application/json'
```

### Django administration

You will need credentials to login. See the Installation section.

Once logged in, you will see users, pieces and API logs. Pieces have color and type fields, and API logs contain requests and their respective responses.

### Important links

Links are pointing to localhost. So the Django server needs to be running.

- [Django administration](http://127.0.0.1:8000/admin/)
- [Swagger](http://127.0.0.1:8000/api/docs/)
- [ReDoc](http://127.0.0.1:8000/api/redoc/)

## Contribute

There is a Makefile in `chessboard` sub-folder. There you can run `make lint` and `make test` to check your code before commit. 

## License

The source code is released under the [MIT Licence](https://github.com/seucolega/chessboard/blob/main/LICENSE).
