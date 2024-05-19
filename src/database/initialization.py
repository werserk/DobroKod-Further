from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создание движка базы данных
engine = create_engine('sqlite:///example.db', echo=True)

# Определение базового класса
Base = declarative_base()

# Определение модели таблицы
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    status = Column(String)
    diagnosis = Column(String)
    name = Column(String)
    email = Column(String)
    chat_id = Column(Integer)
    user_id = Column(Integer)
    request_subject = Column(String)
    request_body = Column(String)
    expert = Column(String)
    is_duplicate = Column(String)

    def __repr__(self):
        return f"<User(status='{self.status}', diagnosis={self.diagnosis}, name={self.name}, email={self.email}, chat_id={self.chat_id}, user_id={self.user_id}, request_subject={self.request_subject}, request_body={self.request_body}, expert={self.expert}, is_duplicate={self.is_duplicate})>"


# Создание таблиц
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Добавление данных в таблицу
first_user = User(status='активный', diagnosis='Рак груди', name='Иван Иванов', email='ivan.ivanov@example.com', chat_id=15, user_id=1, request_subject='Нужна консультация по лечению', request_body='Нужна консультация по назнанченному врачом лечению', expert='лимфолог', is_duplicate='0')
second_user = User(status='активный', diagnosis='Рак груди', name='Иван Иванов', email='ivan.ivanov@example.com', chat_id=15, user_id=1, request_subject='Нужна консультация по лечению', request_body='Нужна консультация по назнанченному врачом лечению', expert='лимфолог', is_duplicate='1')
session.add(first_user)
session.add(second_user)
session.commit()

# Запрос данных из таблицы
for user in session.query(User).all():
    print(user)
