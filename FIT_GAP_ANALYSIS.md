# FIT_GAP_ANALYSIS.md — Native vs Custom Feature Mapping

## 🔍 Overview Fit-Gap Analysis

Prinsip utama pembangunan **ERP-SMS** adalah **Fit-Gap Maximization**. Kami mengevaluasi modul standar ERPNext v15 untuk mengukur persentase kesesuaian (*Fit*) terhadap proses bisnis After-Sales, serta menentukan komponen mana yang membutuhkan ekstensi (*Gap/Customization*).

```
Tingkat Kesesuaian Standard ERPNext v15:
[████████████████░░░░] 75% Fit (Native Core: Stock, Accounts, HR, CRM, POS)
[████░░░░░░░░░░░░░░░░] 25% Custom (Module Specific: Insurance Claim & Repair Intake)
```

---

## 📊 Matriks Pemetaan Fit-Gap

| Modul & Fungsi Bisnis | ERPNext Native Feature | Status Fit/Gap | Strategi Implementasi (Solusi Technical) |
|---|---|---|---|
| **Manajemen Pelanggan** | `Customer`, `Contact`, `Address` | 🟢 100% Fit | Gunakan Doctype `Customer` bawaan tanpa modifikasi. |
| **Manajemen Serial No** | `Serial No`, `Batch` | 🟢 100% Fit | Gunakan `Serial No` bawaan. Tambahkan Custom Field `warranty_expiry_date`. |
| **Penerimaan Barang Servis** | `Issue` / `Maintenance Visit` | 🟡 50% Gap | `Issue` bawaan terlalu sederhana. Buat Custom Doctype `SMS Service Intake`. |
| **Manajemen Polis Asuransi** | *Tidak ada* | 🔴 0% Fit (Gap) | Buat Custom Doctype `SMS Insurance Policy`. |
| **Pengajuan & Approval Klaim**| *Tidak ada* | 🔴 0% Fit (Gap) | Buat Custom Doctype `SMS Insurance Claim` & Workflow Engine Frappe. |
| **Surat Kerja Teknisi** | `Work Order` / `Task` | 🟡 60% Gap | Buat Custom Doctype `SMS Service Order` terhubung ke `Stock Entry`. |
| **Pengeluaran Sparepart** | `Stock Entry (Material Issue)` | 🟢 95% Fit | Gunakan `Stock Entry` tipe *Material Issue*. Trigger otomatis dari Service Order. |
| **Transfer Stok Cabang** | `Stock Entry (Material Transfer)` | 🟢 100% Fit | Gunakan `Stock Entry` bawaan dengan lokasi Gudang Cabang A ➔ B. |
| **Penggajian & Insentif** | `Employee`, `Payroll Entry` | 🟢 90% Fit | Gunakan ERPNext HR & Payroll. Hitung bonus via Custom Script ke `Additional Salary`. |
| **Penagihan Pelanggan** | `Sales Invoice`, `POS Invoice` | 🟢 100% Fit | Gunakan `Sales Invoice` bawaan terhubung ke `SMS Service Order`. |
| **Reimbursement Asuransi** | `Journal Entry` | 🟢 100% Fit | Automasi penerbitan `Journal Entry` saat klaim asuransi berstatus *Settled*. |
| **Laporan Keuangan Cabang** | `Profit and Loss`, `Cost Center` | 🟢 100% Fit | Gunakan `Cost Center` bawaan untuk tiap `SMS Network Node`. |

---

## 🎯 Detail Ekstensi Custom App (`sms_aftersales`)

### 1. Custom Fields pada Doctype Bawaan
Daripada membuat tabel baru, field berikut akan ditambahkan ke Doctype bawaan ERPNext menggunakan `fixtures/custom_field.json`:

- **Doctype `Serial No`:**
  - `custom_insurance_policy` (Link ➔ `SMS Insurance Policy`)
  - `custom_warranty_status` (Select: *Under Warranty / Out of Warranty / Insurance Covered*)
- **Doctype `Sales Invoice`:**
  - `custom_service_order_ref` (Link ➔ `SMS Service Order`)
  - `custom_is_insurance_billed` (Check)

### 2. Form Event Hooks & Triggers

```python
# Custom logic yang memicu Stock Deduction saat Service Order Completed:
def on_service_order_complete(doc, method):
    if doc.status == "Completed" and doc.spareparts:
        stock_entry = frappe.new_doc("Stock Entry")
        stock_entry.purpose = "Material Issue"
        stock_entry.from_warehouse = doc.parts_warehouse
        for item in doc.spareparts:
            stock_entry.append("items", {
                "item_code": item.item_code,
                "qty": item.qty,
                "serial_no": item.serial_no
            })
        stock_entry.insert()
        stock_entry.submit()
```
