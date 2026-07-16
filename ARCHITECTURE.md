# ARCHITECTURE.md — System & Application Architecture Blueprint

## 🏛️ 1. High-Level Multi-Company & Enterprise Architecture

Sistem **ERP-SMS** dirancang menggunakan arsitektur **Multi-Company (Holding Group)** bawaan ERPNext v15. Arsitektur ini memungkinkan **5 Perusahaan (Subsidiary)** beroperasi secara mandiri dalam satu instalasi database terpadu, sekaligus memberikan akses pemantauan (*Consolidated Dashboard & Financial Statements*) bagi para Stakeholder / Direksi di tingkat Holding.

```mermaid
graph TD
    subgraph Holding Level - Stakeholders / Board of Directors
        Holding[SMS Group Holding - Consolidated View]
    end

    subgraph 5 Independent Operating Companies (Subsidiaries)
        C1[Company 1: PT SMS Aftersales Jkt]
        C2[Company 2: PT SMS Aftersales Sby]
        C3[Company 3: PT SMS Insurance Partner]
        C4[Company 4: PT SMS Logistic & Parts]
        C5[Company 5: PT SMS Retail Network]
    end

    Holding ==>|Consolidated Financials & Inter-Company Transfer| C1
    Holding ==>|Real-time Group Analytics| C2
    Holding ==>|Global Inventory & Claim Monitoring| C3
    Holding ==>|Executive Dashboard| C4
    Holding ==>|Group Profit & Loss| C5

    subgraph Data & Resource Isolation per Company
        C1 --- W1[(Warehouse & COA PT 1)]
        C2 --- W2[(Warehouse & COA PT 2)]
        C3 --- W3[(Insurance Policies PT 3)]
        C4 --- W4[(Central Parts Stock PT 4)]
        C5 --- W5[(Retail Outlets PT 5)]
    end
```

---

## 🔒 2. Prinsip Isosiasi Data & Konsolidasi (Data Isolation & Consolidation)

1. **Pemisahan Keuangan (Legal Chart of Accounts):**
   - Masing-masing dari 5 Perusahaan memiliki **Chart of Accounts (COA)**, Nomor Pajak (NPWP), dan Rekening Bank terpisah.
   - Seluruh transaksi `Sales Invoice`, `Purchase Invoice`, dan `Journal Entry` terikat pada field `company` spesifik.
   - **Stakeholder View:** Stakeholder dapat melihat Laporan Laba/Rugi (*Profit & Loss*) dan Neraca (*Balance Sheet*) per masing-masing PT, maupun **Consolidated Financial Statement** gabungan kelima perusahaan.

2. **Isolasi Gudang & Stok (Stock & Warehouse Isolation):**
   - Setiap Gudang (*Warehouse*) diidentifikasi secara tegas pemiliknya, contoh: `Gudang Utama - PT SMS Logistic`, `Gudang Outlet - PT SMS Retail Network`.
   - Transaksi perpindahan stok antar perusahaan menggunakan fitur bawaan **Inter-Company Transactions** (Sales Order di PT A otomatis mengenerate Purchase Order di PT B).

3. **Multi-Company User Permissions:**
   - **Staf Operasional PT A:** Diberikan `User Permission` `Company = PT A`. Mereka HANYA bisa melihat transaksi, stok, dan laporan milik PT A.
   - **Stakeholder / Direksi Holding:** Diberikan role `SMS Holding Executive` TANPA pembatasan `Company`, sehingga bisa memantau dan membandingkan performa 5 perusahaan secara real-time.

---

## 📂 3. Struktur Modul & Custom App Directory Layout

Aplikasi kustom `sms_aftersales` memiliki modul internal yang diisolasi berdasarkan divisi dan domain fungsi:

```
apps/sms_aftersales/
├── sms_aftersales/
│   ├── hooks.py                        <-- Central Frappe Integration Event Hooks
│   ├── patches.txt                     <-- DB Migration Patch Registry
│   ├── fixtures/                       <-- Custom Fields, Property Setters JSON
│   ├── insurance/                      <-- Divisi Asuransi Modul
│   ├── retail_network/                 <-- Divisi Retail & Service Center Network
│   ├── hr_service/                     <-- Divisi HRD & Teknisi Integration
│   ├── api/                            <-- REST API Endpoints untuk Mobile/External Integrasi
│   └── public/                         <-- Static Assets (CSS, JS, Custom UI Widgets)
```

---

## 🔄 4. Integritas Hooks & Override Strategy

Untuk memperluas atau mengubah perilaku standar ERPNext tanpa mengubah kodenya, file `hooks.py` dikonfigurasi sebagai berikut:

```python
# apps/sms_aftersales/sms_aftersales/hooks.py

app_name = "sms_aftersales"
app_title = "SMS After Sales System"

# 1. Export Fixtures Otomatis
fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "SMS Aftersales"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "SMS Aftersales"]]},
    {"dt": "Role Profile", "filters": [["role_profile", "like", "SMS %"]]}
]

# 2. Event Hooks Dokumen Standar ERPNext (Multi-Company aware)
doc_events = {
    "Serial No": {
        "on_update": "sms_aftersales.retail_network.events.sync_serial_warranty"
    },
    "Stock Entry": {
        "on_submit": "sms_aftersales.warehouse.events.validate_aftersales_parts_dispatch"
    }
}
```

---

## ⚡ 5. Background Processing & Caching Strategy

1. **Redis Cache (Port 13000):**
   - Caching master data per perusahaan.
2. **Frappe RQ (Redis Queue):**
   - Background job untuk mengkonsolidasi laporan neraca bulanan kelima anak perusahaan ke holding.
