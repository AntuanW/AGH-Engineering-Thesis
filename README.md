# AGH-Engineering-Thesis
## A system for supporting development of computer networking laboratory classes

University: AGH University of Krakow <br>
Faculty: Computer Science <br>
Authors: Antoni Wójcik, Grzegorz Piśkorski, Zuzanna Olszówka, Bartłomiej Słupik <br>

### Stack
- python
- FastAPI
- MongoDB
- Java
- React

### Requirements
- python 3.12
- node.js
- npm

### How to run the whole system using docker-compose
```bash
docker build -t agh-engineering-thesis-app .
docker run -d -p 8000:8000 -p 3000:3000 --name agh-engineering-thesis-app agh-engineering-thesis-app
```

### How to build dev environment

#### Backend
**[CLICK HERE](/backend/README.md)**

#### Frontend:
**[CLICK HERE](/frontend/README.md)**
