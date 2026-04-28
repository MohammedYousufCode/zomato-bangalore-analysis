import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os

# Set page configuration
st.set_page_config(layout="wide", page_title="Zomato Bangalore Analysis", page_icon="🍽️")

# ── Theme-adaptive CSS via JavaScript ────────────────────────────────────────
# st.context.theme.type is unreliable in Streamlit 1.56 when System theme is used
# and the OS is dark (it always returns "light" unless config.toml is set).
# Solution: inject a <style> block + tiny JS that reads the ACTUAL rendered
# background color of .stApp at runtime, determines dark/light, and applies
# the correct CSS class to the document root — no Python theme detection needed.

st.markdown("""
<style>
    /* ── Header (always the same) ── */
    .header {
        background: linear-gradient(90deg, #CB202D, #E23744);
        padding: 16px 24px;
        border-radius: 8px;
        margin-bottom: 24px;
    }
    .header h1 { color: #ffffff !important; margin: 0; font-size: 28px; }
    .header p  { color: rgba(255,255,255,0.88) !important; margin: 4px 0 0 0; font-size: 14px; }

    /* ── KPI card base (layout only, no colours) ── */
    .kpi-card {
        border-top: 4px solid #E23744;
        border-radius: 8px;
        padding: 16px 12px;
        text-align: center;
        min-height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    :is(.kpi-card) p, :is(.kpi-card) p * {
        font-size: 13px !important;
        margin: 0 !important;
        line-height: 1.3 !important;
    }
    :is(.kpi-card) h2, :is(.kpi-card) h2 * {
        margin: 6px 0 !important;
        font-size: 24px !important;
        font-weight: 700 !important;
        word-break: break-word !important;
        line-height: 1.2 !important;
    }
    :is(.kpi-card) p.subtitle, :is(.kpi-card) p.subtitle * {
        font-size: 12px !important;
    }

    /* ── LIGHT theme card colours ── */
    html.zom-light .kpi-card                          { background: #F2F2F2 !important; box-shadow: 0 2px 8px rgba(0,0,0,0.10); }
    html.zom-light :is(.kpi-card) p                   { color: #555555 !important; }
    html.zom-light :is(.kpi-card) p *                 { color: #555555 !important; }
    html.zom-light :is(.kpi-card) h2                  { color: #1C1C1C !important; }
    html.zom-light :is(.kpi-card) h2 *                { color: #1C1C1C !important; }
    html.zom-light :is(.kpi-card) p.subtitle          { color: #2eaa5e !important; }
    html.zom-light :is(.kpi-card) p.subtitle *        { color: #2eaa5e !important; }
    html.zom-light [data-testid="stSidebar"]          { background-color: #F2F2F2 !important; }

    /* ── DARK theme card colours ── */
    html.zom-dark .kpi-card                           { background: #2a2a2a !important; box-shadow: 0 2px 8px rgba(0,0,0,0.45); }
    html.zom-dark :is(.kpi-card) p                    { color: #aaaaaa !important; }
    html.zom-dark :is(.kpi-card) p *                  { color: #aaaaaa !important; }
    html.zom-dark :is(.kpi-card) h2                   { color: #f0f0f0 !important; }
    html.zom-dark :is(.kpi-card) h2 *                 { color: #f0f0f0 !important; }
    html.zom-dark :is(.kpi-card) p.subtitle           { color: #48C479 !important; }
    html.zom-dark :is(.kpi-card) p.subtitle *         { color: #48C479 !important; }
    html.zom-dark [data-testid="stSidebar"]           { background-color: #1e1e1e !important; }

    /* ── Download button ── */
    .stDownloadButton > button { background-color: #CB202D !important; color: #ffffff !important; border: none !important; border-radius: 6px !important; padding: 8px 20px !important; }
    .stDownloadButton > button:hover { background-color: #a51823 !important; }
</style>

<script>
(function applyTheme() {
    function isDarkBg(el) {
        // Parse rgb(r,g,b) and check perceived brightness
        var bg = window.getComputedStyle(el).backgroundColor;
        var m = bg.match(/\\d+/g);
        if (!m || m.length < 3) return false;
        // Perceived brightness formula
        var lum = (parseInt(m[0]) * 299 + parseInt(m[1]) * 587 + parseInt(m[2]) * 114) / 1000;
        return lum < 128;
    }

    function apply() {
        // Try to find Streamlit's app container for background colour
        var app = document.querySelector('.stApp') ||
                  document.querySelector('[data-testid="stApp"]') ||
                  document.body;
        var dark = isDarkBg(app);
        document.documentElement.classList.remove('zom-light', 'zom-dark');
        document.documentElement.classList.add(dark ? 'zom-dark' : 'zom-light');
    }

    // Run immediately, then watch for theme changes via MutationObserver
    apply();

    // Re-check whenever body/html class or style attributes change
    // (Streamlit swaps Emotion CSS vars when theme toggles)
    var obs = new MutationObserver(function(mutations) {
        for (var m of mutations) {
            if (m.type === 'attributes' || m.type === 'childList') {
                apply();
                break;
            }
        }
    });
    obs.observe(document.documentElement, { attributes: true, childList: true, subtree: false });
    obs.observe(document.body,            { attributes: true, childList: true, subtree: false });

    // Also poll briefly after load for slower renders
    var checks = 0;
    var t = setInterval(function() {
        apply();
        if (++checks >= 10) clearInterval(t);
    }, 300);
})();
</script>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────────

def kpi_card(title, value, subtitle=""):
    st.markdown(f"""
    <div class="kpi-card">
        <p>{title}</p>
        <h2>{value}</h2>
        <p class="subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def add_header():
    total = st.session_state.data['name'].nunique() if 'data' in st.session_state and not st.session_state.data.empty else 0
    locations = st.session_state.data['location'].nunique() if total > 0 else 0
    st.markdown(f"""
    <div class="header">
        <h1>🍽️ Zomato Bangalore Restaurant Analysis</h1>
        <p>Insights from {total:,} unique restaurants across {locations} Bangalore areas</p>
    </div>
    """, unsafe_allow_html=True)


def plotly_layout(fig, height=400):
    """Apply consistent layout — transparent background so dark/light theme shows through."""
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, family='Arial'),
        height=height,
        margin=dict(t=10, b=10, l=10, r=10),
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor='rgba(128,128,128,0.3)',
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128,128,128,0.2)',
    )
    return fig


