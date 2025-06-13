#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 隨機生成櫻花樹程式 - 優化版

import turtle
import random
import math

# 設置視窗
def setup_window():
    window = turtle.Screen()
    window.bgcolor("lightblue")  # 淺藍色背景
    window.title("隨機櫻花樹")
    window.setup(width=800, height=600)
    return window

# 初始化烏龜
def setup_turtle():
    t = turtle.Turtle()
    t.speed(0)  # 最快速度
    t.hideturtle()
    return t

# 繪製櫻花
def draw_cherry_blossom(t, size):
    current_pos = t.position()
    current_heading = t.heading()
    
    # 隨機選擇櫻花顏色
    colors = ["#ffb7c5", "#ffc0cb", "#ff80a0", "#ffaeb9"]
    color = random.choice(colors)
    
    t.pencolor(color)
    t.fillcolor(color)
    t.begin_fill()
    
    # 繪製5瓣花
    for _ in range(5):
        t.forward(size)
        t.right(72)
        t.forward(size)
        t.right(144)
    
    t.end_fill()
    
    # 花心
    t.penup()
    t.goto(current_pos)
    t.pendown()
    t.pencolor("#ffec8b")
    t.fillcolor("#ffec8b")
    t.begin_fill()
    t.circle(size/4)
    t.end_fill()
    
    # 恢復位置
    t.penup()
    t.goto(current_pos)
    t.setheading(current_heading)
    t.pendown()

# 遞歸繪製樹枝 (優化版)
def draw_branch(t, length, angle, depth, min_length=5):
    if length < min_length or depth > 10:  # 增加深度限制
        return
    
    # 樹幹顏色和粗細
    t.pencolor("brown")
    t.pensize(length/10)
    
    # 主幹
    t.forward(length)
    current_pos = t.position()
    current_heading = t.heading()
    
    # 如果達到末端，繪製花朵
    if length < 20:
        draw_cherry_blossom(t, random.uniform(3, 6))
    
    # 右側分支
    right_angle = random.randint(15, 30)
    right_length = length * random.uniform(0.6, 0.8)
    
    t.right(right_angle)
    draw_branch(t, right_length, right_angle, depth+1, min_length)
    
    # 恢復位置
    t.penup()
    t.goto(current_pos)
    t.setheading(current_heading)
    t.pendown()
    
    # 左側分支
    left_angle = random.randint(15, 30)
    left_length = length * random.uniform(0.6, 0.8)
    
    t.left(left_angle)
    draw_branch(t, left_length, left_angle, depth+1, min_length)
    
    # 恢復位置
    t.penup()
    t.goto(current_pos)
    t.setheading(current_heading)
    t.pendown()

# 繪製櫻花樹
def draw_cherry_tree(t):
    # 從底部開始
    t.penup()
    t.goto(0, -200)
    t.setheading(90)  # 向上
    t.pendown()
    
    # 樹幹
    t.pencolor("brown")
    t.pensize(10)
    t.forward(80)
    
    # 開始分支
    initial_length = random.randint(60, 80)
    draw_branch(t, initial_length, 0, 0)

# 添加地面
def draw_ground(t):
    t.penup()
    t.goto(-400, -200)
    t.pendown()
    t.pencolor("#228b22")
    t.fillcolor("#228b22")
    t.begin_fill()
    t.setheading(0)
    for _ in range(2):
        t.forward(800)
        t.right(90)
        t.forward(50)
        t.right(90)
    t.end_fill()

# 添加落櫻效果
def add_falling_petals(count=30):
    petals = []
    colors = ["#ffb7c5", "#ffc0cb", "#ff80a0", "#ffaeb9"]
    
    for _ in range(count):
        # 創建新的烏龜
        p = turtle.Turtle()
        p.speed(0)
        p.hideturtle()
        p.penup()
        
        # 隨機位置
        x = random.randint(-380, 380)
        y = random.randint(-100, 280)
        p.goto(x, y)
        
        # 繪製花瓣
        p.pendown()
        color = random.choice(colors)
        p.pencolor(color)
        p.fillcolor(color)
        p.begin_fill()
        p.circle(random.uniform(2, 4))
        p.end_fill()
        p.penup()
        
        petals.append(p)
    
    return petals

# 添加太陽
def draw_sun(t):
    t.penup()
    t.goto(300, 200)
    t.pendown()
    t.pencolor("#FFD700")
    t.fillcolor("#FFD700")
    t.begin_fill()
    t.circle(30)
    t.end_fill()

# 添加簽名
def add_signature(t):
    t.penup()
    t.goto(-380, -280)
    t.pendown()
    t.pencolor("black")
    t.write("隨機櫻花樹生成器 - 點擊視窗關閉", font=("Arial", 12, "normal"))

# 主函數
def main():
    try:
        # 初始化
        window = setup_window()
        t = setup_turtle()
        
        # 繪製場景
        draw_ground(t)
        draw_sun(t)
        
        # 繪製櫻花樹
        draw_cherry_tree(t)
        
        # 添加落櫻
        petals = add_falling_petals(30)
        
        # 添加簽名
        add_signature(t)
        
        # 完成繪製，隱藏烏龜
        t.hideturtle()
        
        # 等待點擊
        turtle.exitonclick()
        
    except Exception as e:
        print(f"發生錯誤: {e}")
        # 確保視窗顯示
        turtle.mainloop()

if __name__ == "__main__":
    main()