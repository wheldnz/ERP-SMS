# PRD.md — Product Requirement Document (Full Matrix Multi-Company ERP)

## 🎯 1. Objective & Product Vision
Membangun sistem terintegrasi **ERP-SMS** berbasis ERPNext v15 untuk mengkonsolidasi **5 Perusahaan Mandiri**, di mana **setiap perusahaan menjalankan unit bisnis lengkap dengan 6 divisi internal**:

1. **🛡️ Divisi Insurance:** Pengelolaan polis pelanggan & klaim garansi internal PT masing-masing.
2. **👥 Divisi HRD:** Pengelolaan absensi teknisi, kompensasi & KPI servis internal PT masing-masing.
3. **🛍️ Divisi Retail:** Penjualan produk & penerimaan unit rusak di gerai milik PT masing-masing.
4. **🌐 Divisi Network:** Manajemen cabang & mitra servis dalam jaringan PT masing-masing.
5. **💰 Divisi Accounting:** Pembukuan neraca, Laba/Rugi, dan pembukuan resmi atas nama PT masing-masing.
6. **📦 Divisi Warehouse:** Pengelolaan stok suku cadang & gudang milik PT masing-masing.

**Stakeholder Goal:** Mengamati dan membandingkan performa operasional serta keuangan dari ke-5 perusahaan tersebut secara individual maupun terintegrasi (*Consolidated Holding Group Analytics*).

---

## 🏢 2. Struktur Matriks 5 Perusahaan x 6 Divisi

```
                               ┌──────────────────────────────────────────────────────────┐
                               │                 SMS Group Holding                        │
                               │  (Stakeholder Consolidated Monitoring & Analytics)       │
                               └────────────────────────────┬─────────────────────────────┘
                                                            │
        ┌───────────────────┬───────────────────┼───────────────────┬───────────────────┐
        ▼                   ▼                   ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  Perusahaan 1 │   │  Perusahaan 2 │   │  Perusahaan 3 │   │  Perusahaan 4 │   │  Perusahaan 5 │
├───────────────┤   ├───────────────┤   ├───────────────┤   ├───────────────┤   ├───────────────┤
│ • Insurance   │   │ • Insurance   │   │ • Insurance   │   │ • Insurance   │   │ • Insurance   │
│ • HRD         │   │ • HRD         │   │ • HRD         │   │ • HRD         │   │ • HRD         │
│ • Retail      │   │ • Retail      │   │ • Retail      │   │ • Retail      │   │ • Retail      │
│ • Network     │   │ • Network     │   │ • Network     │   │ • Network     │   │ • Network     │
│ • Accounting  │   │ • Accounting  │   │ • Accounting  │   │ • Accounting  │   │ • Accounting  │
│ • Warehouse   │   │ • Warehouse   │   │ • Warehouse   │   │ • Warehouse   │   │ • Warehouse   │
└───────────────┘   └───────────────┘   └───────────────┘   └───────────────┘   └───────────────┘
```

---

## 👥 3. User Personas & Scope Alignment

| Level User | Perusahaan (Company) | Divisi (Department) | Hak Akses Utama |
|---|---|---|---|
| **Stakeholder / Direksi** | 🌐 All 5 Companies | 🌐 All 6 Divisions | Executive Consolidated Dashboard, Group P&L, Stock & Claim Matrix |
| **Branch Manager PT 1** | 🏢 PT 1 Only | 🌐 All 6 Divisions in PT 1 | Memantau seluruh operasional 6 divisi khusus di PT 1 |
| **Retail Staff PT 1** | 🏢 PT 1 Only | 🛍️ Retail Dept | Input `SMS Service Intake` khusus gerai PT 1 |
| **Insurance Assessor PT 2**| 🏢 PT 2 Only | 🛡️ Insurance Dept | Approval `SMS Insurance Claim` khusus transaksi PT 2 |
| **Warehouse Keeper PT 3** | 🏢 PT 3 Only | 📦 Warehouse Dept | Kelola `Stock Entry` & Gudang khusus milik PT 3 |

---

## 📋 4. Key Matrix Requirements

### 📊 A. Group Benchmarking & Performance Comparison (Stakeholders)
1. **F-MX-01:** Stakeholder dapat membandingkan KPI kinerja antar 5 perusahaan secara berdampingan (*Side-by-Side Comparison*):
   - Perbandingan Total Klaim Asuransi (PT 1 vs PT 2 vs PT 3 vs PT 4 vs PT 5).
   - Perbandingan Turn-Around-Time (TAT) Servis Teknisi antar PT.
   - Perbandingan Omset Retail & Profit Margin antar PT.

### 🔒 B. Dual Isolation (Company + Department)
1. **F-MX-02:** Sistem menerapkan *Dual Isolation Constraint*: Staf Divisi Warehouse di PT 1 tidak bisa melihat data Divisi Warehouse di PT 2, maupun data Divisi Accounting di PT 1 yang bukan wewenangnya.
