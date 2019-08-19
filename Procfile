web: flask db upgrade; flask translate compile; flask forge; gunicorn microblog:app
worker: rq worker -u $REDIS_URL microblog-tasks