app_name = "sms_aftersales"
app_title = "SMS After Sales System"
app_publisher = "SMS Team"
app_description = "SMS After Sales Enterprise System - Custom Module for ERPNext v15"
app_email = "dev@sms-aftersales.local"
app_license = "mit"

# Export Fixtures Configuration for Zero-Mutation Deployment
fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "SMS Aftersales"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "SMS Aftersales"]]},
    {"dt": "Role Profile", "filters": [["role_profile", "like", "SMS %"]]}
]

# Event Hooks
doc_events = {
    "Serial No": {
        "on_update": "sms_aftersales.retail_network.events.sync_serial_warranty"
    },
    "Stock Entry": {
        "on_submit": "sms_aftersales.warehouse.events.validate_aftersales_parts_dispatch"
    }
}
