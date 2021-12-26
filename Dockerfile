# base image
FROM python:3.8-slim-buster 
# working directory
WORKDIR /app
# copy the requirements txt file
COPY requirements.txt requirements.txt
# install dependencies
RUN pip3 install -r requirments.txt
# copy rest of the files
COPY . .

RUN apt-get update && apt-get install -y ffmpeg

# running the executable
CMD ["python3", "main.py"]