# ARCHITECTURE.md — System & Application Architecture Blueprint

## 🏛️ 1. Multi-Company Matrix Architecture

Sistem **ERP-SMS** dirancang menggunakan arsitektur **Multi-Company Full Matrix Holding Group**. Dalam arsitektur ini, **setiap Perusahaan (Subsidiary Entity)** beroperasi sebagai entitas bisnis mandiri yang memiliki **6 Divisi Internal Lengkap** di dalam struktur organisasinya sendiri:

```mermaid
graph TD
    subgraph Level Holding - Executive Stakeholders / Board of Directors
        Holding[SMS Group Holding - Consolidated Analytics & Global Monitoring]
    end

    subgraph 5 Independent Full-Suite Operating Companies
        C1[Company 1: PT SMS Region 1]
        C2[Company 2: PT SMS Region 2]
        C3[Company 3: PT SMS Region 3]
        C4[Company 4: PT SMS Region 4]
        C5[Company 5: PT SMS Region 5]
    end

    Holding ==> C1
    Holding ==> C2
    Holding ==> C3
    Holding ==> C4
    Holding ==> C5

    subgraph Struktur 6 Divisi Internal per Perusahaan
        D1[🛡️ Divisi Insurance]
        D2[👥 Divisi HRD]
        D3[🛍️ Divisi Retail]
        D4[🌐 Divisi Network]
        D5[💰 Divisi Accounting]
        D6[📦 Divisi Warehouse]
    end

    C1 --- D1 & D2 & D3 & D4 & D5 & D6
    C2 --- D1 & D2 & D3 & D4 & D5 & D6
    C3 --- D1 & D2 & D3 & D4 & D5 & D6
    C4 --- D1 & D2 & D3 & D4 & D5 & D6
    C5 --- D1 & D2 & D3 & D4 & D5 & D6
```

---

## 🔒 2. Matriks Struktur Organisasi di ERPNext (Company & Department Hierarchy)

Pemetaan hirarki di Frappe/ERPNext dikonfigurasi sebagai berikut:

```
Frappe Core Organization Structure:
├── Company: PT SMS Region 1 (Surabaya)
│   ├── Department: Insurance - PT 1
│   ├── Department: HRD - PT 1
│   ├── Department: Retail - PT 1
│   ├── Department: Network - PT 1
│   ├── Department: Accounting - PT 1
│   └── Department: Warehouse - PT 1
│       └── Warehouse: Main Spareparts - PT 1
├── Company: PT SMS Region 2 (Jakarta)
│   ├── Department: Insurance - PT 2
│   ├── Department: HRD - PT 2
│   ├── Department: Retail - PT 2
│   ├── Department: Network - PT 2
│   ├── Department: Accounting - PT 2
│   └── Department: Warehouse - PT 2
│       └── Warehouse: Main Spareparts - PT 2
... (Berlaku persis sama hingga PT SMS Region 5)
```

---

## 🔍 3. Data Isolation Matrix (Company + Department Isolation)

- **Staf Divisi Retail di PT 1:** Hanya bisa mengakses data penerimaan barang (`SMS Service Intake`) di `Company = PT 1` dan `Department = Retail`.
- **Manager Divisi Insurance di PT 2:** Hanya bisa melakukan approval klaim (`SMS Insurance Claim`) di `Company = PT 2`.
- **Stakeholder Holding:** Memiliki hak akses lintas 5 Perusahaan dan 6 Divisi tanpa batasan (`Full Consolidated Access`).
