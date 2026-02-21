import pytest
from playwright.sync_api import APIRequestContext


@pytest.fixture(scope="session")
def datacenter_api_context(playwright):
    """Create API request context for Datacenter API with authentication"""
    request_context = playwright.request.new_context(
        base_url="https://localhost:8000",
        extra_http_headers={
            "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
        }
    )
    yield request_context
    request_context.dispose()


class TestTwinModelEndpoint:
    """Test suite for /twin/datacenter/v1/model endpoint"""
    
    def test_get_twin_model_success(self, datacenter_api_context: APIRequestContext):
        """Test successful retrieval of datacenter twin model"""
        response = datacenter_api_context.get("/twin/datacenter/v1/model")
        
        # Assert response status
        assert response.ok, f"Request failed with status {response.status}"
        assert response.status == 200
        
        # Get response data
        data = response.json()
        
        # Assert required fields exist
        assert "entityTypes" in data, "Response missing 'entityTypes' key"
        assert "measurements" in data, "Response missing 'measurements' key"
        assert "relationships" in data, "Response missing 'relationships' key"
        
        # Assert entityTypes is an array
        assert isinstance(data["entityTypes"], list), "entityTypes should be an array"
        
        # Assert measurements is an array
        assert isinstance(data["measurements"], list), "measurements should be an array"
        
        # Assert relationships is an array
        assert isinstance(data["relationships"], list), "relationships should be an array"
        
        # Validate entity types structure (if not empty)
        if len(data["entityTypes"]) > 0:
            entity = data["entityTypes"][0]
            assert "id" in entity, "Entity missing 'id' field"
            assert "entityType" in entity, "Entity missing 'entityType' field"
        
        # Validate measurements structure (if not empty)
        if len(data["measurements"]) > 0:
            measurement = data["measurements"][0]
            assert "value" in measurement, "Measurement missing 'value' field"
            assert "measurementType" in measurement, "Measurement missing 'measurementType' field"
        
        # Validate relationships structure (if not empty)
        if len(data["relationships"]) > 0:
            relationship = data["relationships"][0]
            assert "relationshipType" in relationship, "Relationship missing 'relationshipType' field"
    
    def test_get_twin_model_unauthorized(self, playwright):
        """Test twin model endpoint without authentication"""
        # Create context without auth header
        request_context = playwright.request.new_context(
            base_url="https://localhost:8000"
        )
        
        response = request_context.get("/twin/datacenter/v1/model")
        
        # Should return 401 Unauthorized
        assert response.status == 401, f"Expected 401, got {response.status}"
        
        request_context.dispose()
    
    def test_get_twin_model_invalid_token(self, playwright):
        """Test twin model endpoint with invalid bearer token"""
        request_context = playwright.request.new_context(
            base_url="https://localhost:8000",
            extra_http_headers={
                "Authorization": "Bearer INVALID_TOKEN"
            }
        )
        
        response = request_context.get("/twin/datacenter/v1/model")
        
        # Should return 401 Unauthorized
        assert response.status == 401, f"Expected 401, got {response.status}"
        
        request_context.dispose()


