add jar /opt/cloudera/parcels/CDH/lib/hive/lib/json-serde-1.3.8-jar-with-dependencies.jar;

SET hive.cli.print.header=true;
SET mapred.input.dir.recursive=true;
SET hive.mapred.supports.subdirectories=true;


create database hob201820_kkt location '/tmp/hob201820_kkt_test’;
USE hob201820_kkt;


DROP TABLE IF EXISTS table_json;
CREATE EXTERNAL TABLE table_json (
    subtype STRING,
    content struct< userInn:STRING,
		    totalSum:INT,
		    dateTime:STRING
		  >
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
STORED AS TEXTFILE
LOCATION '/data/hive/fns';


SELECT subtype,
	content.userinn AS user_inn,
	content.totalsum AS total_sum,
	CAST(CAST(regexp_replace(content.dateTime, '[^\\d]', '') AS BIGINT) / 1000 AS INT) AS date
FROM table_json LIMIT 100;
