from datetime import datetime, timezone
import logging
from sqlalchemy.exc import SQLAlchemyError
from app.models import db

logger = logging.getLogger(__name__)

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
        """
        新增一筆食譜記錄
        :param title: 食譜名稱 (str)
        :param ingredients: 材料清單 (str)
        :param steps: 烹飪步驟 (str)
        :return: 新建的 Recipe 物件，若發生錯誤則回傳 None
        """
        try:
            new_recipe = cls(title=title, ingredients=ingredients, steps=steps)
            db.session.add(new_recipe)
            db.session.commit()
            return new_recipe
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error creating recipe: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有食譜記錄
        :return: Recipe 物件陣列 (依照建立時間由新到舊排序)
        """
        try:
            return db.session.query(cls).order_by(cls.created_at.desc()).all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching all recipes: {e}")
            return []

    @classmethod
    def get_by_id(cls, recipe_id):
        """
        取得單筆食譜記錄
        :param recipe_id: 食譜的 Primary Key ID
        :return: Recipe 物件，找不到或錯誤則回傳 None
        """
        try:
            return db.session.get(cls, recipe_id)
        except SQLAlchemyError as e:
            logger.error(f"Error fetching recipe id {recipe_id}: {e}")
            return None

    @classmethod
    def search(cls, keyword):
        """
        透過關鍵字搜尋食譜標題與配方材料
        :param keyword: 欲搜尋之字串
        :return: 符合條件的 Recipe 物件陣列
        """
        if not keyword:
            return cls.get_all()
            
        try:
            search_pattern = f"%{keyword}%"
            return db.session.query(cls).filter(
                db.or_(
                    cls.title.ilike(search_pattern),
                    cls.ingredients.ilike(search_pattern)
                )
            ).order_by(cls.created_at.desc()).all()
        except SQLAlchemyError as e:
            logger.error(f"Error searching for keyword '{keyword}': {e}")
            return []

    def update(self, title=None, ingredients=None, steps=None):
        """
        更新此實體的記錄
        :param title: 新的食譜名稱 (可選)
        :param ingredients: 新的材料清單 (可選)
        :param steps: 新的烹飪步驟 (可選)
        :return: 更新後的 Recipe 物件本身，發生錯誤回傳 None
        """
        try:
            if title is not None:
                self.title = title
            if ingredients is not None:
                self.ingredients = ingredients
            if steps is not None:
                self.steps = steps
            db.session.commit()
            return self
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error updating recipe id {self.id}: {e}")
            return None

    def delete(self):
        """
        刪除此實體的記錄
        :return: 成功布林值 (True 代表成功)
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error deleting recipe id {self.id}: {e}")
            return False
