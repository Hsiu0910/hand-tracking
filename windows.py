#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 骰子比大小遊戲

import tkinter as tk
from tkinter import ttk, messagebox
import random
import os
import time

# 創建圓角按鈕的類
class RoundedButton(tk.Canvas):
    def __init__(self, parent, width, height, cornerradius, padding=0, color="#6c5ce7", text='', command=None, **kwargs):
        # 從 kwargs 中取出 font 和 fg 參數，以便它們不會傳遞給 Canvas 初始化
        self.font = kwargs.pop('font', ('微軟正黑體', 12)) if 'font' in kwargs else ('微軟正黑體', 12)
        self.fg_color = kwargs.pop('fg', 'white') if 'fg' in kwargs else 'white'
        
        # 創建 Canvas
        tk.Canvas.__init__(self, parent, borderwidth=0, 
            relief="flat", highlightthickness=0, **kwargs)
        self.command = command
        self.color = color

        if cornerradius > 0.5*width:
            cornerradius = 0.5*width
        if cornerradius > 0.5*height:
            cornerradius = 0.5*height

        # 繪製背景矩形和文字
        self.rect = self.create_rounded_rect(padding, padding, width+padding, height+padding, 
                                            cornerradius, fill=color, outline=color)
        self.text = self.create_text(width/2+padding, height/2+padding, text=text, 
                                     fill=self.fg_color, font=self.font)
        
        self.configure(width=width+2*padding, height=height+2*padding)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def create_rounded_rect(self, x1, y1, x2, y2, r=25, **kwargs):
        points = [
            x1+r, y1,
            x2-r, y1,
            x2, y1,
            x2, y1+r,
            x2, y2-r,
            x2, y2,
            x2-r, y2,
            x1+r, y2,
            x1, y2,
            x1, y2-r,
            x1, y1+r,
            x1, y1
        ]
        return self.create_polygon(points, **kwargs, smooth=True)
    
    def _on_press(self, event):
        darker_color = self._adjust_color(self.color, -20)
        self.itemconfig(self.rect, fill=darker_color, outline=darker_color)
    
    def _on_release(self, event):
        self.itemconfig(self.rect, fill=self.color, outline=self.color)
        if self.command is not None:
            self.command()
            
    def _on_enter(self, event):
        lighter_color = self._adjust_color(self.color, 10)
        self.itemconfig(self.rect, fill=lighter_color, outline=lighter_color)
        self.configure(cursor="hand2")
        
    def _on_leave(self, event):
        self.itemconfig(self.rect, fill=self.color, outline=self.color)
        self.configure(cursor="")
    
    def _adjust_color(self, color, amount):
        # 處理十六進制顏色
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            r = max(0, min(255, r + amount))
            g = max(0, min(255, g + amount))
            b = max(0, min(255, b + amount))
            
            return f'#{r:02x}{g:02x}{b:02x}'
        return color

