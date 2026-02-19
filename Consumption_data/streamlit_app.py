import io
import sys
from typing import List, Tuple, Optional

import pandas as pd
import streamlit as st

# -------------------------
# Page configuration
# -------------------------
st.set_page_config(
    page_title="Daily Temperature Range Finder",
    page_icon="🌡️",
    layout="wide",
)

st.title("🌡️ Daily Temperature Range Finder")
st.caption(
    "Upload your hourly CSV files (2016–2025) and get the list of **days** where the daily average temperature is between the values you choose."
)

with st.expander("CSV format expected (example)", expanded=False):
    st.code(
        "Time; Consumption (net) kWh; Production (net) kWh; Daily average temperature\n"
        "2025-01-01T00:00:00.000+02:00;1,569;0,000;-4,7\n"
        "2025-01-01T01:00:00.000+02:00;1,879;0,000;-4,8\n",
        language="text",
    )
    st.markdown("- **Delimiter:** semicolon `;`  ")
    st.markdown("- **Decimals:** comma `,` (e.g., `-4,7`)  ")
    st.markdown("- **Time zone in Time column:** offset like `+02:00` (Europe/Helsinki)")

# -------------------------
# Helpers
# -------------------------

@st.cache_data(show_spinner=False)
def _read_one_csv(file) -> pd.DataFrame:
    """Read a single CSV file with EU-style separators and return a normalized DataFrame.

    Expected columns (case-insensitive, extra spaces tolerated):
      - Time
      - Daily average temperature (or any column containing the word 'temperature')
    """
    # Try UTF-8 first, then fallback to cp1252/latin-1
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            df = pd.read_csv(
                file,
                sep=";",
                decimal=",",
                encoding=enc,
                engine="python",
            )
            break
        except Exception:
            df = None
    if df is None:
        raise ValueError("Could not read CSV with common encodings (utf-8 / cp1252 / latin-1).")

    # Normalize column names: strip spaces and collapse duplicate spaces
    df.columns = [" ".join(str(c).split()).strip() for c in df.columns]

    # Identify time column
    time_col_candidates = [c for c in df.columns if c.lower() == "time"]
    if not time_col_candidates:
        # try partial match
        time_col_candidates = [c for c in df.columns if "time" in c.lower()]
    if not time_col_candidates:
        raise ValueError("No 'Time' column found.")
    time_col = time_col_candidates[0]

    # Identify temperature column
    temp_col_candidates = [c for c in df.columns if c.lower().strip() == "daily average temperature"]
    if not temp_col_candidates:
        # fallback: any column containing 'temperature'
        temp_col_candidates = [c for c in df.columns if "temperature" in c.lower()]
    if not temp_col_candidates:
        raise ValueError("No temperature column found (expected 'Daily average temperature' or a column containing 'temperature').")
    temp_col = temp_col_candidates[0]

    # Parse datetime with timezone info preserved via UTC then convert to Europe/Helsinki
    t = pd.to_datetime(df[time_col], errors="coerce", utc=True)
    # If the input contained timezone offsets, above yields tz-aware UTC; otherwise it's naive-UTC. That's fine.
    try:
        t_local = t.dt.tz_convert("Europe/Helsinki")
    except Exception:
        # If tz-naive (no offset in source), localize as Helsinki to respect local date boundaries
        t_local = t.dt.tz_localize("Europe/Helsinki")

    df["date_local"] = t_local.dt.date

    # Ensure temperature is numeric; decimal="," should already help, but coerce to be safe
    df[temp_col] = pd.to_numeric(df[temp_col], errors="coerce")

    # Compute daily temperature by taking daily mean of the found temperature column.
    daily = (
        df.groupby("date_local", as_index=False)[temp_col]
        .mean(numeric_only=True)
        .rename(columns={temp_col: "daily_temp_c"})
    )

    return daily