# ── Data loading ─────────────────────────────────────────────────────────────

@st.cache_data
def load_data():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(script_dir, '..', 'zomato_cleaned.csv')
        df = pd.read_csv(data_path)

        # Numeric coercion for rate
        df['rate'] = pd.to_numeric(df['rate'], errors='coerce')

        # Normalise online_order / book_table to 0/1 integers
        for col in ['online_order', 'book_table']:
            if col in df.columns:
                if df[col].dtype == object:
                    df[col] = df[col].str.strip().str.upper().map({'YES': 1, 'NO': 0})
                else:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        # Numeric cost
        if 'cost_for_two' in df.columns:
            df['cost_for_two'] = pd.to_numeric(df['cost_for_two'], errors='coerce')

        # Numeric votes
        if 'votes' in df.columns:
            df['votes'] = pd.to_numeric(df['votes'], errors='coerce')

        # Drop duplicate restaurants — same name + location = same restaurant
        # Raw CSV has ~12k rows due to restaurants listed under multiple meal types
        dedup_cols = [c for c in ['name', 'location'] if c in df.columns]
        if dedup_cols:
            df = df.drop_duplicates(subset=dedup_cols, keep='first').reset_index(drop=True)

        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()


if 'data' not in st.session_state:
    with st.spinner('Loading data...'):
        st.session_state.data = load_data()

df = st.session_state.data

# ── Sidebar navigation ────────────────────────────────────────────────────────

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["City Overview", "Area Deep Dive", "Cuisine & Restaurant Explorer"])

# ── Page 1: City Overview ─────────────────────────────────────────────────────

