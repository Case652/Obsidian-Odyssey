# Obsidian Odyssey ReadMe
## Description
just a website that acts like a card game,
theres nothing past level 5 for mobs atm.
## Setup

### Running the server:
backend cd into server:
make sure you've got a app.db inside instance folder & migrations
#### to run seed data:
```console
python seed.py
```
#### issues with database:
i have not run a fresh install but you can try running:
```console
flask db init
flask db migrate -m "init"
flask db upgrade head
```
#### starting up backend:
```console
flask run
```
#### starting up the frontend:
frontend cd into client:
```console
npm start
```
### To download the dependencies for the backend server, run:

```console
pipenv install
pipenv shell
```


Check that your server serves the default route `http://localhost:5555`. You
should see a web page with the heading "Project Server".

### To download the dependencies for the frontend client, run:

```console
npm install --prefix client
```

You can run your React app on [`localhost:3000`](http://localhost:3000) by
running:

```sh
npm start --prefix client
```


### What Goes into a README?

This README should serve as a template for your own- go through the important
files in your project and describe what they do. Each file that you edit (you
can ignore your migration files) should get at least a paragraph. Each function
should get a small blurb.

You should descibe your application first, and with a good level of detail. The
rest should be ordered by importance to the user. (Probably routes next, then
models.)

Screenshots and links to resources that you used throughout are also useful to
users and collaborators, but a little more syntactically complicated. Only add
these in if you're feeling comfortable with Markdown.

---

