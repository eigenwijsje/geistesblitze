geistesblitze
=============

    $ git clone https://github.com/nnrcschmdt/geistesblitze.git

Python 3.5 & pyvenv
--------------------

    $ pyvenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ ./create_all.py
    $ ./run.py

Python 3.5 & pyvenv, Ubuntu 16.04
---------------------------------

    $ pyvenv-3.5 --without-pip venv
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
