# Mapping the Numbers: praktikum data geospasial dengan Python

Modul praktikum untuk sesi *Mapping the Numbers: Exploring Geospatial Data Through Visualization With Python* pada Pelatihan Internal Software X Survei FOKASI 2.0 2026 (Minggu, 22 November 2026).

Peserta memetakan data survei resmi ke 38 provinsi Indonesia, menggabungkannya dengan katalog gempa, lalu menguji pola persebarannya. Semua data sudah ada di repo ini, jadi notebook bisa langsung dijalankan tanpa API key.

[![Buka di Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Febrianggi/praktikum-geospasial-fokasi/blob/main/Praktikum_Geospasial_SOLUSI.ipynb)

## Cara menjalankan

**Google Colab (disarankan)**

1. Klik tombol *Buka di Colab* di atas, lalu pilih *File › Save a copy in Drive* agar perubahanmu tersimpan.
2. Jalankan sel M0. Sel ini mengunduh `data_praktikum.zip` dari repo ini, mengekstraknya, dan memasang library yang belum ada (sekitar 1 menit).
3. Jalankan sel berikutnya satu per satu. Notebook ini sudah lengkap dengan jawaban dan output, jadi bisa juga dibaca tanpa dijalankan.

Kalau unduhan otomatis gagal, unggah `data_praktikum.zip` ke panel *Files* di Colab (namanya harus persis `data_praktikum.zip`), lalu jalankan M0 lagi.

**Komputer sendiri**

```bash
git clone https://github.com/Febrianggi/praktikum-geospasial-fokasi.git
cd praktikum-geospasial-fokasi
pip install -r requirements.txt
jupyter notebook Praktikum_Geospasial_SOLUSI.ipynb
```

Hasil peta dan tabel tersimpan di folder `output/`.

## Isi modul

| Modul | Isi | Menit |
|---|---|---|
| M0 | Persiapan dan paket data | 3 |
| M1 | Batas 38 provinsi, tabel BPS, sistem koordinat (EPSG:4326 dan EPSG:6933) | 6 |
| M2 | Mencatat koordinat GPS dan memeriksa akurasinya | 6 |
| M3 | Attribute join tabel BPS ke poligon secara 1:1 | 5 |
| M4 | Peta tematik (choropleth) PNG | 7 |
| M5 | Peta interaktif HTML dengan legenda yang sama | 7 |
| M6 | Peta persebaran episentrum USGS, validasi, dan spatial join `within` | 5 |
| M7 | Peringkat, Global Moran's I, dan LISA (KNN k = 4) | 4 |
| M8 | Dari peta ke keputusan | 2 |

## Struktur repo

```
Praktikum_Geospasial_SOLUSI.ipynb    notebook lengkap beserta output dan jawaban
data_praktikum.zip                   isi folder data/ dalam satu berkas, untuk Colab
data/
  sumber/                            data mentah (CSV USGS, GeoJSON batas, halaman tabel BPS)
  olahan/                            data siap pakai, dibuat oleh scripts/prep_data.py
  templat_pencatatan_gps.csv         templat kosong untuk survei GPS
scripts/prep_data.py                 membuat data/olahan/ dari data/sumber/
docs/PANDUAN_PRAKTIKUM.md            jadwal, langkah demo, dan daftar tanya jawab untuk pemateri
```

Untuk membuat ulang `data/olahan/`:

```bash
python scripts/prep_data.py . data/sumber/bps_slhi2025_hlm288.txt
```

## Sumber data

| Data | Sumber | Catatan |
|---|---|---|
| Persentase rumah tangga dengan ketahanan bangunan (atap, dinding, lantai) memenuhi syarat, per provinsi, 2024 | BPS, *Statistik Lingkungan Hidup Indonesia 2025*, Tabel 2.5.14 (data Susenas), kolom Perkotaan dan Perdesaan 2024 | `data/sumber/bps_slhi2025_hlm288.txt` adalah teks halaman tabel; publikasi lengkap ada di situs BPS (bps.go.id) |
| Episentrum gempa M ≥ 4,5, 1 Januari sampai 16 November 2026 (UTC), 94–142° BT, 11,5° LS–6,5° LU | USGS Earthquake Catalog | Domain publik |
| Batas 38 provinsi | GeoJSON publik dari repo GitHub `denyherianto/indonesia-geojson-topojson-maps-with-38-provinces` | Instansi sumber dan lisensinya tidak disebutkan. Pakai hanya untuk latihan; ganti dengan batas resmi Badan Informasi Geospasial untuk analisis resmi |

Indikator BPS ini mengukur atap, dinding, dan lantai yang memenuhi syarat menurut definisi BPS, bukan ketahanan terhadap gempa.

## Pemateri

Febrianggi Caesar Immanuel, Statistika, Universitas Padjadjaran.
