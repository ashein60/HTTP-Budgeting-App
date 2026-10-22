from backend.database_setup import init_all_dbs
from backend.tasks import init_tasks

# Required to access POST and GET requests
from backend.transactions import transaction_controller  # noqa

if __name__ == "__main__":
    init_tasks()
    init_all_dbs()