@st.cache_data(show_spinner=False)
def _combine_daily(files: List) -> pd.DataFrame:
    frames = []
    for f in files:
        try:
            frames.append(_read_one_csv(f))
        except Exception as e:
            st.warning(f"Skipping file '{getattr(f, 'name', 'uploaded')}' → {e}")
    if not frames:
        return pd.DataFrame(columns=["date_local", "daily_temp_c"])  # empty

    daily_all = pd.concat(frames, ignore_index=True)

    # If the same day appears in multiple files, average them (they should be identical for the daily-average column).
    daily = (
        daily_all.groupby("date_local", as_index=False)["daily_temp_c"].mean(numeric_only=True)
        .sort_values("date_local")
        .reset_index(drop=True)
    )
    return daily

# -------------------------
# Sidebar – inputs
# -------------------------
with st.sidebar:
    st.header("Input files")
    uploaded = st.file_uploader(
        "Upload one or more CSV files (2016–2025)",
        type=["csv"],
        accept_multiple_files=True,
        help="CSV must use ';' as delimiter and ',' as decimal separator.",
    )
    st.markdown("\n")

    # Placeholders for range selector once data is loaded
    range_placeholder = st.empty()

# -------------------------
# Main flow
# -------------------------
if not uploaded:
    st.info("Upload your CSVs to begin.")
    st.stop()

with st.spinner("Reading and combining CSVs..."):
    daily_df = _combine_daily(uploaded)

if daily_df.empty:
    st.error("No valid data could be read from the uploaded files.")
    st.stop()

# Determine slider bounds from the data
min_t = float(daily_df["daily_temp_c"].min())
max_t = float(daily_df["daily_temp_c"].max())

with st.sidebar:
    st.header("Filter")
    sel_min, sel_max = st.slider(
        "Daily average temperature range (°C)",
        min_value=float(round(min_t - 0.5, 1)),
        max_value=float(round(max_t + 0.5, 1)),
        value=(float(round(min_t, 1)), float(round(max_t, 1))),
        step=0.1,
        help="Shows days where the **daily average** temperature is between these values (inclusive).",
    )

# Filter inclusive
mask = (daily_df["daily_temp_c"] >= sel_min) & (daily_df["daily_temp_c"] <= sel_max)
result = daily_df.loc[mask].copy()
result.sort_values("date_local", inplace=True)
result.reset_index(drop=True, inplace=True)

# Summary row at the top
left, right, right2 = st.columns([1, 1, 1])
left.metric("Days matched", f"{len(result):,}")
right.metric("Date range in data", f"{daily_df['date_local'].min()} → {daily_df['date_local'].max()}")
right2.metric("Selected range (°C)", f"{sel_min:.1f} to {sel_max:.1f}")

st.markdown("---")

# Show results
st.subheader("Matching days")
# Nice, human-friendly format
result_show = result.copy()
result_show["date_local"] = pd.to_datetime(result_show["date_local"]).dt.strftime("%Y-%m-%d (%a)")
result_show.rename(columns={"date_local": "Date", "daily_temp_c": "Daily avg temp (°C)"}, inplace=True)

st.dataframe(
    result_show,
    use_container_width=True,
    hide_index=True,
)

# Download button
csv_buf = io.StringIO()
# Use semicolon and decimal point in export for wide compatibility
result.rename(columns={"date_local": "Date", "daily_temp_c": "Daily avg temp (C)"}).to_csv(
    csv_buf, index=False, sep=","
)
st.download_button(
    label="⬇️ Download matching days (CSV)",
    data=csv_buf.getvalue(),
    file_name="matching_days.csv",
    mime="text/csv",
)

# Optional: small chart for context
with st.expander("Show chart of daily temperatures (full data)"):
    chart_df = daily_df.copy()
    chart_df["Date"] = pd.to_datetime(chart_df["date_local"])  # for Streamlit's line_chart
    chart_df.sort_values("Date", inplace=True)
    st.line_chart(chart_df.set_index("Date")["daily_temp_c"], height=250)

st.caption("Tip: If your file already has a 'Daily average temperature' column repeated for each hour, this app will still group by day and use the mean value.")