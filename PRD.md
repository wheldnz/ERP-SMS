# PRD.md — Product Requirement Document (ERP-SMS)

## 🎯 1. Objective & Product Vision
Membangun sistem terintegrasi **ERP-SMS** berbasis ERPNext v15 untuk mengotomatisasi seluruh siklus bisnis **After-Sales Services**. Sistem harus menyelesaikan masalah fragmentasi data antar gerai retail, teknisi, bagian klaim asuransi, gudang suku cadang, dan departemen keuangan.

---

## 👥 2. User Personas & Permissions Matrix

| Persona | Divisi | Peran & Tanggung Jawab | Hak Akses Utama |
|---|---|---|---|
| **Frontdesk Retail** | Retail | Menerima unit rusak dari customer, buat Tanda Terima Intake, cek garansi. | Create `SMS Service Intake`, View `Serial No` |
| **Claim Assessor** | Insurance | Verifikasi polis, kelayakan pengajuan klaim, approval pertanggungan biaya. | Full Access `SMS Insurance Policy` & `Claim` |
| **Service Lead** | HRD / Service | Alokasi tiket servis ke teknisi, pantau jam kerja & performa perbaikan. | Full Access `SMS Service Order` & `Tech Log` |
| **Warehouse Keeper**| Warehouse | Menyiapkan sparepart, rilis stok ke lokasi servis, transfer antar gudang. | Full Access `Stock Entry`, `Material Request` |
| **Finance Specialist**| Accounting | Verifikasi tagihan klaim asuransi, neraca cabang, buat invoice/pembayaran. | Full Access `Sales Invoice`, `Journal Entry` |
| **Network Manager** | Network | Menambah lokasi mitra/cabang baru, memantau KPI servis jaringan. | Full Access `SMS Network Node` |

---

## 📋 3. Functional Requirements per Division

### 🛡️ A. Divisi Insurance (Asuransi)
1. **F-INS-01:** Sistem dapat memvalidasi apakah `Serial No` unit yang dibawa memiliki `SMS Insurance Policy` aktif.
2. **F-INS-02:** Pembuat klaim (`SMS Insurance Claim`) dapat mengunggah bukti foto kerusakan dan estimasi biaya perbaikan.
3. **F-INS-03:** Approval Klaim bertahap:
   - Nilai Klaim < Rp 2.000.000 ➔ Auto-approve Assessor Level 1.
   - Nilai Klaim ≥ Rp 2.000.000 ➔ Butuh approval Insurance Manager.
4. **F-INS-04:** Penagihan klaim bulanan ke perusahaan asuransi otomatis mengelompokkan klaim berstatus `Approved` ke dalam satu `Sales Invoice` konsolidasi.

### 🛍️ B. Divisi Retail
1. **F-RET-01:** Penerimaan unit servis (`SMS Service Intake`) mencatat foto fisik unit saat diterima, kelengkapan aksesoris, dan nomor seri.
2. **F-RET-02:** Integrasi cetak struk/Tanda Terima Servis (Print Format thermal & PDF) dengan QR Code pelacakan status online.
3. **F-RET-03:** Integrasi POS untuk transaksi pembayaran biaya jasa/sparepart non-asuransi secara tunai/EDC/QRIS.

### 🌐 C. Divisi Network & Service Center
1. **F-NET-01:** Pendaftaran lokasi baru (Gerai Mandiri vs Mitra Authorized) yang terhubung langsung ke Master Warehouse dan Cost Center ERPNext.
2. **F-NET-02:** Pelacakan transit fisik unit dari Gerai Penerima (Retail) ke Pusat Servis Utama (Central Service Center) via Dokumen Transfer.

### 📦 D. Divisi Warehouse & Spareparts
1. **F-WHS-01:** *Serialized Sparepart Management:* Komponen utama (misal: Mainboard, Screen Assembly) harus memiliki nomor seri unik untuk melacak klaim garansi vendor pabrikan.
2. **F-WHS-02:** *Auto Stock Deduction:* Pembekuan stok sparepart otomatis terjadi saat `SMS Service Order` disetujui, dan penguraian stok (*Stock Ledger Entry*) terjadi saat order dinyatakan `Completed`.

### 👥 E. Divisi HRD & Teknisi
1. **F-HR-01:** Alokasi otomatis pekerjaan servis berdasarkan kualifikasi teknisi (misal: Sertifikasi Perbaikan Handphone / Laptop / Mesin).
2. **F-HR-02:** Perhitungan *Insentif / Bonus Teknisi* berdasarkan jumlah `SMS Service Order` selesai berstatus `Customer Sign-Off Clean`.

### 💰 F. Divisi Accounting & Finance
1. **F-ACC-01:** Otomatisasi Jurnal Piutang Asuransi: Debit Piutang Asuransi, Kredit Pendapatan Jasa Servis saat klaim `Approved`.
2. **F-ACC-02:** Pengenalan Beban Sparepart (Cost of Goods Sold / COGS) real-time berdasarkan HPP (FIFO / Moving Average) ERPNext Stock.

---

## 🔒 4. Non-Functional Requirements (NFR)

1. **Performance:** Pencarian `Serial No` dan pembuatan `SMS Service Intake` harus merespons di bawah **1.5 detik**.
2. **Availability:** Sistem harus mampu memproses 500+ transaksi intake harian lintas 20 cabang tanpa deadlock database.
3. **Security:** Seluruh perubahan status klaim dan penghapusan item transaksi terekam dalam **Audit Trail Log** bawaan Frappe.
