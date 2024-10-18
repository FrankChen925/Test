import sys,json,time,os,uuid
from win32com import client
from  win32gui import GetWindowText, GetForegroundWindow, SetForegroundWindow, EnumWindows
from win32process import GetWindowThreadProcessId

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem, QPushButton,
    QHBoxLayout, QHeaderView, QAbstractItemView, QLineEdit, QDialog, QLabel, QDialogButtonBox, QSplitter,
    QTreeWidget, QTreeWidgetItem, QMessageBox, QInputDialog,QStyle,QCheckBox
)
from PyQt5.QtCore import Qt, QSize
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

        # 設置視窗最大化
        self.showMaximized()

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

        # 從檔案中載入資料
        self.load_data()
        #self.populate_tree()

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
        
        shell = client.Dispatch("WScript.Shell")
        run_venv = ActivateVenv()
        run_venv.open_cmd(shell)
        run_venv.activate_venv(shell,ip,account,password)

    def add_tree_node(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            new_name, ok = QInputDialog.getText(self, "新增節點", "請輸入新節點名稱：")
            if ok and new_name.strip():
                if self.check_duplicate_node(new_name):
                    QMessageBox.warning(self, "錯誤", "節點名稱已存在，請輸入其他名稱！")
                    return
                new_node = QTreeWidgetItem()
                new_node.setText(0, new_name)
                new_node.setIcon(0, QIcon(self.folder_icon))
                selected_item.addChild(new_node)
                self.tree.expandItem(selected_item)
                # 將新節點加入資料並儲存
                self.data[new_name] = []
                self.save_data()

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
            self.save_data()
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
                if self.check_duplicate_node(new_name):
                    QMessageBox.warning(self, "錯誤", "節點名稱已存在，請輸入其他名稱！")
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
        self.populate_table(item.text(0))
        self.set_column_widths([0.282, 0.2, 0.2,0.2,0.1])  # 依百分比設定每列的寬度 (30%, 50%, 20%)

    def populate_tree_with_hierarchy(self, node_data, parent=None):
        if not self.is_valid_node(node_data):
            return

        if parent is None:
            self.tree.clear()
            root = QTreeWidgetItem(self.tree)
            root.setText(0, node_data["name"])
            root.setIcon(0, QIcon(self.folder_icon))
            
            for child in node_data.get("children", []):
                self.populate_tree_with_hierarchy(child, root)
        else:
            child_item = QTreeWidgetItem(parent)
            child_item.setText(0, node_data["name"])
            child_item.setIcon(0, QIcon(self.folder_icon))
            for child in node_data.get("children", []):
                self.populate_tree_with_hierarchy(child, child_item)

        if parent is None:
            self.tree.expandAll()
                
    def populate_table(self, node_name):
        self.table.setRowCount(0)
        selected_node_data = self.find_node_data(self.data, node_name)
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
                connect_button.clicked.connect(lambda: self.connect_to_server(row_position))
                self.table.setCellWidget(row_position, 5, connect_button)
                
                # 設置via_host信息
                via_host_info = {
                    "enabled": connection.get("via_host", False),
                    "connection_id": connection.get("via_host_id")
                }
                self.table.setItem(row_position, 6, QTableWidgetItem(json.dumps(via_host_info)))

    def find_node_data(self, node_data, node_name):
        # 遞迴地在 JSON 資料結構中找到對應名稱的節點資料
        if node_data["name"] == node_name:
            return node_data
        for child in node_data.get("children", []):
            result = self.find_node_data(child, node_name)
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
            "name": "/",
            "connections": [],
            "children": []
        }

    def is_valid_node(self, node):
        """檢查節點資料結構是否包含必要欄位"""
        return isinstance(node, dict) and "name" in node and "connections" in node and "children" in node

    def save_data(self):
        root = self.tree.topLevelItem(0)  # 取得根節點
        if root:
            self.data = self.traverse_tree_and_save_with_hierarchy(root)  # 遍歷整個樹並儲存所有節點的資料

        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            QMessageBox.warning(self, "錯誤", f"保存數據時發生錯誤：{str(e)}")

    def traverse_tree_and_save_with_hierarchy(self, node):
        node_name = node.text(0)
        node_data = {
            "name": node_name,
            "connections": [],
            "children": []
        }

        existing_node_data = self.find_node_data(self.data, node_name)
        if existing_node_data:
            node_data["connections"] = existing_node_data.get("connections", [])

        if node == self.tree.currentItem():
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
            node_data["children"].append(self.traverse_tree_and_save_with_hierarchy(child_node))

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
        shell.SendKeys("ll")
        shell.SendKeys("{ENTER}")

    def open_cmd(self, shell):
        """ opens cmd """
        self.uid = uuid.uuid4()

        shell.run(f"D:\\Tools\\cmder\\vendor\\conemu-maximus5\\ConEmu64.exe /title TestCMD-{self.uid} /cmd cmd /k \"D:\\Tools\\cmder\\vendor\\init.bat\" -new_console:%d")
        time.sleep(6)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
