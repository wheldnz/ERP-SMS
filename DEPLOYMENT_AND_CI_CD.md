# DEPLOYMENT_AND_CI_CD.md — Zero-Downtime & Conflict-Free Deployment Strategy

## 🚀 1. Strategic Environment Pipeline

Sistem **ERP-SMS** mewajibkan **3 Lingkungan Server Terpisah** untuk menjamin kestabilan sistem utama (Live Production):

```mermaid
graph LR
    Dev[Environment 1: Local Developer / Dev VPS] -->|Push Git Feature| Staging[Environment 2: VPS Staging / UAT Server]
    Staging -->|Automated Tests & UAT Sign-off| Prod[Environment 3: VPS Production Live]
    
    subgraph Dev Laptop / Sandbox
        Dev
    end
    
    subgraph VPS Staging (Isolated Site)
        Staging
    end
    
    subgraph VPS Production (Live Customers)
        Prod
    end
```

| Environment | Host URL / Site | Tujuan Utama | Database Policy |
|---|---|---|---|
| **Development** | `sms-dev.local` | Tempat koding, buat Doctype kustom, uji fungsi baru. | Reset kapan saja, dummy data. |
| **Staging / UAT** | `staging.domain.com` | Pengujian fitur gabungan oleh tim QA & perwakilan 6 divisi. | Anonymized dump dari DB Prod. |
| **Production** | `erp.domain.com` | Operasional live 24/7 pengguna asli. | Real data. Strict backup policy. |

---

## 🔒 2. Protokol Deployment Bebas Bentrok (Conflict-Free Deployment)

Bentrokan saat deploy di Frappe/ERPNext umumnya disebabkan oleh dua hal:
1. **Perubahan Custom Field/UI di Production yang tertimpa oleh Git Pull.**
2. **Skema Database tidak cocok karena `bench migrate` lupa dijalankan.**

### 🚫 Aturan Keras Production:
> **TIDAK BOLEH** mengubah Custom Field, Form Script, atau Property Setter langsung dari UI Production Desk! Semua perubahan UI **WAJIB** dilakukan di Dev, di-export ke `fixtures`, dan di-deploy via Git.

---

## 🛠️ 3. Langkah-demi-Langkah Release Management

### Langkah 1: Persiapan di Dev Environment (Developer)
Setiap kali selesai membuat/mengubah fitur:
```bash
cd /home/frappe/frappe-bench

# 1. Export seluruh perubahan metadata ke fixtures JSON
bench --site sms-dev.local export-fixtures

# 2. Periksa status Git
git status

# 3. Commit fixtures dan kode Python/JS
git add apps/sms_aftersales/
git commit -m "feat(insurance): add claim approval workflow & fixtures"
git push origin feature/insurance-claim
```

---

### Langkah 2: Deployment ke VPS Staging / UAT Server
Di server Staging:
```bash
cd /home/frappe/frappe-bench

# 1. Fetch branch staging terbaru
git checkout staging
git pull origin staging

# 2. Jalankan Migrasi Database & Import Fixtures
bench --site staging.domain.com migrate

# 3. Build Static Assets (JS/CSS)
bench build --app sms_aftersales

# 4. Clear Cache & Restart Server Background Workers
bench --site staging.domain.com clear-cache
sudo supervisorctl restart all  # Atau bench restart
```
*Lakukan pengujian UAT menyeluruh di server Staging.*

---

### Langkah 3: Deployment ke VPS Production (Live Release)
Setelah UAT dinyatakan **LULUS (Passed)**:

```bash
cd /home/frappe/frappe-bench

# 1. AUTOMATED BACKUP PRODUCTION (WAJIB PERTAMA!)
bench --site erp.domain.com backup --with-files

# 2. Putar ke Maintenance Mode untuk cegah data corrupt saat migrasi
bench --site erp.domain.com set-maintenance-mode on

# 3. Pull kode final dari branch main
git checkout main
git pull origin main

# 4. Jalankan Migrasi Database Frappe
bench --site erp.domain.com migrate

# 5. Build Assets & Clear Cache
bench build --app sms_aftersales
bench --site erp.domain.com clear-cache

# 6. Matikan Maintenance Mode & Restart Service
bench --site erp.domain.com set-maintenance-mode off
sudo supervisorctl restart all

# 7. Verifikasi Log Error
bench --site erp.domain.com doctor
```

---

## ⏪ 4. Disaster Recovery & Rollback Protocol

Jika saat deployment di Production terjadi fatal error yang menghentikan operasional:

1. **Rollback Kode Git:**
   ```bash
   git reset --hard HEAD~1
   ```
2. **Restore Database dari Backup Otomatis:**
   ```bash
   bench --site erp.domain.com restore /path/to/backup/YYYYMMDD_HHMMSS-erp_domain_com-db.sql.gz
   bench --site erp.domain.com migrate
   bench --site erp.domain.com clear-cache
   ```
3. **Restart Services:**
   ```bash
   sudo supervisorctl restart all
   ```
