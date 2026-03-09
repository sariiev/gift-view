INSERT INTO gift_model_price_bars (
    gift_id,
    model_id,
    "interval",
    timestamp,
    sales_count,
    volume_usd,
    min_price_usd,
    max_price_usd,
    median_price_usd
)
SELECT
    s.gift_id,
    s.model_id,
    :interval AS "interval",
    s.bucket as timestamp,
    COUNT(*) AS sales_count,
    SUM(s.price_usd) as volume_usd,
    MIN(s.price_usd) as min_price_usd,
    MAX(s.price_usd) as max_price_usd,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY s.price_usd) as median_price_usd
FROM (
    SELECT
        gift_id,
        model_id,
        price_usd,

        CASE
            WHEN :interval = '1h' THEN date_trunc('hour', s.timestamp)
            WHEN :interval = '4h' THEN date_trunc('hour', s.timestamp)
                - (EXTRACT(HOUR FROM s.timestamp)::int % 4) * INTERVAL '1 hour'
            WHEN :interval = '1d' THEN date_trunc('day', s.timestamp)
            WHEN :interval = '1w' THEN date_trunc('week', s.timestamp)
        END AS bucket

    FROM sales s
    WHERE
        s.price_usd IS NOT NULL
        AND s.timestamp >= :start
) s

GROUP BY
    s.gift_id,
    s.model_id,
    s.bucket

ON CONFLICT (gift_id, model_id, "interval", "timestamp")
DO UPDATE SET
    sales_count = EXCLUDED.sales_count,
    volume_usd = EXCLUDED.volume_usd,
    min_price_usd = EXCLUDED.min_price_usd,
    max_price_usd = EXCLUDED.max_price_usd,
    median_price_usd = EXCLUDED.median_price_usd;
