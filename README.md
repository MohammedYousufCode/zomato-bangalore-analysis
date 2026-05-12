# 🍽️ Zomato Bangalore Restaurant Performance Analysis

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://zomato-bangalore-analysis.streamlit.app)
[![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit%20App-FF4B4B?style=for-the-badge)](https://zomato-bangalore-analysis.streamlit.app)

End-to-end data analytics project on 12,037 unique Bangalore restaurants — covering data cleaning, PostgreSQL, EDA, and an interactive Streamlit dashboard.

---

## 📖 The Story Behind This Project

Before writing a single line of Python, I spent a year as a Zomato delivery partner in Mysore — completing **2,500+ orders** on a 4-hour daily shift. I knew peak hours not from a dashboard but from traffic and cold food bags. I understood restaurant ratings not as numbers but as the difference between a smooth handoff and a 20-minute wait.

When I found this dataset on Kaggle, I recognised patterns I had already lived. This project is my attempt to quantify them: which areas produce inconsistent restaurants, whether price actually buys quality, and why some restaurants stay invisible despite good food.

---

## 🗂️ Table of Contents

- [Quick Start](#-quick-start)
- [Key Metrics](#-key-metrics)
- [Tech Stack](#-tech-stack)
- [Dataset & Cleaning](#-dataset--cleaning)
- [Business Questions](#️-business-questions)
- [Key Findings](#-key-findings)
- [SQL Analysis](#-sql-analysis)
- [Running the Analysis](#-running-the-analysis)
- [Project Structure](#-project-structure)
- [About Me](#-about-me)

---

## � Quick Start

**Want to explore the data immediately?**

```bash
# Clone and navigate
git clone https://github.com/mohammed-yousuf-aiml/zomato-bangalore-analysis.git
cd zomato-bangalore-analysis

# Install dependencies
pip install -r streamlit_app/requirements.txt

# Launch the interactive dashboard
streamlit run streamlit_app/app.py
```

The Streamlit app is fully self-contained — all cleaned data and visualizations load instantly. No database setup required unless you want to run the SQL queries.

---

## 📈 Key Metrics

| Metric | Value | Context |
|--------|-------|---------|
| **Restaurants Analyzed** | 12,037 | After cleaning 51,000 raw rows |
| **Geographic Coverage** | 93 areas | Across Bangalore |
| **Average Rating** | 3.63 / 5.0 | With median 3.70 (slight left skew) |
| **Rating Range** | 1.8 – 4.9 | Fine Dining leads at 4.1 avg |
| **Highest Low-Rated Area** | Whitefield | 211 restaurants below 3.5 rating |
| **Best-Rated Area** | Lavelle Road | 4.1 average rating |
| **Price-Quality Correlation** | +0.40 | Clear trend: higher price = higher, more consistent rating |
| **Most Popular Type** | Casual Dining + Café | Average 1,500+ votes per restaurant |

---

## �🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Data Processing | Python, pandas, NumPy |
| Visualization | seaborn, matplotlib, Plotly |
| Database | PostgreSQL, SQLAlchemy |
| Dashboard | Streamlit |

---

## 📦 Dataset & Cleaning

**Source:** [Zomato Bangalore Dataset by Himanshu Poddar — Kaggle](https://www.kaggle.com/datasets/himanshupoddar/zomato-bangalore-restaurants)

| Stage | Rows |
|---|---|
| Raw (`zomato.csv`) | ~51,000 |
| After cleaning | **12,037 unique restaurants** |

### Data Dictionary (Final Clean Dataset)

| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| `name` | string | Restaurant name | Unique within location |
| `location` | string | Bangalore area | 93 unique areas |
| `rate` | float | Customer rating | 1.8–4.9 scale, NaN for new restaurants |
| `cost_for_two` | int | Price for two people (₹) | ₹100–₹5,500 range |
| `cuisines` | string | Cuisine types | Comma-separated, multi-cuisine common |
| `rest_type` | string | Restaurant classification | Casual, Fine, Cafe, Quick Bites, etc. |
| `votes` | int | Number of user votes | Popularity/feedback proxy |
| `online_order` | int | Accepts online orders | 1 = Yes, 0 = No |
| `book_table` | int | Allows table reservations | 1 = Yes, 0 = No |

### Cleaning Process

**Notebook:** `02_data_cleaning.ipynb`

- **Dropped unused columns:** `url`, `address`, `phone`, `dish_liked`, `reviews_list`, `menu_item`
- **`rate` column:** Contained `"NEW"`, `"-"`, and `"/5"` strings — stripped and cast to `float`, unparseable values set to `NaN`
- **`approx_cost(for two people)`:** Comma-formatted strings stripped and cast to `int`, renamed to `cost_for_two`
- **`online_order` / `book_table`:** Mapped `Yes/No` → `1/0`
- **Nulls:** Rows with nulls in `location`, `rest_type`, `cuisines`, `cost_for_two` dropped
  - **Result:** 12,037 unique restaurants across 93 areas

**Quality checks applied:**
- No negative votes or costs
- Ratings within valid range (1.8–4.9 or NaN)
- No duplicate name + location pairs
- All string columns trimmed of whitespace

---

## 🏙️ Business Questions

| # | Question |
|---|---|
| 1 | Which cuisines have the highest rating but lowest order volume — hidden gems? |
| 2 | Which Bangalore areas have the most low-rated restaurants? |
| 3 | Is there a correlation between price range and customer rating? |
| 4 | Which restaurant types get the most votes — does that match their rating? |
| 5 | What does rating distribution look like across the city? |

---

## 📊 Key Findings & Insights

### 1. **Rating Distribution is Left-Skewed**
**Finding:** City-wide rating mean **3.63**, median **3.70** — slight left skew from a minority of poor restaurants.

**What this means:** Most restaurants are good (≥3.5), but a tail of underperformers drag the average down.

---

### 2. **IT Corridor Areas Have Quality Consistency Problems**
**Finding:** Low-rated area hotspots (rate < 3.5):
- **Whitefield** — 211 low-rated restaurants
- **Electronic City** — 200
- **Marathahalli** — 195

**Why it matters:** High order volume masks inconsistent quality. Expansion into these areas is riskier than established neighborhoods.

---

### 3. **Price Genuinely Buys Quality & Consistency**
**Finding:** Price vs rating (boxplot analysis):
- **Budget (≤₹300):** Wide distribution, median ~3.5
- **Mid-range (₹300–₹700):** Tighter, median ~3.7
- **Premium (₹700–₹1000):** High consistency, median ~3.9
- **Luxury (₹1,000+):** Narrow, high distribution, median ~4.1

**The insight:** Higher price doesn't just correlate with higher ratings — it correlates with *consistent* quality. Investors in premium segments face less rating volatility.

---

### 4. **Restaurant Type vs Market Visibility**
**Finding:** Restaurant type vs votes:
- **Casual Dining + Café** combinations: Highest average votes (1,500+) — best visibility
- **Fine Dining:** Highest average rating (~4.1) but far fewer votes — quality without visibility
- **Quick Bites:** Low votes and lower average ratings — lowest market appeal

**Business implication:** Fine Dining restaurants need aggressive marketing to overcome low visibility despite superior quality.

---

### 5. **Geographic Opportunity: Lavelle Road**
**Finding:** Top-rated area is **Lavelle Road** with 4.1 average rating.

**Context:** Highest quality area in the city; lower competition for premium dining.

---

### 6. **Feature Engineering Insights**
**Correlation heatmap findings:**
- **`book_table` × `cost_for_two`: 0.61** — expensive restaurants are strongly more likely to offer table booking (premium service indicator)
- **`online_order` × `cost_for_two`: -0.14** — premium restaurants lean away from online orders (brand positioning)

**These patterns suggest:** Premium restaurants differentiate via service (reservations) rather than convenience (delivery).

---

## 🗄️ SQL Analysis

Data loaded into PostgreSQL via SQLAlchemy (`03_load_to_postgresql.ipynb`). Analysis uses CTEs, window functions, and aggregation for deeper insights.

**Queries are organized into two files:**

### `01_basic_analysis.sql` — Foundation Queries

| Query | Purpose | Techniques Used |
|-------|---------|-----------------|
| **Area Rating Summary** | Average, max, min ratings per area (min 20 restaurants) | `AVG()`, `MAX()`, `MIN()`, `HAVING COUNT(*) >= 20` |
| **Low-Rated Areas (CTE)** | Two-step: filter rate < 3.5, count per area | `WITH` CTE, `WHERE rate < 3.5`, `GROUP BY` |
| **Rank Within Area** | Restaurant ranking per location + delta vs area mean | `RANK() OVER (PARTITION BY location ORDER BY rate DESC)` |

### `02_advanced_analysis.sql` — Strategic Insights

| Query | Purpose | Techniques Used |
|-------|---------|-----------------|
| **Price Buckets vs Rating** | Aggregate rating & votes by price tier (4 buckets) | `CASE` for bucketing, `GROUP BY` |
| **Hidden Gems** | High-rated, low-popularity cuisines | Two CTEs + `RANK() OVER ()` on both dimensions |
| **Restaurant Type vs Votes** | Compare popularity & quality by type side-by-side | `RANK() OVER (ORDER BY AVG(votes) DESC)` & `RANK() OVER (ORDER BY AVG(rate) DESC)` |

All queries are **production-ready** with proper indexing recommendations and execution plan notes.

---

## 📊 Visualizations

The analysis includes **7 high-quality static visualizations** (see `visuals/` folder) and **3 interactive Streamlit pages**:

### Static Visualizations (Python/Plotly)
- `01_rating_distribution.png` — Histogram + KDE of city-wide ratings
- `02_low_rated_areas.png` — Bar chart of areas with most restaurants below 3.5
- `03_price_vs_rating.png` — Box plot of rating by price tier
- `04_resttype_vs_votes.png` — Restaurant types ranked by popularity
- `05_popularity_vs_quality.png` — Scatter: votes vs rating with cuisine color coding
- `06_top_areas_rating.png` — Top 10 areas by average rating
- `07_correlation_heatmap.png` — Feature correlations (Pearson)

### Interactive Streamlit Dashboard

| Page | Features |
|------|----------|
| **Page 1: City Overview** | City-wide stats, rating distribution, top/bottom areas |
| **Page 2: Area Deep Dive** | Filter by area, see restaurants ranked by rating, cost breakdown |
| **Page 3: Cuisine Explorer** | Filter cuisines, find hidden gems, spot market trends |

---

## ⚙️ Running the Analysis

### Option 1: Interactive Dashboard (Recommended for Most Users)

```bash
# Clone and navigate
git clone https://github.com/mohammed-yousuf-aiml/zomato-bangalore-analysis.git
cd zomato-bangalore-analysis

# Install dependencies
pip install -r streamlit_app/requirements.txt

# Launch dashboard
streamlit run streamlit_app/app.py
```

The app opens at `http://localhost:8501` with instant data loading.

---

### Option 2: Jupyter Notebooks (For Data Exploration)

**Prerequisites:**
- Python 3.10+
- Jupyter Notebook or JupyterLab
- Virtual environment (recommended)

**Setup:**
```bash
# Navigate to project
cd zomato-bangalore-analysis

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Install all dependencies
pip install -r streamlit_app/requirements.txt

# Start Jupyter
jupyter notebook
```

**Recommended execution order:**
1. `01_data_exploration.ipynb` — Understand raw data structure and anomalies
2. `02_data_cleaning.ipynb` — Follow cleaning decisions step-by-step
3. `03_load_to_postgresql.ipynb` — Load cleaned data to PostgreSQL (optional)
4. `04_eda_analysis.ipynb` — Detailed exploratory data analysis with visualizations

---

### Option 3: PostgreSQL & SQL (Advanced)

**Prerequisites:**
- PostgreSQL 14+ installed and running
- pgAdmin or `psql` CLI for query execution

**Steps:**

1. **Create database and user:**
   ```sql
   CREATE DATABASE zomato_bangalore;
   CREATE USER data_analyst WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE zomato_bangalore TO data_analyst;
   ```

2. **Update `03_load_to_postgresql.ipynb`:**
   - Replace connection string: `postgresql://data_analyst:your_password@localhost:5432/zomato_bangalore`
   - Run all cells to load cleaned data

3. **Execute analysis queries:**
   ```bash
   psql -U data_analyst -d zomato_bangalore -f sql/01_basic_analysis.sql
   psql -U data_analyst -d zomato_bangalore -f sql/02_advanced_analysis.sql
   ```

4. **Or open in pgAdmin GUI** for interactive exploration

---

---

## 🗃️ Project Structure

```
zomato-bangalore-analysis/
│
├── 📄 README.md                                    # This file
├── 📄 LICENSE                                      # MIT License
├── 📄 zomato_cleaned.csv                           # Final clean dataset (12,037 rows)
│
├── 📁 data/                                        # ⚠️ gitignored — not pushed to GitHub
│   └── zomato.csv                                  # Raw dataset (~51,000 rows)
│
├── 📁 notebooks/                                   # Jupyter analysis notebooks
│   ├── 01_data_exploration.ipynb                  # Understand raw data
│   ├── 02_data_cleaning.ipynb                     # Cleaning pipeline
│   ├── 03_load_to_postgresql.ipynb                # Database loading (optional)
│   └── 04_eda_analysis.ipynb                      # Deep exploratory analysis
│
├── 📁 sql/                                         # PostgreSQL queries
│   ├── 01_basic_analysis.sql                      # Foundation queries
│   └── 02_advanced_analysis.sql                   # Strategic insights
│
├── 📁 streamlit_app/                               # Interactive dashboard
│   ├── app.py                                     # Main Streamlit app
│   └── requirements.txt                           # Python dependencies
│
├── 📁 visuals/                                     # Static analysis charts
│   ├── 01_rating_distribution.png
│   ├── 02_low_rated_areas.png
│   ├── 03_price_vs_rating.png
│   ├── 04_resttype_vs_votes.png
│   ├── 05_popularity_vs_quality.png
│   ├── 06_top_areas_rating.png
│   └── 07_correlation_heatmap.png
│
└── 📁 screenshots/                                 # Dashboard screenshots
    ├── page1_city_overview.png
    ├── page2_area_deep_dive.png
    └── page3_cuisine_explorer.png
```

---

## 🎯 Key Features

✅ **Complete data pipeline:** Raw → Cleaned → Analyzed → Visualized  
✅ **Multiple interfaces:** Jupyter notebooks, SQL, Streamlit dashboard  
✅ **Production-quality code:** Idiomatic Python, proper error handling  
✅ **Rich documentation:** Data dictionary, query explanations, business insights  
✅ **Reproducible:** Same results guaranteed with cleaned CSV and seed states  
✅ **Real-world context:** Informed by actual delivery partner experience  

---

## 🔧 Troubleshooting

**Streamlit app won't load:**
```bash
# Ensure dependencies are installed
pip install --upgrade streamlit plotly pandas sqlalchemy

# Check Python version
python --version  # Should be 3.10+
```

**PostgreSQL connection failed:**
- Verify PostgreSQL service is running
- Check connection string matches your credentials
- Ensure database `zomato_bangalore` exists

**Jupyter kernel errors:**
- Restart the kernel (Kernel → Restart in menu)
- Reinstall packages: `pip install --force-reinstall -r streamlit_app/requirements.txt`

**Missing files:**
- Ensure `zomato_cleaned.csv` is in the root directory
- If not, run `02_data_cleaning.ipynb` to regenerate it

---

## 📚 Learning Outcomes

This project demonstrates:

- **Data Engineering:** ETL pipeline, deduplication, data validation
- **SQL Mastery:** CTEs, window functions, aggregations, performance optimization
- **Python Data Science:** pandas, NumPy, scikit-learn workflows
- **Visualization:** Plotly interactive charts, seaborn statistical plots
- **Dashboard Design:** Multi-page Streamlit apps with filtering
- **Business Analysis:** Translating insights into actionable recommendations
- **Documentation:** Clear notebooks, SQL comments, comprehensive README

---

## 👤 About Me

I'm a **final-year BCA student** specializing in data analytics and AI/ML. This project represents my approach to data work: grounded in real-world context (my experience as a Zomato delivery partner) and executed with technical rigor.

**What I bring:**
- Experience turning raw data into strategic insights
- Full-stack data pipelines: collection → cleaning → analysis → visualization
- Proficiency in Python, SQL, databases, and modern analytics tools
- A data storyteller who explains *why* numbers matter

**Currently seeking:** Data Analyst / Junior Data Engineer roles in Hyderabad and Bangalore

**Connect with me:**
- 💼 [LinkedIn](https://linkedin.com/in/mohammed-yousuf-aiml)
- 🐙 [GitHub](https://github.com/mohammed-yousuf-aiml)
- 📧 [Email](mailto:mohammed.yousuf.aiml@gmail.com)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — © 2025 Mohammed Yousuf.

**You are free to:**
- Use this code for educational and commercial purposes
- Modify and distribute the code
- Include this code in your projects

**You must:**
- Include the original license and copyright notice

---

## 🙏 Acknowledgments

- **Dataset:** [Himanshu Poddar on Kaggle](https://www.kaggle.com/datasets/himanshupoddar/zomato-bangalore-restaurants)
- **Libraries:** pandas, NumPy, Plotly, Streamlit, SQLAlchemy
- **Inspiration:** Real-world experience as a Zomato delivery partner in Mysore

---

<p align="center">
  <strong>Built with curiosity, delivered with data.</strong>
  <br>
  <sub>If this project helped you, please consider giving it a ⭐ on GitHub!</sub>
</p>