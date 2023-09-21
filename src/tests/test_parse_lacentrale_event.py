import pytest

from parse_lacentrale_event import parse_lacentrale_event


@pytest.fixture(scope="module")
def parsed_lacentrale_event():
    with open("events/lacentrale.json", "r") as f:
        event = f.read()
    return parse_lacentrale_event(event)


def test_parsed_channel(parsed_lacentrale_event):
    assert parsed_lacentrale_event["channel"] == "lacentrale"


def test_parsed_from_email(parsed_lacentrale_event):
    assert parsed_lacentrale_event["from_email"] == "no_reply@lacentrale.fr"


def test_parsed_to_email(parsed_lacentrale_event):
    assert parsed_lacentrale_event["to_email"] == "volkswagen.f870e411-02bf-4a32-afa0-c7618d7e7315@prochaineauto.com"


def test_parsed_workspace_name(parsed_lacentrale_event):
    assert parsed_lacentrale_event["workspace_name"] == "volkswagen"


def test_parsed_workspace_id(parsed_lacentrale_event):
    assert parsed_lacentrale_event["workspace_id"] == "f870e411-02bf-4a32-afa0-c7618d7e7315"


def test_parsed_brand(parsed_lacentrale_event):
    assert parsed_lacentrale_event["brand"] == "SEAT"


def test_parsed_model(parsed_lacentrale_event):
    assert parsed_lacentrale_event["model"] == "LEON III"


def test_parsed_message(parsed_lacentrale_event):
    assert parsed_lacentrale_event["message"] == "bonjour. je possède un seat Léon 2 style 1.6 TDI de 2010 ,  250000km. pneu neuf , amotisseurs neuf , embrayage neuf . j'aimerais savoir si il y a une possibilité de reprise , et es-ce que vous pouvez faire une livraison à domicile , si achat ."


def test_parsed_firstname(parsed_lacentrale_event):
    assert parsed_lacentrale_event["firstname"] == "jean-baptiste"


def test_parsed_lastname(parsed_lacentrale_event):
    assert parsed_lacentrale_event["lastname"] == "roi"


def test_parsed_customer_email(parsed_lacentrale_event):
    assert parsed_lacentrale_event["customer_email"] == "1cc8bfd6-0009-50c9-9f29-1e6464a55fe2@messagerie.lacentrale.fr"


def test_parsed_subject(parsed_lacentrale_event):
    assert parsed_lacentrale_event["subject"] == "Nouveau message pour votre annonce E109620631 - SEAT LEON III (2) 1.6 TDI 115 START/STOP STYLE BUSINESS"


def test_parsed_contact_info(parsed_lacentrale_event):
    assert parsed_lacentrale_event["contact_info"] == [
        {
            "type": "email",
            "value": "1cc8bfd6-0009-50c9-9f29-1e6464a55fe2@messagerie.lacentrale.fr"
        }
    ]
