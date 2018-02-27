FROM python:2

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV FLASK_APP account.py
ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]