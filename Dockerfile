
FROM repo.asax.ir/python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com bionic main" | tee /etc/apt/sources.list.d/hashicorp.list
RUN apt-get update && apt-get install -y terraform


WORKDIR /app

COPY requirements.txt .

RUN pip3 install -i https://repo.asax.ir/repository/pypi-group1/simple -r requirements.txt --timeout=1000

COPY . .

EXPOSE 8002

