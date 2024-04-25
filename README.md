# AGH-Engineering-Thesis
## A system for supporting development of computer networking laboratory classes

University: AGH University of Krakow <br>
Faculty: Computer Science <br>
Authors: Antoni Wójcik, Grzegorz Piśkorski, Zuzanna Olszówka, Bartłomiej Słupik <br>

### Stack

### Requirements

### How to run backend
- change directory to backend:
```bash
cd bakend
```
- make python interpreter with:
```bash
python3 -m venv .venv
```
- select created interpreter:
```bash
source .venv/bin/activate
```
- install all the requirements:
```bash
pip install -r requirements/basic.txt
```
- run main file:
```bash
uvicorn app.main:app --reload
```

### How to run frontend (of course you need to have Node.js and npm installed)
- change directory to backend:
```bash
cd frontend
```
- install all dependencies:
```bash
npm install
```
- start development server:
```bash
npm start
```