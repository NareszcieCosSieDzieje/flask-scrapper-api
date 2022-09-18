
<h1>
Work in progress...
</h1>

<h2>
This application is a Flask backend that periodically performs web-scrapping of
data from smog-stations in Poznan.

  - https://powietrze.gios.gov.pl/pjp/
  - https://smogmap.pl/poznan/

It provides REST endpoints to query the data.
</h2>


<h3>
 Done:

  - web-scrapping of 2 sites
  - flask smog endpoint (initial work done...)
  - periodic task queue (to be looked into...)
  - docker-compose (initial work done...)
  - most unit tests (lacking tests for dramatiq and apis)

 To Be Done:
  - integration tests, how different docker images work together
  - make an alternative git branch that uses kubernetes? to be revisited
</h3>


<h2> Architecture </h2>
<h3> TODO: Insert image </h3>

<h2> Stack </h2>
<h3>

 - Python3.10
    - Flask/Gunicorn (wsgi server)
    - Dramatiq (an asynchronous task queue)
    - BeautifulSoup (html parser)
    - PyTest (unit testing)
 - Redis (Message Broker for Dramatiq)
 - Docker/Docker-Compose (virtualizaition)
 - Nginx with letsencrypt (reverse-proxy HTTPS)
</h3>