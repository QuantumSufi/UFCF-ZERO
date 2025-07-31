"""
planck_low_l.py   –   ℓ = 2‑20 güç tayfı + fraktal model grafiği
  1) Haritayı (≈50 MB) indirmeye çalışır  ➜ healpy anafast
  2) Harita download  ×  ise: Planck TT power‑spectrum metnini kullanır
"""

import os, urllib.request, numpy as np, matplotlib.pyplot as plt
import warnings

MAP_URLS = [
    # ESA preview mirror (works via HTTP 302)
    "https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/previews/"
    "COM_CMB_IQU-commander_2048_R3.00_full/COM_CMB_IQU-commander_2048_R3.00_full_I_STOKES.fits"
]
PS_URL   = ("https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/"
            "cosmoparams/COM_PowerSpect_CMB-TT-full_R3.01.txt")

FITS_PATH = "data/planck_I_stokes.fits"
PS_PATH   = "data/planck_TT.txt"

os.makedirs("data", exist_ok=True)
os.makedirs("fig",  exist_ok=True)

# ------------------------------------------------------------
def try_download(url, dest):
    try:
        urllib.request.urlretrieve(url, dest)
        return True
    except Exception as e:
        print(f"  failed: {e}")
        return False

# ---------- 1) Harita indirme denemesi ----------
map_ok = False
for link in MAP_URLS:
    if os.path.exists(FITS_PATH):
        map_ok = True
        break
    print(f"Downloading Planck map:\n  {link}")
    if try_download(link, FITS_PATH):
        map_ok = True
        break

if map_ok:
    # healpy yalnız harita yolunu görünce memory‑map okur – düşük RAM
    import healpy as hp
    print("Reading FITS & computing Cl...")
    m = hp.read_map(FITS_PATH, verbose=False)
    cl = hp.anafast(m, lmax=20)
    ell = np.arange(len(cl))
else:
    # ---------- 2) Yedek güç tayfı metni ----------
    if not os.path.exists(PS_PATH):
        print("Map download başarısız ➜ güç tayfı metni indiriliyor …")
        if not try_download(PS_URL, PS_PATH):
            raise RuntimeError("Planck verisi indirilemedi – CI durdu.")
    # Metin dosyasında: ℓ  D_ℓ  σ …
    data = np.loadtxt(PS_PATH)
    ell = data[:, 0].astype(int)
    Dl  = data[:, 1]           # μK²
    cl  = Dl * 2*np.pi / (ell*(ell+1))  # Cl = Dℓ * 2π / ℓ(ℓ+1)

# ---------- 3) ℓ = 2–20 seç ----------
mask = (ell >= 2) & (ell <= 20)
ell_cut, cl_cut = ell[mask], cl[mask]

# ---------- 4) Fraktal model ----------
alpha = 2.3
norm  = cl_cut[0] * (ell_cut[0] ** alpha)
model = norm * ell_cut ** (-alpha)

# ---------- 5) Grafik ----------
plt.figure()
plt.loglog(ell_cut, cl_cut, 'o', label='Planck (PR3)')
plt.loglog(ell_cut, model, '-', label=rf'$\ell^{{-{alpha:.1f}}}$')
plt.xlabel(r'Multipole $\ell$')
plt.ylabel(r'$C_\ell\;[\mu\mathrm{K}^2]$')
plt.title('Low‑ℓ Power Spectrum (2–20)')
plt.legend()
plt.tight_layout()
plt.savefig("fig/low_l_spectrum.png", dpi=300)
print("Saved fig/low_l_spectrum.png")
