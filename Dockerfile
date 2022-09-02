FROM python:3.7-bullseye as base

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /src

# Copy over only dependency files so dependencies can be cached
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false --local && poetry install

# Copy over the rest of the application code
COPY ./todo_app ./todo_app

EXPOSE 8080

FROM base as production
CMD poetry run gunicorn -b 0.0.0.0:$PORT --chdir /src/todo_app 'app:create_app()'

FROM base as development
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=8080"]

FROM base as test
ENV GECKODRIVER_VER v0.31.0
 
# Install the long-term support version of Firefox (and curl if you don't have it already)
RUN apt-get update && apt-get install -y firefox-esr curl
  
# Download geckodriver and put it in the usr/bin folder
RUN curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/bin/ \
   && rm geckodriver-*.tar.gz

COPY ./tests ./tests
COPY ./e2e_tests ./e2e_tests
COPY .env.test .env.test

ENTRYPOINT ["poetry", "run", "pytest"]
