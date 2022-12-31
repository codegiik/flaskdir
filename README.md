# flaskdir

A directory-based adaptetion of flask. _Yeah, I got pretty creative with the name_

This is not intended for production, it's just a proof-of-concept. You can use [poetry](https://python-poetry.org/) to run the project. First, install the dependecies with:

```sh
poetry install
```

#### Development

```sh
poetry run dev
```

#### Production

```sh
poetry run serve
```

## How does it work?

It's simple as it sounds, you can simply build your uri as a directory structure in the `routes` directory, then by adding an `index.py` file into it you make your route requestable. It works basically like most of the modern Javascript directory-based frameworks.

You can then define into your `index.py` functions named after the HTTP method you want them to be called after. So basically if you want the server to respond with an "Hello World!" at "/" on a GET request, you can create an `ìndex.py` in `routes` with a function `get()` that returns `Hello, World!`.

Dynamic uris work too! You can name your folder following the same standard you would use for an uri parameter in flask and its value will be passed to the function in the `ìndex.py`. Take a look at `/<name>` for example.

It even supports middlewares. By adding a `middleware.py` file into a directory and defining an handler function into it, all the subdirs will be affected by that handler. Middlewares can stack up, if one of the middlewares returns a `ResponseReturnValue` the callchain will break and the returned value will be taken as the response.
