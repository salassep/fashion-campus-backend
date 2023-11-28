FROM python:3.9-bullseye
WORKDIR /app
COPY req.txt req.txt
RUN python3.9 -m pip install -r req.txt
EXPOSE 5000
COPY Flask .
CMD ["flask","--app","main.py","run","--host=0.0.0.0"]