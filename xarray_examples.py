
import xarray as xr
import seaborn as sns
import pandas as pd
import bottleneck as bn
from pylab import *

plt.ion()
user = 'xarray'


def open_xarray(exp='xpptut15', run=261, user=user):
    """
    Open xarray dataset
    """
    instrument = exp[0:3]
    path = '/reg/d/psdm/{:}/{:}/scratch/{:}'.format(instrument, exp, user)
    h5file = '{:}/run{:04}.nc'.format(path, run)
    return xr.open_dataset(h5file, engine='h5netcdf')


def groupby_stats(x, attr='ebeam_photon_energy', drop=False,
                  groupby='evr_code_141', stats=['mean', 'std', 'min', 'max'], dataframe=False):
    """
    Compare stats of attr after groupby another attribute. 
    """
    if drop:
        dag = x[attr].dropna(dim='time').groupby(groupby)
        print("dag = x['{:}'].dropna(dim='time').groupby('{:}')".format(attr, groupby))
    else:
        dag = x[attr].groupby(groupby)
        print("dag = x['{:}'].groupby('{:}')".format(attr, groupby))

    if dataframe:
        df = pd.DataFrame({stat: getattr(dag, stat)() for stat in ['mean', 'std', 'min', 'max']})
        print("df = pd.DataFrame({stat: getattr(dag, stat)() for stat in ['mean', 'std', 'min', 'max']})")
        return df
    else:
        da = xr.Dataset({stat: getattr(dag, stat)() for stat in ['mean', 'std', 'min', 'max']})
        print("da = xr.Dataset({stat: getattr(dag, stat)() for stat in ['mean', 'std', 'min', 'max']})")
        return da


def plot_groupby(x, attr='ebeam_photon_energy', groupby='step'):
    """
    Groupby step and plot.
    """
    dag = x[attr].dropna(dim='time').groupby(groupby)
    dag.mean().to_pandas().plot(yerr=dag.std())
    print("dag = x['{:}'].dropna(dim='time').groupby('{:}')".format(attr, groupby))
    print("dag.mean().to_pandas().plot(yerr=dag.std())")


def plot_rolling(x, attr='gas_detector_f_22_ENRC', ntime=100, cut=None):
    """
    Plot gas detector data points with time 
    Then over plot rolling mean with thick grean line
    Rolling method uses bottlneck to speed up calculation
    """
    if cut:
        da = x[attr].where(x[cut]).dropna(dim='time')
        print("da = x['{:}'].where(x['{:}']).dropna(dim='time')".format(attr, cut))
    else:
        da = x[attr]
        print("da = x['{:}']".format(attr))
    print("fig = da.plot(marker='.',linestyle='')")
    print("da.rolling(time={:}).mean().plot(color='g',linewidth=5)".format(ntime))
    fig = da.plot(marker='.', linestyle='')
    da.rolling(time=ntime).mean().plot(color='g', linewidth=5)


def describe(x, attrs, percentiles=[0.05, 0.5, 0.95]):
    """
    Use pandas describe method to build stats summary table
    """
    return x[attrs].to_dataframe().describe(percentiles=percentiles).T


def make_cuts(x, attrs, name='valid_cut', percentiles=[0.05, 0.95], sigma=2):
    """
    Make cuts on data
    """
    df = x.reset_coords()[attrs].to_dataframe()
    df_tbl = df.describe(percentiles=percentiles).T
    minp = int(min(percentiles) * 100)
    maxp = int(max(percentiles) * 100)
    dfcut = (df > df_tbl['{:}%'.format(minp)] - sigma * df_tbl['std']).all(axis=1) \
            & (df < df_tbl['{:}%'.format(maxp)] + sigma * df_tbl['std']).all(axis=1)
    x[name] = dfcut
    print("attrs = {:}".format(attrs))
    print("percentiles = {:}".format(percentiles))
    print("sigma = {:}".format(sigma))
    print("df = x.reset_coords()[attrs].to_dataframe()")
    print("df_tbl = df.describe(percentiles=percentiles).T")
    print("minp = int(min(percentiles)*100)")
    print("maxp = int(max(percentiles)*100)")
    print(
        "dfcut = (df > df_tbl['{:}%']-sigma*df_tbl['std']).all(axis=1) & (df < df_tbl['{:}%']+sigma*df_tbl['std']).all(axis=1)".format(
            minp, maxp))
    print("x['{:}'] = dfcut".format(name))

    return dfcut


def heatmap(x, attrs):
    """
    Use pandas and seaborn to make heatmap of correlations.
    """
    corr = x.reset_coords()[attrs].to_dataframe().corr(method='pearson')
    sns.heatmap(corr, annot=True)
    print("corr = x.reset_coords()[attrs].to_dataframe().corr(method='pearson')")
    print("sns.heatmap(corr,annot=True)")
    return corr


def scatter_plot(x, attrs, cut=None):
    """
    Use pandas and seaborn to make a scatter plot.
    """
    if cut is None:
        dfscat = x.reset_coords()[attrs].to_dataframe()
        print("dfscat = x.reset_coords()[attrs].to_dataframe()")
    else:
        dfscat = x[attrs].where(cut, drop=True).reset_coords()[attrs].to_dataframe()
        print("dfscat = x[attrs].where(cut, drop=True).reset_coords()[attrs].to_dataframe()")

    g = sns.PairGrid(dfscat, diag_sharey=False)
    g.map_lower(sns.kdeplot, cmap="Blues_d")
    g.map_upper(plt.scatter)
    g.map_diag(sns.kdeplot, lw=3)


def get_attrs(x, det=None):
    """
    Helper function to get scalar attributes for an optionally provided detector
    """
    if det:
        attrs = [a for a in x.data_vars if a.startswith(det) and x[a].dims == ('time',)]
    else:
        attrs = [a for a in x.data_vars if x[a].dims == ('time',)]

    return attrs
