from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200


def test_list_grants_returns_four():
    response = client.get("/api/grants")
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_get_grant_by_id_found():
    response = client.get("/api/grants/sfi-2026")
    assert response.status_code == 200
    assert response.json()["id"] == "sfi-2026"


def test_get_grant_by_id_not_found():
    response = client.get("/api/grants/does-not-exist")
    assert response.status_code == 404


def test_match_endpoint_returns_four_results():
    profile = {
        "farm_type": "arable",
        "size_hectares": 10,
        "region": "england",
        "activities": ["arable_cropping"],
        "has_sbi": True,
        "sbi_registered_before_2026_01_01": True,
        "has_existing_elm_agreement": False,
        "has_environmentally_significant_features": False,
    }
    response = client.post("/api/match", json=profile)
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 4
    statuses = {r["status"] for r in results}
    assert statuses.issubset({"matched", "partial", "not_matched"})


def test_match_endpoint_rejects_malformed_body():
    response = client.post("/api/match", json={"farm_type": "not_a_real_type"})
    assert response.status_code == 422
