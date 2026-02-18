> [!NOTE]
> The material was created with the help of ChatGPT and Copilot.

# 📊 Working with Data in Applications

Modern applications are rarely built on a single dataset. Instead, they **combine, enrich, and transform data** from multiple sources into a meaningful structure that supports decision-making, automation, and user interaction.

Let’s walk through this step by step.

---

## 1️⃣ Types of Data

### 🔹 Structured Data

Structured data is **organized in a fixed schema**:

* Rows and columns
* Known data types
* Predictable structure

Examples:

* SQL databases
* CSV files
* Excel spreadsheets

📌 *This is the most common form used in programming courses and backend systems.*

---

### 🔹 Semi-structured Data

Semi-structured data has **structure, but not a rigid schema**.

Examples:

* JSON
* XML
* API responses

📌 Flexible, human-readable, and widely used in web APIs.

---

### 🔹 Unstructured Data

Unstructured data has **no predefined structure**.

Examples:

* Text documents
* Images
* Videos
* Log files (raw)

📌 Requires processing before it can be used in applications.

---

## 2️⃣ CSV – A Fundamental Data Format

### What is CSV?

CSV (Comma-Separated Values) is a **plain text format** where:

* Each row represents one record
* Columns are separated by commas
* The first row usually contains headers

### Why CSV is still important

* Easy to read and write
* Supported by almost every language and tool
* Perfect for data exchange, analysis, and teaching

---

### 📄 Example CSV

```csv
timestamp,temperature_c,consumption_kwh
2025-01-01 00:00, -5.2, 12.4
2025-01-01 01:00, -5.6, 13.1
2025-01-01 02:00, -6.0, 14.0
```

---

## 3️⃣ Combining Data from Multiple Sources

Real systems rarely rely on one dataset.

Examples:

* Energy usage + weather data
* Sales data + customer data
* Sensor data + location data

To combine datasets **reliably**, we use **keys**.

---

## 4️⃣ Keys – The Glue Between Data

### 🔑 What is a Key?

A key is a field that **uniquely identifies** a record or **links records together**.

### Common key types

* `id` (numeric or UUID)
* `timestamp`
* `user_id`
* `device_id`

### Example

* Weather API → temperature by `timestamp`
* CSV file → electricity consumption by `timestamp`

📌 The shared key allows us to **merge the data correctly**.

---

## 5️⃣ Common Data Sources

### 🌐 APIs

* Weather APIs
* Energy market APIs
* Public open data APIs

Characteristics:

* JSON responses
* Real-time or near real-time
* Requires HTTP requests

---

### 🗄 Databases

* SQL (PostgreSQL, SQLite, MySQL)
* NoSQL (MongoDB)

Characteristics:

* Persistent storage
* Structured schema
* Queryable

---

### 📁 Files

* CSV
* JSON
* Excel

Characteristics:

* Simple
* Offline-friendly
* Easy to version and share

---

## 6️⃣ Example: Creating a Unified Data Structure

### Scenario

We combine:

* Electricity consumption (CSV)
* Outdoor temperature (API)

Goal:

> Analyze how temperature affects electricity consumption.

---

## 📋 List of Data Fields (Columns)

| Field name        | Description                               |
| ----------------- | ----------------------------------------- |
| `timestamp`       | Date and time of the measurement          |
| `temperature_c`   | Outdoor temperature in Celsius            |
| `consumption_kwh` | Electricity consumption in kilowatt-hours |

---

## 🧠 What Each Field Represents

* **timestamp**
  Acts as the *primary key* connecting different datasets.

* **temperature_c**
  Environmental factor influencing energy usage.

* **consumption_kwh**
  Core metric we want to analyze and predict.

---

## 📄 Example Combined Data (CSV)

```csv
timestamp,temperature_c,consumption_kwh
2025-01-01 00:00,-5.2,12.4
2025-01-01 01:00,-5.6,13.1
2025-01-01 02:00,-6.0,14.0
```

This CSV could be:

* Generated programmatically
* Stored in a database
* Used for visualization
* Used for machine learning

---

## 7️⃣ Why This Data Is Important for the Application

### 🎯 Practical Value

* Enables **data-driven decisions**
* Makes hidden patterns visible
* Supports forecasting and optimization

### 🔧 Technical Value

* Teaches data modeling
* Demonstrates key-based joins
* Encourages clean data structures

### 📈 Business / System Perspective

* Predict future electricity demand
* Optimize resource usage
* Improve system reliability

---

## 🧠 Mental Model

> **Raw data → Structured data → Linked data → Insight**

If students understand:

* how data is structured,
* how keys connect datasets,
* and why structure matters,

they are no longer just *coding* — they are **engineering systems**.

---





# 🧪 Exercise: Forecast Tomorrow’s Electricity Consumption (Hourly + Summary)

## Application Overview

In Finland, most electricity consumers pay for electricity to **two separate parties**.

