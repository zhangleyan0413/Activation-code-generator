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
        super().__init__(None, title="激活码生成工具", size=(600, 450))
        self.generated_codes = []
        # 初始化设置
        self.config_file = 'config.json'  # 配置文件
        # 尝试加载配置文件
        import json
        import os
        
        # 默认设置
        default_settings = {
            'segments': 4,          # 激活码段数
            'segment_length': 5,    # 每段长度
            'delimiter': '-',       # 分隔符
            'include_digits': True, # 包含数字
            'include_uppercase': True, # 包含大写字母
            'include_lowercase': False, # 包含小写字母
            'include_symbols': False, # 包含特殊字符
            'save_path': '激活码.txt', # 保存路径
            'auto_save': False,     # 自动保存
            'add_timestamp': True,  # 添加时间戳
            'language': 'zh_CN'     # 语言设置
        }
        
        # 尝试加载配置文件
        self.settings = default_settings.copy()
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
        else:
            # 如果配置文件不存在，创建默认配置文件
            try:
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(self.settings, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"创建配置文件失败: {e}")
        # 初始化翻译字典
        self.translations = {
            'zh_CN': {
                'app_title': '激活码生成工具',
                'generate': '生成激活码',
                'save': '保存到文件',
                'batch_generate': '批量生成...',
                'settings': '设置...',
                'help': '使用说明',
                'about': '关于',
                'file': '文件',
                'edit': '编辑',
                'tools': '工具',
                'new': '新建',
                'open': '打开',
                'save_as': '另存为...',
                'exit': '退出',
                'copy': '复制',
                'clear': '清空',
                'batch_count': '数量：',
                'fast_mode': '快速生成模式（适合大量生成）',
                'fast_mode_info': '提示：快速模式可显著提高生成速度，但随机性略有降低',
                'auto_save_option': '生成后自动保存',
                'clear_existing': '清空现有激活码',
                'activation_format': '激活码格式',
                'segments': '段数：',
                'segment_length': '每段长度：',
                'delimiter': '分隔符：',
                'charset': '字符集',
                'include_digits': '包含数字 (0-9)',
                'include_uppercase': '包含大写字母 (A-Z)',
                'include_lowercase': '包含小写字母 (a-z)',
                'include_symbols': '包含特殊字符 (!@#$%^&*)',
                'save_settings': '保存设置',
                'save_path': '保存路径：',
                'browse': '浏览...',
                'auto_save': '自动保存生成的激活码',
                'add_timestamp': '添加生成时间戳',
                'language': '语言',
                'enter_count': '请输入要生成的激活码数量：',
                'positive_integer': '请输入正整数！',
                'valid_number': '请输入有效的数字！',
                'generating': '正在生成激活码，请稍候...',
                'generated': '成功生成 {count} 个激活码！',
                'generate_first': '请先生成激活码！',
                'saved_to': '激活码已保存到 {path}！',
                'save_failed': '保存失败：{error}',
                'open_file': '打开激活码文件',
                'file_opened': '成功打开文件：{path}',
                'open_failed': '打开文件失败：{error}',
                'duplicate_found': '发现重复激活码：',
                'no_duplicates': '未发现重复激活码',
                'copied': '已复制到剪贴板！',
                'clipboard_error': '无法访问剪贴板！',
                'select_first': '请先选中要复制的内容！',
                'usage': '使用说明：',
                'about_text': '激活码生成工具\n版本：1.0.2\n作者：myiunagn\nmade by python3.11.9\n\n本工具用于生成随机激活码，支持批量生成和保存功能。',
                'ok': '确定',
                'cancel': '取消'
            },
            'en_US': {
                'app_title': 'Activation Code Generator',
                'generate': 'Generate Codes',
                'save': 'Save to File',
                'batch_generate': 'Batch Generate...',
                'settings': 'Settings...',
                'help': 'Usage',
                'about': 'About',
                'file': 'File',
                'edit': 'Edit',
                'tools': 'Tools',
                'new': 'New',
                'open': 'Open',
                'save_as': 'Save As...',
                'exit': 'Exit',
                'copy': 'Copy',
                'clear': 'Clear',
                'batch_count': 'Count:',
                'fast_mode': 'Fast Generate Mode (for large batches)',
                'fast_mode_info': 'Note: Fast mode significantly improves generation speed but slightly reduces randomness',
                'auto_save_option': 'Auto save after generation',
                'clear_existing': 'Clear existing codes',
                'activation_format': 'Activation Code Format',
                'segments': 'Segments:',
                'segment_length': 'Segment Length:',
                'delimiter': 'Delimiter:',
                'charset': 'Character Set',
                'include_digits': 'Include digits (0-9)',
                'include_uppercase': 'Include uppercase letters (A-Z)',
                'include_lowercase': 'Include lowercase letters (a-z)',
                'include_symbols': 'Include symbols (!@#$%^&*)',
                'save_settings': 'Save Settings',
                'save_path': 'Save Path:',
                'browse': 'Browse...',
                'auto_save': 'Auto save generated codes',
                'add_timestamp': 'Add generation timestamp',
                'language': 'Language',
                'enter_count': 'Please enter the number of activation codes to generate:',
                'positive_integer': 'Please enter a positive integer!',
                'valid_number': 'Please enter a valid number!',
                'generating': 'Generating activation codes, please wait...',
                'generated': 'Successfully generated {count} activation codes!',
                'generate_first': 'Please generate activation codes first!',
                'saved_to': 'Activation codes saved to {path}!',
                'save_failed': 'Save failed: {error}',
                'open_file': 'Open activation code file',
                'file_opened': 'Successfully opened file: {path}',
                'open_failed': 'Failed to open file: {error}',
                'duplicate_found': 'Duplicate activation codes found:',
                'no_duplicates': 'No duplicate activation codes found',
                'copied': 'Copied to clipboard!',
                'clipboard_error': 'Cannot access clipboard!',
                'select_first': 'Please select content to copy first!',
                'usage': 'Usage:',
                'about_text': 'Activation Code Generator\nVersion: 1.0.2\nAuthor: myiunagn\nmade by python3.11.9\n\nThis tool is used to generate random activation codes, supporting batch generation and save functions.',
                'ok': 'OK',
                'cancel': 'Cancel'
            },
            'es_ES': {
                'app_title': 'Generador de Códigos de Activación',
                'generate': 'Generar Códigos',
                'save': 'Guardar en Archivo',
                'batch_generate': 'Generación por Lote...',
                'settings': 'Configuración...',
                'help': 'Uso',
                'about': 'Acerca de',
                'file': 'Archivo',
                'edit': 'Editar',
                'tools': 'Herramientas',
                'new': 'Nuevo',
                'open': 'Abrir',
                'save_as': 'Guardar Como...',
                'exit': 'Salir',
                'copy': 'Copiar',
                'clear': 'Limpiar',
                'batch_count': 'Cantidad:',
                'fast_mode': 'Modo Rápido (para lotes grandes)',
                'fast_mode_info': 'Nota: El modo rápido mejora significativamente la velocidad pero reduce ligeramente la aleatoriedad',
                'auto_save_option': 'Guardar automáticamente después de generar',
                'clear_existing': 'Limpiar códigos existentes',
                'activation_format': 'Formato del Código',
                'segments': 'Segmentos:',
                'segment_length': 'Longitud del Segmento:',
                'delimiter': 'Delimitador:',
                'charset': 'Conjunto de Caracteres',
                'include_digits': 'Incluir dígitos (0-9)',
                'include_uppercase': 'Incluir letras mayúsculas (A-Z)',
                'include_lowercase': 'Incluir letras minúsculas (a-z)',
                'include_symbols': 'Incluir símbolos (!@#$%^&*)',
                'save_settings': 'Guardar Configuración',
                'save_path': 'Ruta de Guardado:',
                'browse': 'Examinar...',
                'auto_save': 'Guardar automáticamente códigos generados',
                'add_timestamp': 'Agregar marca de tiempo',
                'language': 'Idioma',
                'enter_count': 'Por favor, ingrese el número de códigos de activación a generar:',
                'positive_integer': '¡Por favor, ingrese un entero positivo!',
                'valid_number': '¡Por favor, ingrese un número válido!',
                'generating': 'Generando códigos de activación, por favor espere...',
                'generated': '¡Se generaron exitosamente {count} códigos de activación!',
                'generate_first': '¡Primero genere códigos de activación!',
                'saved_to': '¡Códigos de activación guardados en {path}!',
                'save_failed': 'Error al guardar: {error}',
                'open_file': 'Abrir archivo de códigos de activación',
                'file_opened': 'Archivo abierto exitosamente: {path}',
                'open_failed': 'Error al abrir el archivo: {error}',
                'duplicate_found': 'Se encontraron códigos de activación duplicados:',
                'no_duplicates': 'No se encontraron códigos de activación duplicados',
                'copied': '¡Copiado al portapapeles!',
                'clipboard_error': '¡No se puede acceder al portapapeles!',
                'select_first': '¡Seleccione contenido para copiar primero!',
                'usage': 'Uso:',
                'about_text': 'Generador de Códigos de Activación\nVersión: 1.0.2\nAutor: myiunagn\nHecho con python3.11.9\n\nEsta herramienta se usa para generar códigos de activación aleatorios, compatible con generación por lotes y funciones de guardado.',
                'ok': 'Aceptar',
                'cancel': 'Cancelar'
            },
            'hi_IN': {
                'app_title': 'एक्टिवेशन कोड जनरेटर',
                'generate': 'कोड जनरेट करें',
                'save': 'फ़ाइल में सहेजें',
                'batch_generate': 'बैच जनरेशन...',
                'settings': 'सेटिंग्स...',
                'help': 'उपयोग',
                'about': 'के बारे में',
                'file': 'फ़ाइल',
                'edit': 'संपादित करें',
                'tools': 'उपकरण',
                'new': 'नया',
                'open': 'खोलें',
                'save_as': 'भेजें के रूप में...',
                'exit': 'बाहर निकलें',
                'copy': 'कॉपी करें',
                'clear': 'साफ करें',
                'batch_count': 'संख्या:',
                'fast_mode': 'फास्ट मोड (बड़े बैच के लिए)',
                'fast_mode_info': 'नोट: फास्ट मोड गति में उल्लेखनीय सुधार करता है लेकिन यादृच्छिकता को थोड़ा कम करता है',
                'auto_save_option': 'जनरेशन के बाद ऑटो सेव करें',
                'clear_existing': 'मौजूदा कोड साफ करें',
                'activation_format': 'एक्टिवेशन कोड फॉर्मेट',
                'segments': 'सेगमेंट:',
                'segment_length': 'सेगमेंट लंबाई:',
                'delimiter': 'विभाजक:',
                'charset': 'करैक्टर सेट',
                'include_digits': 'अंक शामिल करें (0-9)',
                'include_uppercase': 'डबल केस अक्षर शामिल करें (A-Z)',
                'include_lowercase': 'लोअरकेस अक्षर शामिल करें (a-z)',
                'include_symbols': 'प्रतीक शामिल करें (!@#$%^&*)',
                'save_settings': 'सेटिंग्स सहेजें',
                'save_path': 'सेव पथ:',
                'browse': 'ब्राउज़ करें...',
                'auto_save': 'जनरेट किए गए कोड ऑटो सेव करें',
                'add_timestamp': 'समय स्टैम्प जोड़ें',
                'language': 'भाषा',
                'enter_count': 'कृपया जनरेट करने के लिए एक्टिवेशन कोड की संख्या दर्ज करें:',
                'positive_integer': 'कृपया एक धनात्मक पूर्णांक दर्ज करें!',
                'valid_number': 'कृपया एक मान्य संख्या दर्ज करें!',
                'generating': 'एक्टिवेशन कोड जनरेट कर रहा है, कृपया प्रतीक्षा करें...',
                'generated': '{count} एक्टिवेशन कोड सफलतापूर्वक जनरेट किए गए!',
                'generate_first': 'कृपया पहले एक्टिवेशन कोड जनरेट करें!',
                'saved_to': 'एक्टिवेशन कोड {path} में सहेजे गए!',
                'save_failed': 'सहेजने में विफल: {error}',
                'open_file': 'एक्टिवेशन कोड फ़ाइल खोलें',
                'file_opened': 'फ़ाइल सफलतापूर्वक खोली गई: {path}',
                'open_failed': 'फ़ाइल खोलने में विफल: {error}',
                'duplicate_found': 'दोहरे एक्टिवेशन कोड पाए गए:',
                'no_duplicates': 'कोई दोहरा एक्टिवेशन कोड नहीं पाया गया',
                'copied': 'क्लिपबोर्ड में कॉपी किया गया!',
                'clipboard_error': 'क्लिपबोर्ड तक पहुंच नहीं हो सकता!',
                'select_first': 'कृपया पहले कॉपी करने के लिए सामग्री का चयन करें!',
                'usage': 'उपयोग:',
                'about_text': 'एक्टिवेशन कोड जनरेटर\nसंस्करण: 1.0.2\nलेखक: myiunagn\npython3.11.9 द्वारा बनाया गया\n\nयह टूल रैंडम एक्टिवेशन कोड जनरेट करने के लिए उपयोग किया जाता है, बैच जनरेशन और सहेजने के कार्यों का समर्थन करता है।',
                'ok': 'ठीक है',
                'cancel': 'रद्द करें'
            },
            'ar_SA': {
                'app_title': 'مولد رموز التفعيل',
                'generate': 'إنشاء رموز',
                'save': 'حفظ في الملف',
                'batch_generate': 'إنشاء دفعة...',
                'settings': 'الإعدادات...',
                'help': 'الاستخدام',
                'about': 'حول',
                'file': 'ملف',
                'edit': 'تحرير',
                'tools': 'أدوات',
                'new': 'جديد',
                'open': 'فتح',
                'save_as': 'حفظ باسم...',
                'exit': 'خروج',
                'copy': 'نسخ',
                'clear': 'مسح',
                'batch_count': 'العدد:',
                'fast_mode': 'وضع سريع (للدفعات الكبيرة)',
                'fast_mode_info': 'ملاحظة: الوضع السريع يحسن سرعة الإنشاء بشكل ملحوظ ولكن يقلل من العشوائية قليلاً',
                'auto_save_option': 'حفظ تلقائيًا بعد الإنشاء',
                'clear_existing': 'مسح الرموز الحالية',
                'activation_format': 'تنسيق الرمز',
                'segments': 'الأجزاء:',
                'segment_length': 'طول الجزء:',
                'delimiter': 'فاصل:',
                'charset': 'مجموعة الأحرف',
                'include_digits': 'تضمين أرقام (0-9)',
                'include_uppercase': 'تضمين حروف كبيرة (A-Z)',
                'include_lowercase': 'تضمين حروف صغيرة (a-z)',
                'include_symbols': 'تضمين رموز (!@#$%^&*)',
                'save_settings': 'حفظ الإعدادات',
                'save_path': 'مسار الحفظ:',
                'browse': 'تصفح...',
                'auto_save': 'حفظ الرموز المتولدة تلقائيًا',
                'add_timestamp': 'إضافة علامة زمنية',
                'language': 'اللغة',
                'enter_count': 'الرجاء إدخال عدد رموز التفعيل المراد إنشاؤها:',
                'positive_integer': 'الرجاء إدخال عدد صحيح موجب!',
                'valid_number': 'الرجاء إدخال رقم صحيح!',
                'generating': 'جارٍ إنشاء رموز التفعيل، الرجاء الانتظار...',
                'generated': 'تم إنشاء {count} رمزًا تفعيلًا بنجاح!',
                'generate_first': 'الرجاء إنشاء رموز التفعيل أولاً!',
                'saved_to': 'تم حفظ رموز التفعيل في {path}!',
                'save_failed': 'فشل الحفظ: {error}',
                'open_file': 'فتح ملف رموز التفعيل',
                'file_opened': 'تم فتح الملف بنجاح: {path}',
                'open_failed': 'فشل فتح الملف: {error}',
                'duplicate_found': 'تم العثور على رموز تكرار:',
                'no_duplicates': 'لم يتم العثور على رموز تكرار',
                'copied': 'نسخ إلى الحافظة!',
                'clipboard_error': 'لا يمكن الوصول إلى الحافظة!',
                'select_first': 'الرجاء تحديد المحتوى لإلنسخه أولاً!',
                'usage': 'الاستخدام:',
                'about_text': 'مولد رموز التفعيل\nالإصدار: 1.0.2\nالناشر: myiunagn\nصنع ب python3.11.9\n\nهذا الأداة تستخدم لإنشاء رموز التفعيل العشوائية، تدعم إنشاء الدفعات وحفظ الوظائف.',
                'ok': 'موافق',
                'cancel': 'إلغاء'
            },
            'pt_BR': {
                'app_title': 'Gerador de Códigos de Ativação',
                'generate': 'Gerar Códigos',
                'save': 'Salvar em Arquivo',
                'batch_generate': 'Geração em Lote...',
                'settings': 'Configurações...',
                'help': 'Uso',
                'about': 'Sobre',
                'file': 'Arquivo',
                'edit': 'Editar',
                'tools': 'Ferramentas',
                'new': 'Novo',
                'open': 'Abrir',
                'save_as': 'Salvar Como...',
                'exit': 'Sair',
                'copy': 'Copiar',
                'clear': 'Limpar',
                'batch_count': 'Quantidade:',
                'fast_mode': 'Modo Rápido (para lotes grandes)',
                'fast_mode_info': 'Nota: O modo rápido melhora significativamente a velocidade mas reduz ligeiramente a aleatoriedade',
                'auto_save_option': 'Salvar automaticamente após gerar',
                'clear_existing': 'Limpar códigos existentes',
                'activation_format': 'Formato do Código',
                'segments': 'Segmentos:',
                'segment_length': 'Comprimento do Segmento:',
                'delimiter': 'Delimitador:',
                'charset': 'Conjunto de Caracteres',
                'include_digits': 'Incluir dígitos (0-9)',
                'include_uppercase': 'Incluir letras maiúsculas (A-Z)',
                'include_lowercase': 'Incluir letras minúsculas (a-z)',
                'include_symbols': 'Incluir símbolos (!@#$%^&*)',
                'save_settings': 'Salvar Configurações',
                'save_path': 'Caminho de Salvamento:',
                'browse': 'Procurar...',
                'auto_save': 'Salvar automaticamente códigos gerados',
                'add_timestamp': 'Adicionar carimbo de tempo',
                'language': 'Idioma',
                'enter_count': 'Por favor, insira o número de códigos de ativação a gerar:',
                'positive_integer': 'Por favor, insira um número inteiro positivo!',
                'valid_number': 'Por favor, insira um número válido!',
                'generating': 'Gerando códigos de ativação, por favor aguarde...',
                'generated': 'Gerados com sucesso {count} códigos de ativação!',
                'generate_first': 'Por favor, gere códigos de ativação primeiro!',
                'saved_to': 'Códigos de ativação salvos em {path}!',
                'save_failed': 'Erro ao salvar: {error}',
                'open_file': 'Abrir arquivo de códigos de ativação',
                'file_opened': 'Arquivo aberto com sucesso: {path}',
                'open_failed': 'Erro ao abrir o arquivo: {error}',
                'duplicate_found': 'Códigos de ativação duplicados encontrados:',
                'no_duplicates': 'Nenhum código de ativação duplicado encontrado',
                'copied': 'Copiado para a área de transferência!',
                'clipboard_error': 'Não é possível acessar a área de transferência!',
                'select_first': 'Por favor, selecione o conteúdo para copiar primeiro!',
                'usage': 'Uso:',
                'about_text': 'Gerador de Códigos de Ativação\nVersão: 1.0.2\nAutor: myiunagn\nFeito com python3.11.9\n\nEsta ferramenta é usada para gerar códigos de ativação aleatórios, compatível com geração em lote e funções de salvamento.',
                'ok': 'OK',
                'cancel': 'Cancelar'
            },
            'ru_RU': {
                'app_title': 'Генератор Кодов Активации',
                'generate': 'Сгенерировать Коды',
                'save': 'Сохранить в Файл',
                'batch_generate': 'Пакетная Генерация...',
                'settings': 'Настройки...',
                'help': 'Использование',
                'about': 'О Программе',
                'file': 'Файл',
                'edit': 'Правка',
                'tools': 'Инструменты',
                'new': 'Новый',
                'open': 'Открыть',
                'save_as': 'Сохранить Как...',
                'exit': 'Выход',
                'copy': 'Копировать',
                'clear': 'Очистить',
                'batch_count': 'Количество:',
                'fast_mode': 'Быстрый Режим (для больших пакетов)',
                'fast_mode_info': 'Примечание: Быстрый режим значительно улучшает скорость, но немного снижает случайность',
                'auto_save_option': 'Автоматически сохранять после генерации',
                'clear_existing': 'Очистить существующие коды',
                'activation_format': 'Формат Кода',
                'segments': 'Сегменты:',
                'segment_length': 'Длина Сегмента:',
                'delimiter': 'Разделитель:',
                'charset': 'Набор Символов',
                'include_digits': 'Включить цифры (0-9)',
                'include_uppercase': 'Включить заглавные буквы (A-Z)',
                'include_lowercase': 'Включить строчные буквы (a-z)',
                'include_symbols': 'Включить символы (!@#$%^&*)',
                'save_settings': 'Сохранить Настройки',
                'save_path': 'Путь Сохранения:',
                'browse': 'Обзор...',
                'auto_save': 'Автоматически сохранять сгенерированные коды',
                'add_timestamp': 'Добавить метку времени',
                'language': 'Язык',
                'enter_count': 'Пожалуйста, введите количество кодов активации для генерации:',
                'positive_integer': 'Пожалуйста, введите положительное целое число!',
                'valid_number': 'Пожалуйста, введите действительное число!',
                'generating': 'Генерация кодов активации, пожалуйста подождите...',
                'generated': 'Успешно сгенерировано {count} кодов активации!',
                'generate_first': 'Пожалуйста, сначала сгенерируйте коды активации!',
                'saved_to': 'Коды активации сохранены в {path}!',
                'save_failed': 'Ошибка сохранения: {error}',
                'open_file': 'Открыть файл кодов активации',
                'file_opened': 'Файл успешно открыт: {path}',
                'open_failed': 'Ошибка открытия файла: {error}',
                'duplicate_found': 'Найдены дублирующиеся коды активации:',
                'no_duplicates': 'Дублирующиеся коды активации не найдены',
                'copied': 'Скопировано в буфер обмена!',
                'clipboard_error': 'Невозможно получить доступ к буферу обмена!',
                'select_first': 'Пожалуйста, сначала выберите контент для копирования!',
                'usage': 'Использование:',
                'about_text': 'Генератор Кодов Активации\nВерсия: 1.0.2\nАвтор: myiunagn\nСделано с python3.11.9\n\nЭтот инструмент используется для генерации случайных кодов активации, поддерживает пакетную генерацию и функции сохранения.',
                'ok': 'ОК',
                'cancel': 'Отмена'
            },
            'ja_JP': {
                'app_title': 'アクティベーションコードジェネレータ',
                'generate': 'コードを生成',
                'save': 'ファイルに保存',
                'batch_generate': '一括生成...',
                'settings': '設定...',
                'help': '使い方',
                'about': 'について',
                'file': 'ファイル',
                'edit': '編集',
                'tools': 'ツール',
                'new': '新規',
                'open': '開く',
                'save_as': '名前を付けて保存...',
                'exit': '終了',
                'copy': 'コピー',
                'clear': 'クリア',
                'batch_count': '数:',
                'fast_mode': '高速モード (大量生成用)',
                'fast_mode_info': '注: 高速モードは生成速度を大幅に向上させますが、ランダム性がわずかに低下します',
                'auto_save_option': '生成後に自動保存',
                'clear_existing': '既存のコードをクリア',
                'activation_format': 'コード形式',
                'segments': 'セグメント:',
                'segment_length': 'セグメント長:',
                'delimiter': '区切り:',
                'charset': '文字セット',
                'include_digits': '数字を含める (0-9)',
                'include_uppercase': '大文字を含める (A-Z)',
                'include_lowercase': '小文字を含める (a-z)',
                'include_symbols': '記号を含める (!@#$%^&*)',
                'save_settings': '設定を保存',
                'save_path': '保存パス:',
                'browse': '参照...',
                'auto_save': '生成されたコードを自動保存',
                'add_timestamp': 'タイムスタンプを追加',
                'language': '言語',
                'enter_count': '生成するアクティベーションコードの数を入力してください:',
                'positive_integer': '正の整数を入力してください!',
                'valid_number': '有効な数字を入力してください!',
                'generating': 'アクティベーションコードを生成中、お待ちください...',
                'generated': '{count}個のアクティベーションコードを正常に生成しました!',
                'generate_first': 'まずアクティベーションコードを生成してください!',
                'saved_to': 'アクティベーションコードが {path} に保存されました!',
                'save_failed': '保存に失敗しました: {error}',
                'open_file': 'アクティベーションコードファイルを開く',
                'file_opened': 'ファイルを正常に開きました: {path}',
                'open_failed': 'ファイルを開くことができません: {error}',
                'duplicate_found': '重複したアクティベーションコードが見つかりました:',
                'no_duplicates': '重複したアクティベーションコードは見つかりませんでした',
                'copied': 'クリップボードにコピーされました!',
                'clipboard_error': 'クリップボードにアクセスできません!',
                'select_first': '最初にコピーするコンテンツを選択してください!',
                'usage': '使い方:',
                'about_text': 'アクティベーションコードジェネレータ\nバージョン: 1.0.2\n作者: myiunagn\npython3.11.9 で作られた\n\nこのツールはランダムなアクティベーションコードを生成するために使用され、バッチ生成と保存機能をサポートしています。',
                'ok': 'OK',
                'cancel': 'キャンセル'
            },
            'de_DE': {
                'app_title': 'Aktivierungs-Code-Generator',
                'generate': 'Codes Generieren',
                'save': 'In Datei Speichern',
                'batch_generate': 'Batch-Generierung...',
                'settings': 'Einstellungen...',
                'help': 'Verwendung',
                'about': 'Über',
                'file': 'Datei',
                'edit': 'Bearbeiten',
                'tools': 'Werkzeuge',
                'new': 'Neu',
                'open': 'Öffnen',
                'save_as': 'Speichern Unter...',
                'exit': 'Beenden',
                'copy': 'Kopieren',
                'clear': 'Löschen',
                'batch_count': 'Anzahl:',
                'fast_mode': 'Schneller Modus (für große Batches)',
                'fast_mode_info': 'Hinweis: Der schnelle Modus verbessert die Geschwindigkeit erheblich, reduziert aber die Zufälligkeit leicht',
                'auto_save_option': 'Automatisch speichern nach der Generierung',
                'clear_existing': 'Vorhandene Codes löschen',
                'activation_format': 'Code-Format',
                'segments': 'Segmente:',
                'segment_length': 'Segmentlänge:',
                'delimiter': 'Trennzeichen:',
                'charset': 'Zeichensatz',
                'include_digits': 'Ziffern einschließen (0-9)',
                'include_uppercase': 'Großbuchstaben einschließen (A-Z)',
                'include_lowercase': 'Kleinbuchstaben einschließen (a-z)',
                'include_symbols': 'Symbole einschließen (!@#$%^&*)',
                'save_settings': 'Einstellungen Speichern',
                'save_path': 'Speicherpfad:',
                'browse': 'Durchsuchen...',
                'auto_save': 'Generierte Codes automatisch speichern',
                'add_timestamp': 'Zeitstempel hinzufügen',
                'language': 'Sprache',
                'enter_count': 'Bitte geben Sie die Anzahl der zu generierenden Aktivierungscodes ein:',
                'positive_integer': 'Bitte geben Sie eine positive ganze Zahl ein!',
                'valid_number': 'Bitte geben Sie eine gültige Zahl ein!',
                'generating': 'Generiere Aktivierungscodes, bitte warten...',
                'generated': '{count} Aktivierungscodes erfolgreich generiert!',
                'generate_first': 'Bitte generieren Sie zuerst Aktivierungscodes!',
                'saved_to': 'Aktivierungscodes in {path} gespeichert!',
                'save_failed': 'Speichern fehlgeschlagen: {error}',
                'open_file': 'Aktivierungscode-Datei öffnen',
                'file_opened': 'Datei erfolgreich geöffnet: {path}',
                'open_failed': 'Öffnen der Datei fehlgeschlagen: {error}',
                'duplicate_found': 'Doppelte Aktivierungscodes gefunden:',
                'no_duplicates': 'Keine doppelten Aktivierungscodes gefunden',
                'copied': 'In die Zwischenablage kopiert!',
                'clipboard_error': 'Zugriff auf die Zwischenablage nicht möglich!',
                'select_first': 'Bitte wählen Sie zuerst den zu kopierenden Inhalt aus!',
                'usage': 'Verwendung:',
                'about_text': 'Aktivierungs-Code-Generator\nVersion: 1.0.2\nAutor: myiunagn\nErstellt mit python3.11.9\n\nDieses Tool wird verwendet, um zufällige Aktivierungscodes zu generieren, unterstützt Batch-Generierung und Speicherfunktionen.',
                'ok': 'OK',
                'cancel': 'Abbrechen'
            },
            'fr_FR': {
                'app_title': 'Générateur de Codes dActivation',
                'generate': 'Générer des Codes',
                'save': 'Enregistrer dans un Fichier',
                'batch_generate': 'Génération par Lot...',
                'settings': 'Paramètres...',
                'help': 'Utilisation',
                'about': 'À Propos',
                'file': 'Fichier',
                'edit': 'Modifier',
                'tools': 'Outils',
                'new': 'Nouveau',
                'open': 'Ouvrir',
                'save_as': 'Enregistrer Sous...',
                'exit': 'Quitter',
                'copy': 'Copier',
                'clear': 'Effacer',
                'batch_count': 'Nombre:',
                'fast_mode': 'Mode Rapide (pour les lots volumineux)',
                'fast_mode_info': 'Note: Le mode rapide améliore considérablement la vitesse mais réduit légèrement le caractère aléatoire',
                'auto_save_option': 'Enregistrer automatiquement après génération',
                'clear_existing': 'Effacer les codes existants',
                'activation_format': 'Format du Code',
                'segments': 'Segments:',
                'segment_length': 'Longueur du Segment:',
                'delimiter': 'Délimiteur:',
                'charset': 'Jeu de Caractères',
                'include_digits': 'Inclure les chiffres (0-9)',
                'include_uppercase': 'Inclure les majuscules (A-Z)',
                'include_lowercase': 'Inclure les minuscules (a-z)',
                'include_symbols': 'Inclure les symboles (!@#$%^&*)',
                'save_settings': 'Enregistrer les Paramètres',
                'save_path': 'Chemin dEnregistrement:',
                'browse': 'Parcourir...',
                'auto_save': 'Enregistrer automatiquement les codes générés',
                'add_timestamp': 'Ajouter un horodatage',
                'language': 'Langue',
                'enter_count': 'Veuillez entrer le nombre de codes dactivation à générer:',
                'positive_integer': 'Veuillez entrer un entier positif !',
                'valid_number': 'Veuillez entrer un nombre valide !',
                'generating': 'Génération de codes dactivation, veuillez patienter...',
                'generated': '{count} codes dactivation générés avec succès !',
                'generate_first': 'Veuillez dabord générer des codes dactivation !',
                'saved_to': 'Codes dactivation enregistrés dans {path} !',
                'save_failed': 'Échec de lenregistrement : {error}',
                'open_file': 'Ouvrir un fichier de codes dactivation',
                'file_opened': 'Fichier ouvert avec succès : {path}',
                'open_failed': 'Échec de louverture du fichier : {error}',
                'duplicate_found': 'Codes dactivation en double trouvés :',
                'no_duplicates': 'Aucun code dactivation en double trouvé',
                'copied': 'Copié dans le presse-papiers !',
                'clipboard_error': 'Impossible daccéder au presse-papiers !',
                'select_first': 'Veuillez dabord sélectionner le contenu à copier !',
                'usage': 'Utilisation :',
                'about_text': 'Générateur de Codes dActivation\nVersion : 1.0.2\nAuteur : myiunagn\nFait avec python3.11.9\n\nCet outil est utilisé pour générer des codes dactivation aléatoires, compatible avec la génération par lot et les fonctions denregistrement.',
                'ok': 'OK',
                'cancel': 'Annuler'
            }
        }
        # 获取当前语言
        self.current_lang = self.settings['language']
        self.init_menu()
        self.init_ui()
    
    def init_menu(self):
        # 获取当前语言的翻译
        lang = self.current_lang
        trans = self.translations.get(lang, self.translations['zh_CN'])
        
        # 创建菜单栏
        menubar = wx.MenuBar()
        
        # 文件菜单
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_NEW, f"&{trans['new']}\tCtrl+N", trans['new'])
        file_menu.Append(wx.ID_OPEN, f"&{trans['open']}\tCtrl+O", trans['open'])
        file_menu.Append(wx.ID_SAVE, f"&{trans['save']}\tCtrl+S", trans['save'])
        file_menu.Append(wx.ID_SAVEAS, f"{trans['save_as']}\tCtrl+Shift+S", trans['save_as'])
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, f"&{trans['exit']}\tCtrl+Q", trans['exit'])
        menubar.Append(file_menu, f"&{trans['file']}")
        
        # 编辑菜单
        edit_menu = wx.Menu()
        edit_menu.Append(wx.ID_COPY, f"&{trans['copy']}\tCtrl+C", trans['copy'])
        edit_menu.Append(wx.ID_CLEAR, f"&{trans['clear']}\tCtrl+L", trans['clear'])
        menubar.Append(edit_menu, f"&{trans['edit']}")
        
        # 工具菜单
        tool_menu = wx.Menu()
        batch_generate = tool_menu.Append(-1, f"&{trans['batch_generate']}", trans['batch_generate'])
        settings = tool_menu.Append(-1, f"&{trans['settings']}", trans['settings'])
        menubar.Append(tool_menu, f"&{trans['tools']}")
        
        # 帮助菜单
        help_menu = wx.Menu()
        help_menu.Append(wx.ID_HELP, f"&{trans['help']}", trans['help'])
        help_menu.AppendSeparator()
        help_menu.Append(wx.ID_ABOUT, f"&{trans['about']}", trans['about'])
        menubar.Append(help_menu, f"&{trans['help']}")
        
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
        # 获取当前语言的翻译
        lang = self.current_lang
        trans = self.translations.get(lang, self.translations['zh_CN'])
        
        # 更新窗口标题
        self.SetTitle(trans['app_title'])
        
        panel = wx.Panel(self)
        
        # 输入区域
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label_cnt = wx.StaticText(panel, label=trans['enter_count'])
        self.entry_cnt = wx.TextCtrl(panel, value="10", size=(80, -1))
        btn_generate = wx.Button(panel, label=trans['generate'])
        btn_save = wx.Button(panel, label=trans['save'])
        
        input_sizer.Add(label_cnt, 0, wx.RIGHT, 10)
        input_sizer.Add(self.entry_cnt, 0, wx.RIGHT, 10)
        input_sizer.Add(btn_generate, 0, wx.RIGHT, 10)
        input_sizer.Add(btn_save, 0)
        
        # 输出区域
        label_output = wx.StaticText(panel, label=trans['generate'] + "：")
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
        # 获取当前语言的翻译
        lang = self.current_lang
        trans = self.translations.get(lang, self.translations['zh_CN'])
        
        try:
            cnt = int(self.entry_cnt.GetValue())
            if cnt <= 0:
                wx.MessageBox(trans['positive_integer'], "错误", wx.OK | wx.ICON_ERROR)
                return
            # 使用设置生成激活码
            self.generated_codes = jhm(cnt, self.settings)
            self.text_output.SetValue("\n".join(self.generated_codes))
            
            # 自动保存
            if self.settings['auto_save']:
                self.on_save(None)
        except ValueError:
            wx.MessageBox(trans['valid_number'], "错误", wx.OK | wx.ICON_ERROR)
    
    def on_save(self, event):
        # 获取当前语言的翻译
        lang = self.current_lang
        trans = self.translations.get(lang, self.translations['zh_CN'])
        
        if not self.generated_codes:
            if event:  # 只有用户主动点击保存时才提示
                wx.MessageBox(trans['generate_first'], "提示", wx.OK | wx.ICON_INFORMATION)
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
                wx.MessageBox(trans['saved_to'].format(path=save_path), "成功", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            if event:  # 只有用户主动点击保存时才提示
                wx.MessageBox(trans['save_failed'].format(error=str(e)), "错误", wx.OK | wx.ICON_ERROR)
    
    def on_save_as(self, event):
        """另存为功能"""
        # 获取当前语言的翻译
        lang = self.current_lang
        trans = self.translations.get(lang, self.translations['zh_CN'])
        
        if not self.generated_codes:
            wx.MessageBox(trans['generate_first'], "提示", wx.OK | wx.ICON_INFORMATION)
            return
        
        # 打开文件对话框让用户选择保存路径
        with wx.FileDialog(self, trans['save_as'], wildcard="文本文件 (*.txt)|*.txt",
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
            
            wx.MessageBox(trans['saved_to'].format(path=save_path), "成功", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(trans['save_failed'].format(error=str(e)), "错误", wx.OK | wx.ICON_ERROR)
    
    def on_new(self, event):
        """新建激活码"""
        self.entry_cnt.SetValue("10")
        self.text_output.SetValue("")
        self.generated_codes = []
    
    def on_open(self, event):
        """打开激活码文件"""
        # 获取当前语言的翻译
        lang = self.current_lang
        trans = self.translations.get(lang, self.translations['zh_CN'])
        
        with wx.FileDialog(self, trans['open_file'], wildcard="文本文件 (*.txt)|*.txt",
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
                    duplicate_info = f"{trans['duplicate_found']}\n\n"
                    for code, count in duplicates.items():
                        duplicate_info += f"{code} ({count})\n"
                    wx.MessageBox(duplicate_info, "重复检测", wx.OK | wx.ICON_WARNING)
                else:
                    wx.MessageBox(f"{trans['file_opened'].format(path=path)}\n{trans['no_duplicates']}", "成功", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(trans['open_failed'].format(error=str(e)), "错误", wx.OK | wx.ICON_ERROR)
    
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
        # 获取当前语言的翻译
        lang = self.current_lang
        trans = self.translations.get(lang, self.translations['zh_CN'])
        
        selected_text = self.text_output.GetStringSelection()
        if selected_text:
            data_obj = wx.TextDataObject()
            data_obj.SetText(selected_text)
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(data_obj)
                wx.TheClipboard.Close()
                wx.MessageBox(trans['copied'], "成功", wx.OK | wx.ICON_INFORMATION)
            else:
                wx.MessageBox(trans['clipboard_error'], "错误", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox(trans['select_first'], "提示", wx.OK | wx.ICON_INFORMATION)
    
    def on_clear(self, event):
        """清空当前激活码"""
        self.text_output.SetValue("")
        self.generated_codes = []
    
    def on_batch_generate(self, event):
        """批量生成激活码"""
        # 获取当前语言的翻译
        lang = self.current_lang
        trans = self.translations.get(lang, self.translations['zh_CN'])
        
        # 创建批量生成对话框
        dialog = wx.Dialog(self, title=trans['batch_generate'], size=(400, 400))
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 生成数量设置
        count_box = wx.StaticBox(dialog, label=trans['batch_count'].rstrip(':'))
        count_sizer = wx.StaticBoxSizer(count_box, wx.VERTICAL)
        
        count_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        count_input_sizer.Add(wx.StaticText(dialog, label=trans['batch_count']), 0, wx.RIGHT, 10)
        self.batch_count_input = wx.SpinCtrl(dialog, min=1, max=10000000000, initial=100000)
        count_input_sizer.Add(self.batch_count_input, 1)
        count_sizer.Add(count_input_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        count_info = wx.StaticText(dialog, label=trans['valid_number'])
        count_sizer.Add(count_info, 0, wx.ALL, 5)
        
        main_sizer.Add(count_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # 生成选项
        generate_box = wx.StaticBox(dialog, label="生成选项")
        generate_sizer = wx.StaticBoxSizer(generate_box, wx.VERTICAL)
        
        fast_mode_check = wx.CheckBox(dialog, label=trans['fast_mode'])
        fast_mode_check.SetValue(False)  # 默认不使用快速模式
        generate_sizer.Add(fast_mode_check, 0, wx.ALL, 5)
        
        fast_mode_info = wx.StaticText(dialog, label=trans['fast_mode_info'])
        generate_sizer.Add(fast_mode_info, 0, wx.ALL, 5)
        
        main_sizer.Add(generate_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # 保存选项
        save_box = wx.StaticBox(dialog, label="保存选项")
        save_sizer = wx.StaticBoxSizer(save_box, wx.VERTICAL)
        
        auto_save_check = wx.CheckBox(dialog, label=trans['auto_save_option'])
        auto_save_check.SetValue(self.settings['auto_save'])
        save_sizer.Add(auto_save_check, 0, wx.ALL, 5)
        
        clear_existing_check = wx.CheckBox(dialog, label=trans['clear_existing'])
        save_sizer.Add(clear_existing_check, 0, wx.ALL, 5)
        
        main_sizer.Add(save_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # 按钮
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_generate = wx.Button(dialog, label=trans['generate'])
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
                    wx.MessageBox(trans['positive_integer'], "错误", wx.OK | wx.ICON_ERROR)
                    return
                
                # 创建临时设置，包含快速生成模式选项
                temp_settings = self.settings.copy()
                temp_settings['fast_mode'] = fast_mode_check.GetValue()
                
                # 显示进度提示
                with wx.BusyInfo(trans['generating']):
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
                wx.MessageBox(trans['generated'].format(count=cnt), "成功", wx.OK | wx.ICON_INFORMATION)
                
                # 自动保存
                if auto_save_check.GetValue():
                    self.on_save(None)
                
                dialog.EndModal(wx.ID_OK)
            except Exception as e:
                wx.MessageBox(f"{trans['save_failed'].format(error=str(e))}", "错误", wx.OK | wx.ICON_ERROR)
        
        btn_generate.Bind(wx.EVT_BUTTON, on_generate_clicked)
        
        dialog.ShowModal()
        dialog.Destroy()
    
    def on_settings(self, event):
        """设置生成参数"""
        # 获取当前语言的翻译
        lang = self.current_lang
        trans = self.translations.get(lang, self.translations['zh_CN'])
        
        # 创建设置对话框
        dialog = wx.Dialog(self, title=trans['settings'], size=(400, 630))
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 激活码格式设置
        format_box = wx.StaticBox(dialog, label=trans['activation_format'])
        format_sizer = wx.StaticBoxSizer(format_box, wx.VERTICAL)
        
        # 段数设置
        segment_sizer = wx.BoxSizer(wx.HORIZONTAL)
        segment_sizer.Add(wx.StaticText(dialog, label=trans['segments']), 0, wx.RIGHT, 10)
        self.segment_spin = wx.SpinCtrl(dialog, min=1, max=10, initial=self.settings['segments'])
        segment_sizer.Add(self.segment_spin, 1)
        format_sizer.Add(segment_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        # 每段长度设置
        length_sizer = wx.BoxSizer(wx.HORIZONTAL)
        length_sizer.Add(wx.StaticText(dialog, label=trans['segment_length']), 0, wx.RIGHT, 10)
        self.length_spin = wx.SpinCtrl(dialog, min=1, max=10, initial=self.settings['segment_length'])
        length_sizer.Add(self.length_spin, 1)
        format_sizer.Add(length_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        # 分隔符设置
        delimiter_sizer = wx.BoxSizer(wx.HORIZONTAL)
        delimiter_sizer.Add(wx.StaticText(dialog, label=trans['delimiter']), 0, wx.RIGHT, 10)
        self.delimiter_input = wx.TextCtrl(dialog, value=self.settings['delimiter'], size=(50, -1))
        delimiter_sizer.Add(self.delimiter_input, 1)
        format_sizer.Add(delimiter_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        main_sizer.Add(format_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # 字符集设置
        charset_box = wx.StaticBox(dialog, label=trans['charset'])
        charset_sizer = wx.StaticBoxSizer(charset_box, wx.VERTICAL)
        
        self.digits_check = wx.CheckBox(dialog, label=trans['include_digits'])
        self.digits_check.SetValue(self.settings['include_digits'])
        charset_sizer.Add(self.digits_check, 0, wx.ALL, 5)
        
        self.uppercase_check = wx.CheckBox(dialog, label=trans['include_uppercase'])
        self.uppercase_check.SetValue(self.settings['include_uppercase'])
        charset_sizer.Add(self.uppercase_check, 0, wx.ALL, 5)
        
        self.lowercase_check = wx.CheckBox(dialog, label=trans['include_lowercase'])
        self.lowercase_check.SetValue(self.settings['include_lowercase'])
        charset_sizer.Add(self.lowercase_check, 0, wx.ALL, 5)
        
        self.symbols_check = wx.CheckBox(dialog, label=trans['include_symbols'])
        self.symbols_check.SetValue(self.settings['include_symbols'])
        charset_sizer.Add(self.symbols_check, 0, wx.ALL, 5)
        
        main_sizer.Add(charset_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # 保存设置
        save_box = wx.StaticBox(dialog, label=trans['save_settings'])
        save_sizer = wx.StaticBoxSizer(save_box, wx.VERTICAL)
        
        save_path_sizer = wx.BoxSizer(wx.HORIZONTAL)
        save_path_sizer.Add(wx.StaticText(dialog, label=trans['save_path']), 0, wx.RIGHT, 10)
        self.save_path_input = wx.TextCtrl(dialog, value=self.settings['save_path'], size=(200, -1))
        save_path_sizer.Add(self.save_path_input, 1)
        browse_btn = wx.Button(dialog, label=trans['browse'])
        browse_btn.Bind(wx.EVT_BUTTON, self.on_browse_save_path)
        save_path_sizer.Add(browse_btn, 0, wx.LEFT, 5)
        save_sizer.Add(save_path_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        self.auto_save_check = wx.CheckBox(dialog, label=trans['auto_save'])
        self.auto_save_check.SetValue(self.settings['auto_save'])
        save_sizer.Add(self.auto_save_check, 0, wx.ALL, 5)
        
        self.timestamp_check = wx.CheckBox(dialog, label=trans['add_timestamp'])
        self.timestamp_check.SetValue(self.settings['add_timestamp'])
        save_sizer.Add(self.timestamp_check, 0, wx.ALL, 5)
        
        main_sizer.Add(save_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # 语言设置
        language_box = wx.StaticBox(dialog, label=trans['language'])
        language_sizer = wx.StaticBoxSizer(language_box, wx.VERTICAL)
        
        language_choice_sizer = wx.BoxSizer(wx.HORIZONTAL)
        language_choice_sizer.Add(wx.StaticText(dialog, label=trans['language'] + "："), 0, wx.RIGHT, 10)
        # 世界使用率前十的语言
        language_names = ["简体中文", "English", "Español", "हिन्दी", "العربية", "Português", "Русский", "日本語", "Deutsch", "Français"]
        self.language_choice = wx.Choice(dialog, choices=language_names)
        # 设置默认选项
        language_codes = ['zh_CN', 'en_US', 'es_ES', 'hi_IN', 'ar_SA', 'pt_BR', 'ru_RU', 'ja_JP', 'de_DE', 'fr_FR']
        try:
            default_index = language_codes.index(self.settings['language'])
            self.language_choice.SetSelection(default_index)
        except ValueError:
            self.language_choice.SetSelection(0)  # 默认简体中文
        language_choice_sizer.Add(self.language_choice, 1)
        language_sizer.Add(language_choice_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        language_info = wx.StaticText(dialog, label="提示：语言更改需要重启程序才能生效")
        language_sizer.Add(language_info, 0, wx.ALL, 5)
        
        main_sizer.Add(language_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # 按钮
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(dialog, wx.ID_OK, trans['ok'])
        btn_cancel = wx.Button(dialog, wx.ID_CANCEL, trans['cancel'])
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
            # 保存语言设置
            language_index = self.language_choice.GetSelection()
            language_codes = ['zh_CN', 'en_US', 'es_ES', 'hi_IN', 'ar_SA', 'pt_BR', 'ru_RU', 'ja_JP', 'de_DE', 'fr_FR']
            if 0 <= language_index < len(language_codes):
                self.settings['language'] = language_codes[language_index]
            else:
                self.settings['language'] = 'zh_CN'  # 默认简体中文
            # 更新当前语言
            self.current_lang = self.settings['language']
            
            # 验证至少选择了一种字符类型
            if not (self.settings['include_digits'] or self.settings['include_uppercase'] or 
                    self.settings['include_lowercase'] or self.settings['include_symbols']):
                wx.MessageBox("至少选择一种字符类型！", "错误", wx.OK | wx.ICON_ERROR)
                # 重置为默认值
                self.settings['include_digits'] = True
                self.settings['include_uppercase'] = True
            
            # 保存设置到配置文件
            import json
            try:
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(self.settings, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"保存配置文件失败: {e}")
        
        dialog.Destroy()
    
    def on_browse_save_path(self, event):
        """浏览保存路径"""
        # 获取当前语言的翻译
        lang = self.current_lang
        trans = self.translations.get(lang, self.translations['zh_CN'])
        
        with wx.FileDialog(self, trans['save'], wildcard="文本文件 (*.txt)|*.txt",
                          style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
            self.save_path_input.SetValue(path)
    
    def on_help(self, event):
        """查看使用说明"""
        # 获取当前语言的翻译
        lang = self.current_lang
        trans = self.translations.get(lang, self.translations['zh_CN'])
        
        help_text = f"{trans['usage']}\n\n"
        help_text += f"1. {trans['enter_count']}\n"
        help_text += f"2. {trans['generate']}\n"
        help_text += "3. " + trans['generated'] + "\n"
        help_text += f"4. {trans['save']}\n"
        help_text += f"5. {trans['open']}\n"
        help_text += f"6. {trans['copy']} {trans['clear']}\n"
        help_text += f"7. {trans['batch_generate']} {trans['settings']}\n"
        
        wx.MessageBox(help_text, trans['help'], wx.OK | wx.ICON_INFORMATION)
    
    def on_about(self, event):
        """关于本程序"""
        # 获取当前语言的翻译
        lang = self.current_lang
        trans = self.translations.get(lang, self.translations['zh_CN'])
        
        wx.MessageBox(trans['about_text'], trans['about'], wx.OK | wx.ICON_INFORMATION)

if __name__ == "__main__":
    app = wx.App()
    frame = ActivationCodeFrame()
    frame.Show()
    app.MainLoop()



    
