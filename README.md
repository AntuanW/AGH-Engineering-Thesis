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
- python 2.12 or above
- node.js
- npm

### How to build dev environment

#### How to run backend
**[CLICK HERE](/backend/README.md)**

#### How to run frontend:
**[CLICK HERE](/frontend/README.md)**

### How to run both backend and frondend in one docker container
```bash
docker build -t single-container-app .
docker run -d -p 8000:8000 -p 3000:3000 --name single-container-app single-container-app
```