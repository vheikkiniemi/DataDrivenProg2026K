import pandas as pd
from pathlib import Path

# ----- File paths (edit these) -----
energy_path = Path("2025.csv")         # Your energy CSV with semicolons and comma decimals
weather_path = Path("2025_weather.csv")       # Your weather CSV with commas and dot decimals
output_path = Path("2025_energy_with_temp.csv")
import pandas as pd

# ---- Read energy file (semicolon + comma decimals) ----
df_energy = pd.read_csv(
    energy_path,
    sep=';',
    decimal=',',
    dtype=str
)
df_energy = df_energy.iloc[:, :-1]


# ---- Read weather file (comma + dot decimals) ----
df_weather = pd.read_csv(
    weather_path,
    sep=',',
    decimal='.',
    dtype=str
)

# ---- Copy weather temperature into energy ----
temperature_column = "Lämpötilan keskiarvo [°C]"

# Overwrite the existing temperature column
df_energy["Daily average temperature"] = df_weather[temperature_column]



# Convert decimal dot → comma for output
df_energy["Daily average temperature"] = (
    df_energy["Daily average temperature"].str.replace('.', ',', regex=False)
)



# ---- Save cleaned output (no duplicate columns) ----
df_energy.to_csv(output_path, sep=';', index=False)
print(df_energy)
print("Done — updated file saved as:", output_path)
