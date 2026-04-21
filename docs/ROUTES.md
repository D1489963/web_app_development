# 食譜收藏系統 - 路由與頁面設計 (ROUTES)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 (View) | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 / 食譜總覽 | GET | `/` | `index.html` | 顯示所有食譜列表（支援 ?q= 關鍵字搜尋） |
| 新增食譜頁面 | GET | `/recipe/create` | `create.html` | 顯示新增食譜表單 |
| 建立食譜 | POST | `/recipe/create` | — | 接收表單，存入資料庫，並重導向至首頁 |
| 食譜詳情 | GET | `/recipe/<id>` | `detail.html` | 顯示單一筆食譜的詳細材料與步驟 |
| 編輯食譜頁面 | GET | `/recipe/<id>/edit` | `edit.html` | 顯示填有既有食譜內容的編輯表單 |
| 更新食譜 | POST | `/recipe/<id>/edit` | — | 接收更新的表單，更新後重導向至該食譜詳情頁 |
| 刪除食譜 | POST | `/recipe/<id>/delete` | — | 刪除指定食譜，完成後重導向至首頁 |

## 2. 每個路由的詳細說明

### 首頁 / 食譜總覽 (`GET /`)
- **輸入**: URL Query Parameter `q` (字串，可選) 
- **處理邏輯**: 
  - 檢查是否有傳入 `q`
  - 如果有，呼叫 `Recipe.search(q)`
  - 如果沒有，呼叫 `Recipe.get_all()`
- **輸出**: 渲染 `index.html`，傳遞 `recipes` 列表與當前 `q`。
- **錯誤處理**: 若搜尋無結果，則列表中顯示「無符合結果」，不報錯。

### 新增食譜頁面 (`GET /recipe/create`)
- **輸入**: 無
- **處理邏輯**: 準備空白表單
- **輸出**: 渲染 `create.html`
- **錯誤處理**: 無特殊錯誤。

### 建立食譜 (`POST /recipe/create`)
- **輸入**: Form Data 包含 `title`, `ingredients`, `steps`
- **處理邏輯**:
  - 驗證必填欄位
  - 呼叫 `Recipe.create(title, ingredients, steps)`
- **輸出**: HTTP 302 重導向回 `/`
- **錯誤處理**: 如果欄位未填寫，可以使用 `flash()` 提示訊息，重新渲染 `create.html` 並保留已輸入內容。

### 食譜詳情 (`GET /recipe/<id>`)
- **輸入**: URL Path Variable `id` (整數)
- **處理邏輯**: 呼叫 `Recipe.get_by_id(id)`
- **輸出**: 渲染 `detail.html`，傳遞 `recipe` 物件。
- **錯誤處理**: 若回傳 `None`，回傳 404 Not Found 錯誤回應。

### 編輯食譜頁面 (`GET /recipe/<id>/edit`)
- **輸入**: URL Path Variable `id` (整數)
- **處理邏輯**: 呼叫 `Recipe.get_by_id(id)`，取得原本資料
- **輸出**: 渲染 `edit.html`，傳遞 `recipe` 物件用於帶入預設值。
- **錯誤處理**: 若回傳 `None`，回傳 404 Not Found 錯誤。

### 更新食譜 (`POST /recipe/<id>/edit`)
- **輸入**: 
  - URL Path Variable `id` (整數)
  - Form Data 包含 `title`, `ingredients`, `steps`
- **處理邏輯**:
  - 呼叫 `Recipe.get_by_id(id)`
  - 驗證資料是否齊全
  - 呼叫 `recipe.update(title, ingredients, steps)`
- **輸出**: HTTP 302 重導向回 `/recipe/<id>`
- **錯誤處理**: 找不到回傳 404，資料未填寫顯示 Flash 訊息並重新渲染 `edit.html`。

### 刪除食譜 (`POST /recipe/<id>/delete`)
- **輸入**: URL Path Variable `id` (整數)
- **處理邏輯**:
  - 呼叫 `Recipe.get_by_id(id)`
  - 呼叫 `recipe.delete()`
- **輸出**: HTTP 302 重導向回 `/`
- **錯誤處理**: 若找不到實體，回傳 404 錯誤。

## 3. Jinja2 模板清單

- `base.html`: 共用骨架範本。包含 HTML `<head>` 資訊、導覽列 (Navbar)、全域 CSS (符合 RWD) 以及頁尾。所有的頁面都會繼承它。
- `index.html`: (繼承 `base.html`) 首頁兼列表總覽，包含搜尋列與食譜清單卡片。
- `create.html`: (繼承 `base.html`) 提供新增食譜的 `<form>` 表單頁。
- `detail.html`: (繼承 `base.html`) 單一食譜完整展示頁面，並在這裡提供「編輯」與「刪除」按鈕（刪除為 POST form 以防 CSRF/意外刪除）。
- `edit.html`: (繼承 `base.html`) 提供編輯既有食譜詳細資料的 `<form>` 表單頁。

## 4. 路由骨架程式碼

（已實作於 `app/routes/recipe.py` 中，使用 Flask Blueprint `recipe_bp` 定義）
