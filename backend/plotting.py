import numpy as np
import pandas as pd
import pydeck as pdk
import h5py
import matplotlib.pyplot as plt
import datetime

from backend.geoloc import get_closest_pixel, get_closest_idxs


def make_closest_data_df(lat, lon, data, num_pixels=100, **kwargs):
    """
    Given a 2D array, get the data around a given location with a given number of pixels.
    """
    lats = np.linspace(90, -90, 721)
    longs = np.linspace(-180, 180, 1440)
    lat_idx, lon_idx = get_closest_pixel(lat, lon)
    lat_idxs, lon_idxs = get_closest_idxs(lat_idx, lon_idx, num_pixels, **kwargs)

    # Get coordinates of the data we cropped
    lats_sf = lats[lat_idxs]
    longs_sf = longs[lon_idxs]

    # Make meshgrid
    lats_sf, longs_sf = np.meshgrid(lats_sf, longs_sf)
    return pd.DataFrame({   'z': data[lat_idxs, :][:, lon_idxs].flatten(), 
                            'latitude': lats_sf.flatten(), 
                            'longitude': longs_sf.flatten() - 180}) # offset


def interactive_plot(lat, lon, time_idx=0, datadir='data/era5', **kwargs):
    """Given data with latitude, longitude and data plot it interactively with pydeck"""

    f = h5py.File(datadir + '/single_week.h5', 'r')
    data = f['tp'][time_idx] # NOTE: modify time_idx in main
    data = make_closest_data_df(lat, lon, data, **kwargs)

    # plot in streamlit
    return pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=data['latitude'].mean(),
            longitude=data['longitude'].mean(),
            zoom=3.5,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'HeatmapLayer',
                data=data,
                get_position= ["longitude", "latitude"],
                # radius=200,
                # elevation_scale=4,
                aggregation=pdk.types.String("MEAN"),
                get_weight='z',
                # elevation_range=[0, 1000],
                pickable=True,
                # extruded=True,
                opacity=0.3,
            ),
        ],
    )


def plot_weather_time_series(time_series):
    u, v, temp = time_series['u10'], time_series['v10'], time_series['t2m']

    plt.rc('font', family='serif')

    # 16 font size
    plt.rcParams.update({'font.size': 18})

    fig, axs = plt.subplots(2,1, figsize=(12, 6))
    axs[0].scatter(np.arange(28), np.sqrt(u**2 + v**2), c='b', s=100, marker='2')
    axs[0].set_title('Wind Speed [km/h]')
    axs[0].set_xticks([0, 4, 8, 12, 16, 20, 24, 28])

    # set labels as number of days from now
    timenow = datetime.datetime.now()
    labels = [timenow + datetime.timedelta(days=i) for i in range(0, 8, 1)]
    labels = [label.strftime('%b-%d') for label in labels]
    axs[0].set_xticklabels(labels)

    axs[1].scatter(np.arange(28), temp, c='r', s=100, marker='2')
    axs[1].set_title('Temperature [C]')
    axs[1].set_xticks([0, 4, 8, 12, 16, 20, 24, 28])
    axs[1].set_xticklabels(labels)
    # axs[1].set_xticklabels(['0', '1', '2', '3', '4', '5', '6', '7'])

    plt.tight_layout()
    return fig
    



if __name__ == "__main__":
    lat = 37.7749
    lon = -122.4194
    data = np.random.rand(721, 1440)
    df = make_closest_data_df(lat, lon, data, num_pixels=100)
    print(df.head())
