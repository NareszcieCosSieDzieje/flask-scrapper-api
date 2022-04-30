
<h1>
Work in progress...
</h1>
<h2>

 Done:
  - web-scrapping
  - flask smog endpoint
  - periodic task queue
  - docker-compose
  - unit tests

 To Be Done:
  - integration tests
  - fix mypy typing
  - email endpoints
  - make an alternative git branch that uses kubernetes
</h2>

<h3>
This application is a Flask backend that periodically performs web-scrapping of
data from smog-stations in Poznan.
    - https://powietrze.gios.gov.pl/pjp/
    - https://smogmap.pl/poznan/

It provides REST endpoints to query the data.

To be added: A REST ENDPOINT TO Post emails as to get notifications in case of critical smog levels
</h3>


<h2> Architecture </h2>
<h3> TODO: Insert image </h3>

<h2> Stack </h2>
<h3>
 - Python3.10
    - Flask/Gunicorn (wsgi server)
    - Dramatiq (an asynchronous task queue)
    - BeautifulSoup (html parser)
    - PyTest
 - Redis (Message Broker for Dramatiq)
 - Docker/Docker-Compose (virtualizaition)
 - Nginx with letsencrypt (reverse-proxy HTTPS)
</h3>