USE hob201820_kkt;

DROP VIEW IF EXISTS task_4_view;


CREATE VIEW task_4_view AS
SELECT user_inn, FROM_UNIXTIME(date, 'HH:mm:ss') AS time, total_sum
FROM kkt_orc
WHERE subtype = "receipt";


SELECT A.user_inn
FROM (
    SELECT user_inn, AVG(total_sum) AS avg_sum
    FROM task_4_view
    WHERE time < '13:00:00'
    GROUP BY user_inn
) A JOIN (
    SELECT user_inn, AVG(total_sum) AS avg_sum
    FROM task_4_view
    WHERE time >= '13:00:00'
    GROUP BY user_inn
) B ON A.user_inn = B.user_inn
WHERE A.avg_sum > B.avg_sum;
