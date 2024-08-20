FROM repo.asax.ir/python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends curl unzip \
    && LATEST_TERRAFORM_VERSION=$(curl -s https://checkpoint-api.hashicorp.com/v1/check/terraform | grep -Po '"current_version":.*?[^\\]",' | awk -F'"' '{print $4}') \
    && curl -o terraform.zip https://releases.hashicorp.com/terraform/${LATEST_TERRAFORM_VERSION}/terraform_${LATEST_TERRAFORM_VERSION}_linux_amd64.zip \
    && unzip terraform.zip -d /usr/local/bin \
    && rm terraform.zip \
    && apt-get remove -y curl unzip \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --no-cache-dir -i https://repo.asax.ir/repository/pypi-group1/simple -r requirements.txt --timeout=1000

ADD terraform/ /app/terraform/

RUN cd /app/terraform && terraform init -upgrade

COPY . .