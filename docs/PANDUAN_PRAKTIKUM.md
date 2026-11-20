# Panduan praktikum dan tanya jawab

Bagian ini tidak ada di PPT pematerian. Isinya dipakai pemateri sesudah materi pengantar (15.10–16.10).

## 1. Jadwal modul praktikum (15.10–15.55, 45 menit)

| Modul | Isi | ToR | Menit | Sel kode |
|---|---|---|---|---|
| M0 | Persiapan dan paket data lokal | – | 3 | In[1]–In[2] |
| M1 | Batas 38 provinsi, tabel BPS, CRS | H.1 | 6 | In[3]–In[5] |
| M2 | Mencatat koordinat GPS dan akurasinya | H.2 | 6 | In[6]–In[7] |
| M3 | Menggabung tabel ke poligon secara 1:1 | H.1, H.3 | 5 | In[8]–In[9] |
| M4 | Peta tematik (choropleth) PNG | H.3 | 7 | In[10]–In[12] |
| M5 | Peta interaktif HTML, legenda sama | H.3 | 7 | In[13]–In[14] |
| M6 | Episentrum USGS dan validasinya | H.2, H.3 | 5 | In[15]–In[17] |
| M7 | Peringkat, Moran's I, LISA | H.4 | 4 | In[18]–In[20] |
| M8 | Dari peta ke keputusan | H.5 | 2 | In[21]–In[23] |

Nomor In[n] merujuk ke notebook `Praktikum_Geospasial_SOLUSI.ipynb`. Bila waktu mepet, M7 dijadikan demo saja.

## 2. Demo Colab (langkah untuk pemateri dan peserta)

1. Buka notebook `Praktikum_Geospasial_SOLUSI.ipynb` lewat tombol *Buka di Colab* di README repo ini.
2. Jalankan sel M0. Sel ini mengunduh dan mengekstrak `data_praktikum.zip`, lalu memasang library yang belum ada, sekitar 1 menit. Bila unduhan gagal, unggah `data_praktikum.zip` ke panel Files (jangan diganti namanya) lalu jalankan M0 lagi.
3. Pilih Runtime › Run all.
4. Demo yang ditunjukkan pemateri:
   - **M4:** peta tematik.
   - **M5:** peta HTML. Arahkan kursor ke NTT (67,50%, kelas 60–<80%) dan tunjukkan layer control.
   - **M6:** peta persebaran.
   - **M7:** Moran's I dan LISA.
5. Hasil tersimpan di folder `output/`. Klik kanan, lalu Download.
6. Cadangan bila Colab lambat: tunjukkan output yang sudah tersimpan di notebook tanpa menjalankan ulang.

Untuk peserta, bagikan tautan repo atau tautan *Buka di Colab*. Peserta memilih File › Save a copy in Drive.

## 3. Hasil yang dibahas di praktikum (tidak ditampilkan di PPT)

| Hasil | Nilai | Letak |
|---|---|---|
| Peringkat 38 provinsi | 40,85% (Papua Pegunungan) sampai 99,39% (Kalimantan Utara); 8 provinsi di bawah nasional 84,71% | M7 In[18], `output/peringkat_ketahanan_bangunan_2024.png` |
| Moran's I (KNN k=4) | I = 0,090; E(I) = −0,027; p ≈ 0,12 (999 permutasi): tidak signifikan | M7 In[19] |
| LISA (α = 0,05) | High-High: Sumatera Utara, Kalimantan Utara, Maluku Utara; tidak ada Low-Low | M7 In[20], `output/peta_lisa_ketahanan_bangunan_2024.png` |
| Kasus keputusan | Provinsi < 80% yang punya episentrum di dalam poligon: Jawa Barat, Banten, NTT, Papua Tengah, Papua Pegunungan | M8 In[21]–In[22] |
| Jawaban kasus (temuan, batasan, rekomendasi) | Kunci jawaban tertulis | Notebook, sel jawaban setelah In[22]; juga sel jawaban M2 dan M7 |

Kode lengkap semua langkah ada di notebook. PPT pengantar sengaja tidak memuat kode.

## 4. Tanya jawab (15.55–16.10, 15 menit, tanpa slide)

| Pertanyaan yang mungkin muncul | Jawaban singkat |
|---|---|
| Kenapa tidak memakai radius untuk memasukkan episentrum ke provinsi? | Radius memaksa titik di laut masuk ke provinsi tertentu dan menambah bias. Provinsi hanya diberikan bila episentrum berada di dalam poligon. |
| Perbedaannya besar, kenapa Moran's I tidak signifikan? | Perbedaan besar tidak sama dengan mengelompok. Provinsi dengan nilai rendah tersebar di barat dan timur. |
| Queen atau KNN? | Queen untuk wilayah daratan. Untuk kepulauan pakai KNN atau jarak, lalu uji sensitivitasnya (k=3 memberi p ≈ 0,06). |
| Apakah indikator ini mengukur ketahanan gempa? | Tidak. Indikator ini tentang atap, dinding, dan lantai yang memenuhi syarat menurut definisi BPS. |
| Bagaimana dengan data survei sendiri? | Pakai `data/templat_pencatatan_gps.csv` dan fungsi `validasi_koordinat` di M2. |
