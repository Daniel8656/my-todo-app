import flet as ft

def main(page: ft.Page):
    page.title = "每日代辦 (手機版預覽)"
    page.window.width = 380   
    page.window.height = 700  
    page.window.resizable = False 
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#FFF8DC" 

    # --- 1. 讀取記憶資料 ---
    # 嘗試從百寶袋拿出 "my_tasks" 這個資料。如果拿不到(第一次用)，就給它一個預設的空清單
    tasks_data = page.client_storage.get("my_tasks") 
    if tasks_data is None:
        tasks_data = {"Work": [], "Life": []}

    current_tab = "Work" 

    # --- 2. 準備 UI 元件 ---
    title = ft.Text("💼 工作任務", size=24, weight=ft.FontWeight.BOLD, color="#333333")
    
    new_task_input = ft.TextField(
        hint_text="新增任務...", 
        expand=True,
        border_color="#C2B280",
        cursor_color="#C2B280"
    )

    tasks_view = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    # --- 3. 核心畫面更新邏輯 ---
    def render_tasks():
        tasks_view.controls.clear() 
        
        def create_task_row(task_name):
            task_checkbox = ft.Checkbox(label=task_name, value=False, fill_color="#4CAF50")
            
            def delete_clicked(e):
                if task_name in tasks_data[current_tab]:
                    tasks_data[current_tab].remove(task_name)
                    # 【關鍵新增】資料改變了，馬上存進百寶袋！
                    page.client_storage.set("my_tasks", tasks_data)
                render_tasks() 

            delete_btn = ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINE, 
                icon_color="red",
                tooltip="刪除任務",
                on_click=delete_clicked
            )
            return ft.Row(controls=[task_checkbox, delete_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        for t in tasks_data[current_tab]:
            tasks_view.controls.append(create_task_row(t))
        
        title.value = "💼 工作任務" if current_tab == "Work" else "🏠 生活瑣事"
        page.update()

    # --- 4. 互動按鈕功能 ---
    def add_btn_clicked(e):
        if new_task_input.value:
            tasks_data[current_tab].append(new_task_input.value)
            # 【關鍵新增】資料增加了，馬上存進百寶袋！
            page.client_storage.set("my_tasks", tasks_data)
            
            new_task_input.value = "" 
            render_tasks() 
            new_task_input.focus()

    # --- 5. 底部導航列 ---
    def tab_changed(e):
        nonlocal current_tab 
        if e.control.selected_index == 0:
            current_tab = "Work"
        else:
            current_tab = "Life"
        render_tasks() 

    page.navigation_bar = ft.NavigationBar(
        selected_index=0, 
        on_change=tab_changed,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.WORK_OUTLINE, selected_icon=ft.Icons.WORK, label="工作"),
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="生活"),
        ],
        bgcolor="#FFF8DC", 
    )

    # --- 6. 組裝 ---
    page.add(
        title,
        ft.Row([new_task_input, ft.IconButton(icon=ft.Icons.SEND, on_click=add_btn_clicked)]),
        tasks_view
    )
    
    render_tasks()

ft.app(target=main, view=ft.WEB_BROWSER, host="192.168.0.106", port=8080)