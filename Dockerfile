FROM almalinux:8

# Accept build-time arguments
ARG GLOBAL_INDEX_URL
ARG GLOBAL_CERT
ARG HTTP_PROXY
ARG HTTPS_PROXY

# Set up environment
ENV PIP_INDEX_URL=${GLOBAL_INDEX_URL}
ENV PIP_CERT=${GLOBAL_CERT}
ENV http_proxy=${HTTP_PROXY}
ENV https_proxy=${HTTPS_PROXY}
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Install system packages
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

# Set python 3.11 as default
RUN alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    alternatives --set python3 /usr/bin/python3.11 && \
    python3 -m ensurepip && \
    python3 -m pip install --no-cache-dir --upgrade pip

# Add user and switch
RUN useradd -m dashuser
USER dashuser

WORKDIR /app

# Copy cert into container
COPY --chown=dashuser:dashuser tls-ca-bundle.pem /app/certs/tls-ca-bundle.pem

# Copy requirements and install
COPY --chown=dashuser:dashuser requirements.txt /app/
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy rest of the code
COPY --chown=dashuser:dashuser . /app/

EXPOSE 8050

CMD ["python3", "app.py"]
