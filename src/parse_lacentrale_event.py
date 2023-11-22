import json
import re
from lxml import etree

def parse_lacentrale_event(event):
    event = json.loads(event)

    # Get the last email after the last '\r\n\t'
    to_email = re.split(r'\r\n\t', event.get("to", ""))[-1].strip('<>')

    from_email = event.get("from", "").split('<')[1].split('>')[0] 

    workspace_name = re.split(r'\r\n\t', event.get("to", ""))[3].strip('<>').split('.')[0][1:]
    workspace_id = re.split(r'\r\n\t', event.get("to", ""))[3].strip('<>').split('.')[1].split('@')[0]
    
    data_from_html = etree.HTML(event['html'])  
    td_element_marque = data_from_html.xpath('//td[contains(text(), "Marque : SEAT")]')

    # If the element is found, extract the text content
    if td_element_marque:
        marque_line = td_element_marque[0].text.strip()
        # Extract the marque value
        marque = marque_line.split(':')[1].strip()
    else:
        marque = None
    # get the subject
    subject_match = re.search(fr'{marque} (\w+ \w+)', event.get("subject", ""), re.IGNORECASE)
    model = subject_match.group(1) if subject_match else None

    #Extract Nom
    td_element_nom = data_from_html.xpath('//td[contains(text(), "Nom :")]')
    if td_element_nom:
        nom_line = td_element_nom[0].text.strip()
        # Extract the nom value to het first name and last name separated by a space
        lastname = nom_line.split(':')[1].strip().split(' ')[1]
        firstname = nom_line.split(':')[1].strip().split(' ')[2]
    
    # Extract the subject
    subject_raw = event.get("subject", "")
    subject_lines = subject_raw.split('\r\n')
    subject = ' '.join(line.strip() for line in subject_lines if line.strip())


    #Extract mail
    td_element_mail = data_from_html.xpath('//td[contains(text(), "Mail :")]')
    if td_element_mail:
        mail_line = td_element_mail[0].text.strip()
        # Extract the mail value
        mail = mail_line.split(':')[1].strip()
    else:
        mail = None

    # extract text from the json
    json_text = event.get("text", "")
    # decode the french text to become readable
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

    # display the final informations in the required formats

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
