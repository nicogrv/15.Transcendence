FROM python:3.12.2-alpine3.19

RUN pip install --upgrade pip 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD ["tail", "-f"]
