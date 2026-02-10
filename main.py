"""
股票分析安卓应用主入口
"""

__version__ = '1.0.0'

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.text import LabelBase
import threading

# 导入核心业务模块
import sys
import os

# 设置模块搜索路径
sys.path.insert(0, os.path.dirname(__file__))

# 暂时不导入复杂模块，避免依赖问题
# from src.core.utils_android import setup_directories, setup_logger, Config


def register_fonts():
    """注册中文字体"""
    font_paths = []
    
    # 1. 尝试项目中的字体文件
    project_fonts = [
        'fonts/NotoSansSC-Regular.ttf',
        'fonts/SourceHanSansSC-Regular.ttf', 
        'fonts/wqy-microhei.ttc'
    ]
    
    for font_path in project_fonts:
        full_path = os.path.join(os.path.dirname(__file__), font_path)
        if os.path.exists(full_path):
            font_paths.append(full_path)
            print(f'找到字体文件: {full_path}')
    
    # 2. Android系统字体
    if platform == 'android':
        system_fonts = [
            '/system/fonts/DroidSansFallback.ttf',
            '/system/fonts/NotoSansCJK-Regular.ttc',
            '/system/fonts/NotoSansSC-Regular.otf'
        ]
        for font_path in system_fonts:
            if os.path.exists(font_path):
                font_paths.append(font_path)
                print(f'找到系统字体: {font_path}')
                break
    
    # 3. 注册找到的第一个字体
    if font_paths:
        try:
            LabelBase.register(
                name='Chinese',
                fn_regular=font_paths[0]
            )
            # 设为默认字体
            LabelBase.register(
                name='Roboto',  # Kivy默认字体名
                fn_regular=font_paths[0]
            )
            print(f'成功注册中文字体: {font_paths[0]}')
        except Exception as e:
            print(f'字体注册失败: {e}')
    else:
        print('警告: 未找到中文字体文件')
        print('请在fonts目录下添加中文字体，参考fonts/README.md')


# 注册字体（在创建任何UI之前）
register_fonts()


