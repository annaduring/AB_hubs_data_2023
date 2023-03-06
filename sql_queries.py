sql_grant = """
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;"""



#create table in db to store part information
sql_create_parts = """
CREATE TABLE IF NOT EXISTS public.partsAB
  (
     uuid           TEXT NOT NULL,
     created        TIMESTAMP,
     updated        TIMESTAMP,
     queued         TIMESTAMP,
     units          TEXT,
     status         TEXT,
     time           NUMERIC,
     ingestion_time TIMESTAMP,
     PRIMARY KEY (uuid)
  )
"""

# Create table in database to store radius and length
sql_create_part_measures = """
CREATE TABLE IF NOT EXISTS public.part_measuresAB
  (
     measure_id  INTEGER NOT NULL,
     uuid        TEXT NOT NULL,
     radius      NUMERIC,
     length      NUMERIC,
     PRIMARY KEY (measure_id),
     CONSTRAINT fk_uuid FOREIGN KEY (uuid) REFERENCES public.parts(uuid)
  ); 
"""

# Copy csv into db table
sql_copy = "COPY {} FROM STDIN DELIMITER ',' CSV HEADER"

# Solution 1: suboptimal but provides more insights into which centers (radius/length) are faulty
solution_1 = """
SELECT uuid,
       radius,
       length,
       CASE
         WHEN length > ( radius * 2 * 10 )
              AND length < ( radius * 2 * 40 ) THEN 'X'
         ELSE ''
       END AS has_unreachable_hole_warning,
       CASE
         WHEN length > ( radius * 2 * 40 ) THEN 'X'
         ELSE ''
       END AS has_unreachable_hole_error
FROM   public.part_measuresab pm; 
"""

# Solution 2: Which part uuid we shuld receive warning/error?
solution_2 = """
WITH cte_meaures
     AS (SELECT uuid,
                radius,
                length,
                CASE
                  WHEN length > ( radius * 2 * 10 )
                       AND length < ( radius * 2 * 40 ) THEN 'X'
                  ELSE ''
                END AS has_unreachable_hole_warning,
                CASE
                  WHEN length > ( radius * 2 * 40 ) THEN 'X'
                  ELSE ''
                END AS has_unreachable_hole_error
         FROM   part_measuresab pm)
SELECT p.uuid,
       p.status,
       p.ingestion_time,
       has_unreachable_hole_warning,
       has_unreachable_hole_error
FROM   (SELECT uuid,
               has_unreachable_hole_warning,
               has_unreachable_hole_error
        FROM   (SELECT uuid,
                       has_unreachable_hole_warning,
                       has_unreachable_hole_error,
                       Row_number()
                         OVER (
                           partition BY uuid
                           ORDER BY CASE WHEN has_unreachable_hole_error = 'X'
                         THEN 1
                         WHEN has_unreachable_hole_warning = 'X' THEN 2 ELSE 3 END )
                       AS
                       priority
                FROM   cte_meaures) AS subquery
        WHERE  priority = 1) AS sub_priority
       RIGHT JOIN partsab p
               ON sub_priority.uuid = p.uuid;
"""