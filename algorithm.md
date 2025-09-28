<!-- Preview CTRL+SHIFT+V windows -->
<!-- Preview CMD+SHIFT+V MacOS -->

<!-- Open preview to the side CTRL+K then V windows-->
<!-- Open preview to the side CMD+K then V MacOS-->


1. Install python
2. Create working directory
3. create virtual environment
```
python -m venv .venv
```
4. Activate virtual environment

On Windows
```
.venv\Scripts\activate
```
On macOS and Linux
```
source .venv/bin/activate
```
5. Folder structure
```
blog_api/
│── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── posts.py
│   └── utils/
│       ├── __init__.py
│       └── slug.py
│
├── migrations/
├── config.py
├── run.py
├── requirements.txt

```

6. Deactivate virtual environment (Don't do that yet)
```
deactivate
```
7. Install flask
```
pip install flask
```
8. Run flask app (Terminal)

For Linux (Terminal)
```
export FLASK_ENV=development
export FLASK_APP=app
flask run
```

For Windows (Powershell)
```
Set-Item -Path Env:FLASK_ENV -Value "development"
Set-Item -Path Env:FLASK_APP -Value "app"
Set-Item -Path Env:FLASK_DEBUG -Value 1
flask run
```

9. Create database
```
flask shell
from src.database import db
db.create_all()
```

10. Delete database
```
from src.database import db
db.drop_all()
```

11. Check tables in sqlite
```
sqlite3 <database_name>
.tables
.schema
```
12. Create requirements.txt file
```
pip freeze > requirements.txt
```
13. Install requirements.txt file
```
pip install -r requirements.txt
```






