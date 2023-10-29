from api.models import User, Record


class ApiServices:

    @classmethod
    def create_user(cls, user_data: dict) -> User | Exception:
        pass

    @classmethod
    def update_user(cls, user_id: int, user_data: dict) -> User | Exception:
        pass

    @classmethod
    def delete_user(cls, user_id: int) -> str | Exception:
        pass

    @classmethod
    def add_record(cls, record_data: dict) -> Record | Exception:
        pass

    @classmethod
    def update_record(cls, record_id: int, record_data: dict) -> Record | Exception:
        pass

    @classmethod
    def delete_record(cls, record_id: int) -> str | Exception:
        pass
