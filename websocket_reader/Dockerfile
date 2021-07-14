FROM python:3.6

# run server
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 1234
CMD ["python3", "./main.py"]