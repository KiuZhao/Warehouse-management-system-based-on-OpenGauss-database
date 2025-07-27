import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import psycopg2, uuid, datetime

# 主题配色
BG_COLOR = "#1e1f29"     # 深灰蓝色背景
BTN_COLOR = "#4a7b9d"    # 深蓝色按钮
BTN_HOVER_COLOR = "#3a6a8d"  # 按钮悬停颜色
BTN_TEXT_COLOR = "#ffffff"   # 白色按钮文字
TITLE_COLOR = "#e0e0ff"      # 浅蓝色标题
TEXT_COLOR = "#d0d0d0"       # 浅灰色文本
ACCENT_COLOR = "#32cd32"     # 绿色强调色
FRAME_COLOR = "#2a2b36"      # 深灰色框架背景
ENTRY_BG = "#3a3b45"        # 深灰色输入框背景
ENTRY_FG = "#ffffff"        # 白色输入框文字

# 字体设置
TITLE_FONT = ("微软雅黑", 24, "bold")
HEADING_FONT = ("微软雅黑", 16, "bold")
LABEL_FONT = ("微软雅黑", 12)
BUTTON_FONT = ("微软雅黑", 12, "bold")
ENTRY_FONT = ("微软雅黑", 12)

# 按钮样式 - 现代风格
def styled_button(master, text, command=None, width=20, height=2):
    btn = tk.Button(
        master,
        text=text,
        command=command,
        width=width,
        height=height,
        font=BUTTON_FONT,
        bg=BTN_COLOR,
        fg=BTN_TEXT_COLOR,
        activebackground=BTN_HOVER_COLOR,
        activeforeground=BTN_TEXT_COLOR,
        bd=0,  # 无边框
        relief="flat",  # 扁平风格
        cursor="hand2",
        padx=10,
        pady=5
    )
    
    # 添加悬停效果
    def on_enter(e):
        btn.config(bg=BTN_HOVER_COLOR)
    
    def on_leave(e):
        btn.config(bg=BTN_COLOR)
    
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    return btn

# ========== 圆角框架类 ==========
class RoundedFrame(tk.Frame):
    def __init__(self, parent, radius=20, **kwargs):
        super().__init__(parent, **kwargs)
        self.radius = radius
        self.canvas = tk.Canvas(self, highlightthickness=0, bg=BG_COLOR)
        self.canvas.pack(fill="both", expand=True)
        self.bind("<Configure>", self._draw_frame)
        
    def _draw_frame(self, event=None):
        self.canvas.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        
        # 绘制圆角矩形
        self.canvas.create_arc((0, 0, self.radius*2, self.radius*2), 
                              start=90, extent=90, fill=FRAME_COLOR, outline=FRAME_COLOR)
        self.canvas.create_arc((width-self.radius*2, 0, width, self.radius*2), 
                              start=0, extent=90, fill=FRAME_COLOR, outline=FRAME_COLOR)
        self.canvas.create_arc((width-self.radius*2, height-self.radius*2, width, height), 
                              start=270, extent=90, fill=FRAME_COLOR, outline=FRAME_COLOR)
        self.canvas.create_arc((0, height-self.radius*2, self.radius*2, height), 
                              start=180, extent=90, fill=FRAME_COLOR, outline=FRAME_COLOR)
        
        # 绘制矩形部分
        self.canvas.create_rectangle(0, self.radius, width, height-self.radius, 
                                    fill=FRAME_COLOR, outline=FRAME_COLOR)
        self.canvas.create_rectangle(self.radius, 0, width-self.radius, height, 
                                    fill=FRAME_COLOR, outline=FRAME_COLOR)