The first is the **local electricity distribution company**, which operates the power grid. This cost is typically based on a fairly stable pricing model that includes a fixed monthly fee and a consumption-based charge. Consumers usually have very limited possibilities to influence these costs in the short term.

The second party is the **energy supplier**, which sells the actual electricity. Energy suppliers offer various pricing models, one of the most common in Finland being **spot-priced electricity**. In this model, the electricity price varies hourly and is determined by multiple market factors. Importantly, consumers usually receive the **next day’s electricity prices one day in advance**.

Knowing future electricity prices allows consumers to actively influence their electricity costs by adjusting when and how electricity is used.

In many Finnish homes, **electric heating is widely used**, and electricity consumption is strongly correlated with **outdoor temperature**. As temperatures drop, heating demand — and thus electricity consumption — typically increases.

This application helps consumers **anticipate the next day’s electricity consumption** by combining:

* historical electricity consumption data,
* outdoor temperature measurements,
* and weather forecasts for the coming day.

By estimating hourly electricity consumption in advance, the application enables users to **adjust indoor temperature settings and energy usage proactively**, especially during hours with high electricity prices. The goal is to reduce total electricity costs without compromising comfort, using data-driven insights rather than reactive decisions.

---

## What I need

https://aina.elenia.fi/ -> Consumption history  
https://www.ilmatieteenlaitos.fi/havaintojen-lataus -> Weather history  
https://www.ilmatieteenlaitos.fi/avoin-data-avattavat-aineistot -> Weather forecast  

```
curl "https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::forecast::harmonie::surface::point::timevaluepair&place=hameenlinna&starttime=2026-02-12T00:00:00Z&endtime=2026-02-13T00:00:00Z&timestep=60&parameters=Temperature,WindSpeedMS,PrecipitationAmount,TotalCloudCover" \
-o hameenlinna_forecast_tomorrow.xml
```

https://dashboard.elering.ee/assets/swagger-ui/index.html -> Electricity price

```
curl -L -o ee_prices.csv \
  "https://dashboard.elering.ee/api/nps/price/csv?fields=ee&start=2026-02-03T00:00:00Z&end=2026-02-03T23:59:59.999Z"
```


## Files you have

### 1) `consumption_actual.csv` (historical actuals)

Format (example):

```csv
timestamp,temperature_c,consumption_kwh
2025-01-01 00:00,-5.2,12.4
2025-01-01 01:00,-5.6,13.1
2025-01-01 02:00,-6.0,14.0
```

### 2) Temperature forecast (from API)

You will fetch tomorrow’s hourly `temperature_2m`.

---

## Goal outputs

### A) `consumption_forecast.csv` (tomorrow hourly forecast)

Same structure as the consumption file, but consumption is forecasted:

```csv
timestamp,temperature_c,consumption_kwh
2026-02-11 00:00,-7.1,13.8
...
```

### B) Summary in console

* total forecast consumption (kWh)
* min / max hourly forecast
* how many historical matches per hour (quality indicator)

---

## ✅ Rule for predicting consumption per hour

For each forecast hour:

1. take forecast temperature `T`
2. find historical rows where `temperature_c` is in `[T-0.5, T+0.5]`
3. predicted `consumption_kwh` = **mean** of those matching rows
4. if no matches exist → fallback strategy:

   * widen window to ±1.0, then ±2.0
   * if still empty → use overall mean consumption (last fallback)

---

## 🧩 Reference Implementation (single file)

Save as: `forecast_consumption.py`

