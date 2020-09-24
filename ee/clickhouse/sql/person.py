from .clickhouse import STORAGE_POLICY, table_engine

DROP_PERSON_TABLE_SQL = """
DROP TABLE person
"""

DROP_PERSON_DISTINCT_ID_TABLE_SQL = """
DROP TABLE person_distinct_id
"""

PERSONS_TABLE_SQL = """
CREATE TABLE person
(
    id UUID,
    created_at datetime,
    team_id Int32,
    properties VARCHAR,
    is_identified Boolean
) ENGINE = {engine} 
Order By (team_id, id)
{storage_policy}
""".format(
    engine=table_engine("person"), storage_policy=STORAGE_POLICY
)

GET_PERSON_SQL = """
SELECT * FROM person WHERE team_id = %(team_id)s
"""

PERSONS_DISTINCT_ID_TABLE_SQL = """
CREATE TABLE person_distinct_id
(
    distinct_id VARCHAR,
    person_id UUID,
    team_id Int32,
    created_at DateTime
) ENGINE = {engine} 
Order By (team_id, distinct_id)
{storage_policy}
""".format(
    engine=table_engine("person_distinct_id", "Replacing"), storage_policy=STORAGE_POLICY
)

GET_DISTINCT_IDS_SQL = """
SELECT * FROM person_distinct_id WHERE team_id = %(team_id)s
"""

GET_DISTINCT_IDS_SQL_BY_ID = """
SELECT * FROM person_distinct_id WHERE team_id = %(team_id)s AND person_id = %(person_id)s
"""

GET_PERSON_BY_DISTINCT_ID = """
SELECT
    person.*
FROM
    person
WHERE
    team_id = %(team_id)s
    AND id IN (
        SELECT
            argMax(person_id, created_at)
        FROM
            person_distinct_id
        WHERE
            distinct_id = %(distinct_id)s
        GROUP BY
            distinct_id
    )
"""

PERSON_DISTINCT_ID_EXISTS_SQL = """
SELECT count(*) FROM person_distinct_id inner join (SELECT arrayJoin({}) as distinct_id) as id_params ON id_params.distinct_id = person_distinct_id.distinct_id where person_distinct_id.team_id = %(team_id)s
"""

PERSON_EXISTS_SQL = """
SELECT count(*) FROM person where id = %(id)s
"""

INSERT_PERSON_SQL = """
INSERT INTO person SELECT %(id)s, now(), %(team_id)s, %(properties)s, 0
"""

INSERT_PERSON_DISTINCT_ID = """
INSERT INTO person_distinct_id SELECT %(distinct_id)s, %(person_id)s, %(team_id)s, now() VALUES
"""

UPDATE_PERSON_PROPERTIES = """
ALTER TABLE person UPDATE properties = %(properties)s where id = %(id)s
"""

UPDATE_PERSON_ATTACHED_DISTINCT_ID = """
ALTER TABLE person_distinct_id UPDATE person_id = %(person_id)s where distinct_id = %(distinct_id)s
"""

DELETE_PERSON_BY_ID = """
ALTER TABLE person DELETE where id = %(id)s
"""

UPDATE_PERSON_IS_IDENTIFIED = """
ALTER TABLE person UPDATE is_identified = %(is_identified)s where id = %(id)s
"""
