-- Rating Distribution by Area
SELECT 
location,
COUNT(*) as total_restaurants,
ROUND(AVG(rate)::numeric, 2) as avg_rating,
MAX(rate) as best_rating,
MIN(rate) as worst_rating
FROM restaurants
WHERE rate IS NOT NULL
GROUP BY location
HAVING COUNT(*) >= 20
ORDER BY avg_rating DESC
LIMIT 15;

-- CTE: Areas With Most Low-Rated Restaurants (Business Question 2)
WITH low_rated AS (
SELECT location, name, rate
FROM restaurants
    WHERE rate < 3.5 AND rate IS NOT NULL
),

area_count AS (
    SELECT location,COUNT(*) as low_rated_count,ROUND(AVG(rate)::numeric, 2) as avg_bad_rating
FROM low_rated GROUP BY location
)
SELECT * FROM area_count
ORDER BY low_rated_count DESC
LIMIT 10;

-- Window Function: Rank Restaurants Within Each Area (Business Question 5)
SELECT location,name,
rate,votes,
RANK() OVER (PARTITION BY location ORDER BY rate DESC) as rank_in_area,
ROUND(AVG(rate) OVER (PARTITION BY location)::numeric, 2) as area_avg_rating,
ROUND(rate - AVG(rate) OVER (PARTITION BY location)::numeric, 2) as vs_area_avg
FROM restaurants
WHERE rate IS NOT NULL AND votes > 20
ORDER BY location, rank_in_area
LIMIT 30;



