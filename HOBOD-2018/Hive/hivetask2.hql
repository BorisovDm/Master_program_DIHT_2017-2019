USE hob201820_kkt;

DROP TABLE IF EXISTS kkt_text;
DROP TABLE IF EXISTS kkt_orc;
DROP TABLE IF EXISTS kkt_parquet;


CREATE TABLE kkt_text
STORED AS TEXTFILE AS

SELECT  content.userinn AS user_inn,
	subtype,
	content.totalsum AS total_sum,
	CAST(CAST(regexp_replace(content.dateTime, '[^\\d]', '') AS BIGINT) / 1000 AS INT) AS date
FROM table_json;


CREATE TABLE kkt_orc
STORED AS ORC AS
SELECT * FROM kkt_text;


CREATE TABLE kkt_parquet
STORED AS PARQUET AS
SELECT * FROM kkt_text;


SELECT user_inn
FROM (
    SELECT user_inn, SUM(total_sum) as total
    FROM kkt_text
    WHERE subtype = "receipt"
    GROUP BY user_inn
    ORDER BY total DESC
    LIMIT 1
) t;
--time: [44.492, 45.368, 45.086, 47.188, 44.703]
--mean: 45.3674
--std: 0.959325096096


SELECT user_inn
FROM (
    SELECT user_inn, SUM(total_sum) as total
    FROM kkt_orc
    WHERE subtype = "receipt"
    GROUP BY user_inn
    ORDER BY total DESC
    LIMIT 1
) t;
--time: [48.972, 55.574, 52.21, 41.657, 48.752]
--mean: 49.433
--std: 4.61662361472

SELECT user_inn
FROM (
    SELECT user_inn, SUM(total_sum) as total
    FROM kkt_parquet
    WHERE subtype = "receipt"
    GROUP BY user_inn
    ORDER BY total DESC
    LIMIT 1
) t;
--time: [51.825, 57.733, 50.391, 50.846, 47.309]
--mean: 51.6208
--std: 3.40895963015
