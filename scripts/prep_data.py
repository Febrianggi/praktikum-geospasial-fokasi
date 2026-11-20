"""Siapkan data olahan dari sumber lokal. Tidak ada data yang ditebak atau disintesis."""
import re, sys, json
import numpy as np, pandas as pd, geopandas as gpd
from shapely.validation import make_valid

P = sys.argv[1]            # folder paket
TXT = sys.argv[2]          # teks halaman 288 PDF BPS (pdftotext -layout)
S, O = P + "/data/sumber/", P + "/data/olahan/"

# ---------- 1. Tabel 2.5.14 BPS ----------
KODE = {"Aceh": 11, "Sumatera Utara": 12, "Sumatera Barat": 13, "Riau": 14, "Jambi": 15, "Sumatera Selatan": 16,
        "Bengkulu": 17, "Lampung": 18, "Kepulauan Bangka Belitung": 19, "Kepulauan Riau": 21, "DKI Jakarta": 31,
        "Jawa Barat": 32, "Jawa Tengah": 33, "DI Yogyakarta": 34, "Jawa Timur": 35, "Banten": 36, "Bali": 51,
        "Nusa Tenggara Barat": 52, "Nusa Tenggara Timur": 53, "Kalimantan Barat": 61, "Kalimantan Tengah": 62,
        "Kalimantan Selatan": 63, "Kalimantan Timur": 64, "Kalimantan Utara": 65, "Sulawesi Utara": 71,
        "Sulawesi Tengah": 72, "Sulawesi Selatan": 73, "Sulawesi Tenggara": 74, "Gorontalo": 75, "Sulawesi Barat": 76,
        "Maluku": 81, "Maluku Utara": 82, "Papua": 91, "Papua Barat": 92, "Papua Selatan": 93, "Papua Tengah": 94,
        "Papua Pegunungan": 95, "Papua Barat Daya": 96}
NUM = r"(\d{1,3},\d{2}|–)"
rows = []
for line in open(TXT, encoding="utf-8"):
    line = re.sub(r"\s+(go|id|\.|ps|w|//w|s:|tp|ht|\.b)\s+", " ", line)  # buang sisa watermark
    m = re.match(r"^\s{1,4}([A-Z][A-Za-z .]+?)\s{2,}" + r"\s+".join([NUM] * 6) + r"\s*$", line)
    if m:
        rows.append([m.group(1).strip()] + [None if v == "–" else float(v.replace(",", ".")) for v in m.groups()[1:]])
cols = ["provinsi_bps", "perkotaan_2023", "perkotaan_2024", "perdesaan_2023", "perdesaan_2024",
        "gabungan_2023", "gabungan_2024"]
bps = pd.DataFrame(rows, columns=cols)
nasional = bps[bps.provinsi_bps == "Indonesia"]
bps = bps[bps.provinsi_bps != "Indonesia"].copy()
assert len(bps) == 38, len(bps)
assert set(bps.provinsi_bps) == set(KODE), set(bps.provinsi_bps) ^ set(KODE)
assert len(nasional) == 1 and nasional.gabungan_2024.iloc[0] == 84.71
bps.insert(0, "kode_bps", bps.provinsi_bps.map(KODE))
bps = bps.sort_values("kode_bps")
bps["sumber"] = ("BPS, Statistik Lingkungan Hidup Indonesia 2025, Tabel 2.5.14 (hlm. 262; hlm. PDF 288); "
                 "Susenas; kolom (7) Perkotaan dan Perdesaan 2024")
bps.to_csv(O + "bps_tabel_2_5_14_ketahanan_bangunan.csv", index=False)
print("BPS:", len(bps), "provinsi | nasional 2024 =", nasional.gabungan_2024.iloc[0],
      "| kosong gabungan_2024 =", bps.gabungan_2024.isna().sum())

# ---------- 2. Batas 38 provinsi ----------
g = gpd.read_file(S + "batas_38_provinsi_denyherianto.geojson")
g["provinsi_bps"] = g["PROVINSI"].replace({"Daerah Istimewa Yogyakarta": "DI Yogyakarta"})
assert g.provinsi_bps.is_unique and set(g.provinsi_bps) == set(KODE)
g["kode_bps"] = g.provinsi_bps.map(KODE)
n_invalid = int((~g.geometry.is_valid).sum())
g["geometry"] = g.geometry.apply(make_valid)
g["geometry"] = g.geometry.apply(lambda x: x if x.geom_type in ("Polygon", "MultiPolygon")
                                 else gpd.GeoSeries([x]).explode().loc[lambda s: s.geom_type.isin(["Polygon", "MultiPolygon"])].union_all())
