from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.recipe import Recipe

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/', methods=['GET'])
def index():
    """
    首頁 / 食譜總覽，支援搜尋 (?q=)
    """
    q = request.args.get('q', '').strip()
    if q:
        recipes = Recipe.search(q)
    else:
        recipes = Recipe.get_all()
    return render_template('index.html', recipes=recipes, q=q)

@recipe_bp.route('/recipe/create', methods=['GET', 'POST'])
def create_recipe():
    """
    新增食譜頁面與邏輯 (GET 顯示表單, POST 接收並寫入)
    """
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        ingredients = request.form.get('ingredients', '').strip()
        steps = request.form.get('steps', '').strip()

        if not title or not ingredients or not steps:
            flash('所有欄位（名稱、材料、步驟）皆為必填。', 'danger')
            return render_template('create.html', title=title, ingredients=ingredients, steps=steps)

        new_recipe = Recipe.create(title=title, ingredients=ingredients, steps=steps)
        if new_recipe:
            flash('食譜新增成功！', 'success')
            return redirect(url_for('recipe.index'))
        else:
            flash('新增食譜時發生錯誤，請稍後再試。', 'danger')

    return render_template('create.html')

@recipe_bp.route('/recipe/<int:id>', methods=['GET'])
def detail(id):
    """
    食譜詳情
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('recipe.index'))
        
    return render_template('detail.html', recipe=recipe)

@recipe_bp.route('/recipe/<int:id>/edit', methods=['GET', 'POST'])
def edit_recipe(id):
    """
    編輯食譜頁面與邏輯 (GET 顯示既有資料表單, POST 接收更新)
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('recipe.index'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        ingredients = request.form.get('ingredients', '').strip()
        steps = request.form.get('steps', '').strip()

        if not title or not ingredients or not steps:
            flash('所有欄位（名稱、材料、步驟）皆為必填。', 'danger')
            # 臨時覆寫在記憶體中（尚未寫入 DB），以便表單重新渲染剛才輸入的內容
            recipe.title = title
            recipe.ingredients = ingredients
            recipe.steps = steps
            return render_template('edit.html', recipe=recipe)

        updated = recipe.update(title=title, ingredients=ingredients, steps=steps)
        if updated:
            flash('食譜更新成功！', 'success')
            return redirect(url_for('recipe.detail', id=id))
        else:
            flash('更新食譜時發生錯誤，請稍後再試。', 'danger')

    return render_template('edit.html', recipe=recipe)

@recipe_bp.route('/recipe/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    刪除食譜
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('recipe.index'))
        
    success = recipe.delete()
    if success:
        flash('食譜已成功刪除。', 'success')
    else:
        flash('刪除食譜時發生錯誤，請稍後再試。', 'danger')
        
    return redirect(url_for('recipe.index'))
