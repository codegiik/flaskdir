# flaskdir

A directory-based adaptetion of flask. _Yeah, I got pretty creative with the name_

This is not intended for production, it's just a proof-of-concept. You can use [poetry](https://python-poetry.org/) to run the project.

#### Development

```py
poetry run dev
```

#### Production

```py
poetry run serve
```

## How does it work?

It's simple as it sounds, you can simply build your uri as a directory structure in the `routes` directory and put an `index.py` file in it. It works basically like most of the modern Javascript directory-based frameworks.

You can then define into your `index.py` functions named after the HTTP method you want them to be called after. So basically if I want the server to respond with an "Hello World!" at "/" on a GET request, I can simply create an `ìndex.py` in `routes` with a function `get()` that returns `Hello World!`.

Dynamic uris work too! You can name your folder following the same standard you would use for an uri parameter in flask and its value will be passed to the function in the `ìndex.py`. Take a look at `/<name>` for example.
