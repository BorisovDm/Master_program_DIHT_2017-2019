USE hob201820_kkt;

DROP VIEW IF EXISTS task_3_view;


CREATE VIEW task_3_view AS
SELECT user_inn, date, SUM(total_sum) as total
FROM (
    SELECT user_inn, FROM_UNIXTIME(date, 'yyyy-MM-dd') AS date, total_sum
    FROM kkt_orc
    WHERE subtype = "receipt"
) t
GROUP BY user_inn, date;


SELECT A.user_inn, A.date
FROM task_3_view A JOIN (
    SELECT user_inn, MAX(total) AS total
    FROM task_3_view
    GROUP BY user_inn
) B
ON A.user_inn = B.user_inn AND A.total = B.total;
