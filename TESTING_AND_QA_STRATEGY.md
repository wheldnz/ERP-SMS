# TESTING_AND_QA_STRATEGY.md — Quality Assurance & Testing Framework

## 🧪 1. Multi-Tiered Testing Pyramid

Untuk menjamin keandalan sistem **ERP-SMS** sebelum menyentuh pengguna akhir, strategi pengujian dibagi menjadi 4 tingkatan:

```
                  ┌───────────────────────┐
                  │  4. UAT Sign-off      │  <-- Perwakilan 6 Divisi Bisnis
               ┌──┴───────────────────────┴──┐
               │  3. Staging Integration Test │  <-- Automated Dry-Run Deployment
            ┌──┴──────────────────────────────┴──┐
            │  2. Modul Logic & Workflow Test    │  <-- Controller Validation Test
         ┌──┴────────────────────────────────────┴──┐
         │  1. Python Unit Test (frappe.tests)       │  <-- Automated CLI Test Runner
         └───────────────────────────────────────────┘
```

---

## 💻 2. Automated Python Unit Testing (`frappe.tests`)

Setiap Doctype kustom atau API endpoint di dalam `apps/sms_aftersales` wajib dilengkapi dengan file pengujian Python di folder `test_[doctype_name].py`.

### Contoh Test Case: `test_sms_insurance_claim.py`

```python
# apps/sms_aftersales/sms_aftersales/insurance/doctype/sms_insurance_claim/test_sms_insurance_claim.py

import frappe
from frappe.tests.utils import FrappeTestCase

class TestSMSInsuranceClaim(FrappeTestCase):

    def setUp(self):
        # 1. Setup Dummy Policy
        self.policy = frappe.get_doc({
            "doctype": "SMS Insurance Policy",
            "policy_number": "TEST-POL-999",
            "coverage_limit": 5000000,
            "valid_start": frappe.utils.nowdate(),
            "valid_expiry": frappe.utils.add_years(frappe.utils.nowdate(), 1),
            "status": "Active"
        })
        if not frappe.db.exists("SMS Insurance Policy", "TEST-POL-999"):
            self.policy.insert()

    def test_claim_exceeding_coverage_limit_should_fail(self):
        """Memastikan klaim yang melebihi limit pertanggungan menembakkan ValidationError"""
        claim = frappe.get_doc({
            "doctype": "SMS Insurance Claim",
            "policy": self.policy.name,
            "claim_amount": 10000000  # 10 Juta (Limit hanya 5 Juta)
        })
        
        # Pengujian harus raise Exception
        self.assertRaises(frappe.ValidationError, claim.insert)

    def test_valid_claim_creation(self):
        """Memastikan klaim di bawah limit berhasil dibuat dengan status Draft"""
        claim = frappe.get_doc({
            "doctype": "SMS Insurance Claim",
            "policy": self.policy.name,
            "claim_amount": 2000000
        })
        claim.insert()
        self.assertEqual(claim.claim_status, "Draft")
```

### Jalankan Unit Test via Command Line:
```bash
bench --site sms-dev.local run-tests --app sms_aftersales
```

---

## 📋 3. Matriks Skenario UAT (User Acceptance Testing)

Sebelum kode di-merge ke branch `main`, perwakilan dari ke-6 divisi wajib menguji skenario ini di server **Staging**:

| ID Test | Divisi | Skenario Pengujian | Hasil yang Diharapkan | Status |
|---|---|---|---|---|
| **UAT-INS-01** | Insurance | Input klaim untuk unit garansi aktif di bawah limit. | Status klaim berubah `Approved`, Service Order siap diproses. | ⬜ Pending |
| **UAT-INS-02** | Insurance | Input klaim untuk polis kadaluarsa. | Sistem menolak pengajuan klaim dengan error message jelas. | ⬜ Pending |
| **UAT-WHS-01** | Warehouse | Penarikan sparepart bernomor seri dari Gudang Cabang. | Stok gudang berkurang 1, serial number bertatus *Issued to Service*. | ⬜ Pending |
| **UAT-RET-01** | Retail | Penerimaan unit di konter retail & cetak Struk Intake. | Tanda Terima terpublikasi dalam bentuk PDF & QR code berfungsi. | ⬜ Pending |
| **UAT-ACC-01** | Accounting | Pencairan Klaim Asuransi oleh Finance. | Journal Entry otomatis terbentuk mengreditkan Piutang Asuransi. | ⬜ Pending |
| **UAT-HRD-01** | HRD | Penyelesaian Service Order oleh Teknisi. | Jam kerja teknisi terekam dan menghitung log insentif di akhir bulan. | ⬜ Pending |

---

## 🛑 4. Gatekeeper Rules untuk Release Live

Status **RELEASE TO PRODUCTION (LIVE)** hanya diberikan jika:
1. ✅ **100% Automated Unit Test** lulus tanpa failure/error.
2. ✅ **0 Unresolved Critical Bugs** di server Staging.
3. ✅ **Seluruh 6 Divisi** memberikan UAT Sign-off Confirmation (Form Tanda Tangan UAT).
4. ✅ **Backup Dry-Run Restore** berhasil dilakukan di Staging tanpa data loss.
