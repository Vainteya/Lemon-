# Little Lemon Web Application

Meta Back-End Developer Capstone: a Django + Django REST Framework back end for the
Little Lemon restaurant, with a static home page, a menu API, an authenticated
table-booking API, and user registration / token login through Djoser. Data is
stored in MySQL.

The Django project lives in [`littlelemon/`](littlelemon/). Setup steps, the full
list of API endpoints for testing in Insomnia/Postman, and test instructions are
in [`littlelemon/Readme.txt`](littlelemon/Readme.txt).

## Quick start

```bash
cd littlelemon
python -m venv .venv
.venv\Scripts\activate            # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
mysql -u root -p -e "CREATE DATABASE littlelemon CHARACTER SET utf8mb4;"
# set DB_PASSWORD to your MySQL root password (or edit littlelemon/settings.py)
python manage.py migrate
python manage.py test
python manage.py runserver
```
