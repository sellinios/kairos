# backend/routers.py
class BackupRouter:
    """
    A router to control all database operations on models for different databases.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read models go to the backup database.
        """
        return 'backup'

    def db_for_write(self, model, **hints):
        """
        Attempts to write models go to the primary database.
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow any relation if a both models are in the same database.
        """
        db_obj1 = hints.get('instance') and hints['instance']._state.db or 'default'
        db_obj2 = hints.get('instance') and hints['instance']._state.db or 'default'
        if db_obj1 == db_obj2:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure that all models end up in the primary database.
        """
        return db == 'default'
