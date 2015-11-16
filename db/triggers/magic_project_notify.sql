CREATE TRIGGER magic_project_notify
AFTER INSERT OR UPDATE OR DELETE ON magic_project
FOR EACH ROW EXECUTE PROCEDURE table_id_notify('events');