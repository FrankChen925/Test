import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem, QPushButton,
    QHBoxLayout, QHeaderView, QAbstractItemView, QLineEdit, QDialog, QLabel, QDialogButtonBox, QSplitter,
    QTreeWidget, QTreeWidgetItem, QMessageBox, QInputDialog
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

DATA_FILE = "ssh_data.json"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python UI with Tabs and Tree")
        self.setGeometry(100, 100, 1000, 600)
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
        self.tab_widget.addTab(ssh_tab, "SSH")

        # 在 SSH 頁籤中加入分隔器佈局
        self.create_ssh_tab(ssh_tab)

        # 從檔案中載入資料
        self.load_data()
        #self.populate_tree()

    def create_ssh_tab(self, ssh_tab):
        # 創建分隔器
        splitter = QSplitter()

        # 創建左側 Tree
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("連線群組")
        self.tree.setColumnCount(1)
        self.tree.setIconSize(QSize(16, 16))
        self.tree.itemClicked.connect(self.on_tree_node_clicked)

        # 右側表格
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["名稱", "IP", "帳號", "密碼", "啟動"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
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

        main_layout = QVBoxLayout(ssh_tab)
        main_layout.addWidget(splitter)

    def add_row(self):
        if not self.tree.currentItem():
            QMessageBox.warning(self, "警告", "請選擇一個節點進行新增連線！")
            return

        dialog = EntryDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            name, ip, account, password = dialog.getInputs()
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(name))
            self.table.setItem(row_position, 1, QTableWidgetItem(ip))
            self.table.setItem(row_position, 2, QTableWidgetItem(account))
            self.table.setItem(row_position, 3, QTableWidgetItem(password))
            connect_button = QPushButton("連線")
            connect_button.clicked.connect(lambda: self.connect_to_server(row_position))
            self.table.setCellWidget(row_position, 4, connect_button)
            self.save_data()

    def remove_row(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.table.removeRow(selected_row)
            self.save_data()

    def edit_row(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            current_name = self.table.item(selected_row, 0).text()
            current_ip = self.table.item(selected_row, 1).text()
            current_account = self.table.item(selected_row, 2).text()
            current_password = self.table.item(selected_row, 3).text()
            dialog = EntryDialog(self, current_name, current_ip, current_account, current_password)
            if dialog.exec_() == QDialog.Accepted:
                name, ip, account, password = dialog.getInputs()
                self.table.setItem(selected_row, 0, QTableWidgetItem(name))
                self.table.setItem(selected_row, 1, QTableWidgetItem(ip))
                self.table.setItem(selected_row, 2, QTableWidgetItem(account))
                self.table.setItem(selected_row, 3, QTableWidgetItem(password))
                self.save_data()

    def connect_to_server(self, row):
        name = self.table.item(row, 0).text()
        ip = self.table.item(row, 1).text()
        account = self.table.item(row, 2).text()
        password = self.table.item(row, 3).text()
        print(f"連線至伺服器：名稱={name}, IP={ip}, 帳號={account}, 密碼={password}")

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
                new_node.setIcon(0, QIcon.fromTheme("folder"))
                selected_item.addChild(new_node)
                self.tree.expandItem(selected_item)
                # 將新節點加入資料並儲存
                self.data[new_name] = []
                self.save_data()

    def remove_tree_node(self):
        selected_item = self.tree.currentItem()
        if selected_item and selected_item.parent():
            node_name = selected_item.text(0)
            del self.data[node_name]  # 刪除資料
            parent = selected_item.parent()
            parent.removeChild(selected_item)
            self.save_data()
        else:
            QMessageBox.warning(self, "警告", "無法刪除根節點或未選擇節點！")

    def edit_tree_node(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            new_name, ok = QInputDialog.getText(self, "修改節點名稱", "請輸入新名稱：", QLineEdit.Normal, selected_item.text(0))
            if ok and new_name.strip():
                if new_name.strip() == "":
                    QMessageBox.warning(self, "錯誤", "節點名稱不可為空白！")
                    return
                if self.check_duplicate_node(new_name):
                    QMessageBox.warning(self, "錯誤", "節點名稱已存在，請輸入其他名稱！")
                    return
                old_name = selected_item.text(0)
                self.data[new_name] = self.data.pop(old_name)  # 更新資料字典中的名稱
                selected_item.setText(0, new_name)
                self.save_data()

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

    def populate_tree_with_hierarchy(self, node_data, parent=None):
        if not self.is_valid_node(node_data):
            return

        if parent is None:
            self.tree.clear()
            root = QTreeWidgetItem(self.tree)
            root.setText(0, node_data["name"])
            root.setIcon(0, QIcon.fromTheme("folder"))
            for child in node_data.get("children", []):
                self.populate_tree_with_hierarchy(child, root)
        else:
            child_item = QTreeWidgetItem(parent)
            child_item.setText(0, node_data["name"])
            child_item.setIcon(0, QIcon.fromTheme("folder"))
            for child in node_data.get("children", []):
                self.populate_tree_with_hierarchy(child, child_item)

        if parent is None:
            self.tree.expandAll()
                
    def populate_table(self, node_name):
        self.table.setRowCount(0)
        # 根據選中的節點名稱來尋找對應的節點資料
        selected_node_data = self.find_node_data(self.data, node_name)
        if selected_node_data:
            for connection in selected_node_data.get("connections", []):
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(connection["name"]))
                self.table.setItem(row_position, 1, QTableWidgetItem(connection["ip"]))
                self.table.setItem(row_position, 2, QTableWidgetItem(connection["account"]))
                self.table.setItem(row_position, 3, QTableWidgetItem(connection["password"]))
                connect_button = QPushButton("連線")
                connect_button.clicked.connect(lambda: self.connect_to_server(row_position))
                self.table.setCellWidget(row_position, 4, connect_button)
    
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
            "name": "Root",
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

        # 將所有資料寫回 JSON 檔案
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def traverse_tree_and_save_with_hierarchy(self, node):
        # 將節點儲存為階層結構，包含名稱、連線資訊、及其子節點
        node_name = node.text(0)
        node_data = {
            "name": node_name,
            "connections": [],  # 初始化連線資訊清單
            "children": []      # 初始化子節點清單
        }

        # 從現有資料中獲取連線資訊
        existing_node_data = self.find_node_data(self.data, node_name)
        if existing_node_data:
            node_data["connections"] = existing_node_data.get("connections", [])

        # 如果這個節點是當前選取的節點，用當前表格中的資料更新連線資訊
        if node == self.tree.currentItem():
            node_data["connections"] = []
            for row in range(self.table.rowCount()):
                connection = {
                    "name": self.table.item(row, 0).text(),
                    "ip": self.table.item(row, 1).text(),
                    "account": self.table.item(row, 2).text(),
                    "password": self.table.item(row, 3).text()
                }
                node_data["connections"].append(connection)

        # 遍歷所有子節點，並將結果加入到 "children" 清單中
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
        root.setText(0, "Root")
        root.setIcon(0, QIcon.fromTheme("folder"))
        for nodeItem in self.data["children"]:
            node_name=nodeItem['name']
            
            if node_name != "Root":
                node = QTreeWidgetItem(root)
                node.setText(0, node_name)
                node.setIcon(0, QIcon.fromTheme("folder"))
        self.tree.expandAll()


class EntryDialog(QDialog):
    def __init__(self, parent=None, name="", ip="", account="", password=""):
        super().__init__(parent)
        self.setWindowTitle("輸入資料")
        layout = QVBoxLayout()

        layout.addWidget(QLabel("名稱:"))
        self.name_input = QLineEdit(name)
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("IP:"))
        self.ip_input = QLineEdit(ip)
        layout.addWidget(self.ip_input)

        layout.addWidget(QLabel("帳號:"))
        self.account_input = QLineEdit(account)
        layout.addWidget(self.account_input)

        layout.addWidget(QLabel("密碼:"))
        self.password_input = QLineEdit(password)
        layout.addWidget(self.password_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def getInputs(self):
        return self.name_input.text(), self.ip_input.text(), self.account_input.text(), self.password_input.text()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
