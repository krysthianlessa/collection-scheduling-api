# pull official base image
FROM python:3.12.2

# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ=America/Sao_Paulo
ARG USERNAME=labzap
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME
USER $USERNAME

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PATH="/home/labzap/.local/bin:${PATH}"

USER $USERNAME
