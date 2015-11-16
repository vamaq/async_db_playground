CREATE SCHEMA core; -- Crea el schema

--------------------------------------
--  Deja el nuevo schema como default
DO
$do$
DECLARE
  search_parth VARCHAR;
  current_database VARCHAR := current_database();
BEGIN
  SELECT array_to_string(ARRAY(
        SELECT DISTINCT trim(unnest(string_to_array(current_setting('search_path')||',core', ',')))
  ),',') INTO search_parth;
  EXECUTE 'ALTER DATABASE '||current_database||' SET search_path TO '||search_parth;
END $do$;

--------------------------------------
-- deja el schema seteado para el resto de la session.
SET SCHEMA 'core';