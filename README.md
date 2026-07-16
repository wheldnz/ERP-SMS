# ERP-SMS (After Sales Enterprise System)

![ERPNext Version](https://img.shields.io/badge/Frappe%2FERPNext-v15-blue.svg)
![Architecture](https://img.shields.io/badge/Architecture-Custom%20App%20Isolated-success.svg)
![Status](https://img.shields.io/badge/Status-Architecture%20%26%20Design%20Phase-orange.svg)

## 📌 Executive Overview

**ERP-SMS** adalah Sistem ERP Enterprise berbasis **Frappe Framework & ERPNext v15** yang dirancang secara khusus untuk mengelola operasional **After-Sales Service** terpadu. Sistem ini mengintegrasikan 6 divisi utama perusahaan ke dalam satu platform terpusat (*Single Source of Truth*):

1. **🛡️ Insurance (Asuransi):** Pengelolaan polis pelanggan, klaim garansi/asuransi, verifikasi pertanggungan, dan kelayakan perbaikan.
2. **👥 HRD & Service Technician:** Manajemen absensi teknisi, penjadwalan servis, kualifikasi keahlian, dan kompensasi/bonus pekerjaan.
3. **🛍️ Retail & Store Front:** Penerimaan unit servis di konter retail, penerbitan tanda terima barang (Service Intake), penyerahan unit, dan pembayaran kasir (POS).
4. **🌐 Network & Service Center:** Pengelolaan jaringan cabang internal, mitra servis resmi (Authorized Service Center), dan transit barang antar jaringan.
5. **💰 Accounting & Finance:** Pembukuan otomatis (General Ledger), Accounts Receivable/Payable, penagihan klaim ke perusahaan asuransi, dan laporan laba/rugi cabang.
6. **📦 Warehouse & Spareparts:** Pengelolaan stok suku cadang (serialized parts), transfer stok antar gudang, *Stock Entry*, dan pemantauan masa garansi part.

---

## 🏛️ Prinsip Utama Arsitektur (Core Architectural Principles)

1. **Zero Core Mutation:** Tidak pernah mengubah source code bawaan `frappe` atau `erpnext`. Seluruh logika kustom diisolasi total di dalam custom app `sms_aftersales`.
2. **Fit-Gap First:** Memaksimalkan modul bawaan ERPNext (*Stock, Accounts, HR, CRM/Support*) dan hanya membuat Doctype kustom untuk logika spesifik *After-Sales & Insurance*.
3. **Conflict-Free Deployment:** Menggunakan fitur `fixtures` Frappe untuk sinkronisasi Custom Field, Property Setter, dan Print Format tanpa risiko bentrokan database saat deployment.
4. **Data Integrity & Auditability:** Setiap transaksi yang memengaruhi stok dan keuangan wajib melalui dokumen resmi ber-sequence (Workflow Approved).

---

## 📂 Peta Dokumentasi Repositori

Repositori ini telah dilengkapi dengan standar dokumentasi kelas enterprise untuk memandu tim developer dan AI Assistant:

| Dokumentasi | Deskripsi & Isi Utama |
|---|---|
| 📑 [AGENTS.md](file:///c:/Users/USER/Documents/present/ERP%20Next/AGENTS.md) | **Aturan Ketat AI & Developer:** Konvensi koding, Doctype naming, Git branching, & protokol pengujian. |
| 📑 [ARCHITECTURE.md](file:///c:/Users/USER/Documents/present/ERP%20Next/ARCHITECTURE.md) | **Arsitektur Sistem:** Struktur custom app, Redis caching, Background Jobs (RQ), dan API Design. |
| 📑 [PRD.md](file:///c:/Users/USER/Documents/present/ERP%20Next/PRD.md) | **Product Requirement Document:** User stories, kebutuhan fitur, dan batasan sistem 6 divisi. |
| 📑 [ERD_AND_DATA_DICTIONARY.md](file:///c:/Users/USER/Documents/present/ERP%20Next/ERD_AND_DATA_DICTIONARY.md) | **Diagram Relasi Tabel (ERD):** Visualisasi relasi data dan Data Dictionary lengkap. |
| 📑 [FIT_GAP_ANALYSIS.md](file:///c:/Users/USER/Documents/present/ERP%20Next/FIT_GAP_ANALYSIS.md) | **Matriks Pemetaan Modul:** Pemisahan antara Modul Native ERPNext vs Custom App. |
| 📑 [BUSINESS_PROCESS_FLOW.md](file:///c:/Users/USER/Documents/present/ERP%20Next/BUSINESS_PROCESS_FLOW.md) | **Alur Bisnis End-to-End:** Diagram BPMN alur penerimaan servis, klaim asuransi, sparepart, & invoicing. |
| 📑 [DEPLOYMENT_AND_CI_CD.md](file:///c:/Users/USER/Documents/present/ERP%20Next/DEPLOYMENT_AND_CI_CD.md) | **Protokol Deploy Bebas Bentrok:** Panduan Git Flow, Export Fixtures, Staging, & Production release. |
| 📑 [TESTING_AND_QA_STRATEGY.md](file:///c:/Users/USER/Documents/present/ERP%20Next/TESTING_AND_QA_STRATEGY.md) | **Strategi Pengujian:** Unit Testing Frappe, Dry-run staging, dan UAT Sign-off protocol. |
| 📑 [SECURITY_AND_PERMISSIONS.md](file:///c:/Users/USER/Documents/present/ERP%20Next/SECURITY_AND_PERMISSIONS.md) | **Keamanan & Role Access:** Role-Based Access Control (RBAC), User Permissions, & Audit Trails. |

---

## 🚀 Quick Start untuk Developer

### Setup Environment Lokal (Development)

```bash
# 1. Inisialisasi Bench v15
bench init --frappe-branch version-15 frappe-bench
cd frappe-bench

# 2. Aktifkan Developer Mode
bench set-config -g developer_mode 1

# 3. Create Site Baru
bench new-site sms-dev.local

# 4. Install ERPNext & Custom App
bench get-app --branch version-15 erpnext
bench get-app https://github.com/wheldnz/ERP-SMS.git sms_aftersales

# 5. Install ke Site
bench --site sms-dev.local install-app erpnext
bench --site sms-dev.local install-app sms_aftersales

# 6. Jalankan Bench
bench start
```

---

## 👨‍💻 Kontribusi & Workflow Git

Silakan baca [AGENTS.md](file:///c:/Users/USER/Documents/present/ERP%20Next/AGENTS.md) dan [DEPLOYMENT_AND_CI_CD.md](file:///c:/Users/USER/Documents/present/ERP%20Next/DEPLOYMENT_AND_CI_CD.md) sebelum mulai mengubah kode atau membuat branch baru.
