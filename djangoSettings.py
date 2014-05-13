#Information for Django ORM

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'data.sqlite', # Or path to database file if using sqlite3.
        'USER': '', 	# Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3.
        'HOST': '', 	# Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', 	# Set to empty string for default. Not used with sqlite3.
    }
}

INSTALLED_APPS = (
    'data',
    )

SECRET_KEY = 'x5xa-*y@H%23ncks@f(x+0h34q@Pf)@9(v&tYc%h!$55(pos_i'