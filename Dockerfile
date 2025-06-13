FROM almalinux:8

ARG GLOBAL_INDEX_URL
ARG HTTP_PROXY
ARG HTTPS_PROXY

ENV PIP_INDEX_URL=${GLOBAL_INDEX_URL}
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
RUN mkdir -p /app/certs

COPY --chown=dashuser:dashuser tls-ca-bundle.pem /app/certs/tls-ca-bundle.pem
COPY --chown=dashuser:dashuser requirements.txt /app/

RUN CERT_PATH="/app/certs/tls-ca-bundle.pem" && \
    if [ -f "$CERT_PATH" ]; then \
      echo "Installing with cert: $CERT_PATH" && \
      python3 -m pip install --no-cache-dir --cert "$CERT_PATH" -r requirements.txt ; \
    else \
      echo "Installing without cert" && \
      python3 -m pip install --no-cache-dir -r requirements.txt ; \
    fi

COPY --chown=dashuser:dashuser . /app/

EXPOSE 8050

CMD ["python3", "app.py"]
