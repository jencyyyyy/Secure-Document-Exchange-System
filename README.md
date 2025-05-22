# SEG Secure Document Transmission

This project securely sends signed XML documents between systems using mutual TLS (client and server certificates) and cryptographic signatures.

---

##  Components

- `generate_certs.sh` - Bash script to generate Root CA and certificates for sender and receiver.
- `seg_sender.py` - Python script to sign and send the XML document securely.
- `seg_receiver.py` - Python script to receive and verify signed XML over HTTPS.
- `document.xml` - XML document to send.

---

## File Structure

```

.
├── generate_certs.sh      # Script to generate Root CA and certs
├── seg_sender.py          # Signs and sends the XML document
├── seg_receiver.py        # Receives signed XML securely
├── document.xml           # XML document to send
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

````

---

## Setup Instructions

### 1.  Install Requirements

```bash

pip install -r requirements.txt
````

### 2.  Generate Certificates

Run the following script to automatically generate:

* Root CA (`rootCA.pem`)
* Sender key and cert (`sender.key`, `sender.crt`)
* Receiver key and cert (`receiver.key`, `receiver.crt` with SAN for `localhost`)

```bash
chmod +x generate_certs.sh
./generate_certs.sh
```

---

## Usage

### Start the Receiver (in one terminal)

```bash
python3 seg_receiver.py
```

### Send Signed Document (in another terminal)

```bash
python3 seg_sender.py
```
* Includes current UTC timestamp in `<TimestampForSignature>`.

---

## Notes

* The receiver must trust `rootCA.pem`.
* The receiver certificate includes `localhost` in SAN to avoid SSL hostname mismatch.

---
