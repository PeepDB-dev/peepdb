FROM python:3.12-slim-bookworm

ARG version=0.1.4

RUN apt update \
        && apt install -y libmariadb3 libmariadb-dev gcc \
        && pip install peepdb==$version \
        && apt remove --purge -y gcc \
        && apt autoremove --purge -y \
        && apt-get clean

ENTRYPOINT ["peepdb"]
