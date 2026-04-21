# 食譜收藏系統 - 流程圖設計 (FLOWCHART)

## 1. 使用者流程圖 (User Flow)

這個流程圖展示了使用者在網站中的主要操作路徑，包含瀏覽、尋找、新增、編輯與刪除食譜。

```mermaid
flowchart LR
    A([使用者造訪首頁]) --> B[首頁 - 食譜列表總覽]
    B --> C{選擇操作}
    
    C -->|尋找食譜| D[輸入關鍵字搜尋]
    D --> E[顯示搜尋結果列表]
    E --> C
    
    C -->|新增食譜| F[點擊新增按鈕]
    F --> G[進入新增表單頁]
    G --> H{填寫資料並送出}
    H -->|驗證失敗| G
    H -->|驗證成功| B
    
    C -->|檢視詳細| I[點擊食譜項目]
    I --> J[食譜詳細內容頁]
    
    J --> K{進階操作}
    K -->|編輯| L[進入編輯表單頁]
    L --> M{修改資料並送出}
    M -->|驗證失敗| L
    M -->|驗證成功| J
    
    K -->|刪除| N[點擊刪除按鈕]
    N --> O{確認刪除？}
    O -->|否| J
    O -->|是| P[執行刪除]
    P --> B
```

## 2. 系統序列圖 (Sequence Diagram)

這張序列圖展示了當使用者執行「新增食譜」時，系統前後端及資料庫的完整互動流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route
    participant Model as SQLAlchemy Model
    participant DB as SQLite
    
    User->>Browser: 點擊「新增食譜」，進入 /recipe/create
    Browser->>Route: GET /recipe/create
    Route-->>Browser: 回傳 create.html 渲染視圖
    
    User->>Browser: 填寫表單（名稱、材料、步驟）並送出
    Browser->>Route: POST /recipe/create (Form Data)
    
    Route->>Route: 後端初步驗證資料 (防範 XSS 等)
    alt 驗證失敗
        Route-->>Browser: 回傳錯誤訊息，停留在新增表單頁
    else 驗證成功
        Route->>Model: 建立 Recipe 物件實體
        Model->>DB: INSERT INTO recipe
        DB-->>Model: 寫入成功
        Model-->>Route: 回傳資料操作狀態
        Route-->>Browser: HTTP 302 重新導向至首頁 (/)
        Browser->>User: 顯示包含新食譜的總覽列表
    end
```

## 3. 功能清單對照表

根據 PRD 定義的使用需求與架構設計，以下是規劃對應的 URL 路徑與 HTTP 請求方法：

| 功能項目 | URL 路徑 | HTTP 方法 | 對應模板 (View) 或 處理邏輯 |
| :--- | :--- | :--- | :--- |
| **首頁 / 列表總覽** | `/` | GET | `index.html` - 取得所有食譜並顯示清單。 |
| **搜尋食譜** | `/?q=關鍵字` | GET | `index.html` - 解析網址的查詢參數，過濾顯示的結果。 |
| **進入新增表單頁** | `/recipe/create` | GET | `create.html` - 提供空白的新增表單。 |
| **執行新增表單** | `/recipe/create` | POST | 接收資料、驗證、寫入資料庫，完成後導回 `/`。 |
| **檢視食譜細節** | `/recipe/<id>` | GET | `detail.html` - 根據傳入的 ID，顯示此食譜之材料與步驟。 |
| **進入編輯表單頁** | `/recipe/<id>/edit` | GET | `edit.html` - 取得指定食譜的現有資料，並帶入表單中。 |
| **執行編輯表單** | `/recipe/<id>/edit` | POST | 接收更新的資料，寫入資料庫，完成後導引回 `/recipe/<id>`。 |
| **執行刪除食譜** | `/recipe/<id>/delete` | POST | 安全起見使用 POST，驗證後執行刪除，導引回首頁 `/`。 |
