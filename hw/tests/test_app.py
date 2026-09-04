import pytest


@pytest.mark.parametrize("url", ["/clients", "/clients/1"])
def test_get_response_200(client, url):
	response = client.get(url)
	assert response.status_code == 200


def test_create_new_client(client):
	data = {
		"name": "Petr",
		"surname": "Petrov",
		"credit_card": "MasterCard",
		"card_number": "123456",
	}
	response = client.post("/clients", json=data)
	assert response.status_code == 201


def test_create_new_parking(client):
	data = {
		"address": "Test address",
		"opened": True,
		"count_places": 10,
		"count_available_places": 10
	}
	response = client.post("/parkings", json=data)
	assert response.status_code == 201


@pytest.mark.parking
def test_client_parking_entry(client):
	new_client_data = {
		"name": "Petr",
		"surname": "Petrov",
		"credit_card": "MasterCard",
		"card_number": "555"
	}
	client_res = client.post("/clients", json=new_client_data)
	client_id = client_res.json.get("id") or 2
	data = {
		"client_id": client_id,
		"parking_id": 1
	}

	response = client.post("/client_parkings", json=data)

	assert response.status_code == 201
	assert response.json["success"] is True
	assert response.json["client-parking"]["time_in"] is not None




@pytest.mark.parking
def test_parking_exit(client):
	new_client_data = {
		"name": "Petr",
		"surname": "Petrov",
		"credit_card": "MasterCard",
		"card_number": "555"
	}
	client_res = client.post("/clients", json=new_client_data)

	client_id = client_res.json.get("id") or 2
	setup_data = {
		"client_id": client_id,
		"parking_id": 1
	}
	client.post("/client_parkings", json=setup_data)

	response = client.delete("/client_parkings", json=setup_data)

	assert response.status_code == 200
	assert response.json["success"] is True
	assert response.json["client-parking"]["time_out"] is not None



