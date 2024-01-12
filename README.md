# README

## Citation: Aerosol-forced AMOC change in CMIP6 historical simulations.
Matthew Menary, Jon Robson, Richard Allan, Ben Booth, Christophe Cassou, Guillaume Gastineau, Jonathan Gregory, Dan Hodson, Colin Jones, Juliette Mignot, Mark Ringer, Rowan Sutton, Laura Wilcox, Rong Zhang

https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2020GL088166

![Figure_AR6_CMIP5-6_AMOC_35N_1000m_Anom-1s d Shaded](https://github.com/mattofficeuk/AR6/assets/39481661/b7d138ab-7783-4f65-b6b0-8e1935073434)

**Data updated: 14th May 2020.** Details:

1) Improved method of calculating the AMOC, by summing upwards from the ocean bottom
2) Improved method of calculating the AMOC, by computing a more precise zonal integral
3) Added more models

This data was processed by Matthew Menary matthew.menary@locean.ipsl.fr

See **PLOTTING_CMIP5-6.py** and **PLOTTING_DAMIP.py** in the **Code** folder for how we plotted this data

This repository contains the processed AMOC index data, along with various verification plots. We use the v-velocities rather than the stream function variable(s), and we end up with a temporally constant offset between our AMOC indices and those derived from the actual streamfunctions. As such, it only makes sense to look at temporal anomalies. The reason for this offset is unclear but likely the result of having to make assumptions on grid-cell widths/heights and masking choices in order to use the v-velocities (not all of this data is uploaded to the CMIP archive). The reason for using the v-velocities is that there are many more models available that way.

A comparison of the two methods for the models that have all the data can be seen in the **Method_Comparison** folder.

Raw time series and time-mean streamfunctions (issues above notwithstanding) of all the data can be seen in the **Verification_Plots** folder.

The data is stored in two versions. Python pickle files in the **pickle_data** folder, and JSON files in the **JSON_data** folder. The following guide assumes use of the *pickle* data. The *JSON* data is the same except stored as a dictionary rather than a list.

### Data file 1: Figure_AR6_CMIP5-6_AMOC_35N_1000m.pkl
(see bottom of README for DAMIP instructions)

This python pickle file was created using Python2.7. It contains a list of 5 variables. The first is the AMOC index in CMIP5 models. The second is the AMOC index in CMIP6 models. The third is a list of the CMIP5 models, which correspond to the same indices as in the AMOC array. The fourth is the same but for CMIP6. The fifth is the year (all data is annual mean values).

**The AMOC arrays are masked-arrays, with missing models/ensemble-members/years masked. When manipulating them, always ensure to use masked array-compatible operations**

It can be read into Python2.7 by doing:

```
with open ('Figure_AR6_CMIP5-6_AMOC_35N_1000m.pkl') as handle:
  amoc_c5_ts, amoc_c6_ts, cmip5_models, cmip6_models, year = pickle.load(handle)
```

If using the *JSON* data then the following will read the data into the same format:

```
with open('Figure_AR6_CMIP5-6_AMOC_35N_1000m.json', 'r') as handle:
    json_load = json.load(handle)

amoc_c5_ts = np.ma.asarray(json_load["amoc_c5_ts"])  # Note the use of numpy masked arrays (np.ma)
amoc_c6_ts = np.ma.asarray(json_load["amoc_c6_ts"])
cmip5_models = json_load["cmip5_models"]
cmip6_models = json_load["cmip6_models"]
year = np.asarray(json_load["year"])
```

The AMOC variables have the following shape: [models, experiments, ensemble-members, latitudes, time]

#### Models:
See lists (variables 3 and 4)

#### Experiments:
```
experiments_cmip5 = ['rcp45', 'rcp85']
experiments_cmip6 = ['ssp119', 'ssp126', 'ssp245', 'ssp370', 'ssp585']
```

Note: All scenario experiments also contain the historical data. Where there was an overlap between historical or scenario data for some reason, we chose the scenario data. For example, to plot the "historical" experiment in CMIP5, just plot the first ~150 years of the array. Reminder: Scenarios begin in 2005 for CMIP5 and 2015 for CMIP6.

#### Ensemble members:
These are the first 10 ensemble members r${ens_num}i1p1f1 in the respective experiments. Where "f1" was not available we have used "f2" or "f3" and so on.

#### Latitudes:
26.5N (index 0) or 35N (index 1)

#### Time:
The simulated year, from 1850 to 2100 inclusive

### Method:
```
To create the figure: Figure_AR6_CMIP5-6_AMOC_35N_1000m_Anom-1s.d.Shaded.png we followed the following algorithm:
1) Choose latitude
2) Compute initial-condition ensemble mean for each model
3) Construct temporal anomaly (over all remaining dimensions)
4a) Compute multimodel mean
4b) Compute multimodel standard deviation
```

Pseudo-code for the Method is provided below:

```
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
```

### Data file 2: Figure_AR6_DAMIP_AMOC_26N_1000m.pkl

This data is structurally the same as the CMIP5/6 historical/scenario data above, except for:

To read in (to Python2.7):

```
with open ('Figure_AR6_DAMIP_AMOC_26N_1000m.pkl') as handle:
  amoc_damip6_ts, damip6_models, year = pickle.load(handle)
```


If using the *JSON* data then the following will read the data into the same format:

```
with open('Figure_AR6_DAMIP_AMOC_26N_1000m.json', 'r') as handle:
    json_load = json.load(handle)

amoc_damip6_ts = np.ma.asarray(json_load["amoc_damip6_ts"])  # Note the use of numpy masked arrays (np.ma)
damip6_models = json_load["damip6_models"]
year = np.asarray(json_load["year"])
```

### Experiments:
```experiments_damip6 = ['historical', 'hist-aer', 'hist-GHG', 'hist-nat', 'hist-stratO3']```

Pseudo-code:

```
ilat_choice = 0

y0, y1 = 1860, 1880
t0 = np.argwhere(year == y0)[0][0]
t1 = np.argwhere(year == y1)[0][0]

amoc_damip6_ts_lat = amoc_damip6_ts[:, :, :, ilat_choice, :]
amoc_damip6_ts_lat_ensmn = amoc_damip6_ts_lat.mean(axis=2)
amoc_damip6_ts_lat_ensmn_timeanom = anomalise3d(amoc_damip6_ts_lat_ensmn, t0, t1)
amoc_damip6_ts_lat_ensmn_timeanom_mmm = amoc_damip6_ts_lat_ensmn_timeanom.mean(axis=0)
amoc_damip6_ts_lat_ensmn_timeanom_mmsd = amoc_damip6_ts_lat_ensmn_timeanom.std(axis=0)
```

### Acknowledgement

We acknowledge the World Climate Research Programme, which, through its Working Group on Coupled Modelling, coordinated and promoted CMIP6. We thank the climate modeling groups for producing and making available their model output, the Earth System Grid Federation (ESGF) for archiving the data and providing access, and the multiple funding agencies who support CMIP6 and ESGF.

### License

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0
International License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg
