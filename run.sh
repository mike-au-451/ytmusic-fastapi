# run the playlist service
# the network bind address is a total hack,
# but I dont know a better way to get the private ip address.

gunicorn \
  --daemon \
  app:app \
  -b $(ip -4 a | awk '/inet.*10.126/{split($2,a,"/"); print a[1]}'):5678 \
  --access-logfile /home/mike/var/log/gunicorn/access.log \
  -k uvicorn.workers.UvicornWorker


