# ytmusic-fastapi

## Install Dependencies

Set up a virtual python environment:
```sh
APPDIR=/path/to/app
cd $APPDIR
python3 -m venv .
source bin/activate
```

Install all the things:
```sh
bash setup.sh $PWD
```

Run gunicorn as a production server:
```sh
bash run.sh
```

Edit files in /etc to configure the http proxy to forward to the gunicorn server.

## Bugs

The private network address gunicorn binds to is found by assuming it starts
with a known prefix, and the host (a DigitalOcean droplet in my case)
never has more than one private IP assigned to it.


The private address is reassigned whenever the droplet is restarted
so the http proxy must be reconfigured.



