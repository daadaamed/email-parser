import pytest

from parse_leboncoin_event import parse_leboncoin_event


@pytest.fixture(scope="module")
def parsed_leboncoin_event():
    with open("events/leboncoin.json", "r") as f:
        event = f.read()
    return parse_leboncoin_event(event)


def test_parsed_channel(parsed_leboncoin_event):
    assert parsed_leboncoin_event["channel"] == "leboncoin"


def test_parsed_from_email(parsed_leboncoin_event):
    assert parsed_leboncoin_event["from_email"] == "message@leboncoin.fr"


def test_parsed_to_email(parsed_leboncoin_event):
    assert parsed_leboncoin_event["to_email"] == "abc.ab77535e-6fe7-4b44-82bb-64c6f82ef5a4@prochaineauto.com"


def test_parsed_workspace_name(parsed_leboncoin_event):
    assert parsed_leboncoin_event["workspace_name"] == "abc"


def test_parsed_workspace_id(parsed_leboncoin_event):
    assert parsed_leboncoin_event["workspace_id"] == "ab77535e-6fe7-4b44-82bb-64c6f82ef5a4"


def test_parsed_brand(parsed_leboncoin_event):
    assert parsed_leboncoin_event["brand"] == "Mazda"


def test_parsed_model(parsed_leboncoin_event):
    assert parsed_leboncoin_event["model"] == "CX-3 2.0L Skyactiv-G 120 4x2 Signature"


def test_parsed_message(parsed_leboncoin_event):
    assert parsed_leboncoin_event["message"] == "« Bonjour, est-ce un véhicule d’importation a-t-il été entretenu dans le réseau Mazda quel est le pourcentage d’usure des pneus et quelles sont les impacts rayures ou accident de la carrosserie merci de me préciser également quelles sont les frais de mise en service cordialement »"


def test_parsed_firstname(parsed_leboncoin_event):
    assert parsed_leboncoin_event["firstname"] == "leonard"


def test_parsed_lastname(parsed_leboncoin_event):
    assert parsed_leboncoin_event["lastname"] == "oxxo"


def test_parsed_customer_phone_number(parsed_leboncoin_event):
    assert parsed_leboncoin_event["customer_phone_number"] == "0123456789"


def test_parsed_customer_email(parsed_leboncoin_event):
    assert parsed_leboncoin_event["customer_email"] == "leonard@orange.fr"


def test_parsed_subject(parsed_leboncoin_event):
    assert parsed_leboncoin_event["subject"] == "Nouveau message concernant l\'annonce \"Mazda CX-3 2.0L Skyactiv-G 120 4x2 Signature\" sur leboncoin"


def test_parsed_links(parsed_leboncoin_event):
    assert parsed_leboncoin_event["links"] == {
        "lead": "https://www.leboncoin.fr/voitures/2085528565.htm"
    }


def test_parsed_contact_info(parsed_leboncoin_event):
    assert parsed_leboncoin_event["contact_info"] == [
        {
            "type": "email",
            "value": "leonard@orange.fr"
        },
        {
            "type": "phone_number",
            "value": "0123456789"
        }
    ]
