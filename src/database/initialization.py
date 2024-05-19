from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Создание движка базы данных
engine = create_engine('sqlite:///example.db', echo=True)

# Определение базового класса
Base = declarative_base()

# Определение модели таблиц
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    chat_id = Column(Integer)
    user_id = Column(Integer)

    tickets = relationship("Ticket", back_populates="user")

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email}, chat_id={self.chat_id}, user_id={self.user_id})>"

class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    status = Column(String)
    diagnosis = Column(String)
    request_subject = Column(String)
    request_body = Column(String)
    expert = Column(String)
    is_duplicate = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="tickets")

    def __repr__(self):
        return f"<Ticket(status='{self.status}', diagnosis={self.diagnosis}, request_subject={self.request_subject}, request_body={self.request_body}, expert={self.expert}, is_duplicate={self.is_duplicate})>"


# Очистка таблиц
Base.metadata.drop_all(engine)
# Создание таблиц
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Добавление данных в таблицу
user = User(name='Иван Иванов', email='ivan.ivanov@example.com', chat_id=15, user_id=1)
first_ticket = Ticket(status='активный', diagnosis='Рак груди', request_subject='Нужна консультация по лечению', request_body='Нужна консультация по назнанченному врачом лечению', expert='лимфолог', is_duplicate='0')
second_ticket = Ticket(status='активный', diagnosis='Рак груди', request_subject='Нужна консультация по лечению', request_body='Нужна консультация по назнанченному врачом лечению', expert='лимфолог', is_duplicate='1')
user.addresses = [first_ticket, second_ticket]
session.add(user)
session.commit()

# Запрос данных из таблиц
for user in session.query(User).all():
    print(user)
    for address in user.addresses:
        print(address)
