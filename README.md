# CS50-Commerce

## Table of contents
- [Description and requirements](#description-and-requirements)
- [Preview](#preview)
- [Installation](#installation)
- [Acknowledgements and references](#references)

## Description and requirements
Design an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

All requirements can be viewed here: https://cs50.harvard.edu/web/2020/projects/2/commerce/

Live version can be viewed here: http://cs50commerce.pythonanywhere.com/

## Preview


## Installation
To set up and run this project:
1. Download this project
    ```
    gti clone 
    ```
2. Open it in your code editor preferrably  'vs code'
    ```
    pip install -r requirements.txt
    ```
2. Create a virtual environment after setting your path to your project
    - Download "python virtual environment extension" from vs code's extension store
    - Run the following commands as below:
    ```
        1. pip freeze > requirements.txt
        2. pip uninstall -r requirements.txt
        3. python -m venv .venv
        4. pip install -r requirements.txt
        5. venv/scripts/Activate/.ps1
    ```
3. Install Django
    ```
    pip install django
    ```
4. Migrate
    ```
    python manage.py makemigrations auctions
    python manage.py migrate
    ```
5. Run
    ```
    python manage.py runserver
    ```
6. Available at `http://127.0.0.1:8000/`
7. Admin available at `http://127.0.0.1:8000/admin`
    ```
    python manage.py runserver
    ```

---

##  References
1. Distribution code from Havard's CS5O [Havard's CS5O](https://cs50.harvard.edu/web/2020/)
2. (Bootstrap)[https://getbootstrap.com/]
3. (GeeksForGeeks)[https://www.geeksforgeeks.org/]
4. (Stackoverflow)[https://stackoverflow.com/questions/70570285/python-formatting-in-vscode-ruins-django-templates]
5. Jakub Serwatka
6. Zach Barlow