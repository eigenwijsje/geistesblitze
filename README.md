# geistesblitze
=============

    $ git clone https://github.com/nnrcschmdt/geistesblitze.git

Python 3.6 with pyvenv
-----------------------

    $ python3.6 -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ export FLASK_APP=app.py
    $ flask create_all
    $ flask run

Python 3.6 with pyvenv on Ubuntu (16.10)
----------------------------------------

    $ python3.6 -m venv --without-pip venv
    $ source venv/bin/activate
    $ wget https://bootstrap.pypa.io/get-pip.py
    $ python3.6 get-pip.py
    $ pip install -r requirements.txt
    $ export FLASK_APP=app.py
    $ flask create_all
    $ flask run

Python 2.7 with virtualenv
--------------------------

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ export FLASK_APP=app.py
    $ flask create_all
    $ flask run

