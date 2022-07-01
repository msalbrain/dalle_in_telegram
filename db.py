from sqlalchemy import Column, String, \
    Integer, select, func
from sqlalchemy.orm import declarative_base, sessionmaker, \
    relationship, Session
from sqlalchemy import create_engine, exc

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)
    last_time = Column(Integer, nullable=False, default=0)


    # def __repr__(self):
    #     return f"User(id={self.id!r}, email_address={self.email!r})"

engine = create_engine("sqlite:///main.db",echo=True, future=True)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    # db = SessionLocal()
    with Session(engine) as db:
        return db

def find_user_id(id, db: Session = get_db(),
              update=False) -> User | None | tuple[User, Session]:
    """
    please don't mind the type annotation of the function,
    this block from ported from somewhere else and i don't want to
    remove it bcos it makes the func look sophisticated

    """
    query = db.query(User).get(id)
    if update:
        return query, db
    return query


def find_user_chat_id(chat_id, db: Session = get_db(),
              update=False) -> User | None | tuple[User, Session]:
    """
    please don't mind the type annotation of the function,
    this block from ported from somewhere else and i don't want to
    remove it bcos it makes the func look sophisticated

    """
    query = db.query(User).where(User.chat_id == int(chat_id)).first()
    if update:
        return query, db
    return query


def insert_user(user: User, db: Session = get_db(), d=False) -> User | None:
    check_user = find_user_chat_id(chat_id=user.chat_id)

    if check_user:
        return None
    else:

        db.add(user)
        try:
            db.commit()
            db.refresh(user)
            if d:
                return user.__dict__
            else:
                return user

        except:
            return None

def find_all():
    u = get_db().query(User).count()
    # u_or = get_db().query(func.count(User.id)).scalar()
    print(u)
    if u < 2:
        return None
    elif u >= 2:
        return u






