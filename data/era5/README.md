# ERA5 Dataset

`single_week.h5` contains single week data we can use for our project: this is data from `fourcastnet`. It is historical data (Nov 2018) since ERA5 is not available in a preprocessed format in real time.

## Data

We use the data from the [FOURCASTNET paper](https://arxiv.org/abs/2202.11214) downloaded from the [Copernicus insitute](https://cds.climate.copernicus.eu/). The data is as follows:

| Levels     | Variables               |
| ---------- | ----------------------- |
| Surface    | U10, V10, T2m, sp, mlsp |
| 1000hPa    | U, V, Z                 |
| 850hPa     | T, U, V, Z, RH          |
| 500hPa     | T, U, V, Z, RH          |
| 50hPa      | Z                       |
| Integrated | TCWV                    |

> Note: there is also the extra variable of `tp` (total precipitation) included in the H5 files, although it has a slightly different format.

These are downloaded from 2 datasets:

1. Surface and Integrated: [ERA5 Single Levels](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=form)
2. Pressure (hPa): [ERA5 Pressure Levels](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=form)

Total estimated weight: ~5TB

### Variables description

<details close>
<summary>U10: 10m u-component of wind </summary>
[m s-1]

> This parameter is the eastward component of the 10m wind. It is the horizontal speed of air moving towards the east, at a height of ten metres above the surface of the Earth, in metres per second. Care should be taken when comparing this parameter with observations, because wind observations vary on small space and time scales and are affected by the local terrain, vegetation and buildings that are represented only on average in the ECMWF Integrated Forecasting System (IFS). This parameter can be combined with the V component of 10m wind to give the speed and direction of the horizontal 10m wind.

</details>

<details close>
<summary>V10: 10m v-component of wind </summary>
[m s-1]

> This parameter is the northward component of the 10m wind. It is the horizontal speed of air moving towards the north, at a height of ten metres above the surface of the Earth, in metres per second. Care should be taken when comparing this parameter with observations, because wind observations vary on small space and time scales and are affected by the local terrain, vegetation and buildings that are represented only on average in the ECMWF Integrated Forecasting System (IFS). This parameter can be combined with the U component of 10m wind to give the speed and direction of the horizontal 10m wind.

</details>

<details close>
<summary>T2m: 2m temperature</summary>
[K]

> This parameter is the temperature of air at 2m above the surface of land, sea or inland waters. 2m temperature is calculated by interpolating between the lowest model level and the Earth's surface, taking account of the atmospheric conditions. This parameter has units of kelvin (K). Temperature measured in kelvin can be converted to degrees Celsius (°C) by subtracting 273.15.

</details>

<details close>
<summary>mslp: Mean sea level pressure	</summary>
[Pa]

> This parameter is the pressure (force per unit area) of the atmosphere at the surface of the Earth, adjusted to the height of mean sea level. It is a measure of the weight that all the air in a column vertically above a point on the Earth's surface would have, if the point were located at mean sea level. It is calculated over all surfaces - land, sea and inland water. Maps of mean sea level pressure are used to identify the locations of low and high pressure weather systems, often referred to as cyclones and anticyclones. Contours of mean sea level pressure also indicate the strength of the wind. Tightly packed contours show stronger winds. The units of this parameter are pascals (Pa). Mean sea level pressure is often measured in hPa and sometimes is presented in the old units of millibars, mb (1 hPa = 1 mb = 100 Pa).

</details>

<details close>
<summary>sp: Surface pressure</summary>
[Pa]

> This parameter is the pressure (force per unit area) of the atmosphere at the surface of land, sea and inland water. It is a measure of the weight of all the air in a column vertically above a point on the Earth's surface. Surface pressure is often used in combination with temperature to calculate air density. The strong variation of pressure with altitude makes it difficult to see the low and high pressure weather systems over mountainous areas, so mean sea level pressure, rather than surface pressure, is normally used for this purpose. The units of this parameter are Pascals (Pa). Surface pressure is often measured in hPa and sometimes is presented in the old units of millibars, mb (1 hPa = 1 mb= 100 Pa).

</details>

<details close>
<summary>TCWV: Total column water vapour</summary>
[kg m-2]

> This parameter is the total amount of water vapour in a column extending from the surface of the Earth to the top of the atmosphere. This parameter represents the area averaged value for a grid box.

</details>

<details close>
<summary>U: U-component of wind</summary>
[m s-1]

> This parameter is the eastward component of the wind. It is the horizontal speed of air moving towards the east. A negative sign indicates air moving towards the west. This parameter can be combined with the V component of wind to give the speed and direction of the horizontal wind.

</details>

<details close>
<summary>V: V-component of wind	</summary>
[m s-1]

> This parameter is the northward component of the wind. It is the horizontal speed of air moving towards the north. A negative sign indicates air moving towards the south. This parameter can be combined with the U component of wind to give the speed and direction of the horizontal wind.

</details>

<details close>
<summary>Z: Geopotential	</summary>
[m2 s-2]

> This parameter is the gravitational potential energy of a unit mass, at a particular location, relative to mean sea level. It is also the amount of work that would have to be done, against the force of gravity, to lift a unit mass to that location from mean sea level. The geopotential height can be calculated by dividing the geopotential by the Earth's gravitational acceleration, g (=9.80665 m s-2). The geopotential height plays an important role in synoptic meteorology (analysis of weather patterns). Charts of geopotential height plotted at constant pressure levels (e.g., 300, 500 or 850 hPa) can be used to identify weather systems such as cyclones, anticyclones, troughs and ridges. At the surface of the Earth, this parameter shows the variations in geopotential (height) of the surface, and is often referred to as the orography.

</details>

<details close>
<summary>RH: Relative humidity	</summary>
[%]

> This parameter is the water vapour pressure as a percentage of the value at which the air becomes saturated (the point at which water vapour begins to condense into liquid water or deposition into ice). For temperatures over 0°C (273.15 K) it is calculated for saturation over water. At temperatures below -23°C it is calculated for saturation over ice. Between -23°C and 0°C this parameter is calculated by interpolating between the ice and water values using a quadratic function.

</details>

## Accounts

We just need the API key, so the email is not important

Steps:

1. Email account creation: [https://temp-mail.org/](https://temp-mail.org/)
   **Note:** you need to use a VPN or use other browser for a new address
2. Create new CDS account: [https://cds.climate.copernicus.eu/user/register](https://cds.climate.copernicus.eu/user/register)
3. Accept terms: [https://cds.climate.copernicus.eu/cdsapp/#!/terms/licence-to-use-copernicus-products](https://cds.climate.copernicus.eu/cdsapp/#!/terms/licence-to-use-copernicus-products)
4. Get API key: [https://cds.climate.copernicus.eu/api-how-to](https://cds.climate.copernicus.eu/api-how-to)
