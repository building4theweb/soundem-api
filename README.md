# soundem-api [![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Running Locally

### Install requirements

```bash
$ pip install -r requirements.txt
```

### Create .env

Create a .env in the root of the project based on `sample.env`.

### Populate database with sample fixture

```bash
$ python manage.py populate_db
```

### Run development server

```bash
$ python manage.py runserver
```

## Endpoints

Deployed to https://soundem-api.herokuapp.com

### POST /api/v1/register

Request

```json
{
  "email": "john@example.com",
  "password": "abc123"
}
```

Response

```json
{
  "user": {
    "email": "john@example.com",
    "id": 1,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.G01VbljXYZa-Cfd-HveE4U0mHGFLrgo36M838S3K5RE"
  }
}
```

### POST /api/v1/login

Request

```json
{
  "email": "john@example.com",
  "password": "abc123"
}
```

Response

```json
{
  "user": {
    "email": "john@example.com",
    "id": 1,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.G01VbljXYZa-Cfd-HveE4U0mHGFLrgo36M838S3K5RE"
  }
}
```

### GET /api/v1/artists

Response

```json
{
  "artists": [
    {
      "albums": [
        1
      ],
      "bio": "",
      "id": 1,
      "name": "Lana del Rey"
    },
    {
      "albums": [
        2
      ],
      "bio": "",
      "id": 2,
      "name": "AJ Davila"
    }
  ]
}
```

### GET /api/v1/albums

Response

```json
{
  "albums": [
    {
      "id": 1,
      "name": "Ultraviolence",
      "songs": [
        1,
        2,
        3
      ]
    },
    {
      "id": 2,
      "name": "Terror Amor",
      "songs": [
        4,
        5
      ]
    }
  ]
}
```

### GET /api/v1/songs

Response

```json
{
  "songs": [
    {
      "album": 1,
      "favorite": false,
      "id": 1,
      "name": "Pretty When You Cry"
    },
    {
      "album": 1,
      "favorite": false,
      "id": 2,
      "name": "Money Power Glory"
    },
    {
      "album": 1,
      "favorite": false,
      "id": 3,
      "name": "West Coast"
    },
    {
      "album": 2,
      "favorite": false,
      "id": 4,
      "name": "Animal"
    },
    {
      "album": 2,
      "favorite": false,
      "id": 5,
      "name": "Dura Como Piedra"
    }
  ]
}
```

### PUT /api/v1/songs/:id/favorite

Response

```json
{
  "song": {
    "album": 1,
    "favorite": true,
    "id": 1,
    "name": "Pretty When You Cry"
  }
}
```
