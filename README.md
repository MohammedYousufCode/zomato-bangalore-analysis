# 🍽️ Zomato Bangalore Restaurant Performance Analysis

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://zomato-bangalore-analysis.streamlit.app)
[![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit%20App-FF4B4B?style=for-the-badge)](https://zomato-bangalore-analysis.streamlit.app)

> **Turning 2,500 deliveries of lived experience into data-driven insight** — a full-stack analytics project covering data cleaning, PostgreSQL, EDA, and an interactive Streamlit dashboard across 8,723 unique Bangalore restaurants.

---

## 📖 The Story Behind This Project

Before I wrote a single line of Python, I spent a year as a Zomato delivery partner in Mysore — completing **2,500+ orders** across a 4-hour daily shift. I knew peak hours not from a dashboard but from traffic jams and cold food bags. I understood restaurant ratings not as numbers but as the difference between a smooth handoff and a 20-minute wait. I watched certain delivery zones flood with orders while others stayed idle all evening.

When I discovered the Zomato Bangalore dataset on Kaggle, I didn't see raw CSV rows — I recognised patterns I had already lived. This project is my attempt to quantify what I experienced on the ground: which areas produce the most inconsistent restaurants, whether price actually buys quality, and why some restaurants remain invisible despite excellent food.

This isn't just a portfolio piece. It's where street-level knowledge meets structured analysis.

---

## 🗂️ Table of Contents

- [Live Demo](#-live-demo)
- [Tech Stack](#-tech-stack)
- [Dataset Overview](#-dataset-overview)
- [Data Cleaning](#-data-cleaning)
- [Business Questions](#️-business-questions-answered)
- [Key Findings](#-key-findings)
- [SQL Analysis](#-sql-analysis)
- [Screenshots](#-screenshots)
- [Project Structure](#-project-structure)
- [How to Run Locally](#-how-to-run-locally)
- [Business Recommendations](#-business-recommendations)
- [About Me](#-about-me)

---

## 🚀 Live Demo

👉 **[zomato-bangalore-analysis.streamlit.app](https://zomato-bangalore-analysis.streamlit.app)**

The app features three interactive pages:
- **City Overview** — rating distributions, correlation heatmap, city-wide KPIs
- **Area Deep Dive** — low-rated hotspots, top-rated localities, area comparisons
- **Cuisine Explorer** — hidden gems, popularity vs quality scatter, cuisine rankings

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Data Processing | Python, pandas, NumPy |
| Visualization | seaborn, matplotlib, Plotly |
| Database | PostgreSQL, SQLAlchemy |
| Dashboard | Streamlit |
| Dataset Source | Kaggle (Himanshu Poddar) |

---

## 📦 Dataset Overview

| Property | Detail |
|---|---|
| Source | [Zomato Bangalore Dataset — Kaggle](https://www.kaggle.com/datasets/himanshupoddar/zomato-bangalore-restaurants) |
| File | `zomato.csv` |
| Raw Rows | ~51,000 |
| Columns | 17 |
| After Cleaning | **8,723 unique restaurants** |
| Geographic Scope | 93 areas across Bangalore |

---

## 🧹 Data Cleaning

The raw dataset had a structural issue that would have distorted every analysis: **Zomato lists the same restaurant multiple times** — once for each service type it offers (Delivery, Dine-out, Buffet, Café, etc.). Left uncleaned, a single restaurant could appear 3–4 times, inflating counts and skewing aggregations.

### Cleaning Steps

**1. Deduplication**
- **Issue:** Same restaurant listed multiple times under different `listed_in(type)` categories
- **Fix:** Deduplicated on `name + location` — retained one row per unique restaurant per area
- **Result:** 51,000 raw rows → **8,723 unique restaurants**

**2. `rate` Column**
- Raw values included strings like `"NEW"` and trailing `/5` suffixes
- Stripped non-numeric characters, converted to `float`, nulls forward-filled with area median

**3. `cost_for_two` Column**
- Contained comma-formatted strings (e.g., `"1,200"`)
- Stripped commas, cast to `integer`

**4. Null Handling**
- Columns with <5% nulls: dropped rows
- Columns with higher null rates: imputed with area-level medians to preserve geographic signal

---

## 🏙️ Business Questions Answered

| # | Question |
|---|---|
| 1 | Which cuisines have the highest rating but lowest order volume — the hidden gems? |
| 2 | Which Bangalore areas have the most low-rated restaurants? |
| 3 | Is there a correlation between price range and customer rating? |
| 4 | Which restaurant types get the most votes — and does that match their rating? |
| 5 | What does rating distribution look like across the entire city? |

---

## 📊 Key Findings

### 🌆 City-Wide Rating Landscape
- The city average rating is **3.63** with a median of **3.70** — a slight left skew caused by a minority of poorly-rated restaurants pulling the mean down. Most Bangalore restaurants cluster between 3.5 and 4.0.

### 📍 Low-Rated Area Hotspots
- **Whitefield leads with 211 low-rated restaurants**, followed by Electronic City (200) and Marathahalli (195)
- All three are IT corridor areas — high-density, high-demand zones where volume has outpaced quality control
- Lavelle Road ranks as the **top-rated area** with an average of 4.1; **Jayanagar** has the highest total restaurant count

### 💸 Price vs. Quality
- **Luxury restaurants (₹1,000+):** Narrow, high-rating distribution — median ~4.1. Consistent quality.
- **Budget restaurants (≤₹300):** Wide, low-rating distribution — median ~3.5. High variance.
- Paying more genuinely does buy more *consistent* quality, even if outliers exist at every tier

### 🏆 Popularity vs. Visibility
- **Casual Dining + Café** combinations attract the highest average votes (1,500+) — the most popular restaurant type in the city
- **Fine Dining** holds a strong average rating of 4.1 but receives far fewer votes — high quality, low street visibility
- This gap represents a marketing opportunity hiding in plain data

### 🔗 Correlation Signals

| Variable Pair | Correlation | Interpretation |
|---|---|---|
| `book_table` × `cost_for_two` | **0.61** | Expensive restaurants are strongly more likely to offer table booking |
| `online_order` × `cost_for_two` | **-0.14** | Premium restaurants lean away from online ordering — they prefer dine-in |

---

## 🗄️ SQL Analysis

Six production-quality SQL queries using **window functions and CTEs**, covering:

| Query | Technique |
|---|---|
| Rating percentile ranking per area | `PERCENT_RANK()` window function |
| Cuisine performance analysis | CTE + `GROUP BY` aggregation |
| Online vs offline order rating comparison | `CASE` + conditional aggregation |
| Restaurant tier classification | `NTILE()` window function |
| Top performers per location | `ROW_NUMBER()` with `PARTITION BY` |
| Price-rating correlation buckets | CTE + bucket joins |

SQL files are in [`/sql`](./sql/).

---

## 📸 Screenshots

### Page 1 — City Overview
![City Overview](screenshots/page1_city_overview.png)

### Page 2 — Area Deep Dive
![Area Deep Dive](screenshots/page2_area_deep_dive.png)

### Page 3 — Cuisine Explorer
![Cuisine Explorer](screenshots/page3_cuisine_explorer.png)

---

## 🗃️ Project Structure

```
zomato-bangalore-analysis/
├── zomato_cleaned.csv
├── README.md
├── .gitignore
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_load_to_postgresql.ipynb
│   └── 04_eda_analysis.ipynb
├── sql/
│   ├── 01_basic_analysis.sql
│   └── 02_advanced_analysis.sql
├── streamlit_app/
│   ├── app.py
│   └── requirements.txt
├── visuals/
│   ├── 01_rating_distribution.png
│   ├── 02_low_rated_areas.png
│   ├── 03_price_vs_rating.png
│   ├── 04_resttype_vs_votes.png
│   ├── 05_popularity_vs_quality.png
│   ├── 06_top_areas_rating.png
│   └── 07_correlation_heatmap.png
└── screenshots/
    ├── page1_city_overview.png
    ├── page2_area_deep_dive.png
    └── page3_cuisine_explorer.png
```

---

## ⚙️ How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/zomato-bangalore-analysis.git
cd zomato-bangalore-analysis
```

**2. Install dependencies**
```bash
pip install pandas numpy seaborn matplotlib sqlalchemy psycopg2-binary streamlit plotly
```

Or install from the requirements file:
```bash
pip install -r streamlit_app/requirements.txt
```

**3. (Optional) Set up PostgreSQL**

Create a local database and update the connection string in `03_load_to_postgresql.ipynb`, then run the notebook to load `zomato_cleaned.csv` into PostgreSQL.

**4. Launch the Streamlit app**
```bash
streamlit run streamlit_app/app.py
```

The app will open at `http://localhost:8501`.

---

## 💡 Business Recommendations

### For Zomato

**1. Targeted Quality Intervention in IT Corridors**
Whitefield, Electronic City, and Marathahalli collectively account for the highest concentration of low-rated restaurants in the city. Zomato should deploy dedicated restaurant onboarding support and periodic quality audits in these zones — not just flag poor performers, but actively help them improve. These areas generate high order volumes; quality inconsistency directly erodes customer trust where it hurts most.

**2. Surface Fine Dining to the Right Audience**
Fine Dining restaurants average a 4.1 rating but receive disproportionately low vote counts — they are invisible on the platform relative to their quality. Zomato should create curated discovery features (premium collections, occasion-based recommendations) that route quality-sensitive users toward these restaurants. The data shows demand for quality; the matching just isn't happening.

### For Restaurant Owners

**3. Invest in Table Booking as a Trust Signal**
The 0.61 correlation between table booking availability and price tier is striking — but the causality can be reversed strategically. Mid-range restaurants that add table booking signal reliability and organisation to customers. Even for smaller establishments, enabling this feature on the Zomato platform likely improves perceived quality and attracts a more committed customer base.

**4. Budget Restaurants: Consistency Beats Ambition**
The wide rating variance in the ≤₹300 tier shows customers aren't expecting a fine dining experience — they are rewarding *consistency*. Budget restaurant owners should focus operational energy on narrowing the bad days rather than chasing high ratings on good ones. A floor of 3.8 sustained week-over-week will outperform occasional 4.5s punctuated by 2.8s in both ratings and repeat orders.

---

## 👤 About Me

I'm a final-year BCA student with hands-on experience as a Zomato delivery partner and a growing skill set in data analytics. I'm actively targeting **Data Analyst roles in Hyderabad and Bangalore** and am open to internships, freelance projects, and full-time opportunities.

**Skills:** Python · pandas · NumPy · SQL · PostgreSQL · Streamlit · Plotly · Data Cleaning · EDA · Dashboard Development

📎 [LinkedIn — Add URL](https://linkedin.com/in/your-profile)

---

The dataset is sourced from Kaggle and credited to Himanshu Poddar.

---

<p align="center">Built with data, delivered with experience.</p>