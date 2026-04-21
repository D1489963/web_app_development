# 食譜收藏系統 - 系統架構設計 (ARCHITECTURE)

## 1. 技術架構說明
- **選用技術與原因**
  - **後端架構**：Python + Flask。輕量、靈活，開發速度快，非常適合實作小型專案與個人使用的 Web 應用。
  - **前端與渲染**：Jinja2 + HTML/CSS。不需要複雜的前後端分離框架（如 React/Vue），採用 Server-Side Rendering (SSR) 可簡化開發流程且能確保流暢體驗。
  - **資料庫**：SQLite + SQLAlchemy (ORM)。無須建置與維護獨立的資料庫伺服器，資料儲存在單一本地檔案中，方便個人備份。並且使用 SQLAlchemy ORM 可以提升資料庫操作效率，並自動防範 SQL Injection 等安全風險。
- **Flask MVC 模式說明**
  - **Model (資料模型)**：定義於 `models/`，負責與 SQLite 互動，設計食譜的屬性（包含食譜名稱、材料、步驟）並處理資料邏輯。
  - **View (視圖)**：定義於 `templates/`，使用 Jinja2 結合前端技術（HTML/CSS），負責將後端處理好的資料渲染為實體的網頁介面。必須實作 RWD 確保手機與平板上的瀏覽體驗。
  - **Controller (控制器)**：定義於 `routes/`，處理 URL 路由及接收使用者的 HTTP 請求（如新增食譜、搜尋表單提交），呼叫對應的 Model 取得資料後，將其傳遞給 View 進行渲染。

## 2. 專案資料夾結構

採用模組化的結構讓系統更具備可讀性與擴展性。

```text
web_app_development/
├── app/
│   ├── __init__.py      ← 設立及初始化 Flask App、載入配置與資料庫 (SQLAlchemy)
│   ├── models/          ← 資料庫模型 (Model)
│   │   ├── __init__.py
│   │   └── recipe.py    ← 食譜的 Table 結構與資料存取邏輯
│   ├── routes/          ← Flask 路由 (Controller)
│   │   ├── __init__.py
│   │   └── recipe.py    ← 處理食譜 CRUD（建立、搜尋、修改、刪除、檢視）
│   ├── templates/       ← Jinja2 HTML 模板 (View)
│   │   ├── base.html    ← 共用的版面與設計（導覽列、頁首、頁尾等）
│   │   ├── index.html   ← 首頁 / 食譜總覽與搜尋結果頁面
│   │   ├── create.html  ← 新增食譜頁面
│   │   ├── edit.html    ← 編輯食譜頁面
│   │   └── detail.html  ← 檢視個別食譜詳細內容的頁面
│   └── static/          ← CSS / JS 等靜態資源
│       ├── css/
│       │   └── style.css ← 負責排版、字型、顏色等，並實踐 RWD 設計
│       └── js/
│           └── main.js   ← 基礎的介面互動腳本（例如刪除時的二次確認等）
├── instance/
│   └── database.db      ← SQLite 資料庫檔案
├── docs/
│   ├── PRD.md           ← 產品需求文件
│   └── ARCHITECTURE.md  ← 系統架構設計文件 (本文件)
├── requirements.txt     ← 專案依賴套件 (Flask, Flask-SQLAlchemy 等)
└── run.py               ← 應用啟動入口，負責啟動 Flask 內建開發伺服器
```

## 3. 元件關係圖

```mermaid
flowchart TD
    Browser[瀏覽器 Browser\n(手機 / 電腦)]

    subgraph Flask Application [Flask 應用程式]
        Router[routes/recipe.py\n(路由控制器)]
        Model[models/recipe.py\n(資料模型)]
        View[templates/\n(Jinja2 模板)]
    end

    DB[(SQLite 資料庫\ninstance/database.db)]

    %% Requests
    Browser -- "1. HTTP Request (GET/POST)" --> Router
    Router -- "2. 操作或調用資料" --> Model
    Model -- "3. 增刪查改" --> DB
    DB -- "4. 回傳 ORM 實體資料" --> Model
    Model -- "5. 將物件交由 Controller 處理" --> Router
    Router -- "6. 資料參數結合模板" --> View
    View -- "7. 渲染出 HTML" --> Router
    Router -- "8. HTTP Response (HTML 解析)" --> Browser
```

## 4. 關鍵設計決策

1. **採用 Server-Side Rendering (SSR) 取代前後端分離 (SPA)**
   - **原因**：此系統為個人管理為主的小型專案。使用 Flask 搭配 Jinja2 能夠以單一語境（在一個系統內使用 Python 解決邏輯，Jinja2 配置介面）完成全棧任務。減少建置與部署 API 及前端框架的相關負擔，能有效縮短第一版的開發週期。
2. **選定 SQLAlchemy 作為核心 ORM 工具**
   - **原因**：雖然可以使用原生 `sqlite3` 模組寫 SQL 語句，但使用 Flask-SQLAlchemy 可以將資料抽象成直覺的 Python 物件，讓 CRUD 更加可讀好寫；同時 ORM 提供自動參數化查詢，天生可有效防範 SQL Injection 的資安攻擊。如果未來應用規模變大也可以極小幅修改後切換為 PostgreSQL。
3. **明確分離 Route (Controller) 與 Model 資料夾**
   - **原因**：為了避免日後代碼全部集中在 `app.py` 中變得雜亂無章（Spaghetti Code），此架構從一開始就設定好目錄切分。這有利於保持程式碼整潔，也方便後續支援標籤、分類或其他新模組的擴充。
4. **專注於基礎防護與行動端適應（RWD）**
   - **原因**：因 PRD 明確提及在「做菜時對照查閱」的情境，前端使用簡單的自定義 CSS 或是輕量的套件（如 Bootstrap5 網格）優先製作響應式頁面，這是一項高優先決策。並且在 Controller 端加入簡單的 HTML escape，透過 Jinja2 預設的自動逃脫 (autoescaping) 防範 XSS 攻擊。
