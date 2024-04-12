import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.close('all')

# set the parameters
folder = '/home/b/b37986/Hsieh_etal_2020/DATA/wave_model/'
mark = ['(a)', '(b)', '(c)']
skip = 20
Lv = 4.5  # L-value
Beq = 342.3868312757202  # equatorial background magnetic field [nT]
wceq = 6.027513227513229e+4  # equatorial electron cyclotron frequency [rad]
fceq = wceq / (2 * np.pi) / 1000  # [kHz]

# load the file
Bk = pd.read_csv(folder + 'Bk.dat', delim_whitespace=True, skiprows=1, header=None)
zs = Bk.iloc[:, 0].values
Lat = Bk.iloc[:, 1].values
wc0 = Bk.iloc[:, 2].values
kz0 = Bk.iloc[:, 3].values
theta = Bk.iloc[:, 7].values
nz = len(zs)
cet = int(nz // 2)+1
Lat[0:cet] = -Lat[0:cet]

ww = pd.read_csv(folder + 'parameters.dat', delim_whitespace=True, skiprows=1, header=None)
cv = ww.iloc[:, 0]
NP = ww.iloc[:, 4]
times = ww.iloc[:, 5]
w_min = ww.iloc[:, 1]
w_max = ww.iloc[:, 2]
dz = ww.iloc[:, 7]

we0 = pd.read_csv(folder + 'Aweq.dat', delim_whitespace=True, skiprows=1, header=None)
tr = we0.iloc[:, 0].values / wceq
Aweq = we0.iloc[:, 1].values
wweq = we0.iloc[:, 2].values

steps = int(times // skip)

# load the binary file
Aw = np.fromfile(folder + 'Aw.dat', dtype='double').reshape(steps, nz).T
ww = np.fromfile(folder + 'ww.dat', dtype='double').reshape(steps, nz).T

# set for plotting
fig = plt.figure(figsize=(7.5, 9.2))

ax1 = fig.add_axes([0.15, 0.68, 0.35, 0.27])
#pcm1 = ax1.pcolormesh(Lat, tr, Aw / wc0[cet] * Beq, shading='flat')
# print(f"Lat.shape: {Lat.shape}")
# print(f"tr.shape: {tr.shape}")
# print(f"Aw / wc0[cet] * Beq shape: {(Aw / wc0[cet] * Beq).shape}")
# pcm1 = ax1.pcolormesh(Lat, tr, Aw / wc0[cet] * Beq, shading='nearest') #problem

# plt.colorbar(pcm1, ax=ax1, label='B_w [nT]')
# ax1.set_xlabel('Latitude [°]')
# ax1.set_ylabel('t [sec]')
# ax1.set_title(mark[0])

ax2 = fig.add_axes([0.7, 0.68, 0.2, 0.27])
ax2.plot(Aweq * Beq, tr, 'k', linewidth=1.5)
ax2.set_xlabel('$B_{\mathrm{weq}}$ [nT]')
ax2.set_ylabel('t [sec]')
ax2.grid(True)

ax3 = fig.add_axes([0.15, 0.3, 0.35, 0.27])
# pcm3 = ax3.pcolormesh(Lat, tr, ww / wc0[cet] * fceq, shading='flat') #same problem as pcm1
# plt.colorbar(pcm3, ax=ax3, label='\omega [kHz]')
# ax3.set_xlabel('Latitude [°]')
# ax3.set_ylabel('t [sec]')
# ax3.set_title(mark[1])

ax4 = fig.add_axes([0.7, 0.3, 0.2, 0.27])
ax4.plot(wweq * fceq, tr, 'k', linewidth=1.5)
ax4.set_xlabel('$\omega_{\mathrm{eq}}$ [kHz]')
ax4.set_ylabel('t [sec]')
ax4.grid(True)

ax5 = fig.add_axes([0.15, 0.08, 0.35, 0.11])
ax5.plot(Lat, theta, 'k', linewidth=2)
ax5.set_xlabel('Latitude [°]')
ax5.set_ylabel(r'$\theta$ [°]')
ax5.grid(True)
ax5.set_title(mark[2])

plt.show()