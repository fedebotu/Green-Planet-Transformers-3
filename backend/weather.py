import numpy as np
import matplotlib.pyplot as plt
import h5py

# [MP] Fixed latitude and longitude range for ERA5 data
LAT_RANGE = np.linspace(90, -90, 721)
LONG_RANGE = np.linspace(-180, 180, 1440)


def get_closest_pixel(lat, lon, lats=LAT_RANGE, longs=LONG_RANGE):
    """
    Given a latitude and longitude, return the closest pixel
    Get the closest pixel (best way would be to interpolate - TODO)
    """
    lat_idx = np.argmin(np.abs(lats - lat))
    long_idx = np.argmin(np.abs(longs - (lon + 180)))
    return lat_idx, long_idx


def get_weather_data(weather_data_dir, lat, lon):
    """
    'u10': '10 meter U wind component [m/s]',
    'v10': '10 meter V wind component [m/s]',
    't2m': '2 meter temperature [K]',
    'sp': 'Surface pressure [Pa]',
    'mslp': 'Mean sea level pressure [Pa]',
    't850': 'Temperature at 850 hPa [K]',
    'u1000': '1000 meter U wind component [m/s]',
    'v1000': '1000 meter V wind component [m/s]',
    'z1000': '1000 meter geopotential [m^2/s^2]',
    'u850': '850 meter U wind component [m/s]',
    'v850': '850 meter V wind component [m/s]',
    'z850': '850 meter geopotential [m^2/s^2]',
    'u500': '500 meter U wind component [m/s]',
    'v500': '500 meter V wind component [m/s]',
    'z500': '500 meter geopotential [m^2/s^2]',
    't500': 'Temperature at 500 hPa [K]',
    'z50': '50 meter geopotential [m^2/s^2]',
    'r500': 'Relative humidity at 500 hPa [%]',
    'r850': 'Relative humidity at 850 hPa [%]',
    'tcwv': 'Total column water vapour [kg/m^2]',
    'sst': 'Sea surface temperature [K]'
    """
    # get the closest pixel
    lat_idx, lon_idx = get_closest_pixel(lat, lon)
    time_idx = 0 # [MP] TODO: identify what time
    # the request is actually about! Right now we take
    # the first index (t=0) as dummy data.

    f = h5py.File(weather_data_dir / 'single_week.h5', 'r')

    raw_variables = ''
    time_series = []
    for var in f.keys():
        # add to prompt with value
        if var in ['u10', 'v10', 'sp', 't2m', 'r850', 'mslp', 't850', 'u1000', \
            'v1000', 'z1000', 'u850', 'v850', 'z850', 'u500', 'v500', 'z500', 't500', \
                'z50', 'r500', 'tcwv']:
            raw_variables += f[var].attrs['description'] + " is: {:.2f} \n".format(f[var][time_idx, lat_idx, lon_idx])
            time_series.append(f[var][:, lat_idx, lon_idx])

    return raw_variables, time_series


def get_better_weather_data(weather_data_dir, lat, lon):
    target_variables = ['u10', 'v10', 't2m', 'tp', 'r850', 'sp']

    # build dictionary of the above with their description and units in square brackets
    # U wind component = eastward wind 
    # V wind component = northward wind
    variables = {'u10': 'Eastward wind  [km/h]',
                'v10': 'Northward wind [km/h]',
                't2m': 'Surface temperature [°C]',
                'tp': 'Total precipitation [mm]',
                'r850': 'Relative humidity [%]',
                'sp': 'Surface pressure [hPa]'}

    # Convert from m/s to km/h, and kelvin to celsius
    conversion_factors = {  'u10': {'factor': 3.6, 'offset': 0},
                            'v10': {'factor': 3.6, 'offset': 0},
                            't2m': {'factor': 1, 'offset': -273.15},
                            'tp': {'factor': 1, 'offset': 0},
                            'r850': {'factor': 1, 'offset': 0},
                            'sp': {'factor': 0.01, 'offset': 0}}

    def rescale(x, var):
        return x * conversion_factors[var]['factor'] + conversion_factors[var]['offset']

    # get the closest pixel
    lat_idx, lon_idx = get_closest_pixel(lat, lon)
    time_idx = 0 # [MP] TODO: identify what time
    # the request is actually about! Right now we take
    # the first index (t=0) as dummy data.

    f = h5py.File(weather_data_dir / 'single_week.h5', 'r')

    raw_variables = ''
    time_series = {}
    for var in f.keys():
        # add to prompt with value
        if var in target_variables:
            raw_variables += "{} is {:.1f}\n".format(variables[var], rescale(f[var][time_idx, lat_idx, lon_idx], var))
            time_series[var] = rescale(f[var][:, lat_idx, lon_idx], var)

    return raw_variables, time_series



def plot_weather_time_series(time_series):
    u, v, temp = time_series['u10'], time_series['v10'], time_series['t2m']

    plt.rc('font', family='serif')
    
    # 16 font size
    plt.rcParams.update({'font.size': 18})

    fig, axs = plt.subplots(2,1, figsize=(12, 6))
    axs[0].scatter(np.arange(28), np.sqrt(u**2 + v**2), c='b', s=100, marker='2')
    axs[0].set_title('Wind Speed [km/h]')
    axs[0].set_xticks([0, 4, 8, 12, 16, 20, 24, 28])
    axs[0].set_xticklabels(['0', '1', '2', '3', '4', '5', '6', '7'])

    axs[1].scatter(np.arange(28), temp, c='r', s=100, marker='2')
    axs[1].set_title('Temperature [C]')
    axs[1].set_xticks([0, 4, 8, 12, 16, 20, 24, 28])
    axs[1].set_xticklabels(['0', '1', '2', '3', '4', '5', '6', '7'])

    plt.tight_layout()
    return fig