assert g.geometry.is_valid.all()
g = g[["kode_bps", "provinsi_bps", "geometry"]].sort_values("kode_bps")
g.to_file(O + "batas_38_provinsi.geojson", driver="GeoJSON")
print("Batas:", len(g), "poligon | geometri tidak valid diperbaiki:", n_invalid)

# ---------- 3. Uji gabung 1:1 ----------
m = g.merge(bps, on=["kode_bps", "provinsi_bps"], how="outer", validate="one_to_one", indicator=True)
assert (m._merge == "both").all() and len(m) == 38
print("Gabung 1:1: 38/38 cocok")

# ---------- 4. Episentrum USGS ----------
u = pd.read_csv(S + "usgs_gempa_2026_M4.5.csv")
u["waktu_utc"] = pd.to_datetime(u["time"], utc=True, errors="coerce")
AWAL, AKHIR = pd.Timestamp("2026-01-01", tz="UTC"), pd.Timestamp("2026-11-17", tz="UTC")
aturan = [
    ("id kosong", u["id"].isna()),
    ("id duplikat", u["id"].duplicated(keep="first")),
    ("koordinat kosong atau bukan angka", pd.to_numeric(u.latitude, errors="coerce").isna() | pd.to_numeric(u.longitude, errors="coerce").isna()),
    ("koordinat di luar rentang bumi", ~u.latitude.between(-90, 90) | ~u.longitude.between(-180, 180)),
    ("di luar kotak studi 94–142 BT, 11,5 LS–6,5 LU", ~u.latitude.between(-11.5, 6.5) | ~u.longitude.between(94, 142)),
    ("waktu kosong atau di luar periode", u.waktu_utc.isna() | (u.waktu_utc < AWAL) | (u.waktu_utc >= AKHIR)),
    ("bukan gempa bumi (type)", u["type"] != "earthquake"),
    ("magnitudo kosong atau < 4,5", u.mag.isna() | (u.mag < 4.5)),
    ("akurasi horizontal tidak tercatat", u.horizontalError.isna()),
]
alasan = pd.Series("", index=u.index)
for nama, gagal in aturan:
    alasan[gagal & (alasan == "")] = nama
keluar = u[alasan != ""].assign(alasan=alasan[alasan != ""])
lolos = u[alasan == ""].copy()
keluar[["id", "time", "latitude", "longitude", "mag", "alasan"]].to_csv(O + "episentrum_dikeluarkan.csv", index=False)
pts = gpd.GeoDataFrame(lolos, geometry=gpd.points_from_xy(lolos.longitude, lolos.latitude), crs="EPSG:4326")
j = gpd.sjoin(pts, g[["kode_bps", "provinsi_bps", "geometry"]], how="left", predicate="within")
assert j.index.is_unique, "titik masuk >1 poligon"
lolos["kode_bps_poligon"] = j["kode_bps"].astype("Int64")
lolos["provinsi_poligon"] = j["provinsi_bps"].fillna("di luar poligon provinsi (laut/negara lain)")
keep = ["id", "time", "latitude", "longitude", "depth", "mag", "magType", "place", "horizontalError",
        "depthError", "status", "kode_bps_poligon", "provinsi_poligon"]
lolos[keep].to_csv(O + "episentrum_valid.csv", index=False)
rek = {r: int((alasan == r).sum()) for r, _ in aturan}
print("USGS:", len(u), "baris | lolos", len(lolos), "| dikeluarkan", len(keluar), rek)
print("Di dalam poligon provinsi:", int(lolos.kode_bps_poligon.notna().sum()))
json.dump({"bps_n": 38, "nasional_2024": 84.71, "usgs_n": len(u), "usgs_lolos": len(lolos),
           "usgs_keluar": len(keluar), "aturan": rek, "periode_utc": [str(u.waktu_utc.min()), str(u.waktu_utc.max())],
           "dalam_poligon": int(lolos.kode_bps_poligon.notna().sum()), "geom_invalid_fixed": n_invalid},
          open(O + "ringkasan_validasi.json", "w"), indent=1)
