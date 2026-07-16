import frappe

def create_seed_data():
    frappe.db.begin()
    
    # 1. Create 5 Operating Companies
    companies = [
        "PT SMS Region 1",
        "PT SMS Region 2",
        "PT SMS Region 3",
        "PT SMS Region 4",
        "PT SMS Region 5"
    ]
    
    for comp in companies:
        if not frappe.db.exists("Company", comp):
            c = frappe.get_doc({
                "doctype": "Company",
                "company_name": comp,
                "default_currency": "IDR",
                "country": "Indonesia"
            })
            c.insert(ignore_permissions=True)
            print(f"Created Company: {comp}")
            
    primary_company = companies[0]

    # 2. Create Sample Customer
    customer_name = "Budi Santoso"
    if not frappe.db.exists("Customer", customer_name):
        cust = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": customer_name,
            "customer_type": "Individual",
            "customer_group": "Individual",
            "territory": "Indonesia"
        })
        cust.insert(ignore_permissions=True)
        print(f"Created Customer: {customer_name}")

    # 3. Create Sample Item & Serial No
    item_code = "IPHONE-15-PRO"
    if not frappe.db.exists("Item", item_code):
        item = frappe.get_doc({
            "doctype": "Item",
            "item_code": item_code,
            "item_name": "iPhone 15 Pro Max 256GB",
            "item_group": "Products",
            "has_serial_no": 1,
            "serial_no_series": "SN-IP15-.#####"
        })
        item.insert(ignore_permissions=True)
        print(f"Created Item: {item_code}")

    serial_no = "SN-IPHONE15-88329"
    if not frappe.db.exists("Serial No", serial_no):
        sn = frappe.get_doc({
            "doctype": "Serial No",
            "serial_no": serial_no,
            "item_code": item_code,
            "company": primary_company
        })
        sn.insert(ignore_permissions=True)
        print(f"Created Serial No: {serial_no}")

    # 4. Create Sample Network Node (Gerai / Service Center)
    node_name = "Gerai Retail & Service Center Surabaya"
    if not frappe.db.exists("SMS Network Node", {"node_name": node_name}):
        # Check default warehouse
        default_wh = frappe.db.get_value("Warehouse", {"company": primary_company}, "name")
        default_cc = frappe.db.get_value("Cost Center", {"company": primary_company}, "name")
        node = frappe.get_doc({
            "doctype": "SMS Network Node",
            "node_name": node_name,
            "company": primary_company,
            "node_type": "Own Branch",
            "warehouse": default_wh or "Main Warehouse - PT SMS Region 1",
            "cost_center": default_cc or "Main - PT SMS Region 1"
        })
        node.insert(ignore_permissions=True)
        print(f"Created Network Node: {node_name}")
    else:
        node = frappe.get_doc("SMS Network Node", {"node_name": node_name})

    # 5. Create Sample Insurance Policy
    policy_number = "POL-2026-889900"
    if not frappe.db.exists("SMS Insurance Policy", {"policy_number": policy_number}):
        policy = frappe.get_doc({
            "doctype": "SMS Insurance Policy",
            "policy_number": policy_number,
            "company": primary_company,
            "customer": customer_name,
            "serial_no": serial_no,
            "insurance_provider": "PT Asuransi Paripurna Indonesia",
            "coverage_limit": 5000000,
            "valid_start": frappe.utils.nowdate(),
            "valid_expiry": frappe.utils.add_years(frappe.utils.nowdate(), 1),
            "status": "Active"
        })
        policy.insert(ignore_permissions=True)
        print(f"Created Insurance Policy: {policy_number}")
    else:
        policy = frappe.get_doc("SMS Insurance Policy", {"policy_number": policy_number})

    # 6. Create Sample Service Intake
    intake = frappe.get_doc({
        "doctype": "SMS Service Intake",
        "company": primary_company,
        "network_node": node.name,
        "customer": customer_name,
        "serial_no": serial_no,
        "is_insurance_covered": 1,
        "insurance_policy": policy.name,
        "physical_condition": "Layar retak halus di pojok kanan atas, casing mulus.",
        "reported_issue": "Layar sentuh kadang tidak merespons dan baterai cepat habis.",
        "status": "Inspection"
    })
    intake.insert(ignore_permissions=True)
    print(f"Created Service Intake: {intake.name}")

    # 7. Create Sample Insurance Claim
    claim = frappe.get_doc({
        "doctype": "SMS Insurance Claim",
        "company": primary_company,
        "policy": policy.name,
        "claim_amount": 2500000,
        "claim_status": "Approved",
        "approval_date": frappe.utils.nowdate(),
        "notes": "Disetujui ganti sparepart layar & baterai original oleh Assessor."
    })
    claim.insert(ignore_permissions=True)
    print(f"Created Insurance Claim: {claim.name}")

    # 8. Create Sample Service Order
    order = frappe.get_doc({
        "doctype": "SMS Service Order",
        "company": primary_company,
        "intake": intake.name,
        "insurance_claim": claim.name,
        "spareparts_cost": 2000000,
        "labor_cost": 500000,
        "status": "In Progress"
    })
    order.insert(ignore_permissions=True)
    print(f"Created Service Order: {order.name}")

    frappe.db.commit()
    print("=== All Sample Data Generated Successfully ===")
