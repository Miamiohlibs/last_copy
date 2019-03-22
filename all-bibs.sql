--all print bibs at Miami 

SELECT
*
--count(*)
--m.record_type_code || m.record_num || 'a'
FROM
sierra_view.bib_record AS b
JOIN
sierra_view.record_metadata AS m
ON
m.id = b.record_id
WHERE
m.campus_code = '' --exclude non-miami, already excludes deleted records as well
AND
b.bcode2 != '@'

--ORDER BY m. ASC
LIMIT 50