class TestDatacenterDetailsEndpoint:
    """Test suite for /twin/datacenter/v1/details/{site_id} endpoint"""
    
    def test_get_datacenter_details_success(self, datacenter_api_context: APIRequestContext):
        """Test successful retrieval of datacenter site details"""
        site_id = "Site-001"
        response = datacenter_api_context.get(f"/twin/datacenter/v1/details/{site_id}")
        
        # Assert response status
        assert response.ok, f"Request failed with status {response.status}"
        assert response.status == 200
        
        # Get response data
        data = response.json()
        
        # Assert required fields exist
        assert "siteId" in data, "Response missing 'siteId' key"
        assert "entities" in data, "Response missing 'entities' key"
        assert "relationships" in data, "Response missing 'relationships' key"
        assert "page" in data, "Response missing 'page' key"
        
        # Validate siteId matches request
        assert data["siteId"] == site_id, f"Expected siteId '{site_id}', got '{data['siteId']}'"
        
        # Assert entities is an array
        assert isinstance(data["entities"], list), "entities should be an array"
        
        # Assert relationships is an array
        assert isinstance(data["relationships"], list), "relationships should be an array"
        
        # Validate entity structure (if not empty)
        if len(data["entities"]) > 0:
            entity = data["entities"][0]
            assert "id" in entity, "Entity missing 'id' field"
            assert "type" in entity, "Entity missing 'type' field"
            assert "attributes" in entity, "Entity missing 'attributes' field"
            
            # Validate attributes structure
            attributes = entity["attributes"]
            assert isinstance(attributes, dict), "attributes should be an object"
        
        # Validate relationship structure (if not empty)
        if len(data["relationships"]) > 0:
            relationship = data["relationships"][0]
            assert "id" in relationship, "Relationship missing 'id' field"
            assert "source" in relationship, "Relationship missing 'source' field"
            assert "target" in relationship, "Relationship missing 'target' field"
            assert "type" in relationship, "Relationship missing 'type' field"
        
        # Validate page structure
        page = data["page"]
        assert isinstance(page, dict), "page should be an object"
    
    def test_get_datacenter_details_with_filters(self, datacenter_api_context: APIRequestContext):
        """Test datacenter details with query parameters for filtering"""
        site_id = "Site-001"
        response = datacenter_api_context.get(
            f"/twin/datacenter/v1/details/{site_id}",
            params={
                "entityType": "PDUType",
                "limit": "10"
            }
        )
        
        # Assert response status
        assert response.ok, f"Request failed with status {response.status}"
        assert response.status == 200
        
        data = response.json()
        
        # Validate filtered entities
        if len(data["entities"]) > 0:
            for entity in data["entities"]:
                # When filtered, entities should match the type
                assert "type" in entity, "Entity missing 'type' field"
    
    def test_get_datacenter_details_with_pagination(self, datacenter_api_context: APIRequestContext):
        """Test datacenter details with pagination parameters"""
        site_id = "Site-001"
        response = datacenter_api_context.get(
            f"/twin/datacenter/v1/details/{site_id}",
            params={
                "limit": "5"
            }
        )
        
        # Assert response status
        assert response.ok, f"Request failed with status {response.status}"
        assert response.status == 200
        
        data = response.json()
        page = data["page"]
        
        # Check if nextCursor exists when there are more results
        if "nextCursor" in page:
            cursor = page["nextCursor"]
            
            # Make second request with cursor
            response2 = datacenter_api_context.get(
                f"/twin/datacenter/v1/details/{site_id}",
                params={
                    "limit": "5",
                    "cursor": cursor
                }
            )
            
            assert response2.ok, f"Paginated request failed with status {response2.status}"
            data2 = response2.json()
            
            # Verify second page has data
            assert "entities" in data2, "Second page missing 'entities' key"
    
    def test_get_datacenter_details_not_found(self, datacenter_api_context: APIRequestContext):
        """Test datacenter details with non-existent site ID"""
        site_id = "NON_EXISTENT_SITE"
        response = datacenter_api_context.get(f"/twin/datacenter/v1/details/{site_id}")
        
        # Should return 404 Not Found
        assert response.status == 404, f"Expected 404, got {response.status}"
    
    def test_get_datacenter_details_invalid_cursor(self, datacenter_api_context: APIRequestContext):
        """Test datacenter details with invalid cursor"""
        site_id = "Site-001"
        response = datacenter_api_context.get(
            f"/twin/datacenter/v1/details/{site_id}",
            params={
                "cursor": "INVALID_CURSOR_VALUE"
            }
        )
        
        # Should return 400 Bad Request
        assert response.status == 400, f"Expected 400, got {response.status}"
    
    def test_get_datacenter_details_unauthorized(self, playwright):
        """Test datacenter details endpoint without authentication"""
        request_context = playwright.request.new_context(
            base_url="https://localhost:8000"
        )
        
        site_id = "Site-001"
        response = request_context.get(f"/twin/datacenter/v1/details/{site_id}")
        
        # Should return 401 Unauthorized
        assert response.status == 401, f"Expected 401, got {response.status}"
        
        request_context.dispose()


class TestOntologyEndpoint:
    """Test suite for /twin/datacenter/v1/ontology endpoint"""
    
    def test_get_ontology_success(self, datacenter_api_context: APIRequestContext):
        """Test successful retrieval of global ontology"""
        response = datacenter_api_context.get("/twin/datacenter/v1/ontology")
        
        # Assert response status
        assert response.ok, f"Request failed with status {response.status}"
        assert response.status == 200
        
        # Get response data
        data = response.json()
        
        # Assert @context exists (JSON-LD structure)
        assert "@context" in data, "Response missing '@context' key"
        
        # Validate @context is namespace mappings
        context = data["@context"]
        assert isinstance(context, dict), "@context should be an object"
        
        # Validate that namespace mappings are URIs
        for prefix, uri in context.items():
            assert isinstance(uri, str), f"Namespace URI for '{prefix}' should be a string"
    
    def test_get_ontology_unauthorized(self, playwright):
        """Test ontology endpoint without authentication"""
        request_context = playwright.request.new_context(
            base_url="https://localhost:8000"
        )
        
        response = request_context.get("/twin/datacenter/v1/ontology")
        
        # Should return 401 Unauthorized
        assert response.status == 401, f"Expected 401, got {response.status}"
        
        request_context.dispose()
    
    def test_get_ontology_invalid_token(self, playwright):
        """Test ontology endpoint with invalid bearer token"""
        request_context = playwright.request.new_context(
            base_url="https://localhost:8000",
            extra_http_headers={
                "Authorization": "Bearer INVALID_TOKEN"
            }
        )
        
        response = request_context.get("/twin/datacenter/v1/ontology")
        
        # Should return 401 Unauthorized
        assert response.status == 401, f"Expected 401, got {response.status}"
        
        request_context.dispose()


