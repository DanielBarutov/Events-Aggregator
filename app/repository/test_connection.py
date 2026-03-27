from typing import Callable


def test_connection(db: Callable):
    result = db.execute("SELECT 1").scalar()
    print("Connection successful", result)
    return result
