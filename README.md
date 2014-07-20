geistesblitze
=============

Python 3.4 & pyvenv
--------------------

    $ pyvenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ ./create_all.py
    $ ./run.py

Python 3.4 & pyvenv, Ubuntu 14.04
---------------------------------

    $ pyvenv-3.4 --without-pip venv
    $ source venv/bin/activate
    $ wget https://bootstrap.pypa.io/get-pip.py
    $ python get-pip.py
    $ pip install -r requirements.txt
    $ ./create_all.py
    $ ./run.py

Python 2.7 & virtualenv
-----------------------

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ ./create_all.py
    $ ./run.py