import pandas as pd

INPUT_FILE = "2020.csv"
OUTPUT_FILE = "2020_refactored.csv"

df = pd.read_csv(INPUT_FILE, sep=";", decimal=",")

# --- 1. Parse "1.1. 00:00:00" format ---
df["Time period"] = pd.to_datetime(
    df["Time period"],
    format="%d.%m. %H:%M:%S",
    errors="coerce"
)

# --- 2. Insert year 2020 ---
df["Time period"] = df["Time period"].apply(
    lambda t: t.replace(year=2020) if pd.notnull(t) else t
)

# --- 3. Apply timezone BEFORE formatting ---
df["Time period"] = df["Time period"].dt.tz_localize(
    "Europe/Helsinki",
    ambiguous="infer",
    nonexistent="shift_forward"
)


# --- 4. Format exactly as desired ---
df["Time period"] = df["Time period"].dt.strftime("%Y-%m-%dT%H:%M:%S.000%z")

# Insert colon into +0200 → +02:00
df["Time period"] = df["Time period"].str.replace(
    r"(\+|−)(\d{2})(\d{2})",
    r"\1\2:\3",
    regex=True
)

# ---- Consumption ---
df["Consumption (net) kWh"] = (
    df["Average power, day"].fillna(0) +
    df["Average power, night"].fillna(0)
)

# ---- Production empty ----
df["Production (net) kWh"] = 0

# ---- Temperature stays as-is ----

final_df = df[[
    "Time period",
    "Consumption (net) kWh",
    "Production (net) kWh",
    "Temperature"
]]

final_df.to_csv(OUTPUT_FILE, sep=";", index=False, decimal=",")

print("Refactored file saved:", OUTPUT_FILE)