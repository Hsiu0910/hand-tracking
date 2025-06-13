#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 隨機生成櫻花樹程式

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
    t.left(90)  # 向上
    t.penup()
    t.backward(150)  # 起始位置在畫面底部
    t.pendown()
    return t

# 繪製樹幹
def draw_trunk(t, branch_len):
    if branch_len > 10:
        # 樹幹顏色
        t.pencolor("brown")
        t.pensize(branch_len / 10)
        
        # 繪製主幹
        t.forward(branch_len)
        
        # 右側分支
        angle_right = random.randint(15, 30)
        length_factor_right = random.uniform(0.65, 0.85)
        t.right(angle_right)
        draw_trunk(t, branch_len * length_factor_right)
        
        # 左側分支
        angle_left = random.randint(15, 30)
        length_factor_left = random.uniform(0.65, 0.85)
        t.left(angle_left + angle_right)  # 調整角度
        draw_trunk(t, branch_len * length_factor_left)
        
        # 回到原位置
        t.right(angle_left)
        t.backward(branch_len)
    else:
        # 在樹枝末端畫櫻花
        draw_cherry_blossom(t)

# 繪製櫻花
def draw_cherry_blossom(t):
    # 儲存當前位置和方向
    pos = t.position()
    heading = t.heading()
    
    # 隨機選擇櫻花的大小和顏色
    size = random.uniform(3, 8)
    colors = ["#ffb7c5", "#ffc0cb", "#ff80a0", "#ffaeb9"]
    color = random.choice(colors)  # 隨機選擇粉色系顏色
    
    t.pencolor(color)
    t.fillcolor(color)
    t.begin_fill()
    
    # 繪製花瓣
    for _ in range(5):
        t.forward(size)
        t.right(72)
        t.forward(size)
        t.right(144)
    
    t.end_fill()
    
    # 花心
    t.penup()
    t.goto(pos)
    t.pendown()
    t.pencolor("#ffec8b")  # 淡黃色
    t.fillcolor("#ffec8b")
    t.begin_fill()
    t.circle(size / 4)
    t.end_fill()
    
    # 恢復位置和方向
    t.penup()
    t.goto(pos)
    t.setheading(heading)
    t.pendown()

# 添加落櫻
def add_falling_petals(window, count=30):
    petals = []
    colors = ["#ffb7c5", "#ffc0cb", "#ff80a0", "#ffaeb9"]
    
    for _ in range(count):
        petal = turtle.Turtle()
        petal.speed(0)
        petal.hideturtle()
        petal.penup()
        
        # 隨機位置
        x = random.randint(-380, 380)
        y = random.randint(-100, 280)
        petal.goto(x, y)
        
        # 隨機選擇顏色
        color = random.choice(colors)
        
        # 繪製小花瓣
        petal.pencolor(color)
        petal.fillcolor(color)
        petal.begin_fill()
        petal.circle(random.uniform(1, 3))
        petal.end_fill()
        
        petals.append(petal)
    
    return petals

# 添加背景元素
def add_background(t):
    # 儲存當前位置和方向
    pos = t.position()
    heading = t.heading()
    
    # 添加地面
    t.penup()
    t.goto(-400, -200)
    t.setheading(0)
    t.pendown()
    t.pencolor("#228b22")  # 綠色
    t.fillcolor("#228b22")
    t.begin_fill()
    for _ in range(2):
        t.forward(800)
        t.right(90)
        t.forward(50)
        t.right(90)
    t.end_fill()
    
    # 添加太陽
    t.penup()
    t.goto(300, 200)
    t.pendown()
    t.pencolor("#FFD700")
    t.fillcolor("#FFD700")
    t.begin_fill()
    t.circle(30)
    t.end_fill()
    
    # 恢復位置和方向
    t.penup()
    t.goto(pos)
    t.setheading(heading)
    t.pendown()

# 添加簽名
def add_signature(t):
    t.penup()
    t.goto(-380, -280)
    t.pencolor("black")
    t.pendown()
    t.write("隨機櫻花樹生成器 - 點擊視窗關閉", font=("Arial", 12, "normal"))

# 主函數
def main():
    # 設置視窗和烏龜
    window = setup_window()
    t = setup_turtle()
    
    # 添加背景
    add_background(t)
    
    # 隨機決定樹的主幹長度
    trunk_length = random.randint(100, 140)
    
    # 繪製樹
    draw_trunk(t, trunk_length)
    
    # 添加落櫻
    petals = add_falling_petals(window, 40)
    
    # 添加簽名
    add_signature(t)
    
    # 顯示結果並等待用戶點擊關閉
    window.exitonclick()

if __name__ == "__main__":
    main()