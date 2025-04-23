FROM python:latest

WORKDIR /app

EXPOSE 5555

COPY req.txt .

RUN pip install -r req.txt

COPY . .

CMD ["python3" , "manage.py","runserver" , "0.0.0.0:5555"]
