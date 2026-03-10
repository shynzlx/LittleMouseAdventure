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
    def __init__(self, rect, text, font_size, bg_color, border_color, text_color, 
                 callback=None, bg_alpha=255):  # 新增 bg_alpha 参数，默认不透明
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font_size = font_size
        
        # 将背景色和透明度组合成 RGBA 四元组
        if len(bg_color) == 3:  # 如果传入的是 RGB 三元组
            self.bg_color = (*bg_color, bg_alpha)
        else:  # 如果已经是 RGBA，则忽略 bg_alpha（也可以选择覆盖 alpha，这里保持简单）
            self.bg_color = bg_color
            
        self.border_color = border_color
        self.text_color = text_color
        self.callback = callback

    def draw(self, surface):
        # 创建带透明通道的中间 Surface
        btn_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        
        # 绘制背景（使用组合后的 RGBA）
        pygame.draw.rect(btn_surface, self.bg_color, btn_surface.get_rect(), border_radius=15)
        # 绘制边框（如果也想让边框透明，可以类似处理，但通常边框不透明）
        pygame.draw.rect(btn_surface, self.border_color, btn_surface.get_rect(), 5, border_radius=15)
        
        # 绘制文字
        font = pygame.font.Font(FONT_MEDIUM[0], self.font_size)
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=btn_surface.get_rect().center)
        btn_surface.blit(text_surf, text_rect)
        
        # 将按钮绘制到目标表面
        surface.blit(btn_surface, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
                return True
        return False