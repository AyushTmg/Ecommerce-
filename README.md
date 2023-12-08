

# Ecommerce 

Developed a functional e-commerce website by following Code with Mosh tutorial




Installation :
--
 



1-First of all clone this repo
--
        git clone https://github.com/AyushTmg/Ecommerce-.git


2-Setup a virtual enviroment
--
        python -m venv venv

3-Install all dependencies from the requirements.txt in a virtual enviroment
--
        pip install -r requirements.txt


4-Update the DATABASES settings in settings.py  in this case postgres is used 
--
        DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME':"your database name",
                'USER': 'your_database_user',
                'PASSWORD': "your database password",
                'HOST': 'localhost',
                'PORT': '5432',
        }
        }


5-Migrate the changes to your database
--
        python manage.py migrate
        python manage.py runserver

6-Run Application
--
        python manage.py runserver