if page == "City Overview":
    add_header()

    if not df.empty:
        total_restaurants = df['name'].nunique()  # Count unique restaurants, not rows
        avg_city_rating = df['rate'].mean() if not df['rate'].isna().all() else 0
        most_popular_area = (
            df['location'].value_counts().index[0]
            if 'location' in df.columns and not df['location'].empty
            else "N/A"
        )

        area_stats = df.groupby('location').agg(
            avg_rating=('rate', 'mean'),
            restaurant_count=('name', 'count')
        ).reset_index()
        area_stats = area_stats[area_stats['restaurant_count'] >= 5]
        top_rated_area = (
            area_stats.loc[area_stats['avg_rating'].idxmax(), 'location']
            if not area_stats.empty else "N/A"
        )

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            kpi_card("Total Restaurants", f"{total_restaurants:,}")
        with col2:
            kpi_card("Avg City Rating", f"{avg_city_rating:.1f} ⭐")
        with col3:
            kpi_card("Most Popular Area", most_popular_area)
        with col4:
            kpi_card("Top Rated Area", top_rated_area)

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        # Top 15 areas by average rating
        with col1:
            st.subheader("Top 15 Areas by Average Rating")
            top_areas_rating = area_stats.nlargest(15, 'avg_rating')
            fig1 = px.bar(
                top_areas_rating,
                y='location',
                x='avg_rating',
                orientation='h',
                labels={'location': 'Area', 'avg_rating': 'Average Rating'},
                color='avg_rating',
                color_continuous_scale=[[0, '#CB202D'], [1, '#FF8C94']],
            )
            fig1 = plotly_layout(fig1)
            fig1.update_yaxes(categoryorder='total ascending')  # highest rated at top
            st.plotly_chart(fig1, use_container_width=True)

        # Top 10 areas by restaurant count
        with col2:
            st.subheader("Top 10 Areas by Number of Restaurants")
            top_areas_count = df['location'].value_counts().nlargest(10).reset_index()
            top_areas_count.columns = ['location', 'count']
            fig2 = px.bar(
                top_areas_count,
                x='location',
                y='count',
                labels={'location': 'Area', 'count': 'Number of Restaurants'},
                color='count',
                color_continuous_scale=[[0, '#CB202D'], [1, '#FF8C94']],
            )
            fig2.update_xaxes(tickangle=-30)
            st.plotly_chart(plotly_layout(fig2), use_container_width=True)

        # Rating distribution histogram  ← FIX: pass DataFrame, not Series
        st.subheader("Rating Distribution Across All Restaurants")
        rate_data = df[['rate']].dropna()
        if not rate_data.empty:
            fig3 = px.histogram(
                rate_data,
                x='rate',
                nbins=20,
                labels={'rate': 'Rating', 'count': 'Number of Restaurants'},
                color_discrete_sequence=['#E23744'],
            )
            fig3.update_traces(marker_line_color='white', marker_line_width=0.5)
            st.plotly_chart(plotly_layout(fig3), use_container_width=True)
        else:
            st.warning("No rating data available for histogram.")

    else:
        st.error("Failed to load data. Please check the data file.")

# ── Page 2: Area Deep Dive ────────────────────────────────────────────────────

