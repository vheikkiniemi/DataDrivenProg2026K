import io
import os
from typing import List
import pandas as pd
import streamlit as st

# -----------------------------------------------------
# Configuration
# -----------------------------------------------------
st.set_page_config(
    page_title="Daily Temperature Range Finder",
    page_icon="🌡️",
    layout="wide",
)

st.title("🌡️ Daily Temperature & Consumption Finder")
st.caption("Automatically loading energy + temperature data from 2016–2025 CSV files.")

YEAR_FILES = [
    "2016_energy_with_temp.csv",
    "2017_energy_with_temp.csv",
    "2018_energy_with_temp.csv",
    "2019_energy_with_temp.csv",
    "2020_energy_with_temp.csv",
    "2021_energy_with_temp.csv",
    "2022_energy_with_temp.csv",
    "2023_energy_with_temp.csv",
    "2024_energy_with_temp.csv",
    "2025_energy_with_temp.csv",
]

# -----------------------------------------------------
# Helper functions
# -----------------------------------------------------

@st.cache_data(show_spinner=False)
def _read_one_csv(filepath: str) -> pd.DataFrame:
    """Reads one CSV file with EU-style separators and extracts:
       - daily average temperature
       - daily consumption (sum of hourly consumption)
    """
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            df = pd.read_csv(
                filepath,
                sep=";",
                decimal=",",
                encoding=enc,
                engine="python",
            )
            break
        except Exception:
            df = None
    if df is None:
        raise ValueError(f"Could not read {filepath}")

    # Normalize columns
    df.columns = [" ".join(str(c).split()).strip() for c in df.columns]

    # Time column
    time_col = next((c for c in df.columns if "time" == c.lower() or "time" in c.lower()), None)
    if not time_col:
        raise ValueError("Time column not found")

    # Temperature column
    temp_col = next(
        (c for c in df.columns if c.lower().strip() == "daily average temperature"
         or "temperature" in c.lower()),
        None
    )
    if not temp_col:
        raise ValueError("Temperature column not found")

    # Consumption column
    cons_col = next(
        (c for c in df.columns if "consumption" in c.lower() and "kwh" in c.lower()),
        None
    )
    if not cons_col:
        raise ValueError("Consumption (net) kWh column not found")

    # Parse datetime
    t = pd.to_datetime(df[time_col], errors="coerce", utc=True)
    try:
        t_local = t.dt.tz_convert("Europe/Helsinki")
    except Exception:
        t_local = t.dt.tz_localize("Europe/Helsinki")

    df["date_local"] = t_local.dt.date

    # Convert numeric values
    df[temp_col] = pd.to_numeric(df[temp_col], errors="coerce")
    df[cons_col] = pd.to_numeric(df[cons_col], errors="coerce")

    # Group daily values
    daily = df.groupby("date_local").agg(
        daily_temp_c=(temp_col, "mean"),
        daily_consumption_kwh=(cons_col, "sum"),
    ).reset_index()

    return daily


@st.cache_data(show_spinner=True)
def load_all_years() -> pd.DataFrame:
    frames = []
    for filename in YEAR_FILES:
        if not os.path.exists(filename):
            st.warning(f"⚠️ Missing file: {filename}")
            continue
        try:
            frames.append(_read_one_csv(filename))
            #st.success(f"Loaded: {filename}")
            print(f"Loaded: {filename}")
        except Exception as e:
            st.error(f"Error in {filename}: {e}")

    if not frames:
        return pd.DataFrame(columns=["date_local", "daily_temp_c", "daily_consumption_kwh"])

    df_all = pd.concat(frames, ignore_index=True)

    # Combine by day, averaging temperature & summing consumption
    df_daily = (
        df_all.groupby("date_local", as_index=False)
        .agg(
            daily_temp_c=("daily_temp_c", "mean"),
            daily_consumption_kwh=("daily_consumption_kwh", "sum"),
        )
        .sort_values("date_local")
        .reset_index(drop=True)
    )
    return df_daily


# -----------------------------------------------------
# Load data
# -----------------------------------------------------
st.subheader("Loading yearly CSV files...")
daily_df = load_all_years()

if daily_df.empty:
    st.error("No valid data loaded. Ensure all CSV files are in the same folder.")
    st.stop()


# -----------------------------------------------------
# Sidebar: filter
# -----------------------------------------------------
st.sidebar.header("Temperature filter")

min_t = float(daily_df["daily_temp_c"].min())
max_t = float(daily_df["daily_temp_c"].max())

# Slider
sel_min, sel_max = st.sidebar.slider(
    "Daily average temperature range (°C)",
    min_value=float(round(min_t - 0.5, 1)),
    max_value=float(round(max_t + 0.5, 1)),
    value=(float(round(min_t, 1)), float(round(max_t, 1))),
    step=0.1,
)

# Manual numeric input
min_input = st.sidebar.number_input(
    "Min temperature (°C)",
    value=sel_min,
    step=0.1,
    format="%.1f",
)

max_input = st.sidebar.number_input(
    "Max temperature (°C)",
    value=sel_max,
    step=0.1,
    format="%.1f",
)

# Final chosen values
min_val = min_input
max_val = max_input

# Filter
mask = (daily_df["daily_temp_c"] >= min_val) & (daily_df["daily_temp_c"] <= max_val)
#mask = (daily_df["daily_temp_c"] >= min_input) & (daily_df["daily_temp_c"] <= max_input)
#mask = (daily_df["daily_temp_c"] >= sel_min) & (daily_df["daily_temp_c"] <= sel_max)
result = daily_df.loc[mask].sort_values("date_local").reset_index(drop=True)

# -----------------------------------------------------
# Display results
# -----------------------------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Days matched", f"{len(result)}")
col2.metric("Data covers", f"{daily_df['date_local'].min()} → {daily_df['date_local'].max()}")
col3.metric("Selected range", f"{sel_min:.1f} to {sel_max:.1f} °C")

st.subheader("Matching days")

result_show = result.copy()
result_show["date_local"] = pd.to_datetime(result_show["date_local"]).dt.strftime("%Y-%m-%d (%a)")
result_show.rename(columns={
    "date_local": "Date",
    "daily_temp_c": "Daily avg temp (°C)",
    "daily_consumption_kwh": "Daily consumption (kWh)",
}, inplace=True)

st.dataframe(result_show, hide_index=True, use_container_width=True)

# Download CSV
#csv_buf = io.StringIO()
#result_show.to_csv(csv_buf, index=False, sep=",")
#st.download_button(
#    "⬇️ Download results as CSV",
#    csv_buf.getvalue(),
#    "matching_days_with_consumption.csv",
#    "text/csv",
#)

# Chart
#with st.expander("Show daily temperature chart"):
#    chart_df = daily_df.copy()
#    chart_df["Date"] = pd.to_datetime(chart_df["date_local"])
#    st.line_chart(chart_df.set_index("Date")[["daily_temp_c"]])
