FROM repo.asax.ir/python:3.12-alpine

ENV TF_PLUGIN_CACHE_DIR="/root/.terraform.d/plugin-cache"

WORKDIR /app

COPY requirements.txt .

RUN ASA_REPO="https://repo.asax.ir/repository" \
    && pip3 install --no-cache-dir -i ${ASA_REPO}/pypi-group1/simple -r requirements.txt --timeout=1000 \
    && sed -i 's/https:\/\/dl-cdn.alpinelinux.org\/alpine/https:\/\/repo.asax.ir\/repository\/dl-cdn.alpinelinux.org--alpine/' /etc/apk/repositories \
    && apk add --no-cache jq \
    && LATEST_TERRAFORM_VERSION=$(wget -qO- ${ASA_REPO}/releases.hashicorp.com/terraform/index.json | jq -r '.versions | keys | .[-1]') \
    && wget -O terraform.zip ${ASA_REPO}/releases.hashicorp.com/terraform/${LATEST_TERRAFORM_VERSION}/terraform_${LATEST_TERRAFORM_VERSION}_linux_amd64.zip \
    && unzip terraform.zip -d /usr/local/bin -x LICENSE.txt \
    && rm terraform.zip \
    && LATEST_PROVIDER_VERSION=$(wget -qO- ${ASA_REPO}/releases.hashicorp.com/terraform-provider-vsphere/index.json | jq -r '.versions | keys | .[-1]') \
    && wget -O terraform-provider-vsphere.zip ${ASA_REPO}/releases.hashicorp.com/terraform-provider-vsphere/${LATEST_PROVIDER_VERSION}/terraform-provider-vsphere_${LATEST_PROVIDER_VERSION}_linux_amd64.zip \
    && mkdir -p ~/.terraform.d/plugin-cache \
    && mkdir -p ~/.terraform.d/plugins/registry.terraform.io/hashicorp/vsphere/${LATEST_PROVIDER_VERSION}/linux_amd64/ \
    && unzip terraform-provider-vsphere.zip -d ~/.terraform.d/plugins/registry.terraform.io/hashicorp/vsphere/${LATEST_PROVIDER_VERSION}/linux_amd64/ -x LICENSE.txt \
    && rm terraform-provider-vsphere.zip

COPY . .