# ========= 管理员登录界面 =========
def open_admin_login(parent_window):
    parent_window.destroy()  # 关闭主窗口

    login_win = tk.Tk()
    login_win.title("仓库管理员登录")
    login_win.geometry("1440x1080")
    login_win.resizable(False, False)
    login_win.configure(bg=BG_COLOR)

    # 上方留白
    tk.Frame(login_win, height=150, bg=BG_COLOR).pack()

    # 标题
    title = tk.Label(
        login_win,
        text="仓库管理员登录",
        font=("微软雅黑", 24, "bold"),
        pady=20,
        fg=TITLE_COLOR,
        bg=BG_COLOR
    )
    title.pack()

    # 表单框架
    form_frame = tk.Frame(login_win, bg=BG_COLOR)
    form_frame.pack(pady=30)

    # 管理员账号
    tk.Label(form_frame, text="管理员账号：", font=("微软雅黑", 12), bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, pady=10, sticky="e")
    entry_admin_id = tk.Entry(form_frame, width=30, font=("微软雅黑", 12))
    entry_admin_id.grid(row=0, column=1, pady=10)

    # 管理员密码
    tk.Label(form_frame, text="管理员密码：", font=("微软雅黑", 12), bg=BG_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, pady=10, sticky="e")
    entry_admin_pwd = tk.Entry(form_frame, width=30, font=("微软雅黑", 12), show="*")
    entry_admin_pwd.grid(row=1, column=1, pady=10)

    btn_frame = tk.Frame(login_win, bg=BG_COLOR)
    btn_frame.pack(pady=100)

    # 登录按钮
    def login_action():
        admin_id = entry_admin_id.get().strip()
        admin_pwd = entry_admin_pwd.get().strip()
        
        def open_admin_dashboard(admin_id):
            dash = tk.Tk()
            dash.title("仓库管理系统后台")
            dash.geometry("1440x1080")
            dash.configure(bg=BG_COLOR)
            # 标题
            tk.Label(
                dash,
                text=f"欢迎，管理员 {admin_id}",
                font=("微软雅黑", 20, "bold"),
                bg=BG_COLOR,
                fg=TITLE_COLOR
            ).pack(pady=60)

            # 按钮容器
            btn_frame = tk.Frame(dash, bg=BG_COLOR)
            btn_frame.pack()

            def open_logs_management(admin_id):
                dash.destroy()
                manage_win = tk.Tk()
                manage_win.title("日志管理")
                manage_win.geometry("1440x1080")
                manage_win.configure(bg=BG_COLOR)

                tk.Label(
                    manage_win, 
                    text="日志管理", 
                    font=("微软雅黑", 20, "bold"), 
                    bg=BG_COLOR, 
                    fg=TITLE_COLOR
                ).pack(pady=20)

                # 日志表格
                columns = ["日志ID", "操作人", "操作日期", "内容"]
                tree = ttk.Treeview(
                    manage_win, 
                    columns=columns, 
                    show="headings", 
                    height=10
                )
                
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, anchor="center", width=100)
                    
                tree.pack(pady=20, padx=20, fill="both", expand=True)

                # 表单区域（用于添加/编辑日志）
                form_frame = tk.Frame(manage_win, bg=BG_COLOR)
                form_frame.pack(pady=20, padx=30, fill="x")
                
                # 日志ID（可编辑）
                tk.Label(
                    form_frame, 
                    text="日志ID：", 
                    font=("微软雅黑", 12), 
                    bg=BG_COLOR, 
                    fg=TEXT_COLOR
                ).grid(row=0, column=0, padx=5, pady=5, sticky="e")
                
                log_id_var = tk.StringVar()
                log_id_entry = tk.Entry(
                    form_frame, 
                    textvariable=log_id_var, 
                    font=("微软雅黑", 12)
                )
                log_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
                
                # 操作日期
                tk.Label(
                    form_frame, 
                    text="操作日期：", 
                    font=("微软雅黑", 12), 
                    bg=BG_COLOR, 
                    fg=TEXT_COLOR
                ).grid(row=1, column=0, padx=5, pady=5, sticky="e")
                
                date_var = tk.StringVar(value=datetime.date.today().strftime("%Y-%m-%d"))
                date_entry = tk.Entry(
                    form_frame, 
                    textvariable=date_var, 
                    font=("微软雅黑", 12)
                )
                date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
                
                # 内容
                tk.Label(
                    form_frame, 
                    text="日志内容：", 
                    font=("微软雅黑", 12), 
                    bg=BG_COLOR, 
                    fg=TEXT_COLOR
                ).grid(row=2, column=0, padx=5, pady=5, sticky="ne")
                
                content_var = tk.StringVar()
                content_entry = tk.Entry(
                    form_frame, 
                    textvariable=content_var, 
                    width=40,
                    font=("微软雅黑", 12)
                )
                content_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w", columnspan=2)

                # 按钮区域
                btn_frame = tk.Frame(manage_win, bg=BG_COLOR)
                btn_frame.pack(pady=20)
                
                def clear_form():
                    log_id_var.set("")
                    date_var.set(datetime.date.today().strftime("%Y-%m-%d"))
                    content_var.set("")
                
                def add_log():
                    log_id = log_id_var.get().strip()
                    date = date_var.get()
                    content = content_var.get().strip()
                    
                    if not content:
                        messagebox.showwarning("警告", "日志内容不能为空")
                        return
                    
                    try:
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        
                        # 如果提供了日志ID，检查是否已存在
                        if log_id:
                            cur.execute("SELECT * FROM operation_logs WHERE log_id = %s", (log_id,))
                            if cur.fetchone():
                                messagebox.showwarning("警告", "该日志ID已存在")
                                return
                        
                        # 插入日志记录
                        if log_id:
                            # 如果指定了ID，使用指定ID
                            cur.execute(
                                "INSERT INTO operation_logs (log_id, operator_username, operation_date, operation_content) VALUES (%s, %s, %s, %s)",
                                (log_id, admin_id, date, content)
                            )
                        else:
                            # 否则使用数据库自动生成的ID
                            cur.execute(
                                "INSERT INTO operation_logs (operator_username, operation_date, operation_content) VALUES (%s, %s, %s)",
                                (admin_id, date, content)
                            )
                        
                        conn.commit()
                        messagebox.showinfo("成功", "日志添加成功")
                        update_logs_table()
                        clear_form()
                    except Exception as e:
                        messagebox.showerror("错误", f"添加日志失败：{e}")
                    finally:
                        if cur: cur.close()
                        if conn: conn.close()
                
                def update_log():
                    original_log_id = log_id_var.get()  # 保存原始ID
                    if not original_log_id:
                        messagebox.showwarning("警告", "请选择要编辑的日志")
                        return
                    
                    new_log_id = log_id_var.get().strip()  # 获取用户输入的新ID
                    date = date_var.get()
                    content = content_var.get().strip()
                    
                    if not content:
                        messagebox.showwarning("警告", "日志内容不能为空")
                        return
                    
                    try:
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        
                        # 检查新ID是否已被使用（除了当前日志）
                        if new_log_id != original_log_id:
                            cur.execute("SELECT * FROM operation_logs WHERE log_id = %s", (new_log_id,))
                            if cur.fetchone():
                                messagebox.showwarning("警告", "该日志ID已被使用")
                                return
                        
                        # 更新日志记录，包括可能的ID修改
                        cur.execute(
                            "UPDATE operation_logs SET log_id = %s, operation_date = %s, operation_content = %s WHERE log_id = %s",
                            (new_log_id, date, content, original_log_id)
                        )
                        
                        conn.commit()
                        messagebox.showinfo("成功", "日志更新成功")
                        update_logs_table()
                        clear_form()
                    except Exception as e:
                        messagebox.showerror("错误", f"更新日志失败：{e}")
                    finally:
                        if cur: cur.close()
                        if conn: conn.close()
                
                def delete_log():
                    log_id = log_id_var.get()
                    if not log_id:
                        messagebox.showwarning("警告", "请选择要删除的日志")
                        return
                    
                    if not messagebox.askyesno("确认", "确定要删除这条日志吗？"):
                        return
                    
                    try:
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        cur.execute(
                            "DELETE FROM operation_logs WHERE log_id = %s",
                            (log_id,)
                        )
                        conn.commit()
                        messagebox.showinfo("成功", "日志删除成功")
                        update_logs_table()
                        clear_form()
                    except Exception as e:
                        messagebox.showerror("错误", f"删除日志失败：{e}")
                    finally:
                        if cur: cur.close()
                        if conn: conn.close()
                
                def on_log_select(event):
                    selected = tree.focus()
                    if not selected: 
                        clear_form()
                        return
                        
                    values = tree.item(selected, "values")
                    if values:
                        log_id_var.set(values[0])
                        date_var.set(values[2])
                        content_var.set(values[3])
                
                # 绑定选择事件
                tree.bind("<<TreeviewSelect>>", on_log_select)
                
                # 按钮
                tk.Button(
                    btn_frame, 
                    text="添加日志", 
                    command=add_log,
                    font=("微软雅黑", 12),
                    bg="#4CAF50",
                    fg="white",
                    padx=15,
                    pady=5
                ).pack(side="left", padx=10)
                
                tk.Button(
                    btn_frame, 
                    text="更新日志", 
                    command=update_log,
                    font=("微软雅黑", 12),
                    bg="#2196F3",
                    fg="white",
                    padx=15,
                    pady=5
                ).pack(side="left", padx=10)
                
                tk.Button(
                    btn_frame, 
                    text="删除日志", 
                    command=delete_log,
                    font=("微软雅黑", 12),
                    bg="#F44336",
                    fg="white",
                    padx=15,
                    pady=5
                ).pack(side="left", padx=10)
                
                tk.Button(
                    btn_frame, 
                    text="返回工作台", 
                    command=lambda: go_back(),
                    font=("微软雅黑", 12),
                    bg=BTN_COLOR,
                    fg="white",
                    padx=15,
                    pady=5
                ).pack(side="left", padx=10)

                # 更新日志表格
                def update_logs_table():
                    tree.delete(*tree.get_children())
                    try:
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        cur.execute("SELECT log_id, operator_username, operation_date, operation_content FROM operation_logs")
                        
                        for row in cur.fetchall():
                            tree.insert("", "end", values=row)
                            
                        cur.close()
                        conn.close()
                    except Exception as e:
                        messagebox.showerror("数据库错误", f"获取日志失败：{e}")

                # 返回工作台
                def go_back():
                    manage_win.destroy()
                    open_admin_dashboard(admin_id)

                # 初始化表格
                update_logs_table()
                manage_win.mainloop()

            # 打开用户管理页面
            def open_user_manage_page():
                user_win = tk.Tk()
                user_win.title("用户管理")
                user_win.geometry("1440x1080")
                user_win.configure(bg=BG_COLOR)

                # ---------- 标题 ----------
                tk.Label(user_win, text="用户管理", font=("微软雅黑", 20, "bold"), bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=20)

                # ---------- 输入表单 ----------
                form_frame = tk.Frame(user_win, bg=BG_COLOR)
                form_frame.pack(pady=10)

                # 输入框区域
                input_frame = tk.Frame(form_frame, bg=BG_COLOR)
                input_frame.pack(side="left", padx=20)

                fields = [
                    ("用户ID", "UserID"),
                    ("用户名", "Username"),
                    ("密码", "Password"),
                    ("姓名", "Name"),
                    ("联系方式", "ContactInfo"),
                    ("用户类型", "UserType")
                ]

                entry_vars = {}
                for idx, (label_text, field_name) in enumerate(fields):
                    tk.Label(
                        input_frame,
                        text=f"{label_text}：",
                        font=("微软雅黑", 12),
                        bg=BG_COLOR,
                        fg=TEXT_COLOR
                    ).grid(row=idx, column=0, pady=5, padx=5, sticky="e")

                    var = tk.StringVar()
                    if field_name == "UserType":
                        entry = ttk.Combobox(input_frame, textvariable=var, width=22, font=("微软雅黑", 12))
                        entry['values'] = ["System Admin", "Procurement Staff", "Warehouse Staff"]
                    else:
                        entry = tk.Entry(input_frame, textvariable=var, width=25, font=("微软雅黑", 12))
                    entry.grid(row=idx, column=1, pady=5, padx=5)
                    entry_vars[field_name] = var

                # 按钮区域
                button_frame = tk.Frame(form_frame, bg=BG_COLOR)
                button_frame.pack(side="left", padx=20)

                # 操作按钮
                styled_button(button_frame, "添加用户", lambda: insert_user()).pack(pady=5)
                styled_button(button_frame, "更新用户信息", lambda: update_user()).pack(pady=5)
                styled_button(button_frame, "删除用户", lambda: delete_user()).pack(pady=5)

                # ---------- 用户列表表格 ----------
                columns = ["用户ID", "用户名", "姓名", "联系方式", "用户类型"]
                tree = ttk.Treeview(user_win, columns=columns, show="headings", height=10)

                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, anchor="center", width=80)

                tree.pack(pady=20)

                # ---------- 返回按钮 ----------
                def go_back():
                    user_win.destroy()
                    open_admin_dashboard(admin_id)

                styled_button(user_win, "返回", lambda: go_back()).pack(pady=10)

                # ---------- 数据库操作函数 ----------
                def update_table():
                    tree.delete(*tree.get_children())
                    try:
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        cur.execute("""
                            SELECT u.user_id, u.username, u.name, u.contact_info, ut.user_type_name
                            FROM Users u
                            JOIN UserDetails ud ON u.user_id = ud.user_id
                            JOIN UserTypes ut ON ud.user_type_id = ut.user_type_id
                        """)
                        for row in cur.fetchall():
                            tree.insert("", "end", values=row)
                        cur.close()
                        conn.close()
                    except Exception as e:
                        messagebox.showerror("错误", f"数据库错误: {e}")
                
                def on_tree_select(event):
                    selected = tree.focus()
                    if not selected:
                        return
                    values = tree.item(selected, "values")
                    entry_vars["UserID"].set(values[0])
                    entry_vars["Username"].set(values[1])
                    entry_vars["Name"].set(values[2])
                    entry_vars["ContactInfo"].set(values[3])
                    entry_vars["UserType"].set(values[4])

                tree.bind("<<TreeviewSelect>>", on_tree_select)

                def insert_user():
                    try:
                        user_id = entry_vars["UserID"].get()
                        username = entry_vars["Username"].get()
                        password = entry_vars["Password"].get()
                        name = entry_vars["Name"].get()
                        contact_info = entry_vars["ContactInfo"].get()
                        user_type = entry_vars["UserType"].get()
                        
                        if not all([user_id, username, password, name, user_type]):
                            messagebox.showwarning("警告", "所有字段必须填写")
                            return
                            
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        
                        # 插入用户
                        cur.execute("""
                            INSERT INTO Users (user_id, username, password, name, contact_info)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (user_id, username, password, name, contact_info))
                        
                        # 获取用户类型ID
                        cur.execute("SELECT user_type_id FROM UserTypes WHERE user_type_name = %s", (user_type,))
                        user_type_id = cur.fetchone()[0]
                        
                        # 插入用户详情
                        cur.execute("""
                            INSERT INTO UserDetails (user_id, user_type_id)
                            VALUES (%s, %s)
                        """, (user_id, user_type_id))
                        
                        conn.commit()
                        cur.close()
                        conn.close()
                        
                        update_table()
                        messagebox.showinfo("成功", "用户添加成功！")
                    except Exception as e:
                        messagebox.showerror("错误", f"添加失败: {e}")

                def update_user():
                    try:
                        selected = tree.focus()
                        if not selected:
                            messagebox.showwarning("提示", "请选择要更新的用户")
                            return
                            
                        user_id = entry_vars["UserID"].get()
                        username = entry_vars["Username"].get()
                        password = entry_vars["Password"].get()
                        name = entry_vars["Name"].get()
                        contact_info = entry_vars["ContactInfo"].get()
                        user_type = entry_vars["UserType"].get()
                        
                        if not all([user_id, username, name, user_type]):
                            messagebox.showwarning("警告", "用户ID、用户名、姓名和用户类型必须填写")
                            return
                            
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        
                        # 更新用户表
                        if password:
                            cur.execute("""
                                UPDATE Users 
                                SET username=%s, password=%s, name=%s, contact_info=%s 
                                WHERE user_id=%s
                            """, (username, password, name, contact_info, user_id))
                        else:
                            cur.execute("""
                                UPDATE Users 
                                SET username=%s, name=%s, contact_info=%s 
                                WHERE user_id=%s
                            """, (username, name, contact_info, user_id))
                        
                        # 获取用户类型ID
                        cur.execute("SELECT user_type_id FROM UserTypes WHERE user_type_name = %s", (user_type,))
                        user_type_id = cur.fetchone()[0]
                        
                        # 更新用户详情表
                        cur.execute("""
                            UPDATE UserDetails 
                            SET user_type_id=%s 
                            WHERE user_id=%s
                        """, (user_type_id, user_id))
                        
                        conn.commit()
                        cur.close()
                        conn.close()
                        
                        update_table()
                        messagebox.showinfo("成功", "用户信息更新成功！")
                    except Exception as e:
                        messagebox.showerror("错误", f"更新失败: {e}")

                def delete_user():
                    try:
                        selected = tree.focus()
                        if not selected:
                            messagebox.showwarning("提示", "请选择要删除的用户")
                            return
                            
                        user_id = entry_vars["UserID"].get()
                        
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        
                        # 先删除用户详情
                        cur.execute("DELETE FROM UserDetails WHERE user_id = %s", (user_id,))
                        
                        # 再删除用户
                        cur.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
                        
                        conn.commit()
                        cur.close()
                        conn.close()
                        
                        update_table()
                        messagebox.showinfo("成功", "用户删除成功！")
                    except Exception as e:
                        messagebox.showerror("错误", f"删除失败: {e}")

                # 初始更新
                update_table()
            
            # 打开货物管理页面
            def open_goods_manage_page():
                goods_win = tk.Tk()
                goods_win.title("货物信息管理")
                goods_win.geometry("1440x1080")
                goods_win.configure(bg=BG_COLOR)

                # ---------- 标题 ----------
                tk.Label(goods_win, text="货物信息管理", font=("微软雅黑", 20, "bold"), bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=20)

                # ---------- 输入表单 ----------
                form_frame = tk.Frame(goods_win, bg=BG_COLOR)
                form_frame.pack(pady=10)

                # 输入框区域
                input_frame = tk.Frame(form_frame, bg=BG_COLOR)
                input_frame.pack(side="left", padx=20)

                fields = [
                    ("货物id", "goods_id"),
                    ("货物名称", "goods_name"),
                    ("产地", "origin"),
                    ("货物编码", "goods_code"),
                    ("货物数量", "number")
                ]

                entry_vars = {}
                for idx, (label_text, field_name) in enumerate(fields):
                    tk.Label(
                        input_frame,
                        text=f"{label_text}：",
                        font=("微软雅黑", 12),
                        bg=BG_COLOR,
                        fg=TEXT_COLOR
                    ).grid(row=idx, column=0, pady=5, padx=5, sticky="e")

                    var = tk.StringVar()
                    entry = tk.Entry(input_frame, textvariable=var, width=25, font=("微软雅黑", 12))
                    entry.grid(row=idx, column=1, pady=5, padx=5)
                    entry_vars[field_name] = var

                # 按钮区域
                button_frame = tk.Frame(form_frame, bg=BG_COLOR)
                button_frame.pack(side="left", padx=20)

                # 操作按钮
                styled_button(button_frame, "添加货物", lambda: insert_goods()).pack(pady=5)
                styled_button(button_frame, "更新货物信息", lambda: update_goods()).pack(pady=5)
                styled_button(button_frame, "删除货物", lambda: delete_goods()).pack(pady=5)

                # ---------- 货物列表表格 ----------
                columns = [label_text for idx, (label_text, field_name) in enumerate(fields)]
                tree = ttk.Treeview(goods_win, columns=columns, show="headings", height=10)

                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, anchor="center", width=80)

                tree.pack(pady=20)

                # ---------- 返回按钮 ----------
                def go_back():
                    goods_win.destroy()
                    open_admin_dashboard(admin_id)

                styled_button(goods_win, "返回", lambda: go_back()).pack(pady=10)

                # ---------- 数据库操作函数 ----------
                def update_table():
                    tree.delete(*tree.get_children())
                    try:
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        cur.execute("SELECT * FROM Goods")
                        for row in cur.fetchall():
                            tree.insert("", "end", values=row)
                        cur.close()
                        conn.close()
                    except Exception as e:
                        messagebox.showerror("错误", f"数据库错误: {e}")
                
                def on_tree_select(event):
                    selected = tree.focus()
                    if not selected:
                        return
                    values = tree.item(selected, "values")
                    for i, (_, field_name) in enumerate(fields):
                        entry_vars[field_name].set(values[i])

                tree.bind("<<TreeviewSelect>>", on_tree_select)

                def insert_goods():
                    try:
                        values = [entry_vars[f].get() for _, f in fields]
                        
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        cur.execute("INSERT INTO Goods VALUES (%s, %s, %s, %s, %s)", tuple(values))
                        conn.commit()
                        cur.close()
                        conn.close()
                        update_table()
                    except Exception as e:
                        messagebox.showerror("错误", f"添加失败: {e}")

                def update_goods():
                    try:
                        selected = tree.focus()
                        if not selected:
                            messagebox.showwarning("提示", "请选择要更新的货物")
                            return
                        selected_id = tree.item(selected)["values"][0]
                        
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        values = [entry_vars[f].get() for _, f in fields[1:]]  # 跳过货物ID
                        cur.execute("""
                            UPDATE Goods SET 
                                goods_name=%s, origin=%s, goods_code=%s, number=%s
                            WHERE goods_id=%s
                        """, (*values, selected_id))
                        conn.commit()
                        cur.close()
                        conn.close()
                        update_table()
                    except Exception as e:
                        messagebox.showerror("错误", f"更新失败: {e}")

                def delete_goods():
                    try:
                        selected = tree.focus()
                        if not selected:
                            messagebox.showwarning("提示", "请选择要删除的货物")
                            return
                        selected_id = tree.item(selected)["values"][0]
                        
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        cur.execute("DELETE FROM Goods WHERE goods_id = %s", (selected_id,))
                        conn.commit()
                        cur.close()
                        conn.close()
                        update_table()
                    except Exception as e:
                        messagebox.showerror("错误", f"删除失败: {e}")

                # 初始更新
                update_table()
            
            # 各按钮事件
            def open_user_manage():
                dash.destroy()
                open_user_manage_page()

            def open_goods_manage():
                dash.destroy()
                open_goods_manage_page()

            def go_back():
                dash.destroy()
                main()

            # 按钮摆放
            styled_button(btn_frame, "管理用户", open_user_manage).pack(pady=15)
            styled_button(btn_frame, "管理货物信息", open_goods_manage).pack(pady=15)
            styled_button(btn_frame, "日志管理", lambda: open_logs_management(admin_id)).pack(pady=10)
            styled_button(btn_frame, "返回", go_back).pack(pady=40)

            dash.mainloop()

        try:
            conn = psycopg2.connect(
                host="localhost",
                port=8888,
                database="warehousemanagementsystem",
                user="dbuser",
                password="Dbuser@1"
            )
            cur = conn.cursor()
            query = """
                SELECT u.user_id 
                FROM Users u
                JOIN UserDetails ud ON u.user_id = ud.user_id
                JOIN UserTypes ut ON ud.user_type_id = ut.user_type_id
                WHERE u.username = %s AND u.password = %s AND ut.user_type_name = 'System Admin'
            """
            cur.execute(query, (admin_id, admin_pwd))
            result = cur.fetchone()

            if result:
                login_win.destroy()
                open_admin_dashboard(admin_id)
            else:
                messagebox.showerror("登录失败", "账号或密码错误！")

            cur.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("数据库错误", str(e))

    styled_button(btn_frame, "登录", login_action).pack(pady=10)

    # 返回首页按钮
    def back_to_home():
        login_win.destroy()
        main()  # 重新打开主界面

    styled_button(btn_frame, "返回首页", back_to_home).pack(pady=10)

    login_win.mainloop()

# ========= 采购员工登录界面 =========
def open_procurement_login(parent_window):
    parent_window.destroy()  # 关闭主窗口

    login_win = tk.Tk()
    login_win.title("采购员工登录")
    login_win.geometry("1440x1080")
    login_win.resizable(False, False)
    login_win.configure(bg=BG_COLOR)

    # 上方留白
    tk.Frame(login_win, height=150, bg=BG_COLOR).pack()

    # 标题
    title = tk.Label(
        login_win,
        text="采购员工登录",
        font=("微软雅黑", 24, "bold"),
        pady=20,
        fg=TITLE_COLOR,
        bg=BG_COLOR
    )
    title.pack()

    # 表单框架
    form_frame = tk.Frame(login_win, bg=BG_COLOR)
    form_frame.pack(pady=30)

    # 采购员工账号
    tk.Label(form_frame, text="采购员工账号：", font=("微软雅黑", 12), bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, pady=10, sticky="e")
    entry_procurement_id = tk.Entry(form_frame, width=30, font=("微软雅黑", 12))
    entry_procurement_id.grid(row=0, column=1, pady=10)

    # 采购员工密码
    tk.Label(form_frame, text="采购员工密码：", font=("微软雅黑", 12), bg=BG_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, pady=10, sticky="e")
    entry_procurement_pwd = tk.Entry(form_frame, width=30, font=("微软雅黑", 12), show="*")
    entry_procurement_pwd.grid(row=1, column=1, pady=10)

    btn_frame = tk.Frame(login_win, bg=BG_COLOR)
    btn_frame.pack(pady=100)

    # 登录按钮
    def login_action():
        ps_id = entry_procurement_id.get().strip()
        ps_pwd = entry_procurement_pwd.get().strip()
        
        def open_procurement_dashboard(ps_id):
            dash = tk.Tk()
            dash.title("仓库管理系统后台")
            dash.geometry("1440x1080")
            dash.configure(bg=BG_COLOR)
            # 标题
            tk.Label(
                dash,
                text=f"欢迎，采购员工 {ps_id}",
                font=("微软雅黑", 20, "bold"),
                bg=BG_COLOR,
                fg=TITLE_COLOR
            ).pack(pady=60)

            # 按钮容器
            btn_frame = tk.Frame(dash, bg=BG_COLOR)
            btn_frame.pack()

            # 打开查询货物页面
            def open_goods_view(ps_id):
                dash.destroy()
                view_win = tk.Tk()
                view_win.title("货物查询")
                view_win.geometry("1440x1080")
                view_win.configure(bg=BG_COLOR)

                tk.Label(view_win, text="货物查询", font=("微软雅黑", 20, "bold"), bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=20)

                form_frame = tk.Frame(view_win, bg=BG_COLOR)
                form_frame.pack(pady=10)

                # 左侧搜索栏
                input_frame = tk.Frame(form_frame, bg=BG_COLOR)
                input_frame.pack(side="left", padx=20)

                search_var = tk.StringVar()
                tk.Label(input_frame, text="搜索：", font=("微软雅黑", 12), bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, pady=5, padx=5)
                tk.Entry(input_frame, textvariable=search_var, width=30, font=("微软雅黑", 12)).grid(row=0, column=1, pady=5, padx=5)

                # 右侧按钮
                button_frame = tk.Frame(form_frame, bg=BG_COLOR)
                button_frame.pack(side="left", padx=20)

                styled_button(button_frame, "查询", lambda: update_table()).pack(pady=5)
                styled_button(button_frame, "返回上级", lambda: go_back()).pack(pady=5)

                # 表格区域
                columns = ["货物id", "货物名称", "产地", "货物编码", "货物数量"]
                tree = ttk.Treeview(view_win, columns=columns, show="headings", height=15)

                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, anchor="center", width=80)

                tree.pack(pady=20)

                def update_table():
                    tree.delete(*tree.get_children())
                    keyword = search_var.get()
                    try:
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        sql = """
                            SELECT * FROM Goods
                            WHERE goods_id::text ILIKE %s OR goods_name ILIKE %s OR origin ILIKE %s OR goods_code ILIKE %s
                        """
                        params = tuple([f"%{keyword}%"] * 4)
                        cur.execute(sql, params)
                        for row in cur.fetchall():
                            tree.insert("", "end", values=row)
                        cur.close()
                        conn.close()
                    except Exception as e:
                        messagebox.showerror("数据库错误", f"错误信息：{e}")

                def go_back():
                    view_win.destroy()
                    open_procurement_dashboard(ps_id)

                update_table()
            
            # 打开添加货物页面
            def open_goods_manage_page():
                goods_win = tk.Tk()
                goods_win.title("添加货物")
                goods_win.geometry("1440x1080")
                goods_win.configure(bg=BG_COLOR)

                # ---------- 标题 ----------
                tk.Label(goods_win, text="货物信息管理", font=("微软雅黑", 20, "bold"), bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=20)

                # ---------- 输入表单 ----------
                form_frame = tk.Frame(goods_win, bg=BG_COLOR)
                form_frame.pack(pady=10)

                # 输入框区域
                input_frame = tk.Frame(form_frame, bg=BG_COLOR)
                input_frame.pack(side="left", padx=20)

                fields = [
                    ("货物id", "goods_id"),
                    ("货物名称", "goods_name"),
                    ("产地", "origin"),
                    ("货物编码", "goods_code"),
                    ("货物数量", "number")
                ]

                entry_vars = {}
                for idx, (label_text, field_name) in enumerate(fields):
                    tk.Label(
                        input_frame,
                        text=f"{label_text}：",
                        font=("微软雅黑", 12),
                        bg=BG_COLOR,
                        fg=TEXT_COLOR
                    ).grid(row=idx, column=0, pady=5, padx=5, sticky="e")

                    var = tk.StringVar()
                    entry = tk.Entry(input_frame, textvariable=var, width=25, font=("微软雅黑", 12))
                    entry.grid(row=idx, column=1, pady=5, padx=5)
                    entry_vars[field_name] = var

                # 按钮区域
                button_frame = tk.Frame(form_frame, bg=BG_COLOR)
                button_frame.pack(side="left", padx=20)

                # 操作按钮
                styled_button(button_frame, "添加货物", lambda: insert_goods()).pack(pady=5)
                #styled_button(button_frame, "更新货物信息", lambda: update_goods()).pack(pady=5)
                #styled_button(button_frame, "删除货物", lambda: delete_goods()).pack(pady=5)

                # ---------- 货物列表表格 ----------
                columns = [label_text for idx, (label_text, field_name) in enumerate(fields)]
                tree = ttk.Treeview(goods_win, columns=columns, show="headings", height=10)

                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, anchor="center", width=80)

                tree.pack(pady=20)

                # ---------- 返回按钮 ----------
                def go_back():
                    goods_win.destroy()
                    open_procurement_dashboard(ps_id)

                styled_button(goods_win, "返回", lambda: go_back()).pack(pady=10)

                # ---------- 数据库操作函数 ----------
                def update_table():
                    tree.delete(*tree.get_children())
                    try:
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        cur.execute("SELECT * FROM Goods")
                        for row in cur.fetchall():
                            tree.insert("", "end", values=row)
                        cur.close()
                        conn.close()
                    except Exception as e:
                        messagebox.showerror("错误", f"数据库错误: {e}")
                
                def on_tree_select(event):
                    selected = tree.focus()
                    if not selected:
                        return
                    values = tree.item(selected, "values")
                    for i, (_, field_name) in enumerate(fields):
                        entry_vars[field_name].set(values[i])

                tree.bind("<<TreeviewSelect>>", on_tree_select)

                def insert_goods():
                    try:
                        values = [entry_vars[f].get() for _, f in fields]
                        
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        cur.execute("INSERT INTO Goods VALUES (%s, %s, %s, %s, %s)", tuple(values))
                        conn.commit()
                        cur.close()
                        conn.close()
                        update_table()
                    except Exception as e:
                        messagebox.showerror("错误", f"添加失败: {e}")

                '''def update_goods():
                    try:
                        selected = tree.focus()
                        if not selected:
                            messagebox.showwarning("提示", "请选择要更新的货物")
                            return
                        selected_id = tree.item(selected)["values"][0]
                        
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        values = [entry_vars[f].get() for _, f in fields[1:]]  # 跳过货物ID
                        cur.execute("""
                            UPDATE Goods SET 
                                goods_name=%s, origin=%s, goods_code=%s, number=%s
                            WHERE goods_id=%s
                        """, (*values, selected_id))
                        conn.commit()
                        cur.close()
                        conn.close()
                        update_table()
                    except Exception as e:
                        messagebox.showerror("错误", f"更新失败: {e}")

                def delete_goods():
                    try:
                        selected = tree.focus()
                        if not selected:
                            messagebox.showwarning("提示", "请选择要删除的货物")
                            return
                        selected_id = tree.item(selected)["values"][0]
                        
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        cur.execute("DELETE FROM Goods WHERE goods_id = %s", (selected_id,))
                        conn.commit()
                        cur.close()
                        conn.close()
                        update_table()
                    except Exception as e:
                        messagebox.showerror("错误", f"删除失败: {e}")'''

                # 初始更新
                update_table()
            
            # 各按钮事件
            def open_goods_manage():
                dash.destroy()
                open_goods_manage_page()

            def go_back():
                dash.destroy()
                main()

            # 按钮摆放
            styled_button(btn_frame, "查询货物", lambda: open_goods_view(ps_id)).pack(pady=10)
            styled_button(btn_frame, "添加货物", open_goods_manage).pack(pady=15)
            styled_button(btn_frame, "返回", go_back).pack(pady=40)

            dash.mainloop()

        try:
            conn = psycopg2.connect(
                host="localhost",
                port=8888,
                database="warehousemanagementsystem",
                user="dbuser",
                password="Dbuser@1"
            )
            cur = conn.cursor()
            query = """
                SELECT u.user_id 
                FROM Users u
                JOIN UserDetails ud ON u.user_id = ud.user_id
                JOIN UserTypes ut ON ud.user_type_id = ut.user_type_id
                WHERE u.username = %s AND u.password = %s AND ut.user_type_name = 'Procurement Staff'
            """
            cur.execute(query, (ps_id, ps_pwd))
            result = cur.fetchone()

            if result:
                login_win.destroy()
                open_procurement_dashboard(ps_id)
            else:
                messagebox.showerror("登录失败", "账号或密码错误！")

            cur.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("数据库错误", str(e))

    styled_button(btn_frame, "登录", login_action).pack(pady=10)

    # 返回首页按钮
    def back_to_home():
        login_win.destroy()
        main()  # 重新打开主界面

    styled_button(btn_frame, "返回首页", back_to_home).pack(pady=10)

    login_win.mainloop()

# ========= 仓库员工登录界面 =========
def open_warehouse_login(parent_window):
    parent_window.destroy()
    login_win = tk.Tk()
    login_win.title("仓库员工登录")
    login_win.geometry("1440x1080")
    login_win.resizable(False, False)
    login_win.configure(bg=BG_COLOR)

    # 上方留白
    tk.Frame(login_win, height=150, bg=BG_COLOR).pack()

    # 标题
    title = tk.Label(
        login_win,
        text="仓库员工登录",
        font=("微软雅黑", 24, "bold"),
        pady=10,
        fg=TITLE_COLOR,
        bg=BG_COLOR
    )
    title.pack()

    # 表单区域
    form_frame = tk.Frame(login_win, bg=BG_COLOR)
    form_frame.pack(pady=30)

    tk.Label(form_frame, text="员工账号：", font=("微软雅黑", 12), bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, pady=10, sticky="e")
    entry_user_id = tk.Entry(form_frame, width=30, font=("微软雅黑", 12))
    entry_user_id.grid(row=0, column=1, pady=10)

    tk.Label(form_frame, text="员工密码：", font=("微软雅黑", 12), bg=BG_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, pady=10, sticky="e")
    entry_user_pwd = tk.Entry(form_frame, width=30, font=("微软雅黑", 12), show="*")
    entry_user_pwd.grid(row=1, column=1, pady=10)

    # 子页面
    def open_warehouse_dashboard(user_id):
        dash = tk.Tk()
        dash.title("仓库员工工作台")
        dash.geometry("1440x1080")
        dash.configure(bg=BG_COLOR)
        try:
            try:
                conn = psycopg2.connect(
                    host="localhost",
                    port=8888,
                    database="warehousemanagementsystem",
                    user="dbuser",
                    password="Dbuser@1"
                )
            except Exception as e:
                messagebox.showerror("数据库连接失败", f"错误信息：{e}")
                return
            cur = conn.cursor()
            cur.execute("SELECT name FROM Users WHERE username = %s", (user_id,))
            result = cur.fetchone()
            user_name = result[0].strip() if result else user_id
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("错误", f"获取用户名失败：{e}")
            user_name = user_id

        tk.Label(
                dash,
                text=f"欢迎，仓库员工{user_id}",
                font=("微软雅黑", 20, "bold"),
                bg=BG_COLOR,
                fg=TITLE_COLOR
            ).pack(pady=60)

        btn_frame = tk.Frame(dash, bg=BG_COLOR)
        btn_frame.pack(pady=80)

        # 打开货物管理页面
        def open_goods_manage_page():
                goods_win = tk.Tk()
                goods_win.title("货物修改和出仓")
                goods_win.geometry("1440x1080")
                goods_win.configure(bg=BG_COLOR)

                # ---------- 标题 ----------
                tk.Label(goods_win, text="货物修改和出仓", font=("微软雅黑", 20, "bold"), bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=20)

                # ---------- 输入表单 ----------
                form_frame = tk.Frame(goods_win, bg=BG_COLOR)
                form_frame.pack(pady=10)

                # 输入框区域
                input_frame = tk.Frame(form_frame, bg=BG_COLOR)
                input_frame.pack(side="left", padx=20)

                fields = [
                    
                    ("货物id", "goods_id"),
                    ("货物名称", "goods_name"),
                    ("产地", "origin"),
                    ("货物编码", "goods_code"),
                    ("货物数量", "number")
                ]

                entry_vars = {}
                for idx, (label_text, field_name) in enumerate(fields):
                    tk.Label(
                        input_frame,
                        text=f"{label_text}：",
                        font=("微软雅黑", 12),
                        bg=BG_COLOR,
                        fg=TEXT_COLOR
                    ).grid(row=idx, column=0, pady=5, padx=5, sticky="e")

                    var = tk.StringVar()
                    entry = tk.Entry(input_frame, textvariable=var, width=25, font=("微软雅黑", 12))
                    entry.grid(row=idx, column=1, pady=5, padx=5)
                    entry_vars[field_name] = var

                # 按钮区域
                button_frame = tk.Frame(form_frame, bg=BG_COLOR)
                button_frame.pack(side="left", padx=20)

                # 操作按钮
                #styled_button(button_frame, "添加货物", lambda: insert_goods()).pack(pady=5)
                styled_button(button_frame, "更新货物信息", lambda: update_goods()).pack(pady=5)
                styled_button(button_frame, "删除货物", lambda: delete_goods()).pack(pady=5)

                # ---------- 货物列表表格 ----------
                columns = [label_text for idx, (label_text, field_name) in enumerate(fields)]
                tree = ttk.Treeview(goods_win, columns=columns, show="headings", height=10)

                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, anchor="center", width=80)

                tree.pack(pady=20)

                # ---------- 返回按钮 ----------
                def go_back():
                    goods_win.destroy()
                    open_warehouse_dashboard(user_id)

                styled_button(goods_win, "返回", lambda: go_back()).pack(pady=10)

                # ---------- 数据库操作函数 ----------
                def update_table():
                    tree.delete(*tree.get_children())
                    try:
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        cur.execute("SELECT * FROM Goods")
                        for row in cur.fetchall():
                            tree.insert("", "end", values=row)
                        cur.close()
                        conn.close()
                    except Exception as e:
                        messagebox.showerror("错误", f"数据库错误: {e}")
                
                def on_tree_select(event):
                    selected = tree.focus()
                    if not selected:
                        return
                    values = tree.item(selected, "values")
                    for i, (_, field_name) in enumerate(fields):
                        entry_vars[field_name].set(values[i])

                tree.bind("<<TreeviewSelect>>", on_tree_select)

                '''def insert_goods():
                    try:
                        values = [entry_vars[f].get() for _, f in fields]
                        
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        cur.execute("INSERT INTO Goods VALUES (%s, %s, %s, %s, %s)", tuple(values))
                        conn.commit()
                        cur.close()
                        conn.close()
                        update_table()
                    except Exception as e:
                        messagebox.showerror("错误", f"添加失败: {e}")'''

                def update_goods():
                    try:
                        selected = tree.focus()
                        if not selected:
                            messagebox.showwarning("提示", "请选择要更新的货物")
                            return
                        selected_id = tree.item(selected)["values"][0]
                        
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        values = [entry_vars[f].get() for _, f in fields[1:]]  # 跳过货物ID
                        cur.execute("""
                            UPDATE Goods SET 
                                goods_name=%s, origin=%s, goods_code=%s, number=%s
                            WHERE goods_id=%s
                        """, (*values, selected_id))
                        conn.commit()
                        cur.close()
                        conn.close()
                        update_table()
                    except Exception as e:
                        messagebox.showerror("错误", f"更新失败: {e}")

                def delete_goods():
                    try:
                        selected = tree.focus()
                        if not selected:
                            messagebox.showwarning("提示", "请选择要删除的货物")
                            return
                        selected_id = tree.item(selected)["values"][0]
                        
                        conn = psycopg2.connect(
                            host="localhost",
                            port=8888,
                            database="warehousemanagementsystem",
                            user="dbuser",
                            password="Dbuser@1"
                        )
                        cur = conn.cursor()
                        cur.execute("DELETE FROM Goods WHERE goods_id = %s", (selected_id,))
                        conn.commit()
                        cur.close()
                        conn.close()
                        update_table()
                    except Exception as e:
                        messagebox.showerror("错误", f"删除失败: {e}")

                # 初始更新
                update_table()
    
        def open_goods_view(user_id):
            # 货物查询功能（保持不变）
            dash.destroy()
            view_win = tk.Tk()
            view_win.title("货物查询")
            view_win.geometry("1440x1080")
            view_win.configure(bg=BG_COLOR)

            tk.Label(view_win, text="货物查询", font=("微软雅黑", 20, "bold"), bg=BG_COLOR, fg=TITLE_COLOR).pack(pady=20)

            form_frame = tk.Frame(view_win, bg=BG_COLOR)
            form_frame.pack(pady=10)

            # 左侧搜索栏
            input_frame = tk.Frame(form_frame, bg=BG_COLOR)
            input_frame.pack(side="left", padx=20)

            search_var = tk.StringVar()
            tk.Label(input_frame, text="搜索：", font=("微软雅黑", 12), bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, pady=5, padx=5)
            tk.Entry(input_frame, textvariable=search_var, width=30, font=("微软雅黑", 12)).grid(row=0, column=1, pady=5, padx=5)

            # 右侧按钮
            button_frame = tk.Frame(form_frame, bg=BG_COLOR)
            button_frame.pack(side="left", padx=20)

            styled_button(button_frame, "查询", lambda: update_table()).pack(pady=5)
            styled_button(button_frame, "返回上级", lambda: go_back()).pack(pady=5)

            # 表格区域
            columns = ["货物id", "货物名称", "产地", "货物编码", "货物数量"]
            tree = ttk.Treeview(view_win, columns=columns, show="headings", height=15)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center", width=80)

            tree.pack(pady=20)

            def update_table():
                tree.delete(*tree.get_children())
                keyword = search_var.get()
                try:
                    conn = psycopg2.connect(
                        host="localhost",
                        port=8888,
                        database="warehousemanagementsystem",
                        user="dbuser",
                        password="Dbuser@1"
                    )
                    cur = conn.cursor()
                    sql = """
                        SELECT * FROM Goods
                        WHERE goods_id::text ILIKE %s OR goods_name ILIKE %s OR origin ILIKE %s OR goods_code ILIKE %s
                    """
                    params = tuple([f"%{keyword}%"] * 4)
                    cur.execute(sql, params)
                    for row in cur.fetchall():
                        tree.insert("", "end", values=row)
                    cur.close()
                    conn.close()
                except Exception as e:
                    messagebox.showerror("数据库错误", f"错误信息：{e}")

            def go_back():
                view_win.destroy()
                open_warehouse_dashboard(user_id)

            update_table()
        
        # 日志查看功能
        def open_logs_view(user_id):
            dash.destroy()
            logs_win = tk.Tk()
            logs_win.title("查看日志")
            logs_win.geometry("1440x1080")
            logs_win.configure(bg=BG_COLOR)

            tk.Label(
                logs_win, 
                text="查看日志", 
                font=("微软雅黑", 20, "bold"), 
                bg=BG_COLOR, 
                fg=TITLE_COLOR
            ).pack(pady=20)

            # 搜索框
            search_frame = tk.Frame(logs_win, bg=BG_COLOR)
            search_frame.pack(pady=10)
            
            tk.Label(
                search_frame, 
                text="搜索内容：", 
                font=("微软雅黑", 12), 
                bg=BG_COLOR, 
                fg=TEXT_COLOR
            ).grid(row=0, column=0, padx=5)
            
            search_var = tk.StringVar()
            search_entry = tk.Entry(
                search_frame, 
                textvariable=search_var, 
                width=30, 
                font=("微软雅黑", 12)
            )
            search_entry.grid(row=0, column=1, padx=5)
            
            tk.Button(
                search_frame, 
                text="搜索", 
                command=lambda: update_logs_table(), 
                font=("微软雅黑", 10),
                bg=BTN_COLOR,
                fg="white",
                padx=10
            ).grid(row=0, column=2, padx=10)

            # 日志表格
            columns = ["日志ID", "操作人", "操作日期", "内容"]
            tree = ttk.Treeview(
                logs_win, 
                columns=columns, 
                show="headings", 
                height=15
            )
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center", width=100)
                
            tree.pack(pady=20, padx=20, fill="both", expand=True)

            # 按钮区域
            btn_frame = tk.Frame(logs_win, bg=BG_COLOR)
            btn_frame.pack(pady=20)
            
            tk.Button(
                btn_frame, 
                text="返回工作台", 
                command=lambda: go_back(), 
                font=("微软雅黑", 12),
                bg=BTN_COLOR,
                fg="white",
                padx=15,
                pady=5
            ).pack(side="left", padx=10)

            # 更新日志表格
            def update_logs_table():
                tree.delete(*tree.get_children())
                keyword = search_var.get()
                try:
                    conn = psycopg2.connect(
                        host="localhost",
                        port=8888,
                        database="warehousemanagementsystem",
                        user="dbuser",
                        password="Dbuser@1"
                    )
                    cur = conn.cursor()
                    sql = """
                        SELECT log_id, operator_username, operation_date, operation_content
                        FROM operation_logs
                        WHERE 
                            log_id::text ILIKE %s OR 
                            operator_username ILIKE %s OR 
                            operation_date::text ILIKE %s OR 
                            operation_content ILIKE %s
                    """
                    params = tuple([f"%{keyword}%"] * 4)
                    cur.execute(sql, params)
                    
                    for row in cur.fetchall():
                        tree.insert("", "end", values=row)
                        
                    cur.close()
                    conn.close()
                except Exception as e:
                    messagebox.showerror("数据库错误", f"获取日志失败：{e}")

            # 返回工作台
            def go_back():
                logs_win.destroy()
                open_warehouse_dashboard(user_id)

            # 初始化表格
            update_logs_table()
            logs_win.mainloop()
        
        # 日志管理功能
        def open_logs_management(user_id):
            dash.destroy()
            manage_win = tk.Tk()
            manage_win.title("日志管理")
            manage_win.geometry("1440x1080")
            manage_win.configure(bg=BG_COLOR)

            tk.Label(
                manage_win, 
                text="日志管理", 
                font=("微软雅黑", 20, "bold"), 
                bg=BG_COLOR, 
                fg=TITLE_COLOR
            ).pack(pady=20)

            # 日志表格
            columns = ["日志ID", "操作人", "操作日期", "内容"]
            tree = ttk.Treeview(
                manage_win, 
                columns=columns, 
                show="headings", 
                height=10
            )
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center", width=100)
                
            tree.pack(pady=20, padx=20, fill="both", expand=True)

            # 表单区域（用于添加/编辑日志）
            form_frame = tk.Frame(manage_win, bg=BG_COLOR)
            form_frame.pack(pady=20, padx=30, fill="x")
            
            # 日志ID（可编辑）
            tk.Label(
                form_frame, 
                text="日志ID：", 
                font=("微软雅黑", 12), 
                bg=BG_COLOR, 
                fg=TEXT_COLOR
            ).grid(row=0, column=0, padx=5, pady=5, sticky="e")
            
            log_id_var = tk.StringVar()
            log_id_entry = tk.Entry(
                form_frame, 
                textvariable=log_id_var, 
                font=("微软雅黑", 12)
            )
            log_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
            
            # 操作日期
            tk.Label(
                form_frame, 
                text="操作日期：", 
                font=("微软雅黑", 12), 
                bg=BG_COLOR, 
                fg=TEXT_COLOR
            ).grid(row=1, column=0, padx=5, pady=5, sticky="e")
            
            date_var = tk.StringVar(value=datetime.date.today().strftime("%Y-%m-%d"))
            date_entry = tk.Entry(
                form_frame, 
                textvariable=date_var, 
                font=("微软雅黑", 12)
            )
            date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
            
            # 内容
            tk.Label(
                form_frame, 
                text="日志内容：", 
                font=("微软雅黑", 12), 
                bg=BG_COLOR, 
                fg=TEXT_COLOR
            ).grid(row=2, column=0, padx=5, pady=5, sticky="ne")
            
            content_var = tk.StringVar()
            content_entry = tk.Entry(
                form_frame, 
                textvariable=content_var, 
                width=40,
                font=("微软雅黑", 12)
            )
            content_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w", columnspan=2)

            # 按钮区域
            btn_frame = tk.Frame(manage_win, bg=BG_COLOR)
            btn_frame.pack(pady=20)
            
            def clear_form():
                log_id_var.set("")
                date_var.set(datetime.date.today().strftime("%Y-%m-%d"))
                content_var.set("")

            def go_back():
                manage_win.destroy()
                open_warehouse_dashboard(user_id)
            
            def add_log():
                log_id = log_id_var.get().strip()
                date = date_var.get()
                content = content_var.get().strip()

            
                
                if not content:
                    messagebox.showwarning("警告", "日志内容不能为空")
                    return
                
                try:
                    conn = psycopg2.connect(
                        host="localhost",
                        port=8888,
                        database="warehousemanagementsystem",
                        user="dbuser",
                        password="Dbuser@1"
                    )
                    cur = conn.cursor()
                    
                    # 如果提供了日志ID，检查是否已存在
                    if log_id:
                        cur.execute("SELECT * FROM operation_logs WHERE log_id = %s", (log_id,))
                        if cur.fetchone():
                            messagebox.showwarning("警告", "该日志ID已存在")
                            return
                    
                    # 插入日志记录
                    if log_id:
                        # 如果指定了ID，使用指定ID
                        cur.execute(
                            "INSERT INTO operation_logs (log_id, operator_username, operation_date, operation_content) VALUES (%s, %s, %s, %s)",
                            (log_id, user_id, date, content)
                        )
                    else:
                        # 否则使用数据库自动生成的ID
                        cur.execute(
                            "INSERT INTO operation_logs (operator_username, operation_date, operation_content) VALUES (%s, %s, %s)",
                            (user_id, date, content)
                        )
                    
                    conn.commit()
                    messagebox.showinfo("成功", "日志添加成功")
                    update_logs_table()
                    clear_form()
                except Exception as e:
                    messagebox.showerror("错误", f"添加日志失败：{e}")
                finally:
                    if cur: cur.close()
                    if conn: conn.close()
            
            def update_log():
                original_log_id = log_id_var.get()  # 保存原始ID
                if not original_log_id:
                    messagebox.showwarning("警告", "请选择要编辑的日志")
                    return
                
                new_log_id = log_id_var.get().strip()  # 获取用户输入的新ID
                date = date_var.get()
                content = content_var.get().strip()
                
                if not content:
                    messagebox.showwarning("警告", "日志内容不能为空")
                    return
                
                try:
                    conn = psycopg2.connect(
                        host="localhost",
                        port=8888,
                        database="warehousemanagementsystem",
                        user="dbuser",
                        password="Dbuser@1"
                    )
                    cur = conn.cursor()
                    
                    # 检查新ID是否已被使用（除了当前日志）
                    if new_log_id != original_log_id:
                        cur.execute("SELECT * FROM operation_logs WHERE log_id = %s", (new_log_id,))
                        if cur.fetchone():
                            messagebox.showwarning("警告", "该日志ID已被使用")
                            return
                    
                    # 更新日志记录，包括可能的ID修改
                    cur.execute(
                        "UPDATE operation_logs SET log_id = %s, operation_date = %s, operation_content = %s WHERE log_id = %s",
                        (new_log_id, date, content, original_log_id)
                    )
                    
                    conn.commit()
                    messagebox.showinfo("成功", "日志更新成功")
                    update_logs_table()
                    clear_form()
                except Exception as e:
                    messagebox.showerror("错误", f"更新日志失败：{e}")
                finally:
                    if cur: cur.close()
                    if conn: conn.close()
            
            def delete_log():
                log_id = log_id_var.get()
                if not log_id:
                    messagebox.showwarning("警告", "请选择要删除的日志")
                    return
                
                if not messagebox.askyesno("确认", "确定要删除这条日志吗？"):
                    return
                
                try:
                    conn = psycopg2.connect(
                        host="localhost",
                        port=8888,
                        database="warehousemanagementsystem",
                        user="dbuser",
                        password="Dbuser@1"
                    )
                    cur = conn.cursor()
                    cur.execute(
                        "DELETE FROM operation_logs WHERE log_id = %s",
                        (log_id,)
                    )
                    conn.commit()
                    messagebox.showinfo("成功", "日志删除成功")
                    update_logs_table()
                    clear_form()
                except Exception as e:
                    messagebox.showerror("错误", f"删除日志失败：{e}")
                finally:
                    if cur: cur.close()
                    if conn: conn.close()
            
            def on_log_select(event):
                selected = tree.focus()
                if not selected: 
                    clear_form()
                    return
                    
                values = tree.item(selected, "values")
                if values:
                    log_id_var.set(values[0])
                    date_var.set(values[2])
                    content_var.set(values[3])
            
            # 绑定选择事件
            tree.bind("<<TreeviewSelect>>", on_log_select)
            
            # 按钮
            tk.Button(
                btn_frame, 
                text="添加日志", 
                command=add_log,
                font=("微软雅黑", 12),
                bg="#4CAF50",
                fg="white",
                padx=15,
                pady=5
            ).pack(side="left", padx=10)
            
            tk.Button(
                btn_frame, 
                text="更新日志", 
                command=update_log,
                font=("微软雅黑", 12),
                bg="#2196F3",
                fg="white",
                padx=15,
                pady=5
            ).pack(side="left", padx=10)
            
            tk.Button(
                btn_frame, 
                text="删除日志", 
                command=delete_log,
                font=("微软雅黑", 12),
                bg="#F44336",
                fg="white",
                padx=15,
                pady=5
            ).pack(side="left", padx=10)
            
            tk.Button(
                btn_frame, 
                text="返回工作台", 
                command=lambda: go_back(),
                font=("微软雅黑", 12),
                bg=BTN_COLOR,
                fg="white",
                padx=15,
                pady=5
            ).pack(side="left", padx=10)

            # 更新日志表格
            def update_logs_table():
                tree.delete(*tree.get_children())
                try:
                    conn = psycopg2.connect(
                        host="localhost",
                        port=8888,
                        database="warehousemanagementsystem",
                        user="dbuser",
                        password="Dbuser@1"
                    )
                    cur = conn.cursor()
                    cur.execute("SELECT log_id, operator_username, operation_date, operation_content FROM operation_logs")
                    
                    for row in cur.fetchall():
                        tree.insert("", "end", values=row)
                        
                    cur.close()
                    conn.close()
                except Exception as e:
                    messagebox.showerror("数据库错误", f"获取日志失败：{e}")

            # 初始化表格
            update_logs_table()
            manage_win.mainloop()

        # 各按钮事件
        def open_goods_manage():
            dash.destroy()
            open_goods_manage_page()

        styled_button(btn_frame, "查询货物", lambda: open_goods_view(user_id)).pack(pady=10)
        styled_button(btn_frame, "货物修改和出仓", lambda: open_goods_manage()).pack(pady=15)
        styled_button(btn_frame, "查看日志", lambda: open_logs_view(user_id)).pack(pady=10)
        styled_button(btn_frame, "日志管理", lambda: open_logs_management(user_id)).pack(pady=10)
        styled_button(btn_frame, "退出登录", lambda: (dash.destroy(), main())).pack(pady=10)

    # 登录行为
    def login_action():
        user_id = entry_user_id.get()
        user_pwd = entry_user_pwd.get()
        try:
            conn = psycopg2.connect(
                host="localhost",
                port=8888,
                database="warehousemanagementsystem",
                user="dbuser",
                password="Dbuser@1"
            )
            cur = conn.cursor()
            query = """
                SELECT u.user_id 
                FROM Users u
                JOIN UserDetails ud ON u.user_id = ud.user_id
                JOIN UserTypes ut ON ud.user_type_id = ut.user_type_id
                WHERE u.username = %s AND u.password = %s AND ut.user_type_name = 'Warehouse Staff'
            """
            cur.execute(query, (user_id, user_pwd))
            result = cur.fetchone()
            if result:
                login_win.destroy()
                open_warehouse_dashboard(user_id)
            else:
                messagebox.showerror("登录失败", "账号或密码错误")
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("数据库错误", str(e))

    # 返回主界面
    def back_to_home():
        login_win.destroy()
        main()

    # 按钮底部对齐
    btn_frame = tk.Frame(login_win, bg=BG_COLOR)
    btn_frame.pack(pady=100)

    styled_button(btn_frame, "登录", login_action).pack(pady=10)
    styled_button(btn_frame, "返回首页", back_to_home).pack(pady=10)

    login_win.mainloop()

# ========= 主界面 =========
def main():
    parent_window = tk.Tk()
    parent_window.title("仓库管理系统")
    parent_window.geometry("1440x1080")
    parent_window.resizable(False, False)
    parent_window.configure(bg=BG_COLOR)

    # 空白Frame用于整体下移
    tk.Frame(parent_window, height=150, bg=BG_COLOR).pack()

    # 标题
    title = tk.Label(
        parent_window,
        text="仓库管理系统",
        font=("微软雅黑", 24, "bold"),
        pady=20,
        fg=TITLE_COLOR,
        bg=BG_COLOR
    )
    title.pack()

    # 按钮区
    button_frame = tk.Frame(parent_window, bg=BG_COLOR)
    button_frame.pack(pady=30)

    styled_button(button_frame, "管理员登录", lambda: open_admin_login(parent_window)).pack(pady=10)
    styled_button(button_frame, "采购员工登录", lambda: open_procurement_login(parent_window)).pack(pady=10)
    styled_button(button_frame, "仓库员工登录", lambda: open_warehouse_login(parent_window)).pack(pady=10)
    styled_button(button_frame, "退出系统", lambda: parent_window.destroy()).pack(pady=10)

    # 图片展示
    try:
        image = Image.open("warehouse.jpg")  # 仓库主题图片
        image = image.resize((450, 180))
        photo = ImageTk.PhotoImage(image)
        img_label = tk.Label(parent_window, image=photo, bg=BG_COLOR)
        img_label.image = photo
        img_label.pack(pady=30)
    except Exception as e:
        img_label = tk.Label(parent_window, text="（仓库图片加载失败）", fg="gray", bg=BG_COLOR)
        img_label.pack(pady=30)

    parent_window.mainloop()

# 启动程序
main()