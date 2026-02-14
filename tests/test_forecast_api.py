import pytest
from playwright.sync_api import APIRequestContext


@pytest.fixture(scope="session")
def api_request_context(playwright):
    """Create API request context with base configuration"""
    request_context = playwright.request.new_context(
        base_url="http://localhost:8000",
        extra_http_headers={
            "Authorization": "Bearer token"
        }
    )
    yield request_context
    request_context.dispose()


def test_forecast_api(api_request_context: APIRequestContext):
    """Test the forecast API endpoint with longitude and latitude parameters"""
    # Make GET request with query parameters
    response = api_request_context.get(
        "/v1/forecast",
        params={
            "longitude": "-122.4194",
            "latitude": "37.7749"
        }
    )
    
    # Assert response status
    assert response.ok, f"Request failed with status {response.status}"
    assert response.status == 200
    
    # Get response data
    response_data = response.json()
    print(f"Response status: {response.status}")
    
    # Assert main data structure exists
    assert "data" in response_data, "Response missing 'data' key"
    data = response_data["data"]
    
    # Assert resource information
    assert "resource" in data, "Response missing 'resource' key"
    resource = data["resource"]
    assert resource["longitude"] == -122.4194, f"Unexpected longitude: {resource['longitude']}"
    assert resource["latitude"] == 37.7749, f"Unexpected latitude: {resource['latitude']}"
    assert "timezone" in resource, "Resource missing 'timezone'"
    assert "elevation" in resource, "Resource missing 'elevation'"
    
    # Assert metrics array
    assert "metrics" in data, "Response missing 'metrics' key"
    metrics = data["metrics"]
    assert isinstance(metrics, list), "Metrics should be a list"
    assert len(metrics) > 0, "Metrics array is empty"
    
    # Validate metrics structure
    expected_metrics = ["dryBulbTemperature", "wetBulbTemperature", "relativeHumidity"]
    metric_names = [m["name"] for m in metrics]
    for expected_metric in expected_metrics:
        assert expected_metric in metric_names, f"Missing metric: {expected_metric}"
    
    # Validate each metric has required fields
    for metric in metrics:
        assert "name" in metric, "Metric missing 'name'"
        assert "unit" in metric, "Metric missing 'unit'"
        assert "quantityKind" in metric, "Metric missing 'quantityKind'"
        assert "description" in metric, "Metric missing 'description'"
    
    # Assert points array
    assert "points" in data, "Response missing 'points' key"
    points = data["points"]
    assert isinstance(points, list), "Points should be a list"
    assert len(points) > 0, "Points array is empty"
    
    # Validate points structure
    for point in points:
        assert "timestamp" in point, "Point missing 'timestamp'"
        assert "dryBulbTemperature" in point, "Point missing 'dryBulbTemperature'"
        assert "wetBulbTemperature" in point, "Point missing 'wetBulbTemperature'"
        assert "relativeHumidity" in point, "Point missing 'relativeHumidity'"
        
        # Validate data types
        assert isinstance(point["timestamp"], str), "Timestamp should be string"
        assert isinstance(point["dryBulbTemperature"], (int, float)), "dryBulbTemperature should be numeric"
        assert isinstance(point["wetBulbTemperature"], (int, float)), "wetBulbTemperature should be numeric"
        assert isinstance(point["relativeHumidity"], (int, float)), "relativeHumidity should be numeric"
    
    print(f"Validation passed! Found {len(points)} forecast points")
