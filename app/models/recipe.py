from datetime import datetime, timezone
from app.models import db

class Recipe(db.Model):
    __tablename__ = 'recipe'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(cls, title, ingredients, steps):
        new_recipe = cls(title=title, ingredients=ingredients, steps=steps)
        db.session.add(new_recipe)
        db.session.commit()
        return new_recipe

    @classmethod
    def get_all(cls):
        return db.session.query(cls).order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, recipe_id):
        return db.session.get(cls, recipe_id)

    @classmethod
    def search(cls, keyword):
        search_pattern = f"%{keyword}%"
        return db.session.query(cls).filter(
            db.or_(
                cls.title.ilike(search_pattern),
                cls.ingredients.ilike(search_pattern)
            )
        ).order_by(cls.created_at.desc()).all()

    def update(self, title=None, ingredients=None, steps=None):
        if title is not None:
            self.title = title
        if ingredients is not None:
            self.ingredients = ingredients
        if steps is not None:
            self.steps = steps
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
