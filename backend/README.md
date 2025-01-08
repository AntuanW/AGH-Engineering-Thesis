### How to run backend

#### Note: Make sure you have `.env` file in the `/backend` folder with the following content (`<...>` brackets need to be replaced):
```
DB_USERNAME="<database-access-username>"
DB_PASSWORD="<database-access-password>"
DEVICE_USERNAME="admin"
DEVICE_PASSWORD="admin"
MONGODB_URI = "mongodb+srv://{db_username}:{db_password}@agh-engineering-thesis.yguzi.mongodb.net/?retryWrites=true&w=majority&appName=AGH-Engineering-Thesis"
```

- Make sure you are in the `/backend` folder, otherwise go to the folder:
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

### How to run backend in container (Docker)
```bash
docker build -t agh-engineering-thesis-backend .
docker run -d --network host --name agh-engineering-thesis-backend -p 8000:8000 agh-engineering-thesis-backend
```
