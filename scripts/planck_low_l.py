"""
planck_low_l.py
ℓ = 2–20 güç tayfı + fraktal model grafiği üretir.
"""

import os, urllib.request, healpy as hp, numpy as np, matplotlib.pyplot as plt

# --- 0. Ayarlar ---
URLS = [
    "https://pla.esac.esa.int/pla-sl/data-action?MAP.MAP_ID=COM_CMB_IQU-commander_2048_R3.00_full&DOWNLOAD",
    "https://lambda.gsfc.nasa.gov/data/planck/pla/2020/component_maps/cmb/COM_CMB_IQU-commander_2048_R3.00_full.fits"
]
FITS_PATH = "data/planck_commander_2048.fits"

# --- 1. İndir (fallback'li) ---
def download_if_needed():
    if os.path.exists(FITS_PATH):
        return
    os.makedirs("data", exist_ok=True)
    for link in URLS:
        try:
            print(f"Downloading Planck map from:\n  {link}")
            urllib.request.urlretrieve(link, FITS_PATH)
            print("Download successful.")
            return
        except Exception as e:
            print(f"Failed ({e}). Trying next mirror...")
    raise RuntimeError("All download mirrors failed.")

download_if_needed()

# --- 2. Haritayı oku (I kanalı) ---
print("Reading FITS...")
cmb_map = hp.read_map(FITS_PATH, field=0, verbose=False)

# --- 3. C_ell hesapla ---
print("Computing Cl...")
cl = hp.anafast(cmb_map, lmax=20)
ell = np.arange(len(cl))

# --- 4. ℓ=2–20 seç ---
mask = (ell >= 2) & (ell <= 20)
ell_cut = ell[mask]
cl_cut = cl[mask]

# --- 5. Fraktal model (α=2.3) ---
alpha = 2.3
norm = cl_cut[0] * (ell_cut[0] ** alpha)
model = norm * ell_cut ** (-alpha)

# --- 6. Grafik ---
os.makedirs("fig", exist_ok=True)
plt.figure()
plt.loglog(ell_cut, cl_cut, 'o', label='Planck 2018')
plt.loglog(ell_cut, model, '-', label=rf'$\ell^{{-{alpha:.1f}}}$')
plt.xlabel(r'Multipole $\ell$')
plt.ylabel(r'$C_\ell\;[\mu\mathrm{K}^2]$')
plt.title('Low‑ℓ Power Spectrum (2–20)')
plt.legend()
plt.tight_layout()
plt.savefig("fig/low_l_spectrum.png", dpi=300)
print("Saved fig/low_l_spectrum.png")
