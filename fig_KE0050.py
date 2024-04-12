# Figure : 50 keV
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from matplotlib.ticker import MaxNLocator

plt.close('all')

print_pdf = 1
min_log = -8
max_log = -1
pit0 = np.array([70, 45, 20])
energy0 = 0.05 + 1e-6 #MeV

KK1 = 20  #keV
KK2 = 200 #keV
dK = 10 #keV
da = 1 #degs
wavename = ['parallel', 'wna20', 'wna60']
casename = ['Parallel', '$θ_{\mathrm{max}}$=20°', '$θ_{\mathrm{max}}$=60°']
mark = ['(a)', '(b)', '(c)'] # 70, 45 and 20 degree respectively
ep1 = 1e-2
deltaep = 1e-2
nenergyp = 601
dx = 1.0
nx = math.floor(90/dx) + 1
nx_long = math.floor(360/dx) + 1

xd = []
for i in range(0,nx):
    xd.append(i*dx)
xd = np.array(xd)
#print(f"xd:{xd}")

xd_long = []
for i in range(1,nx_long):
    xd_long.append(i*dx)
#print(f'xd_long:{xd_long}')

energy = []
for i in range(1,nenergyp):
    energy.append(ep1+deltaep*(i-1)) # from 0.01 to 6.00, increasing by 0.01
energy = np.array(energy)

fig, axes = plt.subplots(3,len(wavename),figsize=(16,8))
fig.suptitle("Green's Function at Initial Kinetic Energy 50keV", fontsize=16)
for wave_i, wave_name in enumerate(wavename):
    ienergy0 = int(math.floor((energy0 - ep1)/deltaep)) +1 
    formatted_ienergy0 = f'{ienergy0:04d}'
    print(f"formatted_ienergy0{formatted_ienergy0}")
    FILEPATH =  (f'/home/b/b37986/Hsieh_etal_2020/DATA/Green/ienergy0{formatted_ienergy0}_{wave_name}.dat')
    print(f"FILEPATH: {FILEPATH}")
    GG = pd.read_csv(FILEPATH, delimiter='\s+', header=None, dtype=float)
    for pti, ax in enumerate(axes[:, wave_i]):
        print(f"mean_GG: {np.mean(GG)}")
        ipit0 = math.floor(pit0[pti]/dx) # pit0 = ([70, 45, 20])
        print(ipit0)
        
        data = np.zeros((nenergyp, nx))
        for ipit in range(nx): # nx=90
            for ienergy in range(nenergyp): # nenergyp=601
                data[ienergy, ipit] = GG.iloc[(ienergy-1)*nx+ipit, ipit0]/dK/da

        print(f"data.dtype: {data.dtype}")
        print(f"mean_data: {np.mean(data)}")
        Kmin=int(KK1/10)
        Kmax=int(KK2/10)
        data = np.where(data <= 1e-8, 1e-8, data)
        data = np.where(data >= 1e-1, 1e-1, data)
        print("pit0[wave_i-1]:", pit0[wave_i-1])
        data_log = np.log10(data) 
        print(f"data_log.dtype: {data_log.dtype}")
        print(f"data_log.shape: {data_log.shape}")
        print(f"mean_data_log: {np.mean(data_log)}")
        print(f"max(data_log): {np.max(data_log)}, min(data_log): {np.min(data_log)}")

        levels = np.linspace(-8, -1, num=70)  # partition the range -8 to 0 into 70 equal segments. 
        X, Y = np.meshgrid(energy[Kmin:Kmax+1], xd)
        print(f"X.dtype: {X.dtype}, Y.dtype: {Y.dtype}")
        print(f"mean_data_log[Kmin:Kmax+1, :]: {np.mean(data_log[Kmin:Kmax+1, :])}")
        c = ax.contourf(X, Y, data_log[Kmin:Kmax+1, :].T, levels=levels, cmap='jet')
        ax.set_xlim([KK1/1000, KK2/1000])
        ax.set_ylim([0, 90])
        if pti==0:
            ax.set_title(f"Case{wave_i+1}: {casename[wave_i]}")
            ax.text(-0.1, 1.1, mark[wave_i], transform=ax.transAxes, fontsize=14, va='top', ha='left')
        if pti == 2:
            ax.set_xlabel('Kinetic energy [MeV]')
        if wave_i==0:
            ax.set_ylabel(r'$\alpha$ [°]')

# fig.subplots_adjust(left=0.05, right=0.85, wspace=0.3, hspace=0.3)

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.9, 0.15, 0.05, 0.7])
cbar = fig.colorbar(c, cax=cbar_ax)
formatter = MaxNLocator(integer=True)
cbar.ax.yaxis.set_major_locator(formatter)
# formatter.set_powerlimits((-3, 3))  
# cbar.ax.yaxis.set_major_formatter(formatter)  
cbar.set_label('$G [keV^{\mathrm{-1}} deg^{\mathrm{-1}}]$', rotation=90, labelpad=20)
plt.show()