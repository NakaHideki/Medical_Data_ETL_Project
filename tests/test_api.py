from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_hello():
    """/ のGETが200を返すか"""
    response = client.get("/")
    assert response.status_code == 200

def test_get_patient_found():
    """存在する患者IDで正しいデータが返るか"""
    response = client.get("/patients/P001")
    assert response.status_code == 200
    assert response.json()["patient_id"] == "P001"

def test_etl_run():
    """/etl/run が正しくクレンジングするか"""
    response = client.get("/etl/run")
    assert response.status_code == 200
    data = response.json()
    assert data["clean_count"] < data["raw_count"]