import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from api.api import api

# Create a FastAPI app and include the router
app = FastAPI()
app.include_router(api)

# Create a TestClient for your FastAPI application
client = TestClient(app)

def test_read_root():
    """
    Test the health check endpoint.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "API is running"}

def test_do_research_success(mocker):
    """
    Test the /do-research endpoint for a successful research.
    """
    # Mock the run_deep_research function to return a successful result
    mocker.patch('api.api.run_deep_research', return_value={"report": "mocked research report"})
    
    response = client.post("/do-research", json={"topic": "test topic"})
    assert response.status_code == 200
    assert response.json() == {"report": "mocked research report"}

def test_do_research_failure_internal_error(mocker):
    """
    Test the /do-research endpoint when run_deep_research raises an exception.
    """
    # Mock the run_deep_research function to raise an exception
    mocker.patch('api.api.run_deep_research', side_effect=Exception("Internal research error"))
    
    response = client.post("/do-research", json={"topic": "test topic"})
    assert response.status_code == 500
    assert "Internal research error" in response.json()["detail"]

def test_do_research_failure_api_error(mocker):
    """
    Test the /do-research endpoint when run_deep_research returns an error dictionary.
    """
    # Mock the run_deep_research function to return an error dictionary
    mocker.patch('api.api.run_deep_research', return_value={"error": "API specific research error"})
    
    response = client.post("/do-research", json={"topic": "test topic"})
    assert response.status_code == 500
    assert "API specific research error" in response.json()["detail"]