class HomeScreen(Screen):
    """主界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title = Label(
            text='股票分析',
            size_hint_y=0.1,
            font_size='24sp',
            bold=True
        )
        layout.add_widget(title)
        
        # 工具栏
        toolbar = GridLayout(cols=2, size_hint_y=0.15, spacing=5)
        
        btn_download = Button(text='下载数据')
        btn_download.bind(on_press=self.download_data)
        toolbar.add_widget(btn_download)
        
        btn_analysis = Button(text='成交量分析')
        btn_analysis.bind(on_press=lambda x: self.switch_screen('analysis'))
        toolbar.add_widget(btn_analysis)
        
        btn_history = Button(text='历史记录')
        btn_history.bind(on_press=lambda x: self.switch_screen('history'))
        toolbar.add_widget(btn_history)
        
        btn_settings = Button(text='设置')
        btn_settings.bind(on_press=lambda x: self.switch_screen('settings'))
        toolbar.add_widget(btn_settings)
        
        layout.add_widget(toolbar)
        
        # 状态栏
        self.status_label = Label(
            text='状态: 就绪',
            size_hint_y=0.08,
            color=(0, 1, 0, 1)
        )
        layout.add_widget(self.status_label)
        
        # 股票列表区域
        self.scroll_view = ScrollView(size_hint_y=0.6)
        self.stock_list = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.stock_list.bind(minimum_height=self.stock_list.setter('height'))
        self.scroll_view.add_widget(self.stock_list)
        layout.add_widget(self.scroll_view)
        
        # 统计信息
        self.info_label = Label(
            text='共0只股票',
            size_hint_y=0.07
        )
        layout.add_widget(self.info_label)
        
        self.add_widget(layout)
    
    def switch_screen(self, screen_name):
        """切换屏幕"""
        self.manager.transition.direction = 'left'
        self.manager.current = screen_name
    
    def download_data(self, instance):
        """下载数据"""
        self.status_label.text = '状态: 准备下载...'
        self.status_label.color = (1, 1, 0, 1)
        
        # 模拟下载过程
        def download_thread():
            import time
            for i in range(1, 6):
                time.sleep(1)
                Clock.schedule_once(
                    lambda dt, progress=i: setattr(
                        self.status_label, 
                        'text', 
                        f'状态: 下载中... {progress*20}%'
                    ),
                    0
                )
            
            Clock.schedule_once(
                lambda dt: setattr(self.status_label, 'text', '状态: 下载完成！'),
                0
            )
            Clock.schedule_once(
                lambda dt: setattr(self.status_label, 'color', (0, 1, 0, 1)),
                0
            )
            Clock.schedule_once(lambda dt: self.load_sample_data(), 0)
        
        threading.Thread(target=download_thread, daemon=True).start()
    
    def load_sample_data(self):
        """加载示例数据"""
        self.stock_list.clear_widgets()
        
        # 示例股票数据
        sample_stocks = [
            {'code': '600000', 'name': '浦发银行', 'ratio': '6.5x', 'price': '11.05'},
            {'code': '000001', 'name': '平安银行', 'ratio': '5.8x', 'price': '15.20'},
            {'code': '300059', 'name': '东方财富', 'ratio': '7.2x', 'price': '18.50'},
        ]
        
        for stock in sample_stocks:
            item = BoxLayout(
                size_hint_y=None,
                height=50,
                padding=5
            )
            
            item.add_widget(Label(text=stock['code'], size_hint_x=0.2))
            item.add_widget(Label(text=stock['name'], size_hint_x=0.3))
            item.add_widget(Label(text=stock['ratio'], size_hint_x=0.25))
            item.add_widget(Label(text=stock['price'], size_hint_x=0.25))
            
            self.stock_list.add_widget(item)
        
        self.info_label.text = f'共{len(sample_stocks)}只股票'


class AnalysisScreen(Screen):
    """成交量分析界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        layout.add_widget(Label(text='成交量分析', size_hint_y=0.1, font_size='20sp'))
        
        btn_back = Button(text='返回', size_hint_y=0.1)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(btn_back)
        
        layout.add_widget(Label(text='功能开发中...', size_hint_y=0.8))
        
        self.add_widget(layout)


class HistoryScreen(Screen):
    """历史记录界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        layout.add_widget(Label(text='历史记录', size_hint_y=0.1, font_size='20sp'))
        
        btn_back = Button(text='返回', size_hint_y=0.1)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(btn_back)
        
        layout.add_widget(Label(text='功能开发中...', size_hint_y=0.8))
        
        self.add_widget(layout)


class SettingsScreen(Screen):
    """设置界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        layout.add_widget(Label(text='设置', size_hint_y=0.1, font_size='20sp'))
        
        btn_back = Button(text='返回', size_hint_y=0.1)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(btn_back)
        
        layout.add_widget(Label(text='功能开发中...', size_hint_y=0.8))
        
        self.add_widget(layout)


class StockAnalysisApp(App):
    """主应用类"""
    
    def build(self):
        """构建应用"""
        # 创建屏幕管理器
        sm = ScreenManager(transition=SlideTransition())
        
        # 添加所有屏幕
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AnalysisScreen(name='analysis'))
        sm.add_widget(HistoryScreen(name='history'))
        sm.add_widget(SettingsScreen(name='settings'))
        
        return sm
    
    def on_start(self):
        """应用启动时"""
        try:
            # 简化初始化，避免复杂依赖
            print(f'应用启动，平台: {platform}')
            # 初始化目录（简化版）
            if platform == 'android':
                from android.storage import app_storage_path
                base_path = app_storage_path()
            else:
                base_path = os.path.dirname(__file__)
            print(f'存储路径: {base_path}')
        except Exception as e:
            print(f'初始化失败: {e}')
    
    def on_pause(self):
        """应用暂停时"""
        return True
    
    def on_resume(self):
        """应用恢复时"""
        pass


if __name__ == '__main__':
    StockAnalysisApp().run()
