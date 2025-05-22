import requests
from datetime import datetime, timezone
import re

def update_timestamp(xml_content):
    # Generate current timestamp in UTC
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    # Replace existing timestamp with new one
    updated_content = re.sub(
        r'<TimestampForSignature>[^<]*</TimestampForSignature>',
        f'<TimestampForSignature>{timestamp}</TimestampForSignature>',
        xml_content
    )
    return updated_content

def send_secure_xml():
    try:
        # Read the document.xml file
        with open('document.xml', 'r', encoding='utf-8') as file:
            xml_content = file.read()
        
        # Update the timestamp in the XML content
        updated_xml = update_timestamp(xml_content)
        
        url = "https://localhost:4443"
        cert = ("sender.crt", "sender.key")
        verify = "rootCA.pem"
        
        # Send the XML as a file
        files = {
            'file': ('document.xml', updated_xml.encode('utf-8'), 'application/xml')
        }

        response = requests.post(url, files=files, cert=cert, verify=verify)
        print("[✓] Response from receiver:", response.text)
        
    except FileNotFoundError:
        print("[x] Error: document.xml file not found")
    except requests.exceptions.SSLError as e:
        print("[x] SSL Error:", e)
    except Exception as e:
        print("[x] Error:", e)

if __name__ == "__main__":
    send_secure_xml()