```python
from __future__ import annotations

import csv
import statistics
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import List, Tuple
import urllib.request
import json


# =========================
# Data models
# =========================

@dataclass(frozen=True)
class ActualRow:
    timestamp: datetime
    temperature_c: float
    consumption_kwh: float


@dataclass(frozen=True)
class ForecastHour:
    timestamp: datetime
    temperature_c: float


@dataclass(frozen=True)
class PredictedRow:
    timestamp: datetime
    temperature_c: float
    consumption_kwh: float
    matches_used: int
    window_used: float


# =========================
# Helpers: parsing / IO
# =========================

def parse_dt(ts: str) -> datetime:
    # Expect "YYYY-MM-DD HH:MM"
    return datetime.strptime(ts.strip(), "%Y-%m-%d %H:%M")


def read_actuals_csv(path: str) -> List[ActualRow]:
    rows: List[ActualRow] = []
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(
                ActualRow(
                    timestamp=parse_dt(r["timestamp"]),
                    temperature_c=float(r["temperature_c"]),
                    consumption_kwh=float(r["consumption_kwh"]),
                )
            )
    if not rows:
        raise ValueError("No rows read from consumption CSV.")
    return rows


def write_forecast_csv(path: str, predicted: List[PredictedRow]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "temperature_c", "consumption_kwh"])
        for p in predicted:
            writer.writerow([
                p.timestamp.strftime("%Y-%m-%d %H:%M"),
                f"{p.temperature_c:.1f}",
                f"{p.consumption_kwh:.3f}",
            ])


# =========================
# Forecast API (Open-Meteo)
# =========================

def fetch_forecast_open_meteo(lat: float, lon: float, target_day: date) -> List[ForecastHour]:
    """
    Fetch hourly temperature forecast for the given day using Open-Meteo.
    No API key required.
    """
    start = target_day.isoformat()
    end = (target_day + timedelta(days=1)).isoformat()

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m"
        f"&start_date={start}&end_date={end}"
        "&timezone=Europe%2FHelsinki"
    )

    with urllib.request.urlopen(url, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    times = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]

    hours: List[ForecastHour] = []
    for t, temp in zip(times, temps):
        # Open-Meteo uses ISO: "YYYY-MM-DDTHH:MM"
        ts = datetime.strptime(t, "%Y-%m-%dT%H:%M")
        hours.append(ForecastHour(timestamp=ts, temperature_c=float(temp)))

    # Ensure we got exactly 24 hours (often yes, but some days may vary due to DST)
    return hours


# =========================
# Prediction logic
# =========================

def find_matches(actuals: List[ActualRow], target_temp: float, window: float) -> List[ActualRow]:
    lo = target_temp - window
    hi = target_temp + window
    return [r for r in actuals if lo <= r.temperature_c <= hi]


def predict_hour(actuals: List[ActualRow], hour: ForecastHour) -> PredictedRow:
    fallback_windows = [0.5, 1.0, 2.0]

    for w in fallback_windows:
        matches = find_matches(actuals, hour.temperature_c, w)
        if matches:
            pred = statistics.mean(m.consumption_kwh for m in matches)
            return PredictedRow(
                timestamp=hour.timestamp,
                temperature_c=hour.temperature_c,
                consumption_kwh=pred,
                matches_used=len(matches),
                window_used=w,
            )

    # Last fallback: overall average consumption
    overall = statistics.mean(r.consumption_kwh for r in actuals)
    return PredictedRow(
        timestamp=hour.timestamp,
        temperature_c=hour.temperature_c,
        consumption_kwh=overall,
        matches_used=0,
        window_used=-1.0,
    )


def build_forecast(actuals: List[ActualRow], forecast_hours: List[ForecastHour]) -> List[PredictedRow]:
    return [predict_hour(actuals, h) for h in forecast_hours]


# =========================
# Summary / reporting
# =========================

def print_summary(predicted: List[PredictedRow]) -> None:
    consumptions = [p.consumption_kwh for p in predicted]
    total = sum(consumptions)

    print("\n=== Forecast Summary ===")
    print(f"Hours forecasted: {len(predicted)}")
    print(f"Total forecast consumption (kWh): {total:.3f}")
    print(f"Min hourly (kWh): {min(consumptions):.3f}")
    print(f"Max hourly (kWh): {max(consumptions):.3f}")

    # Quality indicator: how often we used which window
    windows = {}
    for p in predicted:
        windows[p.window_used] = windows.get(p.window_used, 0) + 1

    print("\nWindow usage count:")
    for w, count in sorted(windows.items(), key=lambda x: x[0]):
        label = "overall-mean fallback" if w == -1.0 else f"±{w:.1f}°C"
        print(f"  {label}: {count} hour(s)")

    # Show a few hours as example
    print("\nFirst 5 forecast rows:")
    for p in predicted[:5]:
        print(
            f"{p.timestamp.strftime('%Y-%m-%d %H:%M')}  "
            f"T={p.temperature_c:.1f}°C  "
            f"pred={p.consumption_kwh:.3f} kWh  "
            f"matches={p.matches_used}  window={p.window_used}"
        )


# =========================
# Main
# =========================

def main() -> None:
    # 1) Read actual historical data
    actuals = read_actuals_csv("consumption_actual.csv")

    # 2) Define target day = tomorrow (local date assumption)
    tomorrow = date.today() + timedelta(days=1)

    # 3) Fetch temperature forecast for tomorrow
    # Example coordinates: Helsinki
    lat, lon = 60.1699, 24.9384
    forecast_hours = fetch_forecast_open_meteo(lat, lon, tomorrow)

    # 4) Create predicted hourly consumption forecast
    predicted = build_forecast(actuals, forecast_hours)

    # 5) Save CSV
    write_forecast_csv("consumption_forecast.csv", predicted)

    # 6) Print summary
    print_summary(predicted)

    print("\n✅ Wrote: consumption_forecast.csv")


if __name__ == "__main__":
    main()
```

---

## 🧠 What we learn

✅ CSV parsing and writing  
✅ joining data sources using a shared dimension (temperature)  
✅ “nearest neighbor” idea (temperature similarity)  
✅ fallback logic and robust data handling  
✅ producing a dataset suitable for later visualization / ML  
