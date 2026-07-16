# BUSINESS_PROCESS_FLOW.md — End-to-End Business Workflows

## 🔄 1. Master After-Sales Service & Insurance Workflow

Diagram urutan berikut menjelaskan alur transaksi lengkap dari kedatangan pelanggan hingga penutupan jurnal keuangan:

```mermaid
sequenceDiagram
    autonumber
    actor Customer as Pelanggan
    participant Retail as Retail / Frontdesk
    participant Ins as Insurance Divisi
    participant Tech as Service Technician
    participant Whs as Warehouse Divisi
    participant Acc as Finance & Accounting

    Customer->>Retail: Serahkan Unit Rusak & Info Polis
    Retail->>Retail: Cek Serial No & Buat SMS Service Intake
    
    alt Unit Memiliki Asuransi
        Retail->>Ins: Trigger SMS Insurance Claim (Status: Draft)
        Ins->>Ins: Verifikasi dokumen & foto kerusakan
        alt Claim Approved
            Ins-->>Retail: Status Claim: Approved
        else Claim Rejected
            Ins-->>Retail: Status Claim: Rejected (Customer Pay Manual)
        end
    end

    Retail->>Tech: Generate SMS Service Order (Work Ticket)
    Tech->>Tech: Diagnosa kebutuhan sparepart
    
    Tech->>Whs: Minta suku cadang via Service Order
    Whs->>Whs: Eksekusi Stock Entry (Material Issue)
    Whs-->>Tech: Serahkan Sparepart (Serialized Part)
    
    Tech->>Tech: Lakukan Perbaikan & Logging Jam Kerja
    Tech->>Retail: Servis Selesai (Status: Completed)
    
    alt Pembayaran oleh Asuransi
        Acc->>Ins: Buat Sales Invoice ke Perusahaan Asuransi
        Ins-->>Acc: Pembayaran Cair ➔ Jurnal Settlement
    else Pembayaran Mandiri
        Retail->>Customer: Tagih via POS Invoice
        Customer-->>Retail: Bayar Tunai / QRIS
    end

    Retail->>Customer: Serahkan Unit Selesai Servis
```

---

## 🛠️ 2. Detailed Workflows per Process

### A. Sub-Process: Insurance Claim Approval Flow

```mermaid
flowchart TD
    A[Klaim Baru Dibuat dari Service Intake] --> B{Nominal Estimasi Perbaikan}
    B -->|< Rp 2.000.000| C[Auto Approve Level 1]
    B -->|>= Rp 2.000.000| D[Queue Review Insurance Manager]
    D --> E{Keputusan Manager}
    E -->|Approve| F[Status: Claim Approved]
    E -->|Reject| G[Status: Rejected - Tagih Customer]
    C --> F
    F --> H[Update Service Order: Pertanggungan Disetujui]
```

### B. Sub-Process: Sparepart Transfer & Stock Accounting

```mermaid
flowchart TD
    A[Teknisi Request Sparepart di Service Order] --> B{Stok di Gudang Cabang Ada?}
    B -->|Ya| C[Submit Stock Entry: Material Issue]
    B -->|Tidak| D[Buat Material Request Transfer ke Gudang Pusat]
    D --> E[Gudang Pusat Kirim: Stock Entry Material Transfer]
    E --> F[Stok Diterima di Gudang Cabang]
    F --> C
    C --> G[Stok Ledger Updated & HPP Terbentuk di Accounting GL]
```

---

## 📊 3. Matrix Dokumentasi & Output per Tahap

| Tahapan | Dokumen ERPNext yang Dihasilkan | Penanggung Jawab | Trigger Otomatis |
|---|---|---|---|
| 1. Reception | `SMS Service Intake` | Frontdesk Retail | Notifikasi WhatsApp/Email ke Customer |
| 2. Claim Assesment | `SMS Insurance Claim` | Insurance Specialist | Lock Limit Polis Asuransi |
| 3. Execution | `SMS Service Order` | Service Lead | Alokasi Teknisi berdasarkan Skill |
| 4. Parts Allocation| `Stock Entry (Material Issue)`| Warehouse Keeper | Potong Stok Serialized Parts |
| 5. Invoicing | `Sales Invoice` / `POS Invoice`| Finance / Kasir | Update Piutang Customer/Asuransi |
| 6. Settlement | `Journal Entry` | Accounting Specialist | Pengakuan Kas & Pelunasan Piutang |
