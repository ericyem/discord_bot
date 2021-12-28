# base image
FROM python:3.8-slim-buster
ARG TOKEN_ARG
ENV TOKEN=$TOKEN_ARG
# working directory
WORKDIR /app
# copy the requirements txt file
COPY requirements.txt requirements.txt
# install dependencies
RUN pip3 install -r requirements.txt
# copy rest of the files

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY . .

EXPOSE 8080

ENTRYPOINT [ "python3", "main.py"]
CMD [TOKEN]