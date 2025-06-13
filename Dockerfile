FROM almalinux:8

ARG GLOBAL_INDEX_URL
ARG GLOBAL_CERT
ARG HTTP_PROXY
ARG HTTPS_PROXY

ENV PIP_INDEX_URL=${GLOBAL_INDEX_URL}
ENV PIP_CERT=${GLOBAL_CERT}
ENV http_proxy=${HTTP_PROXY}
ENV https_proxy=${HTTPS_PROXY}
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN dnf update -y && \
    dnf module reset -y python36 && \
    dnf install -y \
        bash \
        nc \
        glibc-langpack-en \
        python3.11 \
        python3-pip \
        python3-devel \
        git \
        wget && \
    dnf clean all

RUN alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    alternatives --set python3 /usr/bin/python3.11 && \
    python3 -m ensurepip && \
    python3 -m pip install --no-cache-dir --upgrade pip

RUN useradd -m dashuser
USER dashuser

WORKDIR /app

# Always copy the cert if it's expected
COPY --chown=dashuser:dashuser tls-ca-bundle.pem /app/certs/tls-ca-bundle.pem

COPY --chown=dashuser:dashuser requirements.txt /app/

# Conditionally unset PIP_CERT if file is missing to prevent pip errors
RUN if [ ! -f "$PIP_CERT" ]; then echo "Warning: cert file $PIP_CERT not found, disabling pip cert"; unset PIP_CERT; fi && \
    python3 -m pip install --no-cache-dir -r requirements.txt

COPY --chown=dashuser:dashuser . /app/

EXPOSE 8050

CMD ["python3", "app.py"]
