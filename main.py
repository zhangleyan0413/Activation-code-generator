import wx
import random
import datetime

def jhm(cnt, settings=None):
    # 默认设置
    default_settings = {
        'segments': 4,
        'segment_length': 5,
        'delimiter': '-',
        'include_digits': True,
        'include_uppercase': True,
        'include_lowercase': False,
        'include_symbols': False,
        'fast_mode': False  # 快速生成模式
    }
    
    # 使用传入的设置或默认设置
    if settings:
        default_settings.update(settings)
    settings = default_settings
    
    # 构建字符集
    charset = ''
    if settings['include_digits']:
        charset += '0123456789'
    if settings['include_uppercase']:
        charset += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if settings['include_lowercase']:
        charset += 'abcdefghijklmnopqrstuvwxyz'
    if settings['include_symbols']:
        charset += '!@#$%^&*'
    
    # 确保字符集不为空
    if not charset:
        charset = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    charset_length = len(charset)
    delimiter = settings['delimiter']
    segments = settings['segments']
    segment_length = settings['segment_length']
    
    # 快速生成模式
    if settings['fast_mode'] and cnt > 1000:
        import string
        import time
        
        # 使用时间戳作为种子，提高批量生成速度
        random.seed(time.time())
        
        lis = []
        # 预计算每段的字符集索引范围
        max_index = charset_length - 1
        
        for i in range(cnt):
            # 直接生成每段，减少函数调用开销
            code_parts = []
            for j in range(segments):
                # 快速生成一段字符
                part = ''.join([charset[random.randint(0, max_index)] for _ in range(segment_length)])
                code_parts.append(part)
            # 拼接成完整激活码
            code = delimiter.join(code_parts)
            lis.append(code)
        return lis
    else:
        # 标准生成模式
        lis = []
        for i in range(cnt):
            code = ""
            for j in range(segments):
                # 生成每段
                for k in range(segment_length):
                    code += random.choice(charset)
                # 添加分隔符（最后一段除外）
                if j < segments - 1:
                    code += delimiter
            lis.append(code)
        return lis

class ActivationCodeFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="激活码生成工具", size=(600, 400))
        self.generated_codes = []
        # 初始化设置
        self.settings = {
            'segments': 4,          # 激活码段数
            'segment_length': 5,    # 每段长度
            'delimiter': '-',       # 分隔符
            'include_digits': True, # 包含数字
            'include_uppercase': True, # 包含大写字母
            'include_lowercase': False, # 包含小写字母
            'include_symbols': False, # 包含特殊字符
            'save_path': '激活码.txt', # 保存路径
            'auto_save': False,     # 自动保存
            'add_timestamp': True   # 添加时间戳
        }
        self.init_menu()
        self.init_ui()
    
    def init_menu(self):
        # 创建菜单栏
        menubar = wx.MenuBar()
        
        # 文件菜单
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_NEW, "&新建\tCtrl+N", "新建激活码")
        file_menu.Append(wx.ID_OPEN, "&打开\tCtrl+O", "打开激活码文件")
        file_menu.Append(wx.ID_SAVE, "&保存\tCtrl+S", "保存激活码")
        file_menu.Append(wx.ID_SAVEAS, "另存为...\tCtrl+Shift+S", "另存为新文件")
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, "&退出\tCtrl+Q", "退出程序")
        menubar.Append(file_menu, "&文件")
        
        # 编辑菜单
        edit_menu = wx.Menu()
        edit_menu.Append(wx.ID_COPY, "&复制\tCtrl+C", "复制选中的激活码")
        edit_menu.Append(wx.ID_CLEAR, "&清空\tCtrl+L", "清空当前激活码")
        menubar.Append(edit_menu, "&编辑")
        
        # 工具菜单
        tool_menu = wx.Menu()
        batch_generate = tool_menu.Append(-1, "&批量生成...", "批量生成激活码")
        settings = tool_menu.Append(-1, "&设置...", "设置生成参数")
        menubar.Append(tool_menu, "&工具")
        
        # 帮助菜单
        help_menu = wx.Menu()
        help_menu.Append(wx.ID_HELP, "&使用说明", "查看使用说明")
        help_menu.AppendSeparator()
        help_menu.Append(wx.ID_ABOUT, "&关于", "关于本程序")
        menubar.Append(help_menu, "&帮助")
        
        # 设置菜单栏
        self.SetMenuBar(menubar)
        
        # 绑定菜单事件
        self.Bind(wx.EVT_MENU, self.on_new, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, self.on_open, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.on_save, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.on_save_as, id=wx.ID_SAVEAS)
        self.Bind(wx.EVT_MENU, self.on_exit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_copy, id=wx.ID_COPY)
        self.Bind(wx.EVT_MENU, self.on_clear, id=wx.ID_CLEAR)
        self.Bind(wx.EVT_MENU, self.on_batch_generate, batch_generate)
        self.Bind(wx.EVT_MENU, self.on_settings, settings)
        self.Bind(wx.EVT_MENU, self.on_help, id=wx.ID_HELP)
        self.Bind(wx.EVT_MENU, self.on_about, id=wx.ID_ABOUT)
    
    def init_ui(self):
        panel = wx.Panel(self)
        
        # 输入区域
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label_cnt = wx.StaticText(panel, label="生成数量：")
        self.entry_cnt = wx.TextCtrl(panel, value="10", size=(80, -1))
        btn_generate = wx.Button(panel, label="生成激活码")
        btn_save = wx.Button(panel, label="保存到文件")
        
        input_sizer.Add(label_cnt, 0, wx.RIGHT, 10)
        input_sizer.Add(self.entry_cnt, 0, wx.RIGHT, 10)
        input_sizer.Add(btn_generate, 0, wx.RIGHT, 10)
        input_sizer.Add(btn_save, 0)
        
        # 输出区域
        label_output = wx.StaticText(panel, label="生成的激活码：")
        self.text_output = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(550, 250))
        
        # 绑定事件
        btn_generate.Bind(wx.EVT_BUTTON, self.on_generate)
        btn_save.Bind(wx.EVT_BUTTON, self.on_save)
        
        # 主布局
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(input_sizer, 0, wx.ALL, 10)
        main_sizer.Add(label_output, 0, wx.LEFT | wx.BOTTOM, 10)
        main_sizer.Add(self.text_output, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        panel.SetSizer(main_sizer)
        self.Center()
    
    def on_generate(self, event):
        try:
            cnt = int(self.entry_cnt.GetValue())
            if cnt <= 0:
                wx.MessageBox("请输入正整数！", "错误", wx.OK | wx.ICON_ERROR)
                return
            # 使用设置生成激活码
            self.generated_codes = jhm(cnt, self.settings)
            self.text_output.SetValue("\n".join(self.generated_codes))
            
            # 自动保存
            if self.settings['auto_save']:
                self.on_save(None)
        except ValueError:
            wx.MessageBox("请输入有效的数字！", "错误", wx.OK | wx.ICON_ERROR)
    
    def on_save(self, event):
        if not self.generated_codes:
            if event:  # 只有用户主动点击保存时才提示
                wx.MessageBox("请先生成激活码！", "提示", wx.OK | wx.ICON_INFORMATION)
            return
        try:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_path = self.settings['save_path']
            
            # 使用utf-8编码保存文件，确保中文字符正常显示
            with open(save_path, "a", encoding='utf-8') as f:
                if self.settings['add_timestamp']:
                    # 确保时间字符串正确编码
                    time_str = f"生成时间：{current_time}\n"
                    f.write(time_str)
                # 确保个数字符串正确编码
                count_str = f"生成个数：{len(self.generated_codes)}\n"
                f.write(count_str)
                for code in self.generated_codes:
                    f.write(code + "\n")
                f.write("-" * 50 + "\n")
            
            if event:  # 只有用户主动点击保存时才提示
                wx.MessageBox(f"激活码已保存到 {save_path}！", "成功", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            if event:  # 只有用户主动点击保存时才提示
                wx.MessageBox(f"保存失败：{str(e)}", "错误", wx.OK | wx.ICON_ERROR)
    
    def on_save_as(self, event):
        """另存为功能"""
        if not self.generated_codes:
            wx.MessageBox("请先生成激活码！", "提示", wx.OK | wx.ICON_INFORMATION)
            return
        
        # 打开文件对话框让用户选择保存路径
        with wx.FileDialog(self, "另存为", wildcard="文本文件 (*.txt)|*.txt",
                          style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            save_path = fileDialog.GetPath()
        
        try:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 使用utf-8编码保存文件，确保中文字符正常显示
            with open(save_path, "a", encoding='utf-8') as f:
                if self.settings['add_timestamp']:
                    time_str = f"生成时间：{current_time}\n"
                    f.write(time_str)
                count_str = f"生成个数：{len(self.generated_codes)}\n"
                f.write(count_str)
                for code in self.generated_codes:
                    f.write(code + "\n")
                f.write("-" * 50 + "\n")
            
            wx.MessageBox(f"激活码已保存到 {save_path}！", "成功", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"保存失败：{str(e)}", "错误", wx.OK | wx.ICON_ERROR)
    
    def on_new(self, event):
        """新建激活码"""
        self.entry_cnt.SetValue("10")
        self.text_output.SetValue("")
        self.generated_codes = []
    
    def on_open(self, event):
        """打开激活码文件"""
        with wx.FileDialog(self, "打开激活码文件", wildcard="文本文件 (*.txt)|*.txt",
                          style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_output.SetValue(content)
                # 提取激活码到generated_codes
                self.generated_codes = []
                for line in content.split('\n'):
                    line = line.strip()
                    if '-' in line and len(line) == 20:  # 激活码格式：XXX-XXX-XXX-XXX
                        self.generated_codes.append(line)
                
                # 检测重复激活码
                duplicates = self.check_duplicates(self.generated_codes)
                if duplicates:
                    duplicate_info = "发现重复激活码：\n\n"
                    for code, count in duplicates.items():
                        duplicate_info += f"{code} (出现 {count} 次)\n"
                    wx.MessageBox(duplicate_info, "重复检测", wx.OK | wx.ICON_WARNING)
                else:
                    wx.MessageBox(f"成功打开文件：{path}\n未发现重复激活码", "成功", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"打开文件失败：{str(e)}", "错误", wx.OK | wx.ICON_ERROR)
    
    def check_duplicates(self, codes):
        """检测重复激活码"""
        code_count = {}
        duplicates = {}
        
        # 统计每个激活码出现的次数
        for code in codes:
            if code in code_count:
                code_count[code] += 1
            else:
                code_count[code] = 1
        
        # 筛选出出现次数大于1的激活码
        for code, count in code_count.items():
            if count > 1:
                duplicates[code] = count
        
        return duplicates
    
    def on_exit(self, event):
        """退出程序"""
        self.Close(True)
    
    def on_copy(self, event):
        """复制选中的激活码"""
        selected_text = self.text_output.GetStringSelection()
        if selected_text:
            data_obj = wx.TextDataObject()
            data_obj.SetText(selected_text)
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(data_obj)
                wx.TheClipboard.Close()
                wx.MessageBox("已复制到剪贴板！", "成功", wx.OK | wx.ICON_INFORMATION)
            else:
                wx.MessageBox("无法访问剪贴板！", "错误", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("请先选中要复制的内容！", "提示", wx.OK | wx.ICON_INFORMATION)
    
    def on_clear(self, event):
        """清空当前激活码"""
        self.text_output.SetValue("")
        self.generated_codes = []
    
    def on_batch_generate(self, event):
        """批量生成激活码"""
        # 创建批量生成对话框
        dialog = wx.Dialog(self, title="批量生成激活码", size=(400, 400))
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 生成数量设置
        count_box = wx.StaticBox(dialog, label="生成数量")
        count_sizer = wx.StaticBoxSizer(count_box, wx.VERTICAL)
        
        count_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        count_input_sizer.Add(wx.StaticText(dialog, label="数量："), 0, wx.RIGHT, 10)
        self.batch_count_input = wx.SpinCtrl(dialog, min=1, max=10000000000, initial=100000)
        count_input_sizer.Add(self.batch_count_input, 1)
        count_sizer.Add(count_input_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        count_info = wx.StaticText(dialog, label="提示：生成大量激活码可能需要较长时间，建议分批生成")
        count_sizer.Add(count_info, 0, wx.ALL, 5)
        
        main_sizer.Add(count_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # 生成选项
        generate_box = wx.StaticBox(dialog, label="生成选项")
        generate_sizer = wx.StaticBoxSizer(generate_box, wx.VERTICAL)
        
        fast_mode_check = wx.CheckBox(dialog, label="快速生成模式（适合大量生成）")
        fast_mode_check.SetValue(False)  # 默认不使用快速模式
        generate_sizer.Add(fast_mode_check, 0, wx.ALL, 5)
        
        fast_mode_info = wx.StaticText(dialog, label="提示：快速模式可显著提高生成速度，但随机性略有降低")
        generate_sizer.Add(fast_mode_info, 0, wx.ALL, 5)
        
        main_sizer.Add(generate_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # 保存选项
        save_box = wx.StaticBox(dialog, label="保存选项")
        save_sizer = wx.StaticBoxSizer(save_box, wx.VERTICAL)
        
        auto_save_check = wx.CheckBox(dialog, label="生成后自动保存")
        auto_save_check.SetValue(self.settings['auto_save'])
        save_sizer.Add(auto_save_check, 0, wx.ALL, 5)
        
        clear_existing_check = wx.CheckBox(dialog, label="清空现有激活码")
        save_sizer.Add(clear_existing_check, 0, wx.ALL, 5)
        
        main_sizer.Add(save_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # 按钮
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_generate = wx.Button(dialog, label="生成")
        btn_cancel = wx.Button(dialog, wx.ID_CANCEL, "取消")
        btn_sizer.Add(btn_generate, 0, wx.RIGHT, 10)
        btn_sizer.Add(btn_cancel, 0)
        main_sizer.Add(btn_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        dialog.SetSizer(main_sizer)
        dialog.Center()
        
        # 绑定生成按钮事件
        def on_generate_clicked(event):
            try:
                cnt = self.batch_count_input.GetValue()
                if cnt <= 0:
                    wx.MessageBox("请输入正整数！", "错误", wx.OK | wx.ICON_ERROR)
                    return
                
                # 创建临时设置，包含快速生成模式选项
                temp_settings = self.settings.copy()
                temp_settings['fast_mode'] = fast_mode_check.GetValue()
                
                # 显示进度提示
                with wx.BusyInfo("正在生成激活码，请稍候..."):
                    # 使用设置生成激活码
                    new_codes = jhm(cnt, temp_settings)
                
                # 处理清空现有激活码选项
                if clear_existing_check.GetValue():
                    self.generated_codes = new_codes
                else:
                    # 追加到现有激活码
                    self.generated_codes.extend(new_codes)
                
                # 更新文本框
                self.text_output.SetValue("\n".join(self.generated_codes))
                
                # 显示成功提示
                wx.MessageBox(f"成功生成 {cnt} 个激活码！", "成功", wx.OK | wx.ICON_INFORMATION)
                
                # 自动保存
                if auto_save_check.GetValue():
                    self.on_save(None)
                
                dialog.EndModal(wx.ID_OK)
            except Exception as e:
                wx.MessageBox(f"生成失败：{str(e)}", "错误", wx.OK | wx.ICON_ERROR)
        
        btn_generate.Bind(wx.EVT_BUTTON, on_generate_clicked)
        
        dialog.ShowModal()
        dialog.Destroy()
    
    def on_settings(self, event):
        """设置生成参数"""
        # 创建设置对话框
        dialog = wx.Dialog(self, title="设置", size=(400, 520))
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 激活码格式设置
        format_box = wx.StaticBox(dialog, label="激活码格式")
        format_sizer = wx.StaticBoxSizer(format_box, wx.VERTICAL)
        
        # 段数设置
        segment_sizer = wx.BoxSizer(wx.HORIZONTAL)
        segment_sizer.Add(wx.StaticText(dialog, label="段数："), 0, wx.RIGHT, 10)
        self.segment_spin = wx.SpinCtrl(dialog, min=1, max=10, initial=self.settings['segments'])
        segment_sizer.Add(self.segment_spin, 1)
        format_sizer.Add(segment_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        # 每段长度设置
        length_sizer = wx.BoxSizer(wx.HORIZONTAL)
        length_sizer.Add(wx.StaticText(dialog, label="每段长度："), 0, wx.RIGHT, 10)
        self.length_spin = wx.SpinCtrl(dialog, min=1, max=10, initial=self.settings['segment_length'])
        length_sizer.Add(self.length_spin, 1)
        format_sizer.Add(length_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        # 分隔符设置
        delimiter_sizer = wx.BoxSizer(wx.HORIZONTAL)
        delimiter_sizer.Add(wx.StaticText(dialog, label="分隔符："), 0, wx.RIGHT, 10)
        self.delimiter_input = wx.TextCtrl(dialog, value=self.settings['delimiter'], size=(50, -1))
        delimiter_sizer.Add(self.delimiter_input, 1)
        format_sizer.Add(delimiter_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        main_sizer.Add(format_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # 字符集设置
        charset_box = wx.StaticBox(dialog, label="字符集")
        charset_sizer = wx.StaticBoxSizer(charset_box, wx.VERTICAL)
        
        self.digits_check = wx.CheckBox(dialog, label="包含数字 (0-9)")
        self.digits_check.SetValue(self.settings['include_digits'])
        charset_sizer.Add(self.digits_check, 0, wx.ALL, 5)
        
        self.uppercase_check = wx.CheckBox(dialog, label="包含大写字母 (A-Z)")
        self.uppercase_check.SetValue(self.settings['include_uppercase'])
        charset_sizer.Add(self.uppercase_check, 0, wx.ALL, 5)
        
        self.lowercase_check = wx.CheckBox(dialog, label="包含小写字母 (a-z)")
        self.lowercase_check.SetValue(self.settings['include_lowercase'])
        charset_sizer.Add(self.lowercase_check, 0, wx.ALL, 5)
        
        self.symbols_check = wx.CheckBox(dialog, label="包含特殊字符 (!@#$%^&*)")
        self.symbols_check.SetValue(self.settings['include_symbols'])
        charset_sizer.Add(self.symbols_check, 0, wx.ALL, 5)
        
        main_sizer.Add(charset_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # 保存设置
        save_box = wx.StaticBox(dialog, label="保存设置")
        save_sizer = wx.StaticBoxSizer(save_box, wx.VERTICAL)
        
        save_path_sizer = wx.BoxSizer(wx.HORIZONTAL)
        save_path_sizer.Add(wx.StaticText(dialog, label="保存路径："), 0, wx.RIGHT, 10)
        self.save_path_input = wx.TextCtrl(dialog, value=self.settings['save_path'], size=(200, -1))
        save_path_sizer.Add(self.save_path_input, 1)
        browse_btn = wx.Button(dialog, label="浏览...")
        browse_btn.Bind(wx.EVT_BUTTON, self.on_browse_save_path)
        save_path_sizer.Add(browse_btn, 0, wx.LEFT, 5)
        save_sizer.Add(save_path_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        self.auto_save_check = wx.CheckBox(dialog, label="自动保存生成的激活码")
        self.auto_save_check.SetValue(self.settings['auto_save'])
        save_sizer.Add(self.auto_save_check, 0, wx.ALL, 5)
        
        self.timestamp_check = wx.CheckBox(dialog, label="添加生成时间戳")
        self.timestamp_check.SetValue(self.settings['add_timestamp'])
        save_sizer.Add(self.timestamp_check, 0, wx.ALL, 5)
        
        main_sizer.Add(save_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # 按钮
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(dialog, wx.ID_OK, "确定")
        btn_cancel = wx.Button(dialog, wx.ID_CANCEL, "取消")
        btn_sizer.Add(btn_ok, 0, wx.RIGHT, 10)
        btn_sizer.Add(btn_cancel, 0)
        main_sizer.Add(btn_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        dialog.SetSizer(main_sizer)
        dialog.Center()
        
        if dialog.ShowModal() == wx.ID_OK:
            # 保存设置
            self.settings['segments'] = self.segment_spin.GetValue()
            self.settings['segment_length'] = self.length_spin.GetValue()
            self.settings['delimiter'] = self.delimiter_input.GetValue() or '-'  # 默认为'-'
            self.settings['include_digits'] = self.digits_check.GetValue()
            self.settings['include_uppercase'] = self.uppercase_check.GetValue()
            self.settings['include_lowercase'] = self.lowercase_check.GetValue()
            self.settings['include_symbols'] = self.symbols_check.GetValue()
            self.settings['save_path'] = self.save_path_input.GetValue() or '激活码.txt'  # 默认为'激活码.txt'
            self.settings['auto_save'] = self.auto_save_check.GetValue()
            self.settings['add_timestamp'] = self.timestamp_check.GetValue()
            
            # 验证至少选择了一种字符类型
            if not (self.settings['include_digits'] or self.settings['include_uppercase'] or 
                    self.settings['include_lowercase'] or self.settings['include_symbols']):
                wx.MessageBox("至少选择一种字符类型！", "错误", wx.OK | wx.ICON_ERROR)
                # 重置为默认值
                self.settings['include_digits'] = True
                self.settings['include_uppercase'] = True
        
        dialog.Destroy()
    
    def on_browse_save_path(self, event):
        """浏览保存路径"""
        with wx.FileDialog(self, "选择保存文件", wildcard="文本文件 (*.txt)|*.txt",
                          style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
            self.save_path_input.SetValue(path)
    
    def on_help(self, event):
        """查看使用说明"""
        help_text = "使用说明：\n\n"
        help_text += "1. 在生成数量输入框中输入要生成的激活码数量\n"
        help_text += "2. 点击'生成激活码'按钮生成激活码\n"
        help_text += "3. 生成的激活码会显示在下方文本框中\n"
        help_text += "4. 点击'保存到文件'按钮将激活码保存到 激活码.txt 文件\n"
        help_text += "5. 可以通过菜单栏的'文件'菜单打开已有的激活码文件\n"
        help_text += "6. 可以通过菜单栏的'编辑'菜单复制或清空激活码\n"
        help_text += "7. 可以通过菜单栏的'工具'菜单进行批量生成或设置\n"
        
        wx.MessageBox(help_text, "使用说明", wx.OK | wx.ICON_INFORMATION)
    
    def on_about(self, event):
        """关于本程序"""
        about_text = "激活码生成工具\n"
        about_text += "版本：1.0.2\n"
        about_text += "作者：myiunagn\n"
        about_text += "made by python3.11.9"
        
        wx.MessageBox(about_text, "关于", wx.OK | wx.ICON_INFORMATION)

if __name__ == "__main__":
    app = wx.App()
    frame = ActivationCodeFrame()
    frame.Show()
    app.MainLoop()



    
