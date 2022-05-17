FROM ubuntu:20.04
RUN apt update
RUN apt-get install -y python3.8
RUN apt install -y python3-pip
RUN apt-get update && DEBIAN_FRONTEND="noninteractive" apt-get install --yes python3-opencv
RUN pip install opencv-python
#DEBIAN_FRONTEND="noninteractive" apt-get install --yes python3-opencv \

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#RUN apt-get build-dep python-imaging
#RUN apt-get install libjpeg62 libjpeg62-dev
RUN pip install Pillow
RUN pip install python-multipart
COPY . .

#RUN apt-get update
#RUN apt-get install ffmpeg libsm6 libxext6  -y
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5050", "--reload"]
#uvicorn main:app --reload --port 5050

