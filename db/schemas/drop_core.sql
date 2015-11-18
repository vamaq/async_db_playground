DROP SCHEMA core CASCADE;

--------------------------------------
--  Drop schema from search_path
DO
$do$
DECLARE
  search_path VARCHAR;
  current_database VARCHAR := current_database();
BEGIN
  SELECT array_to_string(ARRAY(
        SELECT DISTINCT trim(unnest(string_to_array(current_setting('search_path'), ',')))
        EXCEPT
        SELECT 'core'
  ),',') INTO search_path;
  EXECUTE 'ALTER DATABASE '||current_database||' SET search_path TO '||search_path;
END $do$;
