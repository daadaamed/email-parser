import json
import re
from lxml import etree

def parse_lacentrale_event(event):
    event = json.loads(event)

    to_emails = re.findall(r'<([^>]+)>', event.get("to", ""))
    if to_emails:
        # Get the last email after the last '\r\n\t'
        to_email = re.split(r'\r\n\t', event.get("to", ""))[-1].strip('<>')
        workspace_name = re.split(r'\r\n\t', event.get("to", ""))[3].strip('<>').split('.')[0][1:]
        workspace_id = re.split(r'\r\n\t', event.get("to", ""))[3].strip('<>').split('.')[1].split('@')[0]
        from_email = event.get("from", "").split('<')[1].split('>')[0] if event.get("from") else ""
    
    # html_content = event['html']
    root = etree.HTML(event['html'])  # Use 'html' instead of 'event'
    td_element_marque = root.xpath('//td[contains(text(), "Marque : SEAT")]')

    # If the element is found, extract the text content
    if td_element_marque:
        marque_line = td_element_marque[0].text.strip()
        # Extract the marque value
        marque = marque_line.split(':')[1].strip()
    else:
        marque = None
    
    # Extract model
    # td_element_model = root.xpath('//td[contains(text(), "Mod\u00e8le :")]')
    # if td_element_model:
    #     model_line = td_element_model[0].text.strip()
    #     model = model_line.split(':')[1].strip()
    # else:
    #     model = None
    subject_match = re.search(fr'{marque} (\w+ \w+)', event.get("subject", ""), re.IGNORECASE)
    model = subject_match.group(1) if subject_match else None

    #Extract Nom
    td_element_nom = root.xpath('//td[contains(text(), "Nom :")]')
    if td_element_nom:
        nom_line = td_element_nom[0].text.strip()
        # Extract the nom value
        lastname = nom_line.split(':')[1].strip().split(' ')[1]
        firstname = nom_line.split(':')[1].strip().split(' ')[2]
    
    # Extract the subject
    subject_raw = event.get("subject", "")
    subject_lines = subject_raw.split('\r\n')
    subject = ' '.join(line.strip() for line in subject_lines if line.strip())


    #Extract mail
    td_element_mail = root.xpath('//td[contains(text(), "Mail :")]')
    if td_element_mail:
        mail_line = td_element_mail[0].text.strip()
        # Extract the mail value
        mail = mail_line.split(':')[1].strip()
    else:
        mail = None

    # extract text
    json_text = event.get("text", "")
    decoded_text = bytes(json_text, 'utf-8').decode('unicode_escape')
    parsed_html = etree.HTML(decoded_text)
    extracted_text = ' '.join(parsed_html.xpath('//text()'))
    final_text = extracted_text.encode('latin1').decode('utf-8').replace('\r\n', ' ')

    # contact_info
    contact_info = [
        {
            "type": "email",
            "value": mail
        }
    ]

    # display the final required information

    return {
        "channel": "lacentrale",
        "from_email": from_email,
        "to_email": to_email,
        "workspace_name": workspace_name,
        "workspace_id": workspace_id,
        'brand': marque,
        'model': model,
        'message': final_text,
        'firstname': firstname,
        'lastname': lastname,
        'customer_email': mail,
        'subject': subject,
        'contact_info': contact_info
    }