class DiceCompareGame:
    def __init__(self, master):
        self.master = master
        self.master.title("骰子比大小遊戲")
        self.master.geometry("700x500")
        
        # 改用更柔和的配色方案
        self.bg_color = "#f5f6fa"  # 淺灰背景
        self.accent_color = "#6c5ce7"  # 柔和的紫色
        self.player1_color = "#74b9ff"  # 柔和的藍色
        self.player2_color = "#ff7675"  # 柔和的紅色
        self.text_color = "#2d3436"  # 深灰文字
        
        self.master.configure(bg=self.bg_color)
        self.master.resizable(False, False)  # 固定視窗大小
        
        # 遊戲狀態變數
        self.current_player = 1  # 1 for player 1, 2 for player 2
        self.compare_mode = "大"  # 默認比大
        self.player1_score = 0
        self.player2_score = 0
        self.rounds_played = 0
        self.max_rounds = 5  # 預設5輪遊戲
        
        # 設定樣式
        self.style = ttk.Style()
        self.style.configure("TRadiobutton", 
                            background=self.bg_color, 
                            foreground=self.text_color,
                            font=("微軟正黑體", 11))
        
        # 初始化 UI 元素引用為 None，防止引用錯誤
        self.status_label = None
        
        # 建立UI元件
        self.setup_ui()
        
    def setup_ui(self):
        # 標題標籤
        title_label = tk.Label(
            self.master, 
            text="骰子比大小遊戲", 
            font=("微軟正黑體", 24, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack(pady=10)
        
        # 玩家資訊框架
        players_frame = tk.Frame(self.master, bg=self.bg_color)
        players_frame.pack(fill="x", padx=20)
        
        # 玩家1資訊 - 使用更柔和的藍色
        self.player1_frame = tk.LabelFrame(
            players_frame, 
            text="玩家一", 
            font=("微軟正黑體", 12),
            bg=self.player1_color,
            fg="white",
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=10
        )
        self.player1_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        
        self.player1_dice_label = tk.Label(
            self.player1_frame,
            text="?",
            font=("Arial", 48, "bold"),
            bg=self.player1_color,
            fg="white",
            width=3,
            height=1
        )
        self.player1_dice_label.pack(pady=10)
        
        self.player1_score_label = tk.Label(
            self.player1_frame,
            text=f"分數: {self.player1_score}",
            font=("微軟正黑體", 12),
            bg=self.player1_color,
            fg="white"
        )
        self.player1_score_label.pack(pady=5)
        
        # 玩家2資訊 - 使用更柔和的紅色
        self.player2_frame = tk.LabelFrame(
            players_frame, 
            text="玩家二", 
            font=("微軟正黑體", 12),
            bg=self.player2_color,
            fg="white",
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=10
        )
        self.player2_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)
        
        self.player2_dice_label = tk.Label(
            self.player2_frame,
            text="?",
            font=("Arial", 48, "bold"),
            bg=self.player2_color,
            fg="white",
            width=3,
            height=1
        )
        self.player2_dice_label.pack(pady=10)
        
        self.player2_score_label = tk.Label(
            self.player2_frame,
            text=f"分數: {self.player2_score}",
            font=("微軟正黑體", 12),
            bg=self.player2_color,
            fg="white"
        )
        self.player2_score_label.pack(pady=5)
        
        # 選擇比較模式框架
        mode_frame = tk.Frame(self.master, bg=self.bg_color, padx=10, pady=5)
        mode_frame.pack(fill="x", padx=20, pady=10)
        
        mode_label = tk.Label(
            mode_frame,
            text="選擇比較模式:",
            font=("微軟正黑體", 12),
            bg=self.bg_color,
            fg=self.text_color
        )
        mode_label.pack(side="left", padx=10)
          # 比較模式選擇按鈕 - 先創建但不綁定命令
        self.bigger_button = ttk.Radiobutton(
            mode_frame, 
            text="比大", 
            value="大"
        )
        self.bigger_button.pack(side="left", padx=10)
        
        self.smaller_button = ttk.Radiobutton(
            mode_frame, 
            text="比小", 
            value="小"
        )
        self.smaller_button.pack(side="left", padx=10)
        
        # 當前遊戲狀態資訊
        self.status_label = tk.Label(
            self.master,
            text=f"現在是玩家 {self.current_player} 的回合 - 選擇比{self.compare_mode}",
            font=("微軟正黑體", 12),
            bg=self.bg_color,
            fg=self.accent_color
        )
        self.status_label.pack(pady=10)
        
        # 使用圓角按鈕
        self.roll_button = RoundedButton(
            self.master,
            width=120,
            height=40,
            cornerradius=20,
            padding=5,
            color=self.accent_color,
            text="擲骰子",
            font=("微軟正黑體", 16, "bold"),
            command=self.roll_dice,
            bg=self.bg_color
        )
        self.roll_button.pack(pady=20)
        
        # 回合與遊戲狀態
        self.round_label = tk.Label(
            self.master,
            text=f"回合: {self.rounds_played}/{self.max_rounds}",
            font=("微軟正黑體", 10),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.round_label.pack(pady=5)
        
        # 重新開始按鈕 - 使用圓角按鈕
        self.restart_button = RoundedButton(
            self.master,
            width=100,
            height=30,
            cornerradius=15,
            padding=2,
            color="#a29bfe",  # 淺紫色
            text="重新開始",
            font=("微軟正黑體", 10),
            command=self.restart_game,
            bg=self.bg_color
        )
        self.restart_button.pack(pady=5)
        
        # 強調當前玩家
        self.highlight_current_player()
        
        # 所有 UI 元素已創建，現在綁定按鈕命令
        self.bigger_button.config(command=lambda: self.set_compare_mode("大"))
        self.smaller_button.config(command=lambda: self.set_compare_mode("小"))
        self.bigger_button.invoke()  # 默認選擇比大
    
    def highlight_current_player(self):
        # 重設兩個玩家的框架
        self.player1_frame.config(relief=tk.GROOVE, bd=2)
        self.player2_frame.config(relief=tk.GROOVE, bd=2)
        
        # 強調當前玩家 - 使用更圓滑的陰影效果
        if self.current_player == 1:
            self.player1_frame.config(relief=tk.RAISED, bd=3)
        else:
            self.player2_frame.config(relief=tk.RAISED, bd=3)
    
    def set_compare_mode(self, mode):
        self.compare_mode = mode
        self.status_label.config(text=f"現在是玩家 {self.current_player} 的回合 - 選擇比{self.compare_mode}")
    
    def roll_dice(self):
        # 擲骰子
        dice_value = random.randint(1, 6)
        
        # 顯示骰子值
        if self.current_player == 1:
            self.player1_dice_label.config(text=str(dice_value))
            self.player1_dice_value = dice_value
            self.current_player = 2
            self.status_label.config(text=f"玩家1擲出了 {dice_value}，現在是玩家2的回合 - 選擇比{self.compare_mode}")
        else:
            self.player2_dice_label.config(text=str(dice_value))
            self.player2_dice_value = dice_value
            
            # 判斷輸贏
            self.determine_winner()
            
            # 切換到玩家1回合
            self.current_player = 1
            self.status_label.config(text=f"現在是玩家1的回合 - 選擇比{self.compare_mode}")
            self.rounds_played += 1
            self.round_label.config(text=f"回合: {self.rounds_played}/{self.max_rounds}")
            
            # 檢查遊戲是否結束
            if self.rounds_played >= self.max_rounds:
                self.end_game()
        
        # 更新UI強調當前玩家
        self.highlight_current_player()
    
    def determine_winner(self):
        player1_value = self.player1_dice_value
        player2_value = self.player2_dice_value
        
        # 根據比較模式決定勝者
        if self.compare_mode == "大":
            if player1_value > player2_value:
                self.player1_score += 1
                result = "玩家1獲勝!"
            elif player2_value > player1_value:
                self.player2_score += 1
                result = "玩家2獲勝!"
            else:
                result = "平手!"
        else:  # 比小
            if player1_value < player2_value:
                self.player1_score += 1
                result = "玩家1獲勝!"
            elif player2_value < player1_value:
                self.player2_score += 1
                result = "玩家2獲勝!"
            else:
                result = "平手!"
        
        # 更新分數
        self.player1_score_label.config(text=f"分數: {self.player1_score}")
        self.player2_score_label.config(text=f"分數: {self.player2_score}")
        
        # 創建自訂對話框而不是使用系統的messagebox
        self.show_custom_result(player1_value, player2_value, result)
    
    def show_custom_result(self, player1_value, player2_value, result):
        # 創建一個彈出視窗
        result_window = tk.Toplevel(self.master)
        result_window.title("回合結果")
        result_window.geometry("300x200")
        result_window.configure(bg=self.bg_color)
        result_window.resizable(False, False)
        
        # 讓彈窗置中顯示
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (300 // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (200 // 2)
        result_window.geometry(f"+{x}+{y}")
        
        # 回合結果標題
        title = tk.Label(
            result_window,
            text="回合結果",
            font=("微軟正黑體", 14, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title.pack(pady=10)
        
        # 結果內容
        content_frame = tk.Frame(result_window, bg=self.bg_color)
        content_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # 玩家1結果
        tk.Label(
            content_frame,
            text=f"玩家1: {player1_value}",
            font=("微軟正黑體", 12),
            bg=self.bg_color,
            fg=self.player1_color
        ).pack(anchor="w")
        
        # 玩家2結果
        tk.Label(
            content_frame,
            text=f"玩家2: {player2_value}",
            font=("微軟正黑體", 12),
            bg=self.bg_color,
            fg=self.player2_color
        ).pack(anchor="w")
        
        # 比較模式
        tk.Label(
            content_frame,
            text=f"比較模式: 比{self.compare_mode}",
            font=("微軟正黑體", 12),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(anchor="w", pady=5)
        
        # 結果
        tk.Label(
            content_frame,
            text=result,
            font=("微軟正黑體", 14, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        ).pack(pady=5)
        
        # 確認按鈕
        ok_button = RoundedButton(
            result_window,
            width=80,
            height=30,
            cornerradius=15,
            padding=2,
            color=self.accent_color,
            text="確認",
            font=("微軟正黑體", 10),
            command=result_window.destroy,
            bg=self.bg_color
        )
        ok_button.pack(pady=10)
        
        # 讓彈窗獲得焦點
        result_window.transient(self.master)
        result_window.grab_set()
        self.master.wait_window(result_window)
    
    def end_game(self):
        # 遊戲結束，顯示最終結果
        if self.player1_score > self.player2_score:
            winner = "玩家1"
            winner_color = self.player1_color
        elif self.player2_score > self.player1_score:
            winner = "玩家2"
            winner_color = self.player2_color
        else:
            winner = "平手"
            winner_color = self.accent_color
        
        # 創建遊戲結束視窗
        end_window = tk.Toplevel(self.master)
        end_window.title("遊戲結束")
        end_window.geometry("350x280")
        end_window.configure(bg=self.bg_color)
        end_window.resizable(False, False)
        
        # 讓彈窗置中顯示
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (350 // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (280 // 2)
        end_window.geometry(f"+{x}+{y}")
        
        # 遊戲結束標題
        title = tk.Label(
            end_window,
            text="遊戲結束!",
            font=("微軟正黑體", 18, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title.pack(pady=15)
        
        # 結果內容
        content_frame = tk.Frame(end_window, bg=self.bg_color)
        content_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        # 玩家1分數
        tk.Label(
            content_frame,
            text=f"玩家1分數: {self.player1_score}",
            font=("微軟正黑體", 12),
            bg=self.bg_color,
            fg=self.player1_color
        ).pack(anchor="w", pady=3)
        
        # 玩家2分數
        tk.Label(
            content_frame,
            text=f"玩家2分數: {self.player2_score}",
            font=("微軟正黑體", 12),
            bg=self.bg_color,
            fg=self.player2_color
        ).pack(anchor="w", pady=3)
        
        # 分隔線
        separator = tk.Frame(content_frame, height=1, width=290, bg="#dfe6e9")
        separator.pack(pady=10)
        
        # 最終勝利者
        tk.Label(
            content_frame,
            text="最終勝利者:",
            font=("微軟正黑體", 12),
            bg=self.bg_color,
            fg=self.text_color
        ).pack(pady=3)
        
        tk.Label(
            content_frame,
            text=winner,
            font=("微軟正黑體", 16, "bold"),
            bg=self.bg_color,
            fg=winner_color
        ).pack()
        
        # 按鈕框架
        button_frame = tk.Frame(end_window, bg=self.bg_color)
        button_frame.pack(fill="x", pady=15)
        
        # 再玩一次按鈕
        replay_button = RoundedButton(
            button_frame,
            width=100,
            height=30,
            cornerradius=15,
            padding=2,
            color=self.accent_color,
            text="再玩一次",
            font=("微軟正黑體", 10),
            command=lambda: [end_window.destroy(), self.restart_game()],
            bg=self.bg_color
        )
        replay_button.pack(side="left", padx=20)
        
        # 退出按鈕
        exit_button = RoundedButton(
            button_frame,
            width=100,
            height=30,
            cornerradius=15,
            padding=2,
            color="#a29bfe",
            text="退出遊戲",
            font=("微軟正黑體", 10),
            command=lambda: [end_window.destroy(), self.master.quit()],
            bg=self.bg_color
        )
        exit_button.pack(side="right", padx=20)
        
        # 讓彈窗獲得焦點
        end_window.transient(self.master)
        end_window.grab_set()
        self.master.wait_window(end_window)
    
    def restart_game(self):
        # 重設遊戲狀態
        self.current_player = 1
        self.player1_score = 0
        self.player2_score = 0
        self.rounds_played = 0
        
        # 重設UI
        self.player1_dice_label.config(text="?")
        self.player2_dice_label.config(text="?")
        self.player1_score_label.config(text=f"分數: {self.player1_score}")
        self.player2_score_label.config(text=f"分數: {self.player2_score}")
        self.status_label.config(text=f"現在是玩家1的回合 - 選擇比{self.compare_mode}")
        self.round_label.config(text=f"回合: {self.rounds_played}/{self.max_rounds}")
        
        # 強調當前玩家
        self.highlight_current_player()

if __name__ == "__main__":
    root = tk.Tk()
    game = DiceCompareGame(root)
    root.mainloop()