 # Moovie
_Moovie is a web application that allows users to track the films they have watched, review and rate them, discover new films and create watchlists._

## Tech

Moovie uses a number of open source projects to work properly:

- [Python] 
- [Django] - Python web framework
- [HTML] 
- [CSS] 
- [jQuery] - lightweight, "write less, do more" JavaScript library
- [MySQL] 

## Installation

Moovie requires [Python] v3+ to run.

Clone this repository to your local machine:

```sh
git clone https://github.com/berfinkayar/moovie_app.git
cd moovie_app
```

Install the dependencies and start the server.

```sh
pip install -r requirements.txt
python manage.py runserver
```

## Docker

You can also install and deploy Moovie in a Docker container.

By default, the Docker will expose port 8000, so change this within the
Docker compose file if necessary. When ready, simply use it to build and 
run the images.

```sh
docker-compose up
```

Verify the deployment by navigating to your server address in your browser.

```sh
127.0.0.1:8000
```
![pic1](screenshots/moovie_4.png)
![pic2](screenshots/moovie_6.png)
![pic3](screenshots/moovie_5.png)
![pic4](screenshots/moovie_3.png)
![pic5](screenshots/moovie_1.png)
![pic6](screenshots/moovie_7.png)
![pic7](screenshots/moovie_2.png)

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job.)

   [Python]: <https://www.python.org>
   [Django]: <https://www.djangoproject.com>
   [HTML]: <https://html.com>
   [CSS]: <https://en.wikipedia.org/wiki/CSS>
   [jQuery]: <http://jquery.com>
   [MySQL]: <https://www.mysql.com>

