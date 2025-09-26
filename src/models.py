from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorites: Mapped[list["Favorites"]] = relationship("Favorites", back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    terreno: Mapped[str] = mapped_column(String(20))
    favorites: Mapped[list["Favorites"]] = relationship("Favorites", back_populates="planet")

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "terreno": self.terreno
        }
class People (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    favorites: Mapped[list["Favorites"]] = relationship("Favorites", back_populates="person")
    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
class Favorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'), nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey('people.id'), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="favorites")
    planet: Mapped["Planets"] = relationship("Planets", back_populates="favorites")
    person: Mapped["People"] = relationship("People", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet": self.planet.serialize() if self.planet else None,
            "person": self.person.serialize() if self.person else None
        }