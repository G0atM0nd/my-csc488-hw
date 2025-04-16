import pytest
import xml.etree.ElementTree as ET
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index_status(client):
    # This test just checks that the index returns a 200 status code.
    response = client.get('/')
    assert response.status_code == 200

def test_load_and_get_epochs_xml(client):
    # First, load the data (which should update our global data variables)
    load_response = client.post('/load-data')
    assert load_response.status_code == 200

    # Now get the epochs; this endpoint returns an XML response.
    response = client.get('/epochs')
    assert response.status_code == 200

    # Parse the XML output.
    try:
        root = ET.fromstring(response.data.decode())
    except ET.ParseError:
        pytest.fail("Response from /epochs is not valid XML")

    # Check that the XML contains an <epochs> element.
    epochs_element = root.find('epochs')
    assert epochs_element is not None, "Expected <epochs> tag not found in the XML response"

    # Optionally, check that there is at least one <item> element under <epochs>
    items = epochs_element.findall('item')
    assert len(items) > 0, "No epoch items found in the XML response"

def test_get_country_xml(client):
    # Load the data first.
    load_response = client.post('/load-data')
    assert load_response.status_code == 200

    # Retrieve a specific country's data; adjust 'United_States' if your XML data differs.
    response = client.get('/countries/United_States')
    assert response.status_code == 200

    try:
        root = ET.fromstring(response.data.decode())
    except ET.ParseError:
        pytest.fail("Response from /countries/United_States is not valid XML")

    # Check that the XML root contains expected child elements (for example, regions)
    # This depends on how your to_xml function structures the output.
    # Here we check that there's at least one child element.
    assert len(list(root)) > 0, "Expected child elements not found in the country XML response"
