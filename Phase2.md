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