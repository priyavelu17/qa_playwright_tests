# Datacenter API Playwright Python Tests

This repository contains comprehensive Playwright Python tests for the Digital Twin Datacenter API.

## API Overview

The Datacenter API provides three main endpoints:

1. **GET /twin/datacenter/v1/model** - Get datacenter twin model (entity types, measurements, and relationships)
2. **GET /twin/datacenter/v1/details/{site_id}** - Get datacenter site details (normalized subgraph)
3. **GET /twin/datacenter/v1/ontology** - Get global ontology

All endpoints require Bearer authentication.

## Test Structure

### Test Files

- `test_datacenter_api.py` - Main test suite with comprehensive API tests
- `config.py` - Configuration and test data
- `test_forecast_api.py` - Example forecast API tests (existing)

### Test Classes

#### TestTwinModelEndpoint
Tests for the `/twin/datacenter/v1/model` endpoint:
- ✅ Successful model retrieval
- ✅ Response structure validation
- ✅ Authentication testing (401 unauthorized)
- ✅ Invalid token handling

#### TestDatacenterDetailsEndpoint
Tests for the `/twin/datacenter/v1/details/{site_id}` endpoint:
- ✅ Successful site details retrieval
- ✅ Query parameter filtering (entityType, relationshipType, include, limit)
- ✅ Pagination with cursor support
- ✅ Not found scenarios (404)
- ✅ Invalid cursor handling (400)
- ✅ Authentication testing

#### TestOntologyEndpoint
Tests for the `/twin/datacenter/v1/ontology` endpoint:
- ✅ Successful ontology retrieval
- ✅ JSON-LD structure validation
- ✅ Namespace mappings validation
- ✅ Authentication testing

#### TestEntityValidation
Tests for entity structure validation:
- ✅ SiteType entity structure
- ✅ PowerDeviceType entity with measurements
- ✅ Attributes and state validation

#### TestRelationshipValidation
Tests for relationship structure validation:
- ✅ Relationship type validation
- ✅ Source and target validation
- ✅ Relationship structure compliance

#### TestErrorHandling
Tests for API error responses:
- ✅ Error envelope structure
- ✅ Error codes and messages

## Setup

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install
```

### Configuration

Before running tests, update the authentication token in `test_datacenter_api.py`:

```python
extra_http_headers={
    "Authorization": "Bearer YOUR_ACTUAL_JWT_TOKEN_HERE"
}
```

Or use the `config.py` file to centralize your test configuration.

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/test_datacenter_api.py
```

### Run specific test class
```bash
pytest tests/test_datacenter_api.py::TestTwinModelEndpoint
```

### Run specific test
```bash
pytest tests/test_datacenter_api.py::TestTwinModelEndpoint::test_get_twin_model_success
```

### Run with verbose output
```bash
pytest -v
```

### Run with detailed output and print statements
```bash
pytest -v -s
```

### Generate HTML report
```bash
pytest --html=report.html --self-contained-html
```

## Test Coverage

The test suite covers:

### HTTP Status Codes
- ✅ 200 OK - Successful requests
- ✅ 400 Bad Request - Invalid parameters
- ✅ 401 Unauthorized - Missing/invalid authentication
- ✅ 404 Not Found - Non-existent resources
- ✅ 422 Unprocessable Entity - Invalid value combinations
- ✅ 500 Internal Server Error - Server errors

### API Features
- ✅ Bearer token authentication
- ✅ Query parameter filtering
- ✅ Cursor-based pagination
- ✅ Entity type filtering
- ✅ Relationship type filtering
- ✅ Response structure validation
- ✅ Error response validation

### Entity Types Supported
The API supports 30+ entity types including:
- Location types: SiteType, ElectricalRoom, DataHall, BatteryRoom, GeneratorYard, etc.
- Power equipment: PDUType, UPSType, ATSType, TransformerType, etc.
- Monitoring: PQMeterType, GatewayType, ControllerType, etc.

### Measurement Types Supported
20+ measurement types including:
- Power measurements: ActivePower, ApparentPower, ReactivePower
- Electrical measurements: Voltage, Current, Frequency, PowerFactor
- Battery measurements: SoC, SoH, DCVoltage, DCCurrent
- Environmental: Temperature, Humidity

### Relationship Types Supported
19+ relationship types including:
- Power flow: feeds, fedBy, suppliesPowerTo, suppliedBy
- Location: hasLocation, locatedIn, containsEquipment
- Connection: connectedTo, connectedFrom
- Control: controls, controlledBy
- Protection: protects, protectedBy

## Environment Variables

You can use environment variables for configuration:

```bash
export DATACENTER_API_URL="https://your-api-host:8000"
export DATACENTER_API_TOKEN="your-jwt-token"
```

Then update the fixture:

```python
import os

@pytest.fixture(scope="session")
def datacenter_api_context(playwright):
    request_context = playwright.request.new_context(
        base_url=os.getenv("DATACENTER_API_URL", "https://localhost:8000"),
        extra_http_headers={
            "Authorization": f"Bearer {os.getenv('DATACENTER_API_TOKEN', 'YOUR_JWT_TOKEN_HERE')}"
        }
    )
    yield request_context
    request_context.dispose()
```

## Continuous Integration

Example GitHub Actions workflow:

```yaml
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install
      - name: Run tests
        env:
          DATACENTER_API_URL: ${{ secrets.API_URL }}
          DATACENTER_API_TOKEN: ${{ secrets.API_TOKEN }}
        run: pytest -v
```

## Extending Tests

### Adding New Test Cases

1. Create a new test class or add to existing class
2. Use the `datacenter_api_context` fixture
3. Follow the naming convention: `test_*`

Example:
```python
def test_new_scenario(self, datacenter_api_context: APIRequestContext):
    response = datacenter_api_context.get("/your/endpoint")
    assert response.ok
    # Add your assertions
```

### Testing Specific Entity Types

```python
def test_specific_entity_type(self, datacenter_api_context: APIRequestContext):
    site_id = "Site-001"
    response = datacenter_api_context.get(
        f"/twin/datacenter/v1/details/{site_id}",
        params={"entityType": "UPSType"}
    )
    assert response.ok
    data = response.json()
    # Validate UPS-specific attributes
```

## Troubleshooting

### SSL Certificate Issues

If testing against localhost with self-signed certificates:

```python
request_context = playwright.request.new_context(
    base_url="https://localhost:8000",
    ignore_https_errors=True,  # Add this line
    extra_http_headers={...}
)
```

### Authentication Failures

Ensure your JWT token:
- Is valid and not expired
- Has the correct format: "Bearer YOUR_TOKEN"
- Has appropriate permissions for the API

### Network Timeouts

Increase timeout if needed:

```python
response = datacenter_api_context.get(
    "/twin/datacenter/v1/details/Site-001",
    timeout=30000  # 30 seconds
)
```

## License

[Your License Here]

## Contributing

[Your Contributing Guidelines Here]
