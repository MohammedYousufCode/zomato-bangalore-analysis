-- CTE + Window: Price Range vs Rating (Business Question 3)
WITH price_buckets AS (
    SELECT 
        name,
        rate,
        votes,
        cost_for_two,
        CASE 
            WHEN cost_for_two <= 300  THEN 'Budget (≤300)'
            WHEN cost_for_two <= 600  THEN 'Mid-Range (301-600)'
            WHEN cost_for_two <= 1000 THEN 'Premium (601-1000)'
            ELSE 'Luxury (1000+)'
        END as price_category
    FROM restaurants
    WHERE rate IS NOT NULL AND cost_for_two IS NOT NULL
)
SELECT 
    price_category,
    COUNT(*) as restaurant_count,
    ROUND(AVG(rate)::numeric, 2) as avg_rating,
    ROUND(AVG(votes)::numeric, 0) as avg_votes
FROM price_buckets
GROUP BY price_category
ORDER BY avg_rating DESC;

-- High Rating but Low Votes (Business Question 1)
WITH cuisine_stats AS (
    SELECT 
        cuisines,
        COUNT(*) as restaurant_count,
        ROUND(AVG(rate)::numeric, 2) as avg_rating,
        ROUND(AVG(votes)::numeric, 0) as avg_votes,
        ROUND(AVG(cost_for_two)::numeric, 0) as avg_cost
    FROM restaurants
    WHERE rate IS NOT NULL 
      AND votes > 10
    GROUP BY cuisines
    HAVING COUNT(*) >= 5
),
ranked AS (
    SELECT *,
        RANK() OVER (ORDER BY avg_rating DESC) as rating_rank,
        RANK() OVER (ORDER BY avg_votes ASC) as low_popularity_rank
    FROM cuisine_stats
)
SELECT 
    cuisines,
    avg_rating,
    avg_votes,
    avg_cost,
    rating_rank,
    low_popularity_rank
FROM ranked
WHERE rating_rank <= 30 AND low_popularity_rank <= 30
ORDER BY avg_rating DESC
LIMIT 10;

-- Restaurant Type vs Votes (Business Question 4)
SELECT 
    rest_type,
    COUNT(*) as total_restaurants,
    ROUND(AVG(votes)::numeric, 0) as avg_votes,
    ROUND(AVG(rate)::numeric, 2) as avg_rating,
    SUM(votes) as total_votes,
    RANK() OVER (ORDER BY AVG(votes) DESC) as popularity_rank,
    RANK() OVER (ORDER BY AVG(rate) DESC) as quality_rank
FROM restaurants
WHERE rate IS NOT NULL AND votes > 0
GROUP BY rest_type
HAVING COUNT(*) >= 10
ORDER BY avg_votes DESC;