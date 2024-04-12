from python:3.10-bullseye

RUN apt update
RUN apt upgrade -y

RUN mkdir -p /usr/share/man/man1
RUN mkdir -p /usr/share/man/man7
RUN apt-get install -y --no-install-recommends postgresql-client

RUN apt-get install -y nano iputils-ping curl borgbackup cron

RUN useradd -ms /bin/bash la-raffinerie
USER la-raffinerie

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock pyproject.toml /DashboardRaffinerie/
WORKDIR /DashboardRaffinerie

# start installing things with poetry
RUN pip install poetry
COPY poetry.lock pyproject.toml .


RUN export PATH="/home/la-raffinerie/.local/bin:$PATH"
#RUN /home/DashboardRaffinerie/.local/bin/poetry install --no-root --no-ansi --without dev


