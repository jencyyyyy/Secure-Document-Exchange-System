import requests
from datetime import datetime, timezone
import re
import sys

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

def send_secure_xml(xml_file_path):
    try:
        # Read the specified XML file
        with open(xml_file_path, 'r', encoding='utf-8') as file:
            xml_content = file.read()
        
        # Update the timestamp in the XML content
        updated_xml = update_timestamp(xml_content)
        
        url = "https://localhost:4443"
        cert = ("sender.crt", "sender.key")
        verify = "rootCA.pem"
        
        # Send the XML as a file, preserving the original filename
        files = {
            'file': (xml_file_path, updated_xml.encode('utf-8'), 'application/xml')
        }

        response = requests.post(url, files=files, cert=cert, verify=verify)
        print("[✓] Response from receiver:", response.text)
        
    except FileNotFoundError:
        print(f"[x] Error: XML file '{xml_file_path}' not found")
    except requests.exceptions.SSLError as e:
        print("[x] SSL Error:", e)
    except Exception as e:
        print("[x] Error:", e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python seg_sender.py <xml_file_path>")
        sys.exit(1)
    xml_file_path = sys.argv[1]
    send_secure_xml(xml_file_path)
