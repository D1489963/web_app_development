from flask import Blueprint

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/', methods=['GET'])
def index():
    """
    首頁 / 食譜總覽，支援搜尋 (?q=)
    
    輸入: URL Query Parameter 'q' (字串，可選)
    處理邏輯: 處理搜尋或取得全部資料
    輸出: 渲染 'index.html'
    """
    pass

@recipe_bp.route('/recipe/create', methods=['GET', 'POST'])
def create_recipe():
    """
    新增食譜頁面與邏輯 (GET 顯示表單, POST 接收並寫入)
    
    輸入: Form Data (title, ingredients, steps)
    處理邏輯: 驗證表單必填項並建立 Recipe
    輸出: GET 顯示 'create.html'，POST 後重導向至 '/'
    """
    pass

@recipe_bp.route('/recipe/<int:id>', methods=['GET'])
def detail(id):
    """
    食譜詳情
    
    輸入: Path Variable 'id'
    處理邏輯: 從資料庫依 id 取得 Recipe 實體
    輸出: 渲染 'detail.html' 或 404 Not Found
    """
    pass

@recipe_bp.route('/recipe/<int:id>/edit', methods=['GET', 'POST'])
def edit_recipe(id):
    """
    編輯食譜頁面與邏輯 (GET 顯示既有資料表單, POST 接收更新)
    
    輸入: Path Variable 'id', Form Data (title, ingredients, steps)
    處理邏輯: 驗證並更新 Recipe 實體
    輸出: GET 顯示 'edit.html'，POST 後重導向至 '/recipe/<id>' 或 404
    """
    pass

@recipe_bp.route('/recipe/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    刪除食譜
    
    輸入: Path Variable 'id'
    處理邏輯: 取得實體後刪除
    輸出: HTTP 302 重導向回 '/' 或 404 Not Found
    """
    pass
