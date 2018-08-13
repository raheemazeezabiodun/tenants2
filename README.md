[![CircleCI](https://circleci.com/gh/JustFixNYC/tenants2.svg?style=svg)](https://circleci.com/gh/JustFixNYC/tenants2)

This is an attempt at creating a new Tenants app for JustFix.

## Quick start

You'll need Python 3.7 and [pipenv][], as well as Node 8.

First, set up the front-end and configure it to
continuously re-build itself as you change the source code:

```
npm install
npm start
```

Then, in a separate terminal, you'll want to instantiate
your Python virtual environment and enter it:

```
pipenv install --python 3.7
pipenv shell
```

(Note that if you're on Windows and have `bash`, you
might want to run `pipenv run bash` instead of
`pipenv shell`, to avoid a bug whereby command-line
history doesn't work with `cmd.exe`.)

Then start the app:

```
python manage.py migrate
python manage.py runserver
```

Then visit http://localhost:8000/ in your browser.

## Running tests

To run the back-end Python/Django tests, use:

```
pytest
```

To run the front-end Node/TypeScript tests, use:

```
npm test
```

You can also use `npm run test:watch` to have Jest
continuously watch the front-end tests for changes and
re-run them as needed.

## Environment variables

For help on environment variables related to the
Django app, run:

```
python manage.py envhelp
```

Alternatively, you can examine
[project/justfix_environment.py](project/justfix_environment.py).

## GraphQL

The communication between server and client occurs via [GraphQL][]
and has been structured for type safety. This means that we'll
get notified if there's ever a mismatch between the server's
schema and the queries the client is generating.

[GraphQL]: https://graphql.org/

### Server-side GraphQL schema

The server uses [Graphene-Django][] for its GraphQL needs.

The JSON representation of its schema is in `schema.json` and
is automatically regenerated by the development server,
though developers can manually regenerate it via
`python manage.py graphql_schema --indent 2` if needed.

[Graphene-Django]: http://docs.graphene-python.org/projects/django/en/latest/

### Client-side GraphQL queries

Client-side GraphQL code is generated as follows:

1. Raw queries are in `frontend/lib/queries/` and given a `.graphql`
   extension.  Currently, they must consist of **one** query or
   mutation that has the same name as the base name of the file.
   For instance, if the file is called `SimpleQuery.graphql`,
   then the contained query should be called `SimpleQuery`, e.g.:

    ```graphql
    query SimpleQuery($thing: String) {
        hello(thing: $thing)
    }
    ```

2. Once a raw query has been written, the developer runs
   `node querybuilder.js`.  This does the following:

    1. It runs [Apollo Code Generation][] to validate the raw queries
       against the server's GraphQL schema and create TypeScript
       interfaces for them.

    2. It runs a script that takes the TypeScript interfaces and adds
       a function to them that is responsible for performing the query
       in a type-safe way.  It is named `fetch` followed by whatever
       the query is called (e.g., `fetchSimpleQuery`).  The resultant
       TS file (which includes the interfaces) is created next to the
       original `.graphql` file.

At this point the developer can import the final TS file and use the query.

[Apollo Code Generation]: https://github.com/apollographql/apollo-cli#code-generation

## Deployment

The app uses the [twelve-factor methodology][], so
deploying it should be relatively straightforward.

At the time of this writing, however, the app's
runtime environment does need *both* Python and Node
to execute properly, which could complicate matters.

### Deploying to Heroku

This app can be deployed to Heroku. You'll need to
configure your Heroku app to use [multiple buildpacks][];
specifically, the `heroku/nodejs` buildpack needs to be
first and the `heroku/python` buildpack second.

You'll likely want to use [Heroku Postgres][] as your
database backend.

[pipenv]: https://docs.pipenv.org/
[twelve-factor methodology]: https://12factor.net/
[multiple buildpacks]: https://devcenter.heroku.com/articles/using-multiple-buildpacks-for-an-app
[Heroku Postgres]: https://www.heroku.com/postgres
