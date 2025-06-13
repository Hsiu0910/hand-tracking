#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 猜數字遊戲 - GUI版本 (美化版)

import tkinter as tk
from tkinter import messagebox, ttk
import random
from tkinter.font import Font

class GuessNumberGame:
    def __init__(self, master):
        self.master = master
        self.master.title("猜數字遊戲 - 科技版")
        self.master.geometry("500x420")
        self.master.configure(bg="#1e272e")
        self.master.resizable(False, False)  # 固定視窗大小
        
        # 嘗試設定圓角視窗 (僅支援部分平台)
        try:
            self.master.attributes("-alpha", 0.97)  # 略微透明效果
        except:
            pass
        
        # 設定遊戲主題色彩 - 科技風格
        self.primary_color = "#007bff"  # 明亮藍色
        self.secondary_color = "#00d2d3"  # 青綠色
        self.bg_color = "#1e272e"  # 深灰背景
        self.accent_color = "#ff3f34"  # 鮮紅強調
        self.text_color = "#d1d8e0"  # 淡藍白文字
        self.frame_color = "#2C3A47"  # 稍深一點的框架顏色
        
        # 初始化遊戲數據
        self.min_number = 1
        self.max_number = 100
        self.target_number = random.randint(self.min_number, self.max_number)
        self.attempts = 0
        self.guess_history = []
        
        # 建立界面
        self.create_widgets()
        
        # 應用視窗居中
        self.center_window()
    
    def center_window(self):
        """使視窗在屏幕中央顯示"""
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def create_widgets(self):
        # 建立主框架
        main_frame = tk.Frame(self.master, bg=self.bg_color, padx=20, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 標題標籤
        title_frame = tk.Frame(main_frame, bg=self.bg_color)
        title_frame.pack(pady=(10, 5))
        
        title_label = tk.Label(
            title_frame, 
            text="猜數字遊戲", 
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg=self.primary_color,
        )
        title_label.pack()
        
        # 分隔線
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill='x', pady=5)
        
        # 遊戲說明
        instruction_text = f"系統已生成一個{self.min_number}到{self.max_number}之間的隨機數值，\n請輸入您的預測值："
        instruction_label = tk.Label(
            main_frame, 
            text=instruction_text,
            font=("Consolas", 12),
            bg=self.bg_color,
            fg=self.text_color,
            pady=5
        )
        instruction_label.pack()
        
        # 信息框架 (包含範圍和嘗試次數)
        info_frame = tk.Frame(main_frame, bg=self.bg_color)
        info_frame.pack(pady=5, fill='x')
        
        # 範圍提示 (左側)
        range_frame = tk.Frame(info_frame, bg=self.frame_color, padx=10, pady=5, 
                              relief=tk.GROOVE, bd=2)
        range_frame.pack(side=tk.LEFT, expand=True, fill='x')
        
        range_title = tk.Label(
            range_frame,
            text="< 當前範圍 >",
            font=("Courier", 10, "bold"),
            bg=self.frame_color,
            fg=self.primary_color
        )
        range_title.pack()
        
        self.range_label = tk.Label(
            range_frame, 
            text=f"{self.min_number} - {self.max_number}",
            font=("Courier", 16, "bold"),
            bg=self.frame_color,
            fg=self.text_color
        )
        self.range_label.pack()
        
        # 嘗試次數 (右側)
        attempts_frame = tk.Frame(info_frame, bg=self.frame_color, padx=10, pady=5,
                                 relief=tk.GROOVE, bd=2)
        attempts_frame.pack(side=tk.RIGHT, expand=True, fill='x')
        
        attempts_title = tk.Label(
            attempts_frame,
            text="< 猜測次數 >",
            font=("Courier", 10, "bold"),
            bg=self.frame_color,
            fg=self.primary_color
        )
        attempts_title.pack()
        
        self.attempts_label = tk.Label(
            attempts_frame, 
            text="0",
            font=("Courier", 16, "bold"),
            bg=self.frame_color,
            fg=self.text_color
        )
        self.attempts_label.pack()
        
        # 輸入區域框架
        input_area = tk.Frame(main_frame, bg=self.bg_color, pady=15)
        input_area.pack(fill='x')
        
        # 輸入框
        self.entry = tk.Entry(
            input_area, 
            font=("Arial", 18),
            width=8,
            justify='center',
            bd=2,
            relief=tk.SUNKEN
        )
        self.entry.pack(side=tk.LEFT, padx=(50, 10))
        self.entry.focus()  # 自動獲取焦點
        
        # 猜測按鈕
        guess_button_style = {'font': ("Arial", 14), 'width': 8, 
                             'bg': self.secondary_color, 'fg': 'black',
                             'activebackground': '#27ae60', 'activeforeground': 'black',
                             'relief': tk.RAISED, 'bd': 1}
        
        guess_button = tk.Button(
            input_area, 
            text="猜!", 
            command=self.check_guess,
            **guess_button_style
        )
        guess_button.pack(side=tk.LEFT, padx=(10, 50))
        
        # 歷史記錄框架
        history_frame = tk.LabelFrame(main_frame, text="猜測歷史", 
                                     font=("Arial", 11, "bold"),
                                     bg=self.bg_color, fg=self.primary_color,
                                     padx=10, pady=5)
        history_frame.pack(fill='x', pady=5)
        
        self.history_text = tk.Text(
            history_frame, 
            height=3, 
            width=40, 
            font=("Arial", 10),
            wrap=tk.WORD, 
            bd=1, 
            relief=tk.SUNKEN,
            bg='white'
        )
        self.history_text.pack(side=tk.LEFT, fill='both', expand=True)
        
        # 添加滾動條
        scrollbar = tk.Scrollbar(history_frame, command=self.history_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        self.history_text.config(yscrollcommand=scrollbar.set)
        self.history_text.config(state=tk.DISABLED)  # 設為只讀
        
        # 控制按鈕框架
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(pady=10)
        
        # 重新開始按鈕
        restart_button = tk.Button(
            button_frame, 
            text="重新開始遊戲", 
            font=("Arial", 12),
            command=self.restart_game,
            bg=self.primary_color,
            fg="black",
            padx=10,
            pady=5,
            activebackground='#2980b9',
            activeforeground='black',
            relief=tk.RAISED,
            bd=1
        )
        restart_button.pack()
        
        # 狀態欄
        status_frame = tk.Frame(main_frame, bg="#0a3d62", relief=tk.SUNKEN, bd=1)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = tk.Label(
            status_frame, 
            text="系統就緒... 等待輸入...", 
            font=("Consolas", 10),
            bg="#0a3d62",
            fg="#00d8d6",
            anchor=tk.W,
            padx=5,
            pady=2
        )
        self.status_label.pack(fill=tk.X)
        
        # 綁定回車鍵
        self.master.bind('<Return>', lambda event: self.check_guess())
    
    def update_history(self, guess, result):
        """更新猜測歷史"""
        self.history_text.config(state=tk.NORMAL)
        
        # 為不同結果設置不同顏色
        if "太小了" in result:
            tag = "low"
            color = "#e74c3c"  # 紅色
        elif "太大了" in result:
            tag = "high"
            color = "#3498db"  # 藍色
        else:
            tag = "correct"
            color = "#2ecc71"  # 綠色
        
        self.history_text.tag_configure(tag, foreground=color, font=("Arial", 10, "bold"))
        
        # 添加猜測記錄
        self.history_text.insert(tk.END, f"#{self.attempts}: ", "attempt")
        self.history_text.insert(tk.END, f"{guess} ", tag)
        self.history_text.insert(tk.END, f"({result})\n")
        
        # 保持顯示最新記錄
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)
    
    def check_guess(self):
        # 獲取用戶輸入
        try:
            guess_str = self.entry.get().strip()
            if not guess_str:
                self.status_label.config(text="請輸入一個數字！")
                return
                
            guess = int(guess_str)
            self.entry.delete(0, tk.END)  # 清空輸入框
            
            # 增加嘗試次數
            self.attempts += 1
            self.attempts_label.config(text=f"{self.attempts}")
            
            # 檢查猜測結果
            if guess < self.min_number or guess > self.max_number:
                self.status_label.config(text=f"請輸入{self.min_number}到{self.max_number}之間的數字！")
                self.attempts -= 1  # 不計入此次嘗試
                self.attempts_label.config(text=f"{self.attempts}")
                messagebox.showwarning("範圍錯誤", f"請輸入{self.min_number}到{self.max_number}之間的數字！")
            elif guess < self.target_number:
                result = "太小了"
                self.min_number = max(self.min_number, guess + 1)
                self.range_label.config(text=f"{self.min_number} - {self.max_number}")
                self.update_history(guess, result)
                self.status_label.config(text=f"{guess} 太小了，再試試看！")
                messagebox.showinfo("提示", f"{guess} 太小了，再試試看！")
            elif guess > self.target_number:
                result = "太大了"
                self.max_number = min(self.max_number, guess - 1)
                self.range_label.config(text=f"{self.min_number} - {self.max_number}")
                self.update_history(guess, result)
                self.status_label.config(text=f"{guess} 太大了，再試試看！")
                messagebox.showinfo("提示", f"{guess} 太大了，再試試看！")
            else:
                result = "猜對了！"
                self.update_history(guess, result)
                self.status_label.config(text=f"恭喜您猜對了！答案就是 {self.target_number}！")
                messagebox.showinfo("恭喜", f"恭喜您猜對了！答案就是 {self.target_number}！\n您總共猜了 {self.attempts} 次。")
                self.restart_game()
                
        except ValueError:
            self.status_label.config(text="請輸入有效的數字！")
            messagebox.showwarning("輸入錯誤", "請輸入有效的數字！")
    
    def restart_game(self):
        # 重置遊戲數據
        self.min_number = 1
        self.max_number = 100
        self.target_number = random.randint(self.min_number, self.max_number)
        self.attempts = 0
        
        # 更新界面
        self.range_label.config(text=f"{self.min_number} - {self.max_number}")
        self.attempts_label.config(text=f"{self.attempts}")
        self.entry.delete(0, tk.END)
        self.entry.focus()
        
        # 清空歷史記錄
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state=tk.DISABLED)
        
        # 更新狀態欄
        self.status_label.config(text="遊戲已重新開始！請猜一個新數字...")

def main():
    root = tk.Tk()
    app = GuessNumberGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()