class TestEntityValidation:
    """Test suite for validating entity type structures"""
    
    def test_site_type_entity_structure(self, datacenter_api_context: APIRequestContext):
        """Test SiteType entity structure in details response"""
        site_id = "Site-001"
        response = datacenter_api_context.get(f"/twin/datacenter/v1/details/{site_id}")
        
        if response.ok:
            data = response.json()
            
            # Find SiteType entity
            site_entities = [e for e in data["entities"] if e.get("type") == "SiteType"]
            
            if len(site_entities) > 0:
                site_entity = site_entities[0]
                
                # Validate SiteType attributes
                assert "attributes" in site_entity, "SiteType missing 'attributes'"
                attributes = site_entity["attributes"]
                
                # Check for SiteType-specific attributes
                if "siteId" in attributes:
                    assert isinstance(attributes["siteId"], str), "siteId should be a string"
    
    def test_power_device_entity_structure(self, datacenter_api_context: APIRequestContext):
        """Test PowerDeviceType entity structure with measurements"""
        site_id = "Site-001"
        response = datacenter_api_context.get(
            f"/twin/datacenter/v1/details/{site_id}",
            params={"entityType": "PowerDeviceType"}
        )
        
        if response.ok:
            data = response.json()
            
            if len(data["entities"]) > 0:
                device = data["entities"][0]
                
                # Validate common PowerDevice attributes
                assert "attributes" in device, "PowerDevice missing 'attributes'"
                attributes = device["attributes"]
                
                # Check for optional rated measurements
                if "ratedPower" in attributes:
                    rated_power = attributes["ratedPower"]
                    assert "value" in rated_power, "ratedPower missing 'value'"
                    assert "measurementType" in rated_power, "ratedPower missing 'measurementType'"
                
                # Check for state if present
                if "state" in device:
                    state = device["state"]
                    assert isinstance(state, dict), "state should be an object"


class TestRelationshipValidation:
    """Test suite for validating relationship structures"""
    
    def test_feeds_relationship_structure(self, datacenter_api_context: APIRequestContext):
        """Test 'feeds' relationship structure"""
        site_id = "Site-001"
        response = datacenter_api_context.get(f"/twin/datacenter/v1/details/{site_id}")
        
        if response.ok:
            data = response.json()
            
            # Find feeds relationships
            feeds_rels = [r for r in data["relationships"] if r.get("type") == "feeds"]
            
            if len(feeds_rels) > 0:
                relationship = feeds_rels[0]
                
                # Validate relationship structure
                assert "id" in relationship, "Relationship missing 'id'"
                assert "source" in relationship, "Relationship missing 'source'"
                assert "target" in relationship, "Relationship missing 'target'"
                assert "type" in relationship, "Relationship missing 'type'"
                
                # Validate source and target are non-empty strings
                assert isinstance(relationship["source"], str), "source should be a string"
                assert isinstance(relationship["target"], str), "target should be a string"
                assert len(relationship["source"]) > 0, "source should not be empty"
                assert len(relationship["target"]) > 0, "target should not be empty"


class TestErrorHandling:
    """Test suite for API error responses"""
    
    def test_error_response_structure(self, datacenter_api_context: APIRequestContext):
        """Test error response structure for invalid requests"""
        # Make request with invalid site_id to trigger 404
        response = datacenter_api_context.get("/twin/datacenter/v1/details/INVALID")
        
        if response.status >= 400:
            data = response.json()
            
            # Validate error envelope structure
            assert "error" in data, "Error response missing 'error' key"
            error = data["error"]
            
            # Validate error object
            assert "code" in error, "Error missing 'code' field"
            assert "message" in error, "Error missing 'message' field"
            
            # Validate error field types
            assert isinstance(error["code"], str), "error.code should be a string"
            assert isinstance(error["message"], str), "error.message should be a string"
