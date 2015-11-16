DROP SCHEMA core CASCADE;

--------------------------------------
--  Elimina el esquema del search_path
DO
$do$
DECLARE
  search_parth VARCHAR;
  current_database VARCHAR := current_database();
BEGIN
  SELECT array_to_string(ARRAY(
        SELECT DISTINCT trim(unnest(string_to_array(current_setting('search_path'), ',')))
        EXCEPT
        SELECT 'core'
  ),',') INTO search_parth;
  EXECUTE 'ALTER DATABASE '||current_database||' SET search_path TO '||search_parth;
END $do$;
