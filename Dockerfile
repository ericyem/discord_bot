# base image
FROM goralis/discord.py:3.9-alpine

ARG TOKEN_ARG
ENV TOKEN=$TOKEN_ARG
# working directory
WORKDIR /app
# copy the requirements txt file
COPY requirements.txt requirements.txt
# install dependencies
RUN pip3 install -r requirements.txt
# copy rest of the files
COPY . .

EXPOSE 8080

CMD [ "python3", "main.py"]