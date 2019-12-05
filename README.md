README

Citation: Aerosol forced AMOC variability in CMIP6 historical simulations.
Matthew Menary, Jon Robson et al. (Submitted to GRL, December 2019)

This repository contains the processed AMOC index data, along with various verification plots.

This data was processed by Matthew Menary matthew.menary@locean-ipsl.upmc.fr

See PLOTTING.md for how I plotted this data

Data file 1:
**Figure_AR6_CMIP5-6_AMOC_35N_1000m.pkl**
(see bottom of README for DAMIP instructions)

This python pickle file was created using Python2.7. It contains a list of 5 variables. The first is the AMOC index in CMIP5 models. The second is the AMOC index in CMIP6 models. The third is a list of the CMIP5 models, which correspond to the same indices as in the AMOC array. The fourth is the same but for CMIP6. The fifth is the year (all data is annual mean values).

It can be read into Python2.7 by doing:

with open ('Figure_AR6_CMIP5-6_AMOC_35N_1000m.pkl') as handle:
  amoc_c5_ts, amoc_c6_ts, cmip5_models, cmip6_models, year = pickle.load(handle)
  
The AMOC variables have the following shape: [models, experiments, ensemble-members, latitudes, time]

Models:
See lists (variables 3 and 4)

Experiments:
experiments_cmip5 = ['rcp45', 'rcp85']
experiments_cmip6 = ['ssp119', 'ssp126', 'ssp245', 'ssp370', 'ssp585']

Note: All scenario experiments also contain the historical data. Where there was an overlap between historical or scenario data for some reason, I chose the scenario data. For example, to plot the "historical" experiment in CMIP5, just plot the first ~150 years of the array. Reminder: Scenarios begin in 2005 for CMIP5 and 2015 for CMIP6.

Ensemble members:
These are the first 10 ensemble members r${ens_num}i1p1f1 in the respective experiments. Where "f1" was not available I have used "f2" or "f3" and so on.

Latitudes:
26.5N (index 0) or 35N (index 1)

Time:
The simulated year, from 1850 to 2100 inclusive

Method:
To create the figure: Figure_AR6_CMIP5-6_AMOC_35N_1000m_Anom-1s.d.Shaded.png I followed the following algorithm:
1) Choose latitude
2) Compute initial-condition ensemble mean for each model
3) Construct temporal anomaly (over all remaining dimensions)
4a) Compute multimodel mean
4b) Compute multimodel standard deviation

Pseudo-code for the Method is provided below:

ilat_choice = 1

def anomalise3d(in_arr, t0, t1):
    time_mean = in_arr[:, :, t0:t1].mean(axis=2)
    time_mean_repl = np.repeat(time_mean[:, :, None], nt, axis=2)
    anom = in_arr - time_mean_repl
    return anom

y0, y1 = 1860, 1880
t0 = np.argwhere(year == y0)[0][0]
t1 = np.argwhere(year == y1)[0][0]

amoc_c5_ts_lat = amoc_c5_ts[:, :, :, ilat_choice, :]

amoc_c5_ts_lat_ensmn = amoc_c5_ts_lat.mean(axis=2)

amoc_c5_ts_lat_ensmn_timeanom = anomalise3d(amoc_c5_ts_lat_ensmn, t0, t1)

amoc_c5_ts_lat_ensmn_timeanom_c5mn = amoc_c5_ts_lat_ensmn_timeanom.mean(axis=0)

amoc_c5_ts_lat_ensmn_timeanom_c5sd = amoc_c5_ts_lat_ensmn_timeanom.std(axis=0)

Data file 2:
**Figure_AR6_DAMIP_AMOC_26N_1000m.pkl**

This data is structurally the same as the CMIP5/6 historical/scenario data above, except for:

To read in (to Python2.7):

with open ('Figure_AR6_DAMIP_AMOC_26N_1000m.pkl') as handle:
  amoc_damip6_ts, damip6_models, year = pickle.load(handle)
  
Experiments:
experiments_damip6 = ['historical', 'hist-aer', 'hist-GHG', 'hist-nat', 'hist-stratO3']

Pseudo-code:

ilat_choice = 0

y0, y1 = 1860, 1880
t0 = np.argwhere(year == y0)[0][0]
t1 = np.argwhere(year == y1)[0][0]

amoc_damip6_ts_lat = amoc_damip6_ts[:, :, :, ilat_choice, :]

amoc_damip6_ts_lat_ensmn = amoc_damip6_ts_lat.mean(axis=2)

amoc_damip6_ts_lat_ensmn_timeanom = anomalise3d(amoc_damip6_ts_lat_ensmn, t0, t1)

amoc_damip6_ts_lat_ensmn_timeanom_mmm = amoc_damip6_ts_lat_ensmn_timeanom.mean(axis=0)

amoc_damip6_ts_lat_ensmn_timeanom_mmsd = amoc_damip6_ts_lat_ensmn_timeanom.std(axis=0)
  
