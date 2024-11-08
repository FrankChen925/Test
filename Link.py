import sys,json,time,os,uuid
from win32com import client
from  win32gui import GetWindowText, GetForegroundWindow, SetForegroundWindow, EnumWindows
from win32process import GetWindowThreadProcessId
from datetime import datetime, timedelta

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem, QPushButton,
    QHBoxLayout, QHeaderView, QAbstractItemView, QLineEdit, QDialog, QLabel, QDialogButtonBox, QSplitter,
    QTreeWidget, QTreeWidgetItem, QMessageBox, QInputDialog,QStyle,QCheckBox,QFileDialog,QGroupBox,
    QDateTimeEdit, QTextEdit,QSizePolicy,QButtonGroup,QRadioButton
)
from PyQt5.QtCore import Qt, QSize, QDateTime
from PyQt5.QtGui import QIcon, QColor, QPalette, QPixmap

DATA_FILE = "ssh_data.json"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fask Link")
        self.setGeometry(100, 100, 1000, 600)
        
        # 設置較大的圖標大小
        icon_size = QSize(32, 32)  # 您可以根據需要調整這個大小
        self.folder_icon = self.style().standardIcon(QStyle.SP_DirClosedIcon)
        self.folder_icon = self.folder_icon.pixmap(icon_size).scaled(icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # 獲取電腦圖示
        self.computer_icon = self.style().standardIcon(QStyle.SP_ComputerIcon)

        # 設置深色主題
        self.set_dark_theme()

         # ... 其他初始化代碼 ...
        self.data = self.get_default_data()
    
        # 創建中心部件和佈局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 創建頁籤部件
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # 添加 "SSH" 頁籤
        ssh_tab = QWidget()
        self.tab_widget.addTab(ssh_tab, "SSH站台管理")

        # 在 SSH 頁籤中加入分隔器佈局
        self.create_ssh_tab(ssh_tab)

        # 創建設定按鈕
        settings_button = QPushButton("設定")
        settings_button.clicked.connect(self.show_settings)
        
        # 將設定按鈕加入到工具列
        toolbar = self.addToolBar("工具列")
        toolbar.addWidget(settings_button)

         # 添加 "產生Log網址" 頁籤
        log_url_tab = QWidget()
        self.tab_widget.addTab(log_url_tab, "產生Log網址")
        self.create_log_url_tab(log_url_tab)
        
        # 設置視窗最大化
        self.showMaximized()

        # 載入設定
        self.settings = self.load_settings()

        # 從檔案中載入資料
        self.load_data()
        
    def show_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # 重新載入設定
            self.settings = self.load_settings()
            QMessageBox.information(self, "成功", "設定已儲存！")

    def load_settings(self):
        try:
            with open("settings.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"cmder_path": "D:\\Tools\\cmder\\vendor\\conemu-maximus5\\ConEmu64.exe"}
        except json.JSONDecodeError:
            return {"cmder_path": "D:\\Tools\\cmder\\vendor\\conemu-maximus5\\ConEmu64.exe"}

    def create_log_url_tab(self, tab):
        layout = QVBoxLayout(tab)

        # 環境選擇區域
        env_group = QGroupBox("環境選擇")
        env_layout = QHBoxLayout()
        env_layout.setSpacing(20)
        
        # 創建環境選擇的 button group
        self.env_button_group = QButtonGroup()
        self.hc_radio = QRadioButton("HC")
        self.lt_radio = QRadioButton("LT")
        
        # 添加到 button group
        self.env_button_group.addButton(self.hc_radio)
        self.env_button_group.addButton(self.lt_radio)
        
        self.hc_radio.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # 設定 OMI 為預設選項
        self.hc_radio.setChecked(True)  # 加入這行

        env_layout.addWidget(self.hc_radio)
        env_layout.addWidget(self.lt_radio)
        env_group.setLayout(env_layout)
        layout.addWidget(env_group)
        
        # 日期時間選擇區域
        datetime_group = QGroupBox("日期時間選擇")
        datetime_layout = QVBoxLayout()
        
        # 開始時間
        start_layout = QHBoxLayout()
        self.start_datetime_label = QLabel("開始時間:")
        self.start_datetime_label.setStyleSheet("color: white;")
        self.start_datetime = QDateTimeEdit()
        self.start_datetime.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.start_datetime.setDateTime(QDateTime.currentDateTime())

        self.start_datetime_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        start_layout.addWidget(self.start_datetime_label)
        start_layout.addWidget(self.start_datetime)
        datetime_layout.addLayout(start_layout)

        self.delta_checkbox = QCheckBox("Delta Time")
        self.delta_checkbox.setStyleSheet("color: white;")
        datetime_layout.addWidget(self.delta_checkbox)

        datetime_group.setLayout(datetime_layout)
        layout.addWidget(datetime_group)

        # Log類型選擇區域
        log_type_group = QGroupBox("Log類型")
        log_type_layout = QHBoxLayout()
        log_type_layout.setSpacing(20)
        
        # 創建 Log 類型的 button group
        self.log_type_button_group = QButtonGroup()
        self.omi_radio = QRadioButton("OMI")
        self.brm_radio = QRadioButton("BRM")
        self.mes_radio = QRadioButton("MES")
        self.ei_gui_radio = QRadioButton("EI GUI")
        self.ei_mes_radio = QRadioButton("EI MES")
        
        # 添加到 button group
        self.log_type_button_group.addButton(self.omi_radio)
        self.log_type_button_group.addButton(self.brm_radio)
        self.log_type_button_group.addButton(self.mes_radio)
        self.log_type_button_group.addButton(self.ei_gui_radio)
        self.log_type_button_group.addButton(self.ei_mes_radio)
        
        # 設定 OMI 為預設選項
        self.omi_radio.setChecked(True)  # 加入這行

        # 設定大小策略
        self.omi_radio.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.brm_radio.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.mes_radio.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ei_gui_radio.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        log_type_layout.addWidget(self.omi_radio)
        log_type_layout.addWidget(self.brm_radio)
        log_type_layout.addWidget(self.mes_radio)
        log_type_layout.addWidget(self.ei_gui_radio)
        log_type_layout.addWidget(self.ei_mes_radio)
        
        log_type_group.setLayout(log_type_layout)
        layout.addWidget(log_type_group)

        # 關鍵字輸入區域
        keyword_group = QGroupBox("關鍵字")
        keyword_layout = QVBoxLayout()
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("輸入要查詢的關鍵字")
        keyword_layout.addWidget(self.keyword_input)
        keyword_group.setLayout(keyword_layout)
        layout.addWidget(keyword_group)

        # 生成的URL顯示區域
        url_group = QGroupBox("生成的網址")
        url_layout = QVBoxLayout()
        self.url_display = QTextEdit()
        self.url_display.setReadOnly(True)
        url_layout.addWidget(self.url_display)
        url_group.setLayout(url_layout)
        layout.addWidget(url_group)

        # 按鈕區域
        button_layout = QHBoxLayout()
        generate_button = QPushButton("產生Log網址")
        generate_button.clicked.connect(self.generate_log_url)
        button_layout.addWidget(generate_button)
        layout.addLayout(button_layout)

        # 添加彈性空間
        layout.addStretch()

    def generate_log_url(self):
        """生成Log��址的邏輯"""
        if not (self.hc_checkbox.isChecked() or self.lt_checkbox.isChecked()):
            QMessageBox.warning(self, "警告", "請至少選擇一個環境 (HC/LT)！")
            return

        if not any([
            self.omi_checkbox.isChecked(),
            self.brm_checkbox.isChecked(),
            self.mes_checkbox.isChecked(),
            self.ei_gui_checkbox.isChecked(),
            self.ei_mes_checkbox.isChecked()
        ]):
            QMessageBox.warning(self, "警告", "請至少選擇一種Log類型！")
            return

        # 從設定檔加載網址
        settings = self.load_settings()

        generated_urls = []

        # 獲取時間範圍
        start_time = self.start_datetime.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        end_time = None
        if self.delta_checkbox.isChecked():
            end_time = self.end_datetime.dateTime().toString("yyyy-MM-dd HH:mm:ss")

        keyword = self.keyword_input.text().strip()

        # 為每個選擇的環境生成URL
        environments = []
        if self.hc_checkbox.isChecked():
            environments.append(("HC", {
                "mes": settings.get("mes_log_hc_string", ""),
                "ei": settings.get("ei_log_hc_string", ""),
                "old": settings.get("old_log_hc_string", "")
            }))
        if self.lt_checkbox.isChecked():
            environments.append(("LT", {
                "mes": settings.get("mes_log_lt_string", ""),
                "ei": settings.get("ei_log_lt_string", ""),
                "old": settings.get("old_log_lt_string", "")
            }))

        for env_name, urls in environments:
            if self.mes_checkbox.isChecked():
                base_url = urls["mes"]
                if base_url:
                    url = f"{base_url}?startTime={start_time}"
                    if end_time:
                        url += f"&endTime={end_time}"
                    if keyword:
                        url += f"&keyword={keyword}"
                    generated_urls.append(f"MES Log {env_name}:\n{url}\n")

            if self.ei_mes_checkbox.isChecked() or self.ei_gui_checkbox.isChecked():
                base_url = urls["ei"]
                if base_url:
                    url = f"{base_url}?startTime={start_time}"
                    if end_time:
                        url += f"&endTime={end_time}"
                    if keyword:
                        url += f"&keyword={keyword}"
                    if self.ei_mes_checkbox.isChecked():
                        generated_urls.append(f"EI MES Log {env_name}:\n{url}\n")
                    if self.ei_gui_checkbox.isChecked():
                        generated_urls.append(f"EI GUI Log {env_name}:\n{url}\n")

            if self.omi_checkbox.isChecked() or self.brm_checkbox.isChecked():
                base_url = urls["old"]
                if base_url:
                    url = f"{base_url}?startTime={start_time}"
                    if end_time:
                        url += f"&endTime={end_time}"
                    if keyword:
                        url += f"&keyword={keyword}"
                    if self.omi_checkbox.isChecked():
                        generated_urls.append(f"OMI Log {env_name}:\n{url}\n")
                    if self.brm_checkbox.isChecked():
                        generated_urls.append(f"BRM Log {env_name}:\n{url}\n")

        # 顯示生成的URL
        self.url_display.setText("\n".join(generated_urls))

    def set_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)

        self.setPalette(dark_palette)

        # 設置應用程序樣式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #353535;
            }
            QTreeWidget {
                background-color: #252525;
                color: #ffffff;
                border: 1px solid #555555;
            }
            QTreeWidget::item:selected {
                background-color: #2979ff;  /* 使用更明顯的藍色 */
                color: white;
            }
            QTreeWidget::item:hover {
                background-color: #1565c0;  /* 懸停時的顏色 */
                color: white;
            }
            QTableWidget {
                background-color: #252525;
                color: #ffffff;
                gridline-color: #555555;
                border: 1px solid #555555;
            }
            QHeaderView::section {
                background-color: #353535;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #555555;
            }
            QPushButton {
                background-color: #454545;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:pressed {
                background-color: #353535;
            }
            QTabWidget::pane {
                border: 1px solid #555555;
            }
            QTabBar::tab {
                background-color: #353535;
                color: #ffffff;
                padding: 8px;
                border: 1px solid #555555;
            }
            QTabBar::tab:selected {
                background-color: #454545;
            }
            QLineEdit {
                background-color: #252525;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 3px;
            }
            QCheckBox,QRadioButton { 
                font-size: 20px;
                font-weight: bold;
            }
            QGroupBox {
                color: #ffffff;
                border: 2px solid #555555;
                border-radius: 5px;
                margin-top: 1em;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """)

    def set_application_font(self, font_family, font_size):
        style_sheet = f"""
            QWidget {{
                font-family: {font_family};
                font-size: {font_size}px;
            }}
        """
        QApplication.instance().setStyleSheet(style_sheet)

    def set_tree_font(self, font_family, font_size):
        self.tree.setStyleSheet(f"""
            QTreeWidget {{
                font-family: {font_family};
                font-size: {font_size}px;
            }}
        """)

    def set_grid_font(self, font_family, font_size):
        self.table.setStyleSheet(f"""
            QTableWidget {{
                font-family: {font_family};
                font-size: {font_size}px;
            }}
        """)

    def create_ssh_tab(self, ssh_tab):
        # 創建分隔器
        splitter = QSplitter()

        # 設置分隔器的樣式
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #555555;
            }
        """)

        # 創建左側 Tree
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("連線群組")
        self.tree.setColumnCount(1)
        self.tree.setIconSize(QSize(32, 32))  # 設置與圖標相同的大小
        self.tree.itemClicked.connect(self.on_tree_node_clicked)

        # 右側表格
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["","名稱", "IP", "帳號", "密碼", "啟動", "透過主機"])
        self.table.setColumnHidden(6, True)  # 隱藏 "透過主機連線" 列

        # 設置第一列（圖示列）的寬度
        self.table.setColumnWidth(0, 10)  # 根據需要調整寬度

        # 隱藏行號 (最前面的列號標題)
        self.table.verticalHeader().setVisible(False)
        #self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 設定選擇行
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 在右側表格加入控制按鈕
        control_layout = QHBoxLayout()
        add_button = QPushButton("新增")
        remove_button = QPushButton("刪除")
        edit_button = QPushButton("修改")

        control_layout.addWidget(add_button)
        control_layout.addWidget(remove_button)
        control_layout.addWidget(edit_button)

        add_button.clicked.connect(self.add_row)
        remove_button.clicked.connect(self.remove_row)
        edit_button.clicked.connect(self.edit_row)

        # Tree 按鈕區
        tree_control_layout = QHBoxLayout()
        add_node_button = QPushButton("新增節點")
        remove_node_button = QPushButton("刪除節點")
        edit_node_button = QPushButton("修改節點名稱")

        tree_control_layout.addWidget(add_node_button)
        tree_control_layout.addWidget(remove_node_button)
        tree_control_layout.addWidget(edit_node_button)

        add_node_button.clicked.connect(self.add_tree_node)
        remove_node_button.clicked.connect(self.remove_tree_node)
        edit_node_button.clicked.connect(self.edit_tree_node)

        # 左側佈局
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.tree)
        left_layout.addLayout(tree_control_layout)

        # 右側佈局
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.table)
        right_layout.addLayout(control_layout)

        # 左右分割設定
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 1)  # 左側 Tree 佔 20%
        splitter.setStretchFactor(1, 9)  # 右側 Grid 佔 80%

        self.set_application_font("Consolas",20)

        self.set_tree_font("微軟正黑體", 27)
        self.set_grid_font("微軟正黑體", 24)

        main_layout = QVBoxLayout(ssh_tab)
        main_layout.addWidget(splitter)

    def set_column_widths(self, column_widths):
        """用百分比設定每個欄位的寬度."""
        total_width = self.table.viewport().width()
        icon_width = 10  # 固定圖示列寬度
        remaining_width = total_width - icon_width
        self.table.setColumnWidth(0, icon_width)

        for index, width_ratio in enumerate(column_widths):
            self.table.setColumnWidth(index+1, int(remaining_width  * width_ratio))

    def on_resize(self, event):
        """視窗大小改變時，自動調整欄位寬度."""
        self.set_column_widths([0.282, 0.17, 0.17,0.17,0.1])
        super().resizeEvent(event)

    def add_row(self):
        if not self.tree.currentItem():
            QMessageBox.warning(self, "警告", "請選擇一個節點進行新增連線！")
            return

        dialog = EntryDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            name, ip, account, password, via_host = dialog.getInputs()
            selected_connection_id = dialog.get_selected_connection_id()  # 獲取選中的連線ID
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            # 產生唯一識別碼
            unique_id = str(uuid.uuid4())

            # 添加電腦圖示
            icon_label = QLabel(self.table)
            icon_label.setPixmap(self.computer_icon.pixmap(QSize(32, 32)))
            icon_label.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(row_position, 0, icon_label)

            # 將唯一識別碼存儲在第一個單元格的userData中
            name_item = QTableWidgetItem(name)
            name_item.setData(Qt.UserRole, unique_id)
            
            self.table.setItem(row_position, 1, name_item)
            self.table.setItem(row_position, 2, QTableWidgetItem(ip))
            self.table.setItem(row_position, 3, QTableWidgetItem(account))
            self.table.setItem(row_position, 4, QTableWidgetItem(password))
            connect_button = QPushButton("連線")
            connect_button.clicked.connect(lambda: self.connect_to_server(row_position))
            self.table.setCellWidget(row_position, 5, connect_button)

            # 在第6列儲存via_host和連線ID的信息
            via_host_info = {
                "enabled": via_host,
                "connection_id": selected_connection_id if via_host else None
            }

            self.table.setItem(row_position, 6, QTableWidgetItem(json.dumps(via_host_info)))

            self.save_data()

    def edit_row(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            # 獲取當前行的所有數據，包括unique_id
            current_name_item = self.table.item(selected_row, 1)
            current_unique_id = current_name_item.data(Qt.UserRole)  # 保存原有的unique_id
            current_name = current_name_item.text()
            current_ip = self.table.item(selected_row, 2).text()
            current_account = self.table.item(selected_row, 3).text()
            current_password = self.table.item(selected_row, 4).text()
            
            # 解析當前的via_host信息
            via_host_info = json.loads(self.table.item(selected_row, 6).text())
            current_via_host = via_host_info.get("enabled", False)
            current_via_host_id = via_host_info.get("connection_id")

            dialog = EntryDialog(
                self, 
                current_name, 
                current_ip, 
                current_account, 
                current_password, 
                current_via_host,
                current_via_host_id
            )
            
            if dialog.exec_() == QDialog.Accepted:
                name, ip, account, password, via_host = dialog.getInputs()
                selected_connection_id = dialog.get_selected_connection_id()
                
                # 創建新的QTableWidgetItem並保留原有的unique_id
                name_item = QTableWidgetItem(name)
                name_item.setData(Qt.UserRole, current_unique_id)  # 使用原有的unique_id
                
                self.table.setItem(selected_row, 1, name_item)
                self.table.setItem(selected_row, 2, QTableWidgetItem(ip))
                self.table.setItem(selected_row, 3, QTableWidgetItem(account))
                self.table.setItem(selected_row, 4, QTableWidgetItem(password))
                
                # 更新via_host信息
                via_host_info = {
                    "enabled": via_host,
                    "connection_id": selected_connection_id if via_host else None
                }
                self.table.setItem(selected_row, 6, QTableWidgetItem(json.dumps(via_host_info)))
                
                self.save_data()

    def remove_row(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.table.removeRow(selected_row)
            self.save_data()

    def connect_to_server(self, row):
        name = self.table.item(row, 1).text()
        ip = self.table.item(row, 2).text()
        account = self.table.item(row, 3).text()
        password = self.table.item(row, 4).text()
        
        # 解析via_host資訊
        via_host_info = json.loads(self.table.item(row, 6).text())
        is_via_host = via_host_info.get("enabled", False)
        via_host_id = via_host_info.get("connection_id")
        
        shell = client.Dispatch("WScript.Shell")
        run_venv = ActivateVenv()

        if is_via_host and via_host_id:
            # 找到中繼主機的連線資訊
            via_host_conn = self.find_connection_by_id(self.data, via_host_id)
            if via_host_conn:
                run_venv.open_cmd(shell,name)
                # 先連接到中繼主機
                run_venv.activate_venv(shell, via_host_conn["ip"], via_host_conn["account"], via_host_conn["password"])
                time.sleep(1)  # 等待連接建立
                # 然後從中繼主機連接到目標主機
                run_venv.activate_venv(shell, ip, account, password)
            else:
                QMessageBox.warning(self, "錯誤", "找不到指定的中繼主機連線資訊！")
        else:
            run_venv.open_cmd(shell,name)
            # 直接連接到目標主機
            run_venv.activate_venv(shell, ip, account, password)

    def find_connection_by_id(self,node_data, target_id):
        # 檢查當前節點的connections
        for conn in node_data.get("connections", []):
            if conn.get("id") == target_id:
                return conn
        
        # 遞迴檢查子節點
        for child in node_data.get("children", []):
            result = self.find_connection_by_id(child, target_id)
            if result:
                return result
        return None

    def add_tree_node(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            new_name, ok = QInputDialog.getText(self, "新增節點", "請輸入新節點名稱：")
            if ok and new_name.strip():
                new_node = QTreeWidgetItem()
                new_node.setText(0, new_name)
                new_node.setIcon(0, QIcon(self.folder_icon))
                
                # 生成新的 node_id
                new_node_id = str(uuid.uuid4())
                new_node.setData(0, Qt.UserRole, new_node_id)
                
                selected_item.addChild(new_node)
                self.tree.expandItem(selected_item)
                
                # 將新節點加入資料並儲存
                parent_node_id = selected_item.data(0, Qt.UserRole)
                self.add_node_to_data(parent_node_id, new_name, new_node_id)
                self.save_data()

    def add_node_to_data(self, parent_node_id, new_name, new_node_id):
        def add_recursive(node):
            if node["node_id"] == parent_node_id:
                node["children"].append({
                    "node_id": new_node_id,
                    "name": new_name,
                    "connections": [],
                    "children": []
                })
                return True
            for child in node["children"]:
                if add_recursive(child):
                    return True
            return False

        add_recursive(self.data)

    def remove_tree_node(self):
        """刪除選中的樹形節點，同時更新資料結構."""
        selected_item = self.tree.currentItem()
        if selected_item and selected_item.parent():
            node_name = selected_item.text(0)

            # 刪除樹上的節點
            parent = selected_item.parent()
            parent.removeChild(selected_item)

            # 遞迴地在 self.data 中刪除該節點的資料
            parent_name = parent.text(0)
            parent_data = self.find_node_data(self.data, parent_name)
            if parent_data:
                # 刪除父節點中的對應子節點
                self.remove_node_from_data(parent_data, node_name)

            # 儲存更新後的資料
            self.save_data(isRemoveNode=True)
        else:
            QMessageBox.warning(self, "警告", "無法刪除根節點或未選擇節點！")

    def remove_node_from_data(self, parent_data, node_name):
        """遞迴地在父節點資料中移除指定名稱的子節點."""
        for i, child in enumerate(parent_data["children"]):
            if child["name"] == node_name:
                del parent_data["children"][i]
                return
            self.remove_node_from_data(child, node_name)

    def edit_tree_node(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            old_name = selected_item.text(0)
            new_name, ok = QInputDialog.getText(self, "修改節點名稱", "請輸入新名稱：", QLineEdit.Normal, old_name)
            if ok and new_name.strip() and new_name != old_name:
                if new_name.strip() == "":
                    QMessageBox.warning(self, "錯誤", "節點名稱不可為空白！")
                    return
                
                # 更新樹形結構
                selected_item.setText(0, new_name)
                
                # 更新數據結構
                try:
                    self.update_node_name_in_data(old_name, new_name)
                    self.save_data()
                except KeyError as e:
                    QMessageBox.warning(self, "錯誤", f"更新節點名稱時發生錯誤：{str(e)}")
                    # 回滾樹形結構的更改
                    selected_item.setText(0, old_name)

    def update_node_name_in_data(self, old_name, new_name):
        def update_recursive(node):
            if isinstance(node, dict):
                if node.get("name") == old_name:
                    node["name"] = new_name
                    return True
                for child in node.get("children", []):
                    if update_recursive(child):
                        return True
            return False

        if not update_recursive(self.data):
            raise KeyError(f"找不到節點：{old_name}")

    def check_duplicate_node(self, node_name):
        root = self.tree.topLevelItem(0)  # 根節點
        return self.find_node_by_name(root, node_name)

    def find_node_by_name(self, node, name):
        if node.text(0) == name:
            return True
        for i in range(node.childCount()):
            if self.find_node_by_name(node.child(i), name):
                return True
        return False

    def on_tree_node_clicked(self, item, column):
        node_id = item.data(0, Qt.UserRole)
        self.populate_table(node_id)
        self.set_column_widths([0.282, 0.2, 0.2,0.2,0.1])

    def populate_tree_with_hierarchy(self, node_data, parent=None):
        if not self.is_valid_node(node_data):
            return

        if parent is None:
            self.tree.clear()
            root = QTreeWidgetItem(self.tree)
            root.setText(0, node_data["name"])
            root.setIcon(0, QIcon(self.folder_icon))
            root.setData(0, Qt.UserRole, node_data["node_id"])
            
            for child in node_data.get("children", []):
                self.populate_tree_with_hierarchy(child, root)
        else:
            child_item = QTreeWidgetItem(parent)
            child_item.setText(0, node_data["name"])
            child_item.setIcon(0, QIcon(self.folder_icon))
            child_item.setData(0, Qt.UserRole, node_data["node_id"])
            for child in node_data.get("children", []):
                self.populate_tree_with_hierarchy(child, child_item)

        if parent is None:
            self.tree.expandAll()
                
    def create_connect_button(self, row_position):
        """創建連線按鈕並綁定對應行號"""
        connect_button = QPushButton("連線")
        def on_button_clicked():
            self.connect_to_server(row_position)
        connect_button.clicked.connect(on_button_clicked)
        return connect_button

    def populate_table(self, node_id):
        self.table.setRowCount(0)
        selected_node_data = self.find_node_data_by_id(self.data, node_id)
        if selected_node_data:
            for connection in selected_node_data.get("connections", []):
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)

                # 添加電腦圖示
                icon_label = QLabel(self.table)
                icon_label.setPixmap(self.computer_icon.pixmap(QSize(32, 32)))
                icon_label.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(row_position, 0, icon_label)

                # 創建帶有唯一識別碼的項目
                name_item = QTableWidgetItem(connection["name"])
                name_item.setData(Qt.UserRole, connection.get("id", str(uuid.uuid4())))  # 使用已存在的id或創建新的
                
                self.table.setItem(row_position, 1, name_item)
                self.table.setItem(row_position, 2, QTableWidgetItem(connection["ip"]))
                self.table.setItem(row_position, 3, QTableWidgetItem(connection["account"]))
                self.table.setItem(row_position, 4, QTableWidgetItem(connection["password"]))
                connect_button = QPushButton("連線")
                
                # 使用專門的函式創建按鈕
                connect_button = self.create_connect_button(row_position)
                self.table.setCellWidget(row_position, 5, connect_button)
                #connect_button.clicked.connect(lambda checked, row=row_position: self.connect_to_server(row))
                #self.table.setCellWidget(row_position, 5, connect_button)
                
                # 設置via_host信息
                via_host_info = {
                    "enabled": connection.get("via_host", False),
                    "connection_id": connection.get("via_host_id")
                }
                self.table.setItem(row_position, 6, QTableWidgetItem(json.dumps(via_host_info)))

    def find_node_data_by_id(self, node_data, node_id):
        if node_data["node_id"] == node_id:
            return node_data
        for child in node_data.get("children", []):
            result = self.find_node_data_by_id(child, node_id)
            if result:
                return result
        return None
    
    def load_data(self):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as file:
                self.data = json.load(file)

            if not self.is_valid_node(self.data):
                QMessageBox.warning(self, "錯誤", "載入的 JSON 資料格式不正確，已重置為初始格式！")
                self.data = self.get_default_data()
                self.save_data()

            self.populate_tree_with_hierarchy(self.data)
        except FileNotFoundError:
            self.data = self.get_default_data()
            self.save_data()
            self.populate_tree_with_hierarchy(self.data)
        except json.JSONDecodeError:
            QMessageBox.warning(self, "錯誤", "JSON 檔案格式錯誤，已重置為初始格式！")
            self.data = self.get_default_data()
            self.save_data()
            self.populate_tree_with_hierarchy(self.data)

    def get_default_data(self):
        """返回一個包含根節點的初始資料結構"""
        return {
            "node_id": str(uuid.uuid4()),
            "name": "/",
            "connections": [],
            "children": []
        }

    def is_valid_node(self, node):
        """檢查節點資料結構是否包含必要欄位"""
        return isinstance(node, dict) and "name" in node and "connections" in node and "children" in node

    def save_data(self,isRemoveNode=False):
        root = self.tree.topLevelItem(0)  # 取得根節點
        if root:
            self.data = self.traverse_tree_and_save_with_hierarchy(root,isRemoveNode)  # 遍歷整個樹並儲存所有節點的資料

        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            QMessageBox.warning(self, "錯誤", f"保存數據時發生錯誤：{str(e)}")

    def traverse_tree_and_save_with_hierarchy(self, node, isRemoveNode=False):
        node_name = node.text(0)
        node_id = node.data(0, Qt.UserRole)
        node_data = {
            "node_id": node_id,
            "name": node_name,
            "connections": [],
            "children": []
        }

        existing_node_data = self.find_node_data_by_id(self.data, node_id)
        if existing_node_data:
            node_data["connections"] = existing_node_data.get("connections", [])

        if node == self.tree.currentItem() and not isRemoveNode:
            node_data["connections"] = []
            for row in range(self.table.rowCount()):
                # 獲取唯一識別碼
                name_item = self.table.item(row, 1)
                unique_id = name_item.data(Qt.UserRole) if name_item else str(uuid.uuid4())
                
                # 解析via_host信息
                via_host_info = json.loads(self.table.item(row, 6).text())
                
                connection = {
                    "id": unique_id,  # 保存唯一識別碼
                    "name": self.table.item(row, 1).text(),
                    "ip": self.table.item(row, 2).text(),
                    "account": self.table.item(row, 3).text(),
                    "password": self.table.item(row, 4).text(),
                    "via_host": via_host_info.get("enabled", False),
                    "via_host_id": via_host_info.get("connection_id")
                }
                node_data["connections"].append(connection)

        for i in range(node.childCount()):
            child_node = node.child(i)
            node_data["children"].append(self.traverse_tree_and_save_with_hierarchy(child_node, isRemoveNode))

        return node_data
  
    def load_data_from_file(self):
        """從檔案中載入現有資料"""
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = self.get_default_data()
            
    def populate_tree(self):
        self.tree.clear()
        root = QTreeWidgetItem(self.tree)
        root.setText(0, "/")
        root.setIcon(0, QIcon(self.folder_icon))
        for nodeItem in self.data["children"]:
            node_name=nodeItem['name']
            
            if node_name != "/":
                node = QTreeWidgetItem(root)
                node.setText(0, node_name)
                node.setIcon(0, QIcon(self.folder_icon))
        self.tree.expandAll()

class EntryDialog(QDialog):
    def __init__(self, parent=None, name="", ip="", account="", password="", via_host=False, via_host_id=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("輸入資料")
        self.setMinimumWidth(400)
        layout = QVBoxLayout()
        
        # 為對話框中的樹狀結構設置相同的選取樣式
        self.setStyleSheet("""
            QTreeWidget {
                background-color: #252525;
                color: #ffffff;
                border: 1px solid #555555;
            }
            QTreeWidget::item:selected {
                background-color: #2979ff;
                color: white;
            }
            QTreeWidget::item:hover {
                background-color: #1565c0;
                color: white;
            }
        """)

        # 記錄當前選擇的連線資訊
        self.selected_connection = None
        self.selected_connection_id = via_host_id  # 新增：儲存已選擇的連線ID

        # 基本輸入欄位
        layout.addWidget(QLabel("名稱: *"))
        self.name_input = QLineEdit(name)
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("IP: *"))
        self.ip_input = QLineEdit(ip)
        layout.addWidget(self.ip_input)

        layout.addWidget(QLabel("帳號: *"))
        self.account_input = QLineEdit(account)
        layout.addWidget(self.account_input)

        layout.addWidget(QLabel("密碼: *"))
        self.password_input = QLineEdit(password)
        layout.addWidget(self.password_input)

        # 透過主機連線 checkbox
        self.via_host_checkbox = QCheckBox("透過主機連線")
        self.via_host_checkbox.setChecked(via_host)
        self.via_host_checkbox.stateChanged.connect(self.on_checkbox_changed)
        layout.addWidget(self.via_host_checkbox)

        # 選擇連線提示標籤
        self.connection_label = QLabel("請選擇連線主機: *")
        self.connection_label.setVisible(via_host)
        layout.addWidget(self.connection_label)

        # 新增樹狀結構
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("連線群組")
        self.tree.setColumnCount(1)
        self.tree.setEnabled(via_host)
        self.tree.itemClicked.connect(self.on_tree_item_clicked)
        layout.addWidget(self.tree)

        # 顯示當前選擇的連線
        self.selected_label = QLabel()
        self.selected_label.setVisible(via_host)
        layout.addWidget(self.selected_label)

        # 如果有預設的via_host_id，在樹狀結構載入後選中對應的項目
        self.tree.itemClicked.connect(self.on_tree_item_clicked)
        if via_host_id:
            self.restore_selected_connection(via_host_id)

        # 載入樹狀結構資料
        if hasattr(parent, 'data'):
            self.populate_tree_with_hierarchy(parent.data)

            # 如果有勾選 via_host 且有 via_host_id，自動展開並選取節點
            if via_host and via_host_id:
                self.tree.expandAll()  # 展開所有節點
                self.restore_selected_connection(via_host_id)

        # 按鈕
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def restore_selected_connection(self, via_host_id):
        """根據saved_connection_id恢復選中狀態"""
        def find_connection_item(item):
            # 檢查當前項目
            conn_data = item.data(0, Qt.UserRole)
            if conn_data and conn_data.get('id') == via_host_id:
                return item
            
            # 遞迴檢查子項目
            for i in range(item.childCount()):
                result = find_connection_item(item.child(i))
                if result:
                    return result
            return None

        # 從根節點開始搜索
        root = self.tree.topLevelItem(0)
        if root:
            found_item = find_connection_item(root)
            if found_item:
                # 確保父節點都被展開
                parent = found_item.parent()
                while parent:
                    parent.setExpanded(True)
                    parent = parent.parent()
                
                # 選中找到的項目
                self.tree.setCurrentItem(found_item)
                self.on_tree_item_clicked(found_item, 0)
                
                # 確保選中的項目可見
                self.tree.scrollToItem(found_item)

    def on_checkbox_changed(self, state):
        """當checkbox狀態改變時更新UI元件"""
        is_checked = state == Qt.Checked
        self.tree.setEnabled(is_checked)
        self.connection_label.setVisible(is_checked)
        self.selected_label.setVisible(is_checked)
        if not is_checked:
            self.selected_connection = None
            self.selected_label.setText("")

    def populate_tree_with_hierarchy(self, node_data, parent=None):
        """遞迴填充樹狀結構"""
        if not isinstance(node_data, dict):
            return

        if parent is None:
            self.tree.clear()
            root = QTreeWidgetItem(self.tree)
            root.setText(0, node_data["name"])
            if hasattr(self.parent, 'folder_icon'):
                root.setIcon(0, QIcon(self.parent.folder_icon))
            
            self.add_connections_to_node(root, node_data.get("connections", []))
            
            for child in node_data.get("children", []):
                self.populate_tree_with_hierarchy(child, root)
        else:
            child_item = QTreeWidgetItem(parent)
            child_item.setText(0, node_data["name"])
            if hasattr(self.parent, 'folder_icon'):
                child_item.setIcon(0, QIcon(self.parent.folder_icon))
            
            self.add_connections_to_node(child_item, node_data.get("connections", []))
            
            for child in node_data.get("children", []):
                self.populate_tree_with_hierarchy(child, child_item)

    def add_connections_to_node(self, node, connections):
        """為節點添加連線資訊"""
        for conn in connections:
            conn_item = QTreeWidgetItem(node)
            conn_item.setText(0, f"{conn['name']} ({conn['ip']})")
            if hasattr(self.parent, 'computer_icon'):
                conn_item.setIcon(0, self.parent.computer_icon)
            # 儲存連線資訊到item中
            conn_item.setData(0, Qt.UserRole, conn)

    def on_tree_item_clicked(self, item, column):
        """處理樹節點點擊事件"""
        conn_data = item.data(0, Qt.UserRole)
        if conn_data:
            self.selected_connection = conn_data
            self.selected_connection_id = conn_data.get('id')  # 保存選中連線的ID
            self.selected_label.setText(f"已選擇連線: {conn_data['name']} ({conn_data['ip']})")
        else:
            self.selected_connection = None
            self.selected_connection_id = None
            self.selected_label.setText("")

    def get_selected_connection_id(self):
        """獲取選擇的連線ID"""
        return self.selected_connection_id

    def validate_and_accept(self):
        """驗證輸入資料並決定是否接受"""
        # 檢查必填欄位
        if not all([
            self.name_input.text().strip(),
            self.ip_input.text().strip(),
            self.account_input.text().strip(),
            self.password_input.text().strip()
        ]):
            QMessageBox.warning(self, "警告", "請填寫所有必填欄位（標有 * 號的欄位）")
            return

        # 如果勾選了"透過主機連線"，檢查是否選擇了連線
        if self.via_host_checkbox.isChecked() and not self.selected_connection:
            QMessageBox.warning(self, "警告", "請選擇一個連線主機")
            return

        self.accept()

    def getInputs(self):
        return (
            self.name_input.text().strip(),
            self.ip_input.text().strip(),
            self.account_input.text().strip(),
            self.password_input.text().strip(),
            self.via_host_checkbox.isChecked()
        )

    def get_selected_connection(self):
        """獲取選擇的連線資訊"""
        return self.selected_connection

class ActivateVenv:

    uid=""

    def activate_venv(self, shell,ip,account,password):
        """activates venv of the active command prompt"""

        shell.SendKeys(f"ssh {account}@{ip}")
        shell.SendKeys("{ENTER}")
        time.sleep(1)
        shell.SendKeys(password)
        shell.SendKeys("{ENTER}")
        time.sleep(1)

    def open_cmd(self, shell,cmdName="Cmder Console"):
        """ opens cmd """
        self.uid = uuid.uuid4()

        # 載入設定中的執行字串
        try:
            with open("settings.json", 'r', encoding='utf-8') as f:
                settings = json.load(f)
                exec_string = settings.get("exec_string", "D:\\Tools\\cmder\\vendor\\conemu-maximus5\\ConEmu64.exe /title \"{cmdName}-{uid}\" /cmd cmd /k \"D:\\Tools\\cmder\\vendor\\init.bat\" -new_console:%d")
        except:
            exec_string = "D:\\Tools\\cmder\\vendor\\conemu-maximus5\\ConEmu64.exe /title \"{cmdName}-{uid}\" /cmd cmd /k \"D:\\Tools\\cmder\\vendor\\init.bat\" -new_console:%d"
        
        # 替換變數
        exec_string = exec_string.format(cmdName=cmdName, uid=self.uid)
        
        shell.run(exec_string)
        time.sleep(10)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("設定")
        self.setMinimumWidth(1100)
        self.setMinimumHeight(900)
        
        # 載入現有設定
        self.settings = self.load_settings()
        
        # 設置深色主題
        self.setStyleSheet("""
            QDialog {
                background-color: #353535;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit {
                background-color: #252525;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px;
            }
            QPushButton {
                background-color: #454545;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px;
                min-width: 80px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:pressed {
                background-color: #353535;
            }
            QGroupBox {
                color: #ffffff;
                border: 2px solid #555555;
                border-radius: 5px;
                margin-top: 1em;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """)

        # 創建主要布局
        main_layout = QVBoxLayout()
        
        # 創建 SSH Panel
        ssh_group = QGroupBox("SSH")
        ssh_layout = QVBoxLayout()
        
        exec_string_layout = QVBoxLayout()
        exec_string_label = QLabel("執行字串:")
        self.exec_string_input = QLineEdit(self.settings.get("exec_string", ""))
        self.exec_string_input.setPlaceholderText("輸入shell.run的執行字串")
        
        exec_string_layout.addWidget(exec_string_label)
        exec_string_layout.addWidget(self.exec_string_input)
        ssh_layout.addLayout(exec_string_layout)
        ssh_group.setLayout(ssh_layout)
        main_layout.addWidget(ssh_group)

        # 創建 MES Log Panel
        mes_group = QGroupBox("MES Log")
        mes_layout = QVBoxLayout()
        
        # MES Log HC
        mes_hc_label = QLabel("HC:")
        self.mes_hc_input = QLineEdit(self.settings.get("mes_log_hc_string", ""))
        self.mes_hc_input.setPlaceholderText("輸入MES Log HC的網址")
        
        # MES Log LT
        mes_lt_label = QLabel("LT:")
        self.mes_lt_input = QLineEdit(self.settings.get("mes_log_lt_string", ""))
        self.mes_lt_input.setPlaceholderText("輸入MES Log LT的網址")
        
        mes_layout.addWidget(mes_hc_label)
        mes_layout.addWidget(self.mes_hc_input)
        mes_layout.addWidget(mes_lt_label)
        mes_layout.addWidget(self.mes_lt_input)
        mes_group.setLayout(mes_layout)
        main_layout.addWidget(mes_group)

        # 創建 EI Log Panel
        ei_group = QGroupBox("EI Log")
        ei_layout = QVBoxLayout()
        
        # EI Log HC
        ei_hc_label = QLabel("HC:")
        self.ei_hc_input = QLineEdit(self.settings.get("ei_log_hc_string", ""))
        self.ei_hc_input.setPlaceholderText("輸入EI Log HC的網址")
        
        # EI Log LT
        ei_lt_label = QLabel("LT:")
        self.ei_lt_input = QLineEdit(self.settings.get("ei_log_lt_string", ""))
        self.ei_lt_input.setPlaceholderText("輸入EI Log LT的網址")
        
        ei_layout.addWidget(ei_hc_label)
        ei_layout.addWidget(self.ei_hc_input)
        ei_layout.addWidget(ei_lt_label)
        ei_layout.addWidget(self.ei_lt_input)
        ei_group.setLayout(ei_layout)
        main_layout.addWidget(ei_group)

        # 創建 Old Log Panel
        old_group = QGroupBox("Old Log")
        old_layout = QVBoxLayout()
        
        # Old Log HC
        old_hc_label = QLabel("HC:")
        self.old_hc_input = QLineEdit(self.settings.get("old_log_hc_string", ""))
        self.old_hc_input.setPlaceholderText("輸入Old Log HC的網址")
        
        # Old Log LT
        old_lt_label = QLabel("LT:")
        self.old_lt_input = QLineEdit(self.settings.get("old_log_lt_string", ""))
        self.old_lt_input.setPlaceholderText("輸入Old Log LT的網址")
        
        old_layout.addWidget(old_hc_label)
        old_layout.addWidget(self.old_hc_input)
        old_layout.addWidget(old_lt_label)
        old_layout.addWidget(self.old_lt_input)
        old_group.setLayout(old_layout)
        main_layout.addWidget(old_group)

        # 添加彈性空間
        main_layout.addStretch()
        
        # 按鈕區域
        button_box = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.save_settings)
        button_box.rejected.connect(self.reject)
        
        button_box.button(QDialogButtonBox.Save).setText("儲存")
        button_box.button(QDialogButtonBox.Cancel).setText("取消")
        
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

    def load_settings(self):
        try:
            with open("settings.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "exec_string": "D:\\Tools\\cmder\\vendor\\conemu-maximus5\\ConEmu64.exe /title \"{cmdName}-{uid}\" /cmd cmd /k \"D:\\Tools\\cmder\\vendor\\init.bat\" -new_console:%d",
                "mes_log_hc_string": "",
                "mes_log_lt_string": "",
                "ei_log_hc_string": "",
                "ei_log_lt_string": "",
                "old_log_hc_string": "",
                "old_log_lt_string": ""
            }
        except json.JSONDecodeError:
            return {
                "exec_string": "D:\\Tools\\cmder\\vendor\\conemu-maximus5\\ConEmu64.exe /title \"{cmdName}-{uid}\" /cmd cmd /k \"D:\\Tools\\cmder\\vendor\\init.bat\" -new_console:%d",
                "mes_log_hc_string": "",
                "mes_log_lt_string": "",
                "ei_log_hc_string": "",
                "ei_log_lt_string": "",
                "old_log_hc_string": "",
                "old_log_lt_string": ""
            }

    def save_settings(self):
        settings = {
            "exec_string": self.exec_string_input.text().strip(),
            "mes_log_hc_string": self.mes_hc_input.text().strip(),
            "mes_log_lt_string": self.mes_lt_input.text().strip(),
            "ei_log_hc_string": self.ei_hc_input.text().strip(),
            "ei_log_lt_string": self.ei_lt_input.text().strip(),
            "old_log_hc_string": self.old_hc_input.text().strip(),
            "old_log_lt_string": self.old_lt_input.text().strip()
        }
        
        # 驗證執行字串不為空
        if not settings["exec_string"]:
            QMessageBox.warning(self, "錯誤", "SSH執行字串不能為空！")
            return
            
        try:
            with open("settings.json", 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"儲存設定時發生錯誤：{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
