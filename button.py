# button.py - 按钮类，封装按钮的绘制和事件处理
# 所有界面的按钮都将使用这个类，实现UI与逻辑的解耦

import pygame
from constants import FONT_MEDIUM  # 导入字体常量，用于文字渲染

class Button:
    """
    通用按钮类
    属性：
        rect: 按钮的矩形区域 (pygame.Rect)
        text: 按钮上显示的文本
        font_size: 字体大小
        bg_color: 背景颜色
        border_color: 边框颜色
        text_color: 文字颜色
        callback: 点击时执行的函数（无参数）
    """
    def __init__(self, rect, text, font_size, bg_color, border_color, text_color, callback=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font_size = font_size
        self.bg_color = bg_color
        self.border_color = border_color
        self.text_color = text_color
        self.callback = callback

    def draw(self, surface):
        """绘制按钮到指定表面"""
        # 绘制背景圆角矩形
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=15)
        # 绘制边框
        pygame.draw.rect(surface, self.border_color, self.rect, 5, border_radius=15)
        # 渲染文字
        font = pygame.font.Font(FONT_MEDIUM[0], self.font_size)
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        """
        处理事件
        如果是鼠标左键点击且点在按钮内，则执行回调函数
        返回 True 表示事件已被处理，否则返回 False
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
                return True
        return False