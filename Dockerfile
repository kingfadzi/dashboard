FROM almalinux:8

ARG GLOBAL_INDEX_URL
ARG GLOBAL_CERT
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG HOST_UID=1000
ARG HOST_GID=1000

# -----------------------------
# Environment & Proxy Setup
# -----------------------------
ENV PIP_INDEX_URL=${GLOBAL_INDEX_URL}
ENV http_proxy=${HTTP_PROXY}
ENV https_proxy=${HTTPS_PROXY}
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# -----------------------------
# Base System Setup
# -----------------------------
RUN dnf update -y && \
dnf module reset -y python36 && \
dnf install -y \
bash \
nc \
glibc-langpack-en \
python3.11 \
python3.11-pip \
python3.11-devel \
git \
wget \
curl && \
dnf clean all

RUN alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
alternatives --set python3 /usr/bin/python3.11 && \
python3 -m ensurepip && \
python3 -m pip install --no-cache-dir --upgrade pip

# -----------------------------
# Optional CA Certificate
# -----------------------------
COPY tls-ca-bundle.pem* /tmp/ca.pem
RUN if [ -f /tmp/ca.pem ]; then \
echo "Installing custom CA certificate..." && \
mkdir -p /etc/pki/ca-trust/source/anchors && \
cp /tmp/ca.pem /etc/pki/ca-trust/source/anchors/tls-ca-bundle.pem && \
update-ca-trust extract && \
echo "[global]" > /etc/pip.conf && \
echo "cert = /etc/pki/ca-trust/source/anchors/tls-ca-bundle.pem" >> /etc/pip.conf; \
else \
echo "No custom CA certificate provided - skipping installation"; \
fi

# -----------------------------
# User Setup
# -----------------------------
RUN existing_group=$(getent group ${HOST_GID} | cut -d: -f1) && \
if [ -z "$existing_group" ]; then \
groupadd -g ${HOST_GID} dashuser; \
else \
groupmod -n dashuser "$existing_group"; \
fi && \
existing_user=$(getent passwd ${HOST_UID} | cut -d: -f1) && \
if [ -z "$existing_user" ]; then \
useradd -m -u ${HOST_UID} -g dashuser dashuser; \
else \
usermod -l dashuser "$existing_user"; \
fi

# -----------------------------
# Copy and Install
# -----------------------------
WORKDIR /app
COPY --chown=dashuser:dashuser requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY --chown=dashuser:dashuser . /app/

# -----------------------------
# Permissions
# -----------------------------
RUN chown -R ${HOST_UID}:${HOST_GID} /app

USER dashuser

EXPOSE 8050

CMD ["python3", "app.py"]