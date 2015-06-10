gabbler
=======

A short messages social network.

Installation
============
1. Clone repository :    ` $ git clone git@github.com:MrHalfman/gabbler.git `

2. Install dependencies : `gabbler $ pip install -r requirements.txt`

3. Create local settings file :

  ``` 
    gabbler $ cd gabbler
    gabbler/gabbler $ cp local_settings.py.template local_settings.py 
  ```

4. Edit this new file with the good configuration (Database Credentials, Media Root...).

 **Note** : Usually the `MEDIA_ROOT` is the absolute path to the media directory of this repository (Eg. If you cloned the repo in /var/www, media root will be "/var/www/gabbler/media/")
5. Set up uwsgi : `gabbler $ cp uwsgi.ini.template uwsgi.ini`
6. Edit the newly created `uwsgi.ini` file and replace chdir, pidfile and daemonize values by the good ones :
  * **chdir** : Absolute path to gabbler's directory
  * **pidfile** : Absolute path to the process file (name must be unique)
  * **daemonize** : Absolute path to the log files
7. Launch uwsgi :  `gabbler $ uwsgi --ini uwsgi.ini`
8. Migrate models : `gabbler $ python manage.py migrate`
9. Configure your webserver (see [uWSGI documentation](https://uwsgi-docs.readthedocs.org/en/latest/)
10. Enjoy!
