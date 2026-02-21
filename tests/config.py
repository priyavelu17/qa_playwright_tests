# Datacenter API Testing Configuration

# Base URL for the API
BASE_URL = "https://localhost:8000"

# Authentication token (replace with actual JWT token)
AUTH_TOKEN = "YOUR_JWT_TOKEN_HERE"

# Test data for site IDs
VALID_SITE_IDS = [
    "Site-001",
    "Site-002",
    "Site-003"
]

INVALID_SITE_IDS = [
    "NON_EXISTENT_SITE",
    "INVALID_ID",
    ""
]

# Entity types to test
ENTITY_TYPES = [
    "SiteType",
    "ElectricalRoom",
    "DataHall",
    "BatteryRoom",
    "GeneratorYard",
    "GeneratorRoom",
    "Rack",
    "PowerDeviceType",
    "SwitchgearType",
    "FeederType",
    "TransformerType",
    "ATSType",
    "UPSType",
    "BESSType",
    "BMSType",
    "GeneratorSetType",
    "PDUType",
    "RPPType",
    "BuswayType",
    "RackPDUType",
    "STSType",
    "PQMeterType",
    "GatewayType",
    "ControllerType",
    "MCCType",
    "MotorFeederType",
    "SPDType",
    "GroundingNetworkType",
    "UtilityMeterType"
]

# Relationship types to test
RELATIONSHIP_TYPES = [
    "containsEquipment",
    "hasLocation",
    "fedBy",
    "feeds",
    "locatedIn",
    "suppliedBy",
    "suppliesPowerTo",
    "forDevice",
    "hasElectrical",
    "hasTelemetryStream",
    "hasTelemetryPoint",
    "protects",
    "protectedBy",
    "connectedTo",
    "connectedFrom",
    "controls",
    "controlledBy",
    "hasPhase",
    "hasDocument"
]

# Measurement types to test
MEASUREMENT_TYPES = [
    "ActivePower",
    "Voltage",
    "Current",
    "ActiveEnergyExport",
    "ActiveEnergyImport",
    "ApparentPower",
    "DCCurrent",
    "DCVoltage",
    "Frequency",
    "PowerFactor",
    "ReactivePower",
    "RemainingTime",
    "SoC",
    "SoH",
    "THDI",
    "THDV",
    "Temperature",
    "Humidity",
    "VoltageLL",
    "VoltageLN"
]

# Pagination settings
DEFAULT_LIMIT = 10
MAX_LIMIT = 100
