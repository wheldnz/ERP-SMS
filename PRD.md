# PRD.md — Product Requirement Document (ERP-SMS Multi-Company)

## 🎯 1. Objective & Product Vision
Membangun sistem terintegrasi **ERP-SMS** berbasis ERPNext v15 untuk mengkonsolidasi **5 Perusahaan (Subsidiaries)** ke dalam satu sistem ERP Holding. 

Sistem ini menjamin bahwa setiap anak perusahaan dapat mengelola keuangan, gudang suku cadang, dan operasionalnya secara independen atas nama badan hukum (PT) masing-masing, sementara para **Stakeholder / Direksi** memiliki akses **Consolidated Executive Dashboard** real-time untuk memantau performa grup.

---

## 🏢 2. Arsitektur Multi-Perusahaan (5 Entities Structure)

| Kode Entity | Nama Badan Hukum (Contoh) | Lingkup Operasional Utama |
|---|---|---|
| **HOLDING** | `SMS Group Holding` | Konsolidasi Keuangan Group & Monitoring Direksi |
| **PT 1** | `PT SMS Aftersales Jakarta` | Operasional Service Center & Repair Jabodetabek |
| **PT 2** | `PT SMS Aftersales Surabaya` | Operasional Service Center & Repair Jawa Timur |
| **PT 3** | `PT SMS Insurance Partner` | Pengelolaan Polis & Penjaminan Klaim Asuransi |
| **PT 4** | `PT SMS Logistic & Spareparts` | Gudang Pusat & Impor Suku Cadang |
| **PT 5** | `PT SMS Retail Store Network` | Jaringan Gerai Penerimaan Unit Retail |

---

## 👥 3. User Personas & Permissions Matrix

| Persona | Entitas (Company Scope) | Hak Akses Utama |
|---|---|---|
| **Stakeholder / Director** | 🌐 All 5 Companies | Executive Dashboard, Consolidated Financial Statements, Group Stock View |
| **Branch Manager PT 1** | 🏢 Restricted to PT 1 | Full Operational Access for PT 1 only |
| **Insurance Officer PT 3** | 🏢 Restricted to PT 3 | Management of Policies & Claims for PT 3 |
| **Warehouse Keeper PT 4** | 🏢 Restricted to PT 4 | Central Parts Warehouse Stock Entries & Inter-Company Transfer |
| **Retail Staff PT 5** | 🏢 Restricted to PT 5 | Service Intake at PT 5 Outlets |

---

## 📋 4. Key Multi-Company Functional Requirements

### 📊 A. Multi-Company Financial Consolidation (Holding Stakeholders)
1. **F-MC-01:** Stakeholder dapat melihat Laporan Laba/Rugi (*Profit & Loss*) dan Neraca (*Balance Sheet*) per masing-masing PT maupun laporan konsolidasi gabungan (Holding).
2. **F-MC-02:** *Inter-Company Auto Elimination:* Transaksi penjualan/pembelian internal antar 5 anak perusahaan otomatis ditandai sebagai *Inter-Company Trade* untuk keperluan eliminasi konsolidasi akuntansi.

### 📦 B. Inter-Company Stock Transfer (PT Logistic ➔ PT Service)
1. **F-MC-03:** Ketika PT 1 (Service Center) membutuhkan sparepart dari PT 4 (Gudang Pusat Logistik), sistem menyediakan workflow **Inter-Company Purchase Order (PO) ➔ Sales Order (SO)** otomatis.
2. **F-MC-04:** Penelusuran *Serial No* sparepart bersifat global sehingga riwayat garansi pabrikan tetap terlacak meskipun barang telah dijual antar anak perusahaan.

### 🛡️ C. Cross-Company Insurance Claim Settlement (PT Insurance ➔ PT Repair)
1. **F-MC-05:** Ketika klaim asuransi pelanggan disetujui di PT 3 (Insurance), sistem otomatis memicu pembentukan piutang di PT 1 (Service Center yang mengerjakan unit) dan utang klaim di PT 3.

---

## 🔒 5. Non-Functional Requirements (NFR)

1. **Strict Data Privacy:** Staf dari PT A sama sekali tidak boleh melihat dokumen transaksi atau saldo bank milik PT B.
2. **Consolidated Performance:** Dashboard Stakeholder yang menggabungkan analytics 5 anak perusahaan harus memuat data dalam waktu di bawah **2.5 detik**.
