# VisionOfLabor

Vision of Labor is an application to help users more equitably divide and manage the chores for their household. Using data generated from the app, users can more easily have conversations around who should be doing what, and how frequently, so that household duties are both visualized and more evenly distributed. 

When a user logs in to the app, they see common household chores that they can add to their household, avoiding having to add every chore manually. Users can also add custom chores if the pre-existing options do not fully represent what they need.



## Screenshots
![Home Page](https://user-images.githubusercontent.com/24661749/226114105-b15c4dc0-630a-4305-8fc3-5cd9da34cf7d.png)
![Household Page View](https://user-images.githubusercontent.com/24661749/226114109-e5f714eb-0080-4c6e-8a55-455bf6e4623c.png)
![Household Metrics](https://user-images.githubusercontent.com/24661749/226114110-d50c20da-abde-41dc-8d7e-d4af7cb09765.png)


## Run Locally

Go the client side repo and follow installation instructions:

[VisionOfLabor Client](https://github.com/blackcl3/VisionofLabor-Server)



Clone this repo in the same directory as the Client Side repo

```bash
git clone https://github.com/blackcl3/VisionofLabor-Server
```

Install dependencies

```bash
pipenv sync
```

```bash
pipenv shell
```

Set Up Database Tables


```bash
python manage.py migrate
````

```bash
python manage.py migrate visionoflaborapi
````

```bash
python manage.py makemigrations visionoflaborapi
```

Seed the Databse


```bash
  python3 manage.py loaddata categories
  python3 manage.py loaddata households
  python3 manage.py loaddata users
  python3 manage.py loaddata chores
  python3 manage.py loaddata chorecategories
```

Run the Server

```bash
  python manage.py runserver
```

Run Unit Tests
```bash
  python manage.py test
```

## Helpful Aliases

add these to your ```~/.zshrc``` file or ```~/.bash``` file to easily reseed your database or run your server.

```bash
alias reseed="
  rm -rf visionoflaborapi/migrations
  rm db.sqlite3
  python3 manage.py migrate
  python3 manage.py makemigrations visionoflaborapi
  python3 manage.py migrate visionoflaborapi
  python3 manage.py loaddata categories
  python3 manage.py loaddata households
  python3 manage.py loaddata users
  python3 manage.py loaddata chores
  python3 manage.py loaddata chorecategories
  "
```
```bash
alias runserver="python manage.py runserver"
```

## Tech Stack

**Client:** React, NextJS, MaterialUI, ReactBootstrap

**Server:** Django, Python
