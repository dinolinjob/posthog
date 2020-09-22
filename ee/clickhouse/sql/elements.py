from .clickhouse import STORAGE_POLICY, table_engine

DROP_ELEMENTS_TABLE_SQL = """
DROP TABLE elements
"""

ELEMENTS_TABLE_SQL = """
CREATE TABLE elements
(
    id UUID,
    text VARCHAR,
    tag_name VARCHAR,
    href VARCHAR,
    attr_id VARCHAR,
    attr_class Array(VARCHAR),
    nth_child Int32,
    nth_of_type Int32,
    attributes VARCHAR,
    order Int32,
    team_id Int32,
    created_at DateTime,
    elements_hash VARCHAR
) ENGINE = {engine} 
PARTITION BY toYYYYMM(created_at)
ORDER BY (team_id, elements_hash, order)
{storage_policy}
""".format(
    engine=table_engine("elements", "Replacing"), storage_policy=STORAGE_POLICY
)

INSERT_ELEMENTS_SQL = """
INSERT INTO elements SELECT 
    generateUUIDv4(), 
    %(text)s,
    %(tag_name)s,
    %(href)s,
    %(attr_id)s,
    %(attr_class)s,
    %(nth_child)s,
    %(nth_of_type)s,
    %(attributes)s,
    %(order)s,
    %(team_id)s,
    now(),
    %(elements_hash)s
"""

GET_ELEMENTS_BY_ELEMENTS_HASH_SQL = """
    SELECT 
        argMax(id, created_at) id,
        any(text) text,
        any(tag_name) tag_name,
        any(href) href,
        any(attr_id) attr_id,
        any(attr_class) attr_class,
        any(nth_child) nth_child,
        any(nth_of_type) nth_of_type,
        any(attributes) attributes,
        order,
        team_id,
        max(created_at) created_at_,
        elements_hash
    FROM elements
    WHERE elements_hash = %(elements_hash)s AND team_id=%(team_id)s
    GROUP BY team_id, elements_hash, order
    ORDER BY order
"""

GET_ALL_ELEMENTS_SQL = """
SELECT * FROM elements {final} ORDER by order ASC 
"""

ELEMENTS_WITH_ARRAY_PROPS = """
CREATE TABLE elements_with_array_props_view
(
    id UUID,
    text VARCHAR,
    tag_name VARCHAR,
    href VARCHAR,
    attr_id VARCHAR,
    attr_class Array(VARCHAR),
    nth_child Int32,
    nth_of_type Int32,
    attributes VARCHAR,
    order Int32,
    team_id Int32,
    created_at DateTime,
    elements_hash VARCHAR,
    array_attribute_keys Array(VARCHAR),
    array_attribute_values Array(VARCHAR)
) ENGINE = {engine}
PARTITION BY toYYYYMM(created_at)
ORDER BY (team_id, elements_hash, order)
{storage_policy}
""".format(
    engine=table_engine("elements_with_array_props_view"), storage_policy=STORAGE_POLICY
)

ELEMENTS_WITH_ARRAY_PROPS_MAT = """
CREATE MATERIALIZED VIEW elements_with_array_props_mv
TO elements_with_array_props_view
AS SELECT
id,
text,
tag_name,
href,
attr_id,
attr_class,
nth_child,
nth_of_type,
attributes,
order,
team_id,
elements_hash,
arrayMap(k -> k.1, JSONExtractKeysAndValues(attributes, 'varchar')) array_attribute_keys,
arrayMap(k -> k.2, JSONExtractKeysAndValues(attributes, 'varchar')) array_attribute_values
FROM elements
"""

ELEMENTS_PROPERTIES_MAT = """
CREATE MATERIALIZED VIEW elements_properties_view
ENGINE = MergeTree()
ORDER BY (key, value, id)
POPULATE
AS SELECT id,
team_id,
array_attribute_keys as key,
array_attribute_values as value
from elements_with_array_props_view
ARRAY JOIN array_attribute_keys, array_attribute_values
"""

ELEMENT_TAG_COUNT = """
SELECT concat('<', elements.tag_name, '> ', elements.text) AS tag_name,
       events.elements_hash as tag_hash,
       count(*) as tag_count
FROM events
JOIN elements ON (elements.elements_hash = events.elements_hash AND elements.order = toInt32(0))
WHERE events.team_id = %(team_id)s AND event = '$autocapture'
GROUP BY tag_name, tag_hash
ORDER BY tag_count desc, tag_name
LIMIT %(limit)s
"""
