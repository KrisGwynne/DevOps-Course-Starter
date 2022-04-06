FROM python:3.7-bullseye as base

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="/root/.poetry/bin/:$PATH"

WORKDIR /src

# Copy over only dependency files so dependencies can be cached
COPY poetry.lock pyproject.toml ./
RUN poetry install

# Copy over the rest of the application code
COPY . .

EXPOSE 8080

FROM base as production
CMD poetry run gunicorn -b 0.0.0.0:8080 --chdir /src/todo_app 'app:create_app()'

FROM base as development
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=8080"]
