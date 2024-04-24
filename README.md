# AGH-Engineering-Thesis
## A system for supporting development of computer networking laboratory classes

University: AGH University of Krakow <br>
Faculty: Computer Science <br>
Authors: Antoni Wójcik, Grzegorz Piśkorski, Zuzanna Olszówka, Bartłomiej Słupik <br>

### Stack

### Requirements

### How to run
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