elif page == "Area Deep Dive":
    add_header()

    if not df.empty:
        st.sidebar.subheader("Filter by Area")
        all_locations = sorted(df['location'].dropna().unique())
        selected_location = st.sidebar.selectbox("Select Area", all_locations, index=0)

        area_df = df[df['location'] == selected_location].copy()

        if not area_df.empty:
            restaurants_in_area = len(area_df)
            avg_rating_area = area_df['rate'].mean() if not area_df['rate'].isna().all() else 0
            avg_cost_area = area_df['cost_for_two'].mean() if not area_df['cost_for_two'].isna().all() else 0
            online_order_pct = (
                (area_df['online_order'].sum() / len(area_df)) * 100
                if len(area_df) > 0 else 0
            )

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                kpi_card("Restaurants in Area", f"{restaurants_in_area}")
            with col2:
                kpi_card("Avg Rating", f"{avg_rating_area:.1f} ⭐")
            with col3:
                kpi_card("Avg Cost for Two", f"₹{avg_cost_area:.0f}")
            with col4:
                kpi_card("% Online Ordering", f"{online_order_pct:.1f}%")

            st.markdown("<br>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            # Top 10 restaurants by votes
            with col1:
                st.subheader(f"Top 10 Restaurants in {selected_location} by Votes")
                top_votes = area_df.nlargest(10, 'votes')
                if not top_votes.empty:
                    fig1 = px.bar(
                        top_votes,
                        x='votes',
                        y='name',
                        orientation='h',
                        labels={'votes': 'Votes', 'name': 'Restaurant'},
                        color='votes',
                        color_continuous_scale=[[0, '#CB202D'], [1, '#FF8C94']],
                    )
                    st.plotly_chart(plotly_layout(fig1), use_container_width=True)
                else:
                    st.warning("No vote data available.")

            # Rating distribution boxplot  ← FIX: pass DataFrame with named column
            with col2:
                st.subheader(f"Rating Distribution in {selected_location}")
                rate_data_area = area_df[['rate']].dropna()
                if not rate_data_area.empty:
                    fig2 = px.box(
                        rate_data_area,
                        y='rate',
                        points="all",
                        labels={'rate': 'Rating'},
                        color_discrete_sequence=['#E23744'],
                    )
                    st.plotly_chart(plotly_layout(fig2), use_container_width=True)
                else:
                    st.warning("No rating data available for boxplot.")

            # Restaurant table
            st.subheader(f"All Restaurants in {selected_location}")
            table_df = area_df.sort_values('rate', ascending=False)
            display_df = table_df[['name', 'rate', 'votes', 'cuisines', 'cost_for_two']].copy()
            display_df.columns = ['Name', 'Rating', 'Votes', 'Cuisines', 'Cost for Two (₹)']
            display_df['Cost for Two (₹)'] = display_df['Cost for Two (₹)'].apply(
                lambda x: f"₹{x:.0f}" if pd.notnull(x) else "N/A"
            )
            display_df['Rating'] = display_df['Rating'].apply(
                lambda x: f"{x:.1f}" if pd.notnull(x) else "N/A"
            )
            st.dataframe(display_df, use_container_width=True, height=400)
        else:
            st.warning(f"No data available for area: {selected_location}")
    else:
        st.error("Failed to load data. Please check the data file.")

# ── Page 3: Cuisine & Restaurant Explorer ────────────────────────────────────

elif page == "Cuisine & Restaurant Explorer":
    add_header()

    if not df.empty:
        st.sidebar.subheader("Filters")

        # Build cuisine list
        all_cuisines = set()
        for cuisines_str in df['cuisines'].dropna():
            if isinstance(cuisines_str, str):
                all_cuisines.update(c.strip() for c in cuisines_str.split(','))
        all_cuisines = sorted(all_cuisines)

        selected_cuisines = st.sidebar.multiselect(
            "Cuisine Type",
            options=all_cuisines,
            default=[]
        )

        # Price range slider — compute from data to avoid hardcoded limits
        cost_min_data = int(df['cost_for_two'].dropna().min()) if not df['cost_for_two'].isna().all() else 100
        cost_max_data = int(df['cost_for_two'].dropna().max()) if not df['cost_for_two'].isna().all() else 6000
        min_cost, max_cost = st.sidebar.slider(
            "Price Range (₹ for two)",
            min_value=cost_min_data,
            max_value=cost_max_data,
            value=(cost_min_data, cost_max_data),
            step=50
        )

        # Min rating slider
        min_rating = st.sidebar.slider(
            "Minimum Rating",
            min_value=2.0,
            max_value=5.0,
            value=2.0,
            step=0.1
        )

        # Apply filters
        filtered_df = df.copy()

        if selected_cuisines:
            def cuisine_match(cuisines_str):
                if pd.isna(cuisines_str):
                    return False
                cuisines_list = [c.strip() for c in str(cuisines_str).split(',')]
                return any(cuisine in cuisines_list for cuisine in selected_cuisines)
            filtered_df = filtered_df[filtered_df['cuisines'].apply(cuisine_match)]

        filtered_df = filtered_df[
            (filtered_df['cost_for_two'] >= min_cost) &
            (filtered_df['cost_for_two'] <= max_cost)
        ]

        filtered_df = filtered_df[
            (filtered_df['rate'] >= min_rating) &
            (filtered_df['rate'].notna())
        ]

        # KPIs
        filtered_count = len(filtered_df)
        avg_rating_filtered = filtered_df['rate'].mean() if not filtered_df['rate'].isna().all() else 0
        avg_cost_filtered = filtered_df['cost_for_two'].mean() if not filtered_df['cost_for_two'].isna().all() else 0
        online_order_pct_filtered = (
            (filtered_df['online_order'].sum() / len(filtered_df)) * 100
            if len(filtered_df) > 0 else 0
        )

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            kpi_card("Filtered Restaurants", f"{filtered_count:,}")
        with col2:
            kpi_card("Avg Rating", f"{avg_rating_filtered:.1f} ⭐")
        with col3:
            kpi_card("Avg Cost for Two", f"₹{avg_cost_filtered:.0f}")
        with col4:
            kpi_card("% Online Ordering", f"{online_order_pct_filtered:.1f}%")

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        # Top cuisines by average rating
        with col1:
            st.subheader("Top Cuisines by Average Rating")
            cuisine_list = []
            for cuisines_str in filtered_df['cuisines'].dropna():
                if isinstance(cuisines_str, str):
                    cuisine_list.extend(c.strip() for c in cuisines_str.split(','))

            if cuisine_list:
                cuisine_counts = pd.Series(cuisine_list).value_counts().reset_index()
                cuisine_counts.columns = ['cuisine', 'count']

                exploded_df = filtered_df.assign(
                    cuisine=filtered_df['cuisines'].str.split(',')
                ).explode('cuisine')
                exploded_df['cuisine'] = exploded_df['cuisine'].str.strip()
                cuisine_rating = exploded_df.groupby('cuisine')['rate'].mean().reset_index()
                cuisine_rating = cuisine_rating.merge(cuisine_counts, on='cuisine')
                top_cuisines = cuisine_rating.nlargest(10, 'rate')

                if not top_cuisines.empty:
                    fig1 = px.bar(
                        top_cuisines,
                        x='cuisine',
                        y='rate',
                        labels={'cuisine': 'Cuisine', 'rate': 'Average Rating'},
                        color='rate',
                        color_continuous_scale=[[0, '#CB202D'], [1, '#FF8C94']],
                    )
                    fig1.update_xaxes(tickangle=-30)
                    st.plotly_chart(plotly_layout(fig1), use_container_width=True)
                else:
                    st.warning("No cuisine data available for chart.")
            else:
                st.warning("No cuisine data available.")

        # Bubble chart: votes vs rating
        with col2:
            st.subheader("Votes vs Rating (by cost category)")

            def cost_category(cost):
                if pd.isna(cost):
                    return "Unknown"
                elif cost < 500:
                    return "Budget (<₹500)"
                elif cost < 1500:
                    return "Mid-range (₹500–1500)"
                else:
                    return "Premium (₹1500+)"

            plot_df = filtered_df.copy()
            plot_df['cost_category'] = plot_df['cost_for_two'].apply(cost_category)
            plot_df = plot_df.dropna(subset=['rate', 'votes'])

            if not plot_df.empty:
                fig2 = px.scatter(
                    plot_df,
                    x='votes',
                    y='rate',
                    size='cost_for_two',
                    color='cost_category',
                    labels={
                        'votes': 'Votes',
                        'rate': 'Rating',
                        'cost_for_two': 'Cost for Two (₹)',
                        'cost_category': 'Cost Category'
                    },
                    color_discrete_map={
                        "Budget (<₹500)":        "#CB202D",
                        "Mid-range (₹500–1500)": "#E23744",
                        "Premium (₹1500+)":      "#48C479",
                        "Unknown":               "#696969"
                    },
                    size_max=20,
                    opacity=0.75,
                )
                st.plotly_chart(plotly_layout(fig2), use_container_width=True)
            else:
                st.warning("No data available for scatter plot.")

        # Filtered restaurant table
        st.subheader("Filtered Restaurants")
        if not filtered_df.empty:
            cols_needed = ['name', 'online_order', 'book_table', 'rate', 'votes',
                           'location', 'rest_type', 'cuisines', 'cost_for_two',
                           'listed_in(type)', 'listed_in(city)']
            # Only keep columns that actually exist in the dataframe
            cols_present = [c for c in cols_needed if c in filtered_df.columns]
            display_df = filtered_df[cols_present].copy()

            rename_map = {
                'name': 'Name', 'online_order': 'Online Order', 'book_table': 'Book Table',
                'rate': 'Rating', 'votes': 'Votes', 'location': 'Location',
                'rest_type': 'Restaurant Type', 'cuisines': 'Cuisines',
                'cost_for_two': 'Cost for Two', 'listed_in(type)': 'Listed In (Type)',
                'listed_in(city)': 'Listed In (City)'
            }
            display_df.rename(columns={k: v for k, v in rename_map.items() if k in display_df.columns}, inplace=True)

            if 'Online Order' in display_df.columns:
                display_df['Online Order'] = display_df['Online Order'].map({1: 'Yes', 0: 'No'}).fillna('N/A')
            if 'Book Table' in display_df.columns:
                display_df['Book Table'] = display_df['Book Table'].map({1: 'Yes', 0: 'No'}).fillna('N/A')
            if 'Cost for Two' in display_df.columns:
                display_df['Cost for Two'] = display_df['Cost for Two'].apply(
                    lambda x: f"₹{x:.0f}" if pd.notnull(x) else "N/A"
                )
            if 'Rating' in display_df.columns:
                display_df['Rating'] = display_df['Rating'].apply(
                    lambda x: f"{x:.1f}" if pd.notnull(x) else "N/A"
                )

            st.dataframe(display_df, use_container_width=True, height=400)

            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="⬇️ Download Filtered Data as CSV",
                data=csv,
                file_name="zomato_filtered_restaurants.csv",
                mime="text/csv"
            )
        else:
            st.warning("No restaurants match the selected filters.")
    else:
        st.error("Failed to load data. Please check the data file.")

# ── Footer ────────────────────────────────────────────────────────────────────

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: #696969;'>Zomato Bangalore Analysis • Built with Streamlit</p>",
    unsafe_allow_html=True
)
