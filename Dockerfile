FROM almalinux:8

ARG GLOBAL_INDEX_URL
ARG GLOBAL_CERT
ARG HTTP_PROXY
ARG HTTPS_PROXY

ENV PIP_INDEX_URL=${GLOBAL_INDEX_URL}
ENV PIP_CERT=${GLOBAL_CERT}
ENV http_proxy=${HTTP_PROXY}
ENV https_proxy=${HTTPS_PROXY}

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

ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    alternatives --set python3 /usr/bin/python3.11 && \
    python3 -m ensurepip && \
    python3 -m pip install --no-cache-dir --upgrade pip

RUN useradd -m dashuser
USER dashuser

WORKDIR /app

COPY --chown=dashuser:dashuser requirements.txt /app/

RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY --chown=dashuser:dashuser . /app/

EXPOSE 8050

CMD ["python3", "app.py"]
