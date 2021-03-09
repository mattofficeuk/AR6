import numpy as np
import pickle

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

save_file = '/data/mmenary/python_saves/Figure_AR6_DAMIP_AMOC_26N_1000m.pkl'
with open(save_file, 'rb') as handle:
    print "Loading data: {:s}".format(save_file)
    amoc_damip6_ts, damip6_models, year = pickle.load(handle)

ilat_choice = 0

def anomalise3d(in_arr, t0, t1):
    time_mean = in_arr[:, :, t0:t1].mean(axis=2)
    time_mean_repl = np.repeat(time_mean[:, :, None], nt, axis=2)
    anom = in_arr - time_mean_repl
    return anom

target_lats = [26.5, 35]
experiments_damip6 = ['historical', 'hist-aer', 'hist-GHG', 'hist-nat', 'hist-stratO3']
nt = len(year)

y0, y1 = 1860, 1880
t0 = np.argwhere(year == y0)[0][0]
t1 = np.argwhere(year == y1)[0][0]

amoc_damip6_ts_lat_ensmn = amoc_damip6_ts[:, :, :, ilat_choice, :].mean(axis=2)
amoc_damip6_ts_lat_ensmn_timeanom = anomalise3d(amoc_damip6_ts_lat_ensmn, t0, t1)
amoc_damip6_ts_lat_ensmn_timeanom_mmm = amoc_damip6_ts_lat_ensmn_timeanom.mean(axis=0)
amoc_damip6_ts_lat_ensmn_timeanom_mmsd = amoc_damip6_ts_lat_ensmn_timeanom.std(axis=0)

y2, y3 = 2004, 2017
t2 = np.argwhere(year == y2)[0][0]
t3 = np.argwhere(year == y3)[0][0]
iexpt = experiments_damip6.index('historical')

# rapid_anom = rapid_amoc + (amoc_damip6_ts_lat_ensmn_timeanom_mmm[iexpt, t2:t3].mean() - rapid_amoc.mean())

fontsize = 22
alpha = 0.1
lw1 = 4
lw2 = 2
xlim = (1850, 2020)
ylim = (-5, 3)
target_lat = target_lats[ilat_choice]
years_list = [y0, y1, 2005, 2015]
# mask_index_cutoff = 166  # Mask the smoothed data after this point, as ensemble size differences cause issues

color_damip = ['purple', 'blue', 'green', 'orange', 'grey']

plt.figure(figsize=(15, 8))

gs1 = gridspec.GridSpec(1, 1)
gs1.update(left=0, right=1, hspace=0.2)

ax1 = plt.subplot(gs1[0, 0])
for iexpt, expt in enumerate(experiments_damip6):
    middle = amoc_damip6_ts_lat_ensmn_timeanom_mmm[iexpt, :]
    mini = amoc_damip6_ts_lat_ensmn_timeanom_mmm[iexpt, :] - amoc_damip6_ts_lat_ensmn_timeanom_mmsd[iexpt]
    maxi = amoc_damip6_ts_lat_ensmn_timeanom_mmm[iexpt, :] + amoc_damip6_ts_lat_ensmn_timeanom_mmsd[iexpt]
    plt.plot(year, middle, color=color_damip[iexpt], label='{:s}'.format(experiments_damip6[iexpt]), lw=lw1)
    if expt == 'historical':
        plt.fill_between(year, mini, maxi, color=color_damip[iexpt], alpha=alpha)
        
plt.plot(year, amoc_damip6_ts_lat_ensmn_timeanom_mmm[1:, :].sum(axis=0), lw=lw2, color='k', linestyle=':')
        
# plt.plot(rapid_year, rapid_anom, color='k', lw=lw1, label='RAPID (anomaly adjusted)')

# This will make the figure shown in Figure_AR6_CMIP5-6_AMOC_35N_1000m_Anom-1s.d.Shaded.png
plt.xlim(xlim)
plt.ylim(ylim)
plt.axhline(0, linestyle=':', color='k')
for yy in years_list:
    plt.axvline(yy, color='k', linestyle=':')
plt.title('Multi-model mean AMOC anomaly at {:.1f}N, 1000m in CMIP6 DAMIP ensemble'.format(target_lat), fontsize=fontsize)
plt.legend(loc=3, ncol=3, fontsize=fontsize*0.8)
plt.xticks(fontsize=fontsize)
plt.yticks(fontsize=fontsize)
plt.ylabel('AMOC anomaly [Sv]', fontsize=fontsize)
plt.xlabel('Model year', fontsize=fontsize)
plt.show()
