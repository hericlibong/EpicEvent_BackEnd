from config import SessionLocal as Session

class BaseDAO:
    def __init__(self):
        self.session = Session()

    def commit(self):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        
    def close(self):
        self.session.close()