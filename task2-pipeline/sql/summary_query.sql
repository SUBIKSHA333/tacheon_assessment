-- Summary: Average weather risk score and dominant marketing
-- recommendation per day for Chennai
SELECT
    DATE(timestamp)                        AS date,
    city,
    ROUND(AVG(temperature_c), 1)           AS avg_temp_c,
    ROUND(AVG(weather_risk_score), 2)      AS avg_risk_score,
    ROUND(MAX(precipitation_mm), 1)        AS max_precipitation_mm,
    COUNTIF(marketing_recommendation =
        'Good day for outdoor campaigns')  AS good_hours,
    COUNTIF(marketing_recommendation =
        'Consider indoor/digital campaigns') AS moderate_hours,
    COUNTIF(marketing_recommendation =
        'Pause outdoor, boost digital spend') AS bad_hours
FROM
    `fyndai-test-project.marketing_weather.hourly_conditions`
GROUP BY
    date, city
ORDER BY
    date DESC;

-- Sample output (8 rows):
-- date        | city    | avg_temp_c | avg_risk_score | max_precipitation_mm | good_hours | moderate_hours | bad_hours
-- 2026-05-29  | Chennai | 33.5       | 12.88          | 0.0                  | 4          | (scroll)       | (scroll)
-- 2026-05-28  | Chennai | 33.4       | 11.44          | 0.0                  | 10         | ...            | ...
-- 2026-05-27  | Chennai | 32.8       | 12.54          | 0.0                  | 7          | ...            | ...
-- 2026-05-26  | Chennai | 34.0       | 10.01          | 0.5                  | 11         | ...            | ...
-- 2026-05-25  | Chennai | 34.1       | 9.83           | 0.4                  | 15         | ...            | ...
-- 2026-05-24  | Chennai | 34.0       | 10.46          | 1.9                  | 11         | ...            | ...
-- 2026-05-23  | Chennai | 32.9       | 15.64          | 0.0                  | 1          | ...            | ...
-- 2026-05-22  | Chennai | 33.5       | 10.4           | 0.0                  | 12         | ...            | ...