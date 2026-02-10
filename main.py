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
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.text import LabelBase
import threading
import os
import sys
import glob

# 设置模块搜索路径
sys.path.insert(0, os.path.dirname(__file__))

from data_manager import DataManager


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


# 注册字体（在创建任何UI之前）
register_fonts()


class HomeScreen(Screen):
    """主界面"""
    
    def __init__(self, data_manager, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = data_manager
        
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
        self.scroll_view = ScrollView(size_hint_y=0.67)
        self.stock_list = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.stock_list.bind(minimum_height=self.stock_list.setter('height'))
        self.scroll_view.add_widget(self.stock_list)
        layout.add_widget(self.scroll_view)
        
        self.add_widget(layout)
        
        # 加载初始数据
        Clock.schedule_once(lambda dt: self.load_latest_results(), 0.5)
    
    def switch_screen(self, screen_name):
        """切换屏幕"""
        self.manager.transition.direction = 'left'
        self.manager.current = screen_name
    
    def load_latest_results(self):
        """加载最新的分析结果"""
        self.stock_list.clear_widgets()
        
        # 获取数据统计
        stock_count = self.data_manager.get_stock_count()
        
        # 添加统计信息头部
        info_header = Label(
            text=f'数据统计: 共 {stock_count} 只股票',
            size_hint_y=None,
            height=30,
            font_size='14sp',
            bold=True
        )
        self.stock_list.add_widget(info_header)
        
        # 尝试加载最新的分析结果
        history_files = self.data_manager.get_history_files()
        
        if history_files:
            latest_file = history_files[0]
            results = self.data_manager.load_history_result(latest_file['filepath'])
            
            if results:
                # 显示最新分析结果
                result_header = Label(
                    text=f'\n最近分析结果 ({latest_file["date"]})：',
                    size_hint_y=None,
                    height=40,
                    font_size='14sp'
                )
                self.stock_list.add_widget(result_header)
                
                # 添加表头
                header = Label(
                    text=f'{"代码":<10} {"名称":<10} {"倍数":<8} {"日期"}',
                    size_hint_y=None,
                    height=30,
                    font_name='RobotoMono-Regular',
                    bold=True
                )
                self.stock_list.add_widget(header)
                
                # 显示前10条结果
                for row in results[:10]:
                    stock_code = row['stock_code']
                    stock_name = row['stock_name']
                    volume_ratio = float(row['volume_ratio'])
                    date = row['date']
                    
                    # 截断股票名称
                    if len(stock_name) > 6:
                        stock_name = stock_name[:6]
                    
                    text = f'{stock_code:<10} {stock_name:<10} {volume_ratio:>5.1f}x {date}'
                    
                    result_label = Label(
                        text=text,
                        size_hint_y=None,
                        height=30,
                        font_name='RobotoMono-Regular'
                    )
                    self.stock_list.add_widget(result_label)
                
                if len(results) > 10:
                    more_label = Label(
                        text=f'\n... 还有 {len(results) - 10} 只股票',
                        size_hint_y=None,
                        height=40,
                        color=(0.7, 0.7, 0.7, 1)
                    )
                    self.stock_list.add_widget(more_label)
                
                self.status_label.text = f'状态: 显示最近 {len(results[:10])} 只股票'
                self.status_label.color = (0, 1, 0, 1)
            else:
                self.show_no_results()
        else:
            self.show_no_results()
    
    def show_no_results(self):
        """显示无结果提示"""
        no_result_label = Label(
            text='\n暂无分析结果\n\n请点击"成交量分析"执行分析',
            size_hint_y=None,
            height=100
        )
        self.stock_list.add_widget(no_result_label)
        
        self.status_label.text = '状态: 暂无数据'
        self.status_label.color = (1, 0.5, 0, 1)
    
    def download_data(self, instance):
        """下载数据"""
        self.status_label.text = '状态: 功能开发中...'
        self.status_label.color = (1, 1, 0, 1)
        
        # TODO: 集成真实的数据下载功能
        # 暂时提示用户手动准备数据
        Clock.schedule_once(lambda dt: self.show_download_message(), 1)
    
    def show_download_message(self):
        self.status_label.text = '状态: 请确保数据目录中有股票数据'


class VolumeAnalysisScreen(Screen):
    """成交量分析界面"""
    
    def __init__(self, data_manager, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = data_manager
        self.analysis_results = None
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题栏
        header = BoxLayout(size_hint_y=0.08, spacing=5)
        
        btn_back = Button(text='返回', size_hint_x=0.3)
        btn_back.bind(on_press=lambda x: self.go_back())
        header.add_widget(btn_back)
        
        title = Label(text='成交量分析', font_size='20sp', bold=True)
        header.add_widget(title)
        
        btn_analyze = Button(text='开始分析', size_hint_x=0.3)
        btn_analyze.bind(on_press=self.start_analysis)
        header.add_widget(btn_analyze)
        
        layout.add_widget(header)
        
        # 状态栏
        self.status_label = Label(
            text='状态: 就绪',
            size_hint_y=0.06,
            color=(0, 1, 0, 1)
        )
        layout.add_widget(self.status_label)
        
        # 结果列表
        self.scroll_view = ScrollView(size_hint_y=0.86)
        self.results_list = GridLayout(cols=1, spacing=5, size_hint_y=None, padding=5)
        self.results_list.bind(minimum_height=self.results_list.setter('height'))
        self.scroll_view.add_widget(self.results_list)
        layout.add_widget(self.scroll_view)
        
        self.add_widget(layout)
    
    def go_back(self):
        """返回主界面"""
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'
    
    def start_analysis(self, instance):
        """开始分析"""
        self.status_label.text = '状态: 分析中...'
        self.status_label.color = (1, 1, 0, 1)
        self.results_list.clear_widgets()
        
        # 在后台线程执行分析
        threading.Thread(target=self.do_analysis, daemon=True).start()
    
    def do_analysis(self):
        """执行分析"""
        try:
            results_df = self.data_manager.analyze_volume_surge(
                progress_callback=self.on_progress
            )
            
            Clock.schedule_once(lambda dt: self.show_results(results_df), 0)
        
        except Exception as e:
            error_msg = f'分析失败: {str(e)}'
            Clock.schedule_once(lambda dt: self.show_error(error_msg), 0)
    
    def on_progress(self, processed, total, found_count):
        """进度更新"""
        progress_text = f'状态: 已处理 {processed}/{total}, 找到 {found_count} 只'
        Clock.schedule_once(
            lambda dt: setattr(self.status_label, 'text', progress_text),
            0
        )
    
    def show_results(self, results):
        """显示结果"""
        self.analysis_results = results
        self.results_list.clear_widgets()
        
        if not results:
            self.status_label.text = '状态: 未找到符合条件的股票'
            self.status_label.color = (1, 0.5, 0, 1)
            
            no_result_label = Label(
                text='未找到符合条件的股票\n\n规则：成交量 >= 前7天平均的5倍\n且收盘价 > 均线',
                size_hint_y=None,
                height=100
            )
            self.results_list.add_widget(no_result_label)
        else:
            self.status_label.text = f'状态: 找到 {len(results)} 只股票'
            self.status_label.color = (0, 1, 0, 1)
            
            # 保存结果
            self.data_manager.save_analysis_result(results)
            
            # 添加表头
            header = Label(
                text=f'{"代码":<10} {"名称":<10} {"倍数":<8} {"日期"}',
                size_hint_y=None,
                height=30,
                font_name='RobotoMono-Regular',
                bold=True
            )
            self.results_list.add_widget(header)
            
            # 显示结果
            for row in results:
                stock_code = row['stock_code']
                stock_name = row['stock_name']
                volume_ratio = float(row['volume_ratio'])
                date = row['date']
                
                # 截断股票名称
                if len(stock_name) > 6:
                    stock_name = stock_name[:6]
                
                text = f'{stock_code:<10} {stock_name:<10} {volume_ratio:>5.1f}x {date}'
                
                result_label = Label(
                    text=text,
                    size_hint_y=None,
                    height=30,
                    font_name='RobotoMono-Regular'
                )
                self.results_list.add_widget(result_label)
    
    def show_error(self, error_msg):
        """显示错误"""
        self.status_label.text = f'状态: {error_msg}'
        self.status_label.color = (1, 0, 0, 1)


class HistoryScreen(Screen):
    """历史记录界面"""
    
    def __init__(self, data_manager, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = data_manager
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题栏
        header = BoxLayout(size_hint_y=0.08, spacing=5)
        
        btn_back = Button(text='返回', size_hint_x=0.3)
        btn_back.bind(on_press=lambda x: self.go_back())
        header.add_widget(btn_back)
        
        title = Label(text='历史记录', font_size='20sp', bold=True)
        header.add_widget(title)
        
        btn_refresh = Button(text='刷新', size_hint_x=0.3)
        btn_refresh.bind(on_press=lambda x: self.load_history())
        header.add_widget(btn_refresh)
        
        layout.add_widget(header)
        
        # 状态栏
        self.status_label = Label(
            text='状态: 就绪',
            size_hint_y=0.06,
            color=(0, 1, 0, 1)
        )
        layout.add_widget(self.status_label)
        
        # 历史记录列表
        self.scroll_view = ScrollView(size_hint_y=0.86)
        self.history_list = GridLayout(cols=1, spacing=5, size_hint_y=None, padding=5)
        self.history_list.bind(minimum_height=self.history_list.setter('height'))
        self.scroll_view.add_widget(self.history_list)
        layout.add_widget(self.scroll_view)
        
        self.add_widget(layout)
        
        # 加载历史记录
        Clock.schedule_once(lambda dt: self.load_history(), 0.5)
    
    def go_back(self):
        """返回主界面"""
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'
    
    def load_history(self):
        """加载历史记录"""
        self.history_list.clear_widgets()
        self.status_label.text = '状态: 加载中...'
        self.status_label.color = (1, 1, 0, 1)
        
        history_files = self.data_manager.get_history_files()
        
        if not history_files:
            self.status_label.text = '状态: 暂无历史记录'
            self.status_label.color = (1, 0.5, 0, 1)
            
            no_history_label = Label(
                text='暂无历史记录\n\n请先执行成交量分析',
                size_hint_y=None,
                height=100
            )
            self.history_list.add_widget(no_history_label)
        else:
            self.status_label.text = f'状态: 共 {len(history_files)} 条记录'
            self.status_label.color = (0, 1, 0, 1)
            
            for history in history_files:
                history_item = BoxLayout(size_hint_y=None, height=60, spacing=5)
                
                info_layout = BoxLayout(orientation='vertical')
                
                date_label = Label(
                    text=history['date'],
                    size_hint_y=0.5,
                    font_size='14sp'
                )
                info_layout.add_widget(date_label)
                
                count_label = Label(
                    text=f'找到 {history["count"]} 只股票',
                    size_hint_y=0.5,
                    font_size='12sp',
                    color=(0.7, 0.7, 0.7, 1)
                )
                info_layout.add_widget(count_label)
                
                history_item.add_widget(info_layout)
                
                btn_view = Button(
                    text='查看',
                    size_hint_x=0.3
                )
                btn_view.bind(
                    on_press=lambda x, fp=history['filepath']: self.view_history(fp)
                )
                history_item.add_widget(btn_view)
                
                self.history_list.add_widget(history_item)
    
    def view_history(self, filepath):
        """查看历史记录详情"""
        self.history_list.clear_widgets()
        self.status_label.text = '状态: 加载中...'
        
        try:
            results = self.data_manager.load_history_result(filepath)
            
            if not results:
                self.status_label.text = '状态: 记录为空'
                return
            
            self.status_label.text = f'状态: 共 {len(results)} 只股票'
            self.status_label.color = (0, 1, 0, 1)
            
            # 添加返回按钮
            btn_back_to_list = Button(
                text='返回列表',
                size_hint_y=None,
                height=40
            )
            btn_back_to_list.bind(on_press=lambda x: self.load_history())
            self.history_list.add_widget(btn_back_to_list)
            
            # 添加表头
            header = Label(
                text=f'{"代码":<10} {"名称":<10} {"倍数":<8} {"日期"}',
                size_hint_y=None,
                height=30,
                font_name='RobotoMono-Regular',
                bold=True
            )
            self.history_list.add_widget(header)
            
            # 显示结果
            for row in results:
                stock_code = row['stock_code']
                stock_name = row.get('stock_name', stock_code)
                volume_ratio = float(row['volume_ratio'])
                date = row['date']
                
                # 截断股票名称
                if len(stock_name) > 6:
                    stock_name = stock_name[:6]
                
                text = f'{stock_code:<10} {stock_name:<10} {volume_ratio:>5.1f}x {date}'
                
                result_label = Label(
                    text=text,
                    size_hint_y=None,
                    height=30,
                    font_name='RobotoMono-Regular'
                )
                self.history_list.add_widget(result_label)
        
        except Exception as e:
            self.status_label.text = f'状态: 加载失败 - {str(e)}'
            self.status_label.color = (1, 0, 0, 1)


class SettingsScreen(Screen):
    """设置界面"""
    
    def __init__(self, data_manager, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = data_manager
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题栏
        header = BoxLayout(size_hint_y=0.08, spacing=5)
        
        btn_back = Button(text='返回', size_hint_x=0.3)
        btn_back.bind(on_press=lambda x: self.go_back())
        header.add_widget(btn_back)
        
        title = Label(text='设置', font_size='20sp', bold=True)
        header.add_widget(title)
        
        header.add_widget(Label(size_hint_x=0.3))  # 占位
        
        layout.add_widget(header)
        
        # 设置内容
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        content.add_widget(Label(
            text='应用设置',
            size_hint_y=None,
            height=40,
            font_size='18sp',
            bold=True
        ))
        
        content.add_widget(Label(
            text=f'版本: {__version__}',
            size_hint_y=None,
            height=30
        ))
        
        content.add_widget(Label(
            text=f'数据目录: {self.data_manager.base_path}',
            size_hint_y=None,
            height=60,
            text_size=(400, None),
            halign='left'
        ))
        
        content.add_widget(Label(
            text='功能说明',
            size_hint_y=None,
            height=40,
            font_size='18sp',
            bold=True
        ))
        
        help_text = '''
下载数据: 下载股票列表和历史数据
成交量分析: 分析成交量暴涨的股票
历史记录: 查看之前的分析结果
        '''
        
        content.add_widget(Label(
            text=help_text.strip(),
            size_hint_y=None,
            height=150,
            text_size=(400, None),
            halign='left',
            valign='top'
        ))
        
        layout.add_widget(content)
        self.add_widget(layout)
    
    def go_back(self):
        """返回主界面"""
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'


class StockAnalysisApp(App):
    """股票分析应用"""
    
    def build(self):
        """构建应用界面"""
        # 初始化数据管理器
        if platform == 'android':
            from android.storage import app_storage_path
            base_path = app_storage_path()
        else:
            base_path = os.path.join(os.path.dirname(__file__), 'data')
        
        self.data_manager = DataManager(base_path)
        
        # 创建屏幕管理器
        sm = ScreenManager()
        
        # 添加各个界面
        sm.add_widget(HomeScreen(self.data_manager, name='home'))
        sm.add_widget(VolumeAnalysisScreen(self.data_manager, name='analysis'))
        sm.add_widget(HistoryScreen(self.data_manager, name='history'))
        sm.add_widget(SettingsScreen(self.data_manager, name='settings'))
        
        return sm
    
    def on_start(self):
        """应用启动时"""
        try:
            print(f'应用启动，平台: {platform}')
            print(f'存储路径: {self.data_manager.base_path}')
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
