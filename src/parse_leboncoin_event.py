import json
import re
from lxml import etree
from bs4 import BeautifulSoup

def parse_leboncoin_event(event):
    event = json.loads(event)
    # extracting to_email from_email workspace_name and workspace_id
    to_email = re.findall(r'<([^>]+)>', event.get("to", ""))[-1]
    workspace_name = re.split(r'\r\n\t', event.get("to", ""))[3].strip('<>').split('.')[0][1:]
    workspace_id = re.split(r'\r\n\t', event.get("to", ""))[3].strip('<>').split('.')[1].split('@')[0]
    from_email = event.get("from", "").split('<')[1].split('>')[0] if event.get("from") else ""

    # Extracting firstname
    firstname_match = re.findall(r'Pr\u00e9nom : (\w+)', event.get('text', ''))
    firstname = firstname_match[0] if firstname_match else None

    # Extracting last_name:
    last_name_pattern = re.compile(r'Nom : (\w+)')
    lastname = last_name_pattern.search(event.get('text', '')).group(1)

    # Extract email
    email_match = re.search(r'E-mail\s*:\s*([\w.-]+@[a-zA-Z]+\.[a-zA-Z]+)', event.get('text', ''))
    email = email_match.group(1) if email_match else None

    # Extract phone number
    phone_match = re.search(r'Téléphone\s*:\s*([\d\s-]+)', event.get('text', ''))
    phone_number = phone_match.group(1).split()[0] if phone_match else None

    # Extracting message from text
    message_match = re.search(r'«(.*?)»', event['text'], re.DOTALL)
    message = '« ' + message_match.group(1).replace('\r\n', '').strip() + ' »' if message_match else None

    # extract the subject:
    subject = event.get("subject", "").replace('\r\n', '')

    # extract link:
    link_match = re.search(r'Lien\s*:\s*([\s\S]+?)\s*\(', event['text'])    
    link = link_match.group(1).strip() if link_match else None

    # extract the brand and the model, i used the library beautifulsoup for the html in the json
    soup = BeautifulSoup(event.get("html", ""), 'html.parser')
    brand_model_element = soup.find('b')
    brand_model_text = brand_model_element.text.strip()
    brand = brand_model_text.split(' ')[0] if brand_model_element else None
    model = brand_model_text.split(' ', 1)[1] if brand_model_element else None
    return {
        "channel": "leboncoin",
        "from_email": from_email,
        "to_email": to_email,
        "workspace_name": workspace_name,
        "workspace_id": workspace_id,
        'brand': brand,
        'model': model,
        'message': message,
        'firstname': firstname,
        'lastname': lastname,
        'customer_email': email,
        'customer_phone_number': phone_number,
        'subject': subject,
        'links':  {"lead": link},
        'contact_info':  [
        {'type': 'email', 'value': email},
        {'type': 'phone_number', 'value': phone_number}
    ]
    }
