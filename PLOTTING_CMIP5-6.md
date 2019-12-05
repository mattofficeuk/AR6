## To plot the AMOCs in Python2.7 I did the following.

This corresponds to the image file:

```
Figure_AR6_CMIP5-6_AMOC_35N_1000m_Anom-1s.d.Shaded.png
```

```
import numpy as np
import pickle

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

save_file = '/data/mmenary/python_saves/Figure_AR6_CMIP5-6_AMOC_35N_1000m.pkl'
with open(save_file, 'rb') as handle:
    print "Loading data: {:s}".format(save_file)
    amoc_c5_ts, amoc_c6_ts, cmip5_models, cmip6_models, year = pickle.load(handle)

ilat_choice = 1

def anomalise3d(in_arr, t0, t1):
    time_mean = in_arr[:, :, t0:t1].mean(axis=2)
    time_mean_repl = np.repeat(time_mean[:, :, None], nt, axis=2)
    anom = in_arr - time_mean_repl
    return anom

target_lats = [26.5, 35]
experiments_cmip5 = ['rcp45', 'rcp85']
experiments_cmip6 = ['ssp119', 'ssp126', 'ssp245', 'ssp370', 'ssp585']
nt = len(year)

y0, y1 = 1860, 1880
t0 = np.argwhere(year == y0)[0][0]
t1 = np.argwhere(year == y1)[0][0]

amoc_c5_ts_lat_ensmn = amoc_c5_ts[:, :, :, ilat_choice, :].mean(axis=2)
amoc_c5_ts_lat_ensmn_timeanom = anomalise3d(amoc_c5_ts_lat_ensmn, t0, t1)
amoc_c5_ts_lat_ensmn_timeanom_c5mn = amoc_c5_ts_lat_ensmn_timeanom.mean(axis=0)
amoc_c5_ts_lat_ensmn_timeanom_c5sd = amoc_c5_ts_lat_ensmn_timeanom.std(axis=0)

amoc_c6_ts_lat_ensmn = amoc_c6_ts[:, :, :, ilat_choice, :].mean(axis=2)
amoc_c6_ts_lat_ensmn_timeanom = anomalise3d(amoc_c6_ts_lat_ensmn, t0, t1)
amoc_c6_ts_lat_ensmn_timeanom_c6mn = amoc_c6_ts_lat_ensmn_timeanom.mean(axis=0)
amoc_c6_ts_lat_ensmn_timeanom_c6sd = amoc_c6_ts_lat_ensmn_timeanom.std(axis=0)

fontsize = 22
alpha = 0.1
lw1 = 4
lw2 = 2
xlim = (1850, 2100)
ylim = (-10, 4)
target_lat = target_lats[ilat_choice]
years_list = [y0, y1, 2005, 2015]
# mask_index_cutoff = 166  # Mask the smoothed data after this point, as ensemble size differences cause issues

color_c5 = ['blue', 'grey', 'black']
color_c6 = ['red', 'cyan', 'green', 'orange', 'crimson', 'purple']

plt.figure(figsize=(14, 12))

gs1 = gridspec.GridSpec(2, 1)
gs1.update(left=0, right=1, hspace=0.2)

ax1 = plt.subplot(gs1[0, 0])

iexpt = 0
iscenario_start = np.argwhere(year == 2005)[0][0]
middle = amoc_c5_ts_lat_ensmn_timeanom_c5mn[iexpt, :]
mini = amoc_c5_ts_lat_ensmn_timeanom_c5mn[iexpt, :] - amoc_c5_ts_lat_ensmn_timeanom_c5sd[iexpt]
maxi = amoc_c5_ts_lat_ensmn_timeanom_c5mn[iexpt, :] + amoc_c5_ts_lat_ensmn_timeanom_c5sd[iexpt]
plt.plot(year[:iscenario_start], middle[:iscenario_start], color=color_c5[iexpt], label='CMIP5 {:s}'.format('historical'), lw=lw1)
plt.fill_between(year[:iscenario_start], mini[:iscenario_start], maxi[:iscenario_start], color=color_c5[iexpt], alpha=alpha)
for iexpt, expt in enumerate(experiments_cmip5):
    middle = amoc_c5_ts_lat_ensmn_timeanom_c5mn[iexpt, :]
    mini = amoc_c5_ts_lat_ensmn_timeanom_c5mn[iexpt, :] - amoc_c5_ts_lat_ensmn_timeanom_c5sd[iexpt]
    maxi = amoc_c5_ts_lat_ensmn_timeanom_c5mn[iexpt, :] + amoc_c5_ts_lat_ensmn_timeanom_c5sd[iexpt]
    plt.plot(year[iscenario_start:], middle[iscenario_start:], color=color_c5[iexpt+1], label='CMIP5 {:s}'.format(experiments_cmip5[iexpt]), lw=lw1)
#     if expt == 'rcp85':
#         plt.fill_between(year[iscenario_start:], mini[iscenario_start:], maxi[iscenario_start:], color=color_c5[iexpt+1], alpha=alpha)

iexpt = 0
iscenario_start = np.argwhere(year == 2015)[0][0]
middle = amoc_c6_ts_lat_ensmn_timeanom_c6mn[iexpt, :]
mini = amoc_c6_ts_lat_ensmn_timeanom_c6mn[iexpt, :] - amoc_c6_ts_lat_ensmn_timeanom_c6sd[iexpt]
maxi = amoc_c6_ts_lat_ensmn_timeanom_c6mn[iexpt, :] + amoc_c6_ts_lat_ensmn_timeanom_c6sd[iexpt]
plt.plot(year[:iscenario_start], middle[:iscenario_start], color=color_c6[iexpt], label='CMIP6 {:s}'.format('historical'), lw=lw1)
plt.fill_between(year[:iscenario_start], mini[:iscenario_start], maxi[:iscenario_start], color=color_c6[iexpt], alpha=alpha)
for iexpt, expt in enumerate(experiments_cmip6):
    middle = amoc_c6_ts_lat_ensmn_timeanom_c6mn[iexpt, :]
    mini = amoc_c6_ts_lat_ensmn_timeanom_c6mn[iexpt, :] - amoc_c6_ts_lat_ensmn_timeanom_c6sd[iexpt]
    maxi = amoc_c6_ts_lat_ensmn_timeanom_c6mn[iexpt, :] + amoc_c6_ts_lat_ensmn_timeanom_c6sd[iexpt]
    plt.plot(year[iscenario_start:], middle[iscenario_start:], color=color_c6[iexpt+1], label='CMIP6 {:s}'.format(experiments_cmip6[iexpt]), lw=lw1)
#     if expt == 'ssp585':
#         plt.fill_between(year[iscenario_start:], mini[iscenario_start:], maxi[iscenario_start:], color=color_c6[iexpt+1], alpha=alpha)

plt.xlim(xlim)
plt.ylim(ylim)
plt.axhline(0, linestyle=':', color='k')
for yy in years_list:
    plt.axvline(yy, color='k', linestyle=':')
plt.title('Multi-model mean AMOC anomaly at {:.1f}N, 1000m in CMIP5 and CMIP6 ensembles'.format(target_lat), fontsize=fontsize)
plt.legend(loc=3, ncol=3, fontsize=fontsize*0.8)
plt.xticks(fontsize=fontsize)
plt.yticks(fontsize=fontsize)
plt.ylabel('AMOC anomaly [Sv]', fontsize=fontsize)
plt.xlabel('Model year', fontsize=fontsize)
plt.show()
