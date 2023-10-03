FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
    
EXPOSE 6789

CMD ["mage", "start", "uber_analysis"]

