#!/bin/bash

# Check if OpenSSL is installed
if ! command -v openssl &> /dev/null
then
    echo "[x] Error: OpenSSL is not installed."
    echo "👉 Please install it first:"
    echo "   Debian/Ubuntu: sudo apt install openssl"
    echo "   Arch Linux:    sudo pacman -S openssl"
    echo "   RedHat/CentOS: sudo yum install openssl"
    echo "   macOS (brew):  brew install openssl"
    exit 1
fi

echo "[✓] OpenSSL found, proceeding with certificate generation..."
# ... .......... ........... ...


set -e

echo "[*] Cleaning up old certs..."
rm -f rootCA.* sender.* receiver.* *.csr *.srl

echo "[*] Creating OpenSSL config files..."

# Root CA config
cat > openssl_root_ca.cnf <<EOF
[ req ]
default_bits       = 2048
prompt             = no
default_md         = sha256
x509_extensions    = v3_ca
distinguished_name = dn

[ dn ]
CN = MyRootCA

[ v3_ca ]
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid:always,issuer
basicConstraints = critical, CA:TRUE
keyUsage = critical, digitalSignature, cRLSign, keyCertSign
EOF

# Receiver config with SAN = localhost
cat > openssl_receiver.cnf <<EOF
[ req ]
default_bits       = 2048
prompt             = no
default_md         = sha256
distinguished_name = dn
req_extensions     = req_ext

[ dn ]
CN = SEG-Receiver

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = localhost
EOF

echo "[*] Generating Root CA certificate..."
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout rootCA.key -out rootCA.pem \
  -days 1024 -config openssl_root_ca.cnf

echo "[*] Generating SEG-Receiver key and CSR..."
openssl genrsa -out receiver.key 2048
openssl req -new -key receiver.key -out receiver.csr -config openssl_receiver.cnf

echo "[*] Signing SEG-Receiver certificate with SAN=localhost..."
openssl x509 -req -in receiver.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial \
  -out receiver.crt -days 500 -sha256 -extfile openssl_receiver.cnf -extensions req_ext

echo "[*] Generating SEG-Sender key and CSR..."
openssl genrsa -out sender.key 2048
openssl req -new -key sender.key -out sender.csr -subj "/CN=SEG-Sender"

echo "[*] Signing SEG-Sender certificate..."
openssl x509 -req -in sender.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial \
  -out sender.crt -days 500 -sha256

echo "[✔] All certificates generated successfully!"
