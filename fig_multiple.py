import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.io import loadmat
from scipy.interpolate import interp1d # supplement

def fig_multiple(mat1, mat2):
    KK    = np.logspace(-2,np.log10(8000),200)  # Kinetic energy [MeV]
    rest_mass = 0.51099895                          # Electron rest mass [MeV] by E=mc**2
    gamma_k = KK / rest_mass + 1                     # from fig_WnDH.m Line 164
    col_name = range(1,15,1)

    Bk = pd.read_csv('/home/b/b37986/Hsieh_etal_2020/DATA/Bk.dat', delimiter='\s+', names=col_name, encoding='shift-jis')
    Bk = Bk.fillna(0)
    zs = Bk.iloc[1:, 0].values
    zs = zs.astype(float)
    print(f'zs: {zs}')

    Lat = Bk.iloc[1:, 1].values
    Lat = Lat.astype(float)
    print(f'Lat: {Lat}')

    Lat[:3330] = -Lat[:3330]
    Bz0 = Bk.iloc[:, 2].values
    wc0 = Bk.iloc[1:, 3].values
    wc0 = wc0.astype(float)
    kz0 = Bk.iloc[1:, 4].values
    kz0 = kz0.astype(float)
    kz1 = Bk.iloc[1:, 5].values
    kz1 = kz1.astype(float)
    nz = Bk.iloc[:, 2].values
    nz = len(zs)
    cet = int(nz // 2) + 1

    ww0 = 0.25
    ww1 = 0.5
    tt = 0.0000166125

    # 色の設定
    colorn = np.array([[.5, 0, .5],
                    [0, 0, 1],
                    [1, 0, 0],
                    [0, .5, 0]])

    colorp = np.array([[.7, .05, .05],
                    [0, 0, .7],
                    [0, .7, 0],
                    [1, 0, 0],
                    [0, .5, 0],
                    [0, .7, .7]])

    tr = mat2['tr']
    tr = tr * tt

    Zz = mat2['Zz']
    Zz = Zz.astype(float)

    interp_func = interp1d(zs, Lat, fill_value="extrapolate") # linear supplement between zs and Lat
    Latt = interp_func(Zz)

    plt.figure(figsize=(6, 9))
    ax1 = plt.subplot(2, 1, 1)
    ax1.set_xlim([-12, 12])
    ax1.set_ylim([-0.4, 0.4])
    ax2 = plt.subplot(2, 1, 2)

    # Calculate and Plot Resonance Velocity
    for nthi in range(2, 4):
        gamma = gamma_k[nthi]
        nth = nthi - 2
        print(len(wc0), len(kz0))
        print(f"type(ww0): {type(ww0)}, {ww0}, type(nth): {type(nth)}, type(wc0): {type(wc0)}, {wc0}, type(gamma): {type(gamma)}, type(kz0): {type(kz0)}")
        VR = (ww0 - nth * wc0 / gamma) / kz0 # Resonance Velocity
        VR[cet] = np.nan
        ax1.plot(Lat, VR, ':', color=colorn[nthi, :], linewidth=1)

        VR = (ww1 - nth * wc0 / gamma) / kz1
        VR[cet] = np.nan
        ax1.plot(Lat, VR, '-.', color=colorn[nthi, :], linewidth=1)

    # Plot Data Points
    Vzz = mat2["Vzz"]
    ci = 0
    ax1.plot(Latt[:, ci],   Vzz[:, ci],       color=colorp[ci, :], linewidth=1.5)
    ax1.plot(Latt[0, ci],   Vzz[0, ci], 'o',  color=colorp[ci, :], markerfacecolor=colorp[ci, :], linewidth=1.5)
    ax1.plot(Latt[-1, ci],  Vzz[-1, ci], 'o', color=colorp[ci, :], markerfacecolor='white', linewidth=1.5)

    # Calculate and Plot ΔK
    KE = mat2["KE"] # Kinetic Energy
    for ci in range(1):
        ax2.plot(tr, KE[:, ci] - KE[0, ci], color=colorp[ci, :], linewidth=1.5)

    plt.tight_layout()
    plt.show()
    plt.savefig('/home/b/b37986/Hsieh_etal_2020/kuribayashi/fig_multiple.png', dpi=300)
    plt.savefig('/home/b/b37986/Hsieh_etal_2020/kuribayashi/fig_multiple.pdf', dpi=500)
    
mat1 = loadmat('/home/b/b37986/Hsieh_etal_2020/DATA/multiple1.mat')
mat2 = loadmat('/home/b/b37986/Hsieh_etal_2020/DATA/multiple2.mat')

fig_multiple(mat1, mat2)

