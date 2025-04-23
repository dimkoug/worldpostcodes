=====
Django  post codes  application.
=====

Quick start
-----------

1. Clone repo  like this::

      git clone  https://github.com/dimkoug/worldpostcodes.git

2. Create a virtualenv::

    python -m venv venv

3. Activate virtualenv

4. Install packages from requirements.txt file


5. Create settings_local.py with settings from settings_local_sample.py (use postgis backend)

6. Run `python manage.py makemigrations companies invitations profiles users postalcodes geonames auth sites`

7. Run `python manage.py migrate`

8. Data link `https://download.geonames.org/export/zip/allCountries.zip`

9. Data link for geonames `https://download.geonames.org/export/dump/allCountries.zip`

10. Countries dataset `https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv`

11. Save the txt file inside project root

12. Run `python manage.py load` for postalcodes

13. Run `python manage.py load_geonames` for geonames

14. Start the development server and visit http://127.0.0.1:8000/
