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
    `your-gcp-project-id.marketing_weather.hourly_conditions`
GROUP BY
    date, city
ORDER BY
    date DESC;