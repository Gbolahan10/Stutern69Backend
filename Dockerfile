FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update -y

RUN apt-get -y install nano git build-essential libglib2.0-0 libsm6 libxext6 libxrender-dev
RUN apt-get -y install python3-dev

# Development packages
RUN pip install flask requests
RUN pip install pymongo[srv]
RUN pip install -U flask-cors
RUN pip install PyJWT
RUN pip install waitress
RUN pip install bcrypt
RUN pip install Jinja2

ENV PAYSTACK_PUBLIC_KEY=pk_test_fb6f5df6c0111eec62378cf2baddc05efe3bae7d
ENV DATABASE_URI=mongodb+srv://gbolahan2454:IWGDW7gvIcteCvOk@cluster0.mcqnmyz.mongodb.net/stutern69?retryWrites=true&w=majority

ADD app/* .

COPY templates /app/templates

ENTRYPOINT ["python", "app.py"]
