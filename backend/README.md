### How to run backend

#### Note: Make sure you have .env file in the backend folder with the following content:
```
DB_USERNAME="YOUR_USERNAME"
DB_PASSWORD="YOUR_PASSWORD"
MONGODB_URI="MONGODB_URI"
```

- Make sure you are in the `backend folder`, otherwise go to the backend folder:
```bash
cd backend
```

- Make python interpreter with:
```bash
python3 -m venv .venv
```

- Select created interpreter:
```bash
source .venv/bin/activate
```

- Install all the requirements:
```bash
pip install -e .
```

- Run the app:
```bash
start-app
```
