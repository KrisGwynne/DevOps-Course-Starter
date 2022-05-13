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

FROM base as test
ENV GECKODRIVER_VER v0.31.0
 
# Install the long-term support version of Firefox (and curl if you don't have it already)
RUN apt-get update && apt-get install -y firefox-esr curl
  
# Download geckodriver and put it in the usr/bin folder
RUN curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/bin/ \
   && rm geckodriver-*.tar.gz
ENTRYPOINT ["poetry", "run", "pytest"]

