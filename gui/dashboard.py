# gui/dashboard.py
import sys
import pandas as pd
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem,
                             QPushButton, QLineEdit, QLabel,
                             QMessageBox, QFileDialog, QHeaderView,
                             QGroupBox, QFormLayout, QSpinBox)
from PyQt5.QtCore import Qt
from db import (get_prompts_for_user, insert_prompt, update_prompt,
                delete_prompt, get_prompt_by_id)
from gui.prompt_dialog import PromptDialog
from gui.prompt_detail import PromptDetail

class Dashboard(QWidget):
    def __init__(self, user_row):
        super().__init__()
        self.user_row = user_row
        self.setWindowTitle(f"Prompt Repository - {self.user_row['username']}")
        self.resize(900, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search by text, LLM or use...")
        self.search_edit.textChanged.connect(self.refresh_table)
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_edit)
        self.layout.addLayout(search_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Prompt Text", "LLM Used", "Performance",
            "Intended Use", "Updated At"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.layout.addWidget(self.table)

        # Buttons
        btn_layout = QHBoxLayout()
        self.create_btn = QPushButton("Create")
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")
        self.view_btn = QPushButton("View")
        self.export_btn = QPushButton("Export CSV")
        btn_layout.addWidget(self.create_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.view_btn)
        btn_layout.addWidget(self.export_btn)
        self.layout.addLayout(btn_layout)

        # Statistics
        self.stats_group = QGroupBox("Statistics")
        stats_layout = QFormLayout()
        self.total_prompts_lbl = QLabel("0")
        self.avg_score_lbl = QLabel("N/A")
        stats_layout.addRow("Total Prompts:", self.total_prompts_lbl)
        stats_layout.addRow("Avg Performance Score:", self.avg_score_lbl)
        self.stats_group.setLayout(stats_layout)
        self.layout.addWidget(self.stats_group)

        # Connections
        self.create_btn.clicked.connect(self.create_prompt)
        self.edit_btn.clicked.connect(self.edit_prompt)
        self.delete_btn.clicked.connect(self.delete_prompt)
        self.view_btn.clicked.connect(self.view_prompt)
        self.export_btn.clicked.connect(self.export_csv)

        self.refresh_table()

    def refresh_table(self):
        filter_text = self.search_edit.text()
        prompts = get_prompts_for_user(self.user_row['id'], filter_text)
        self.table.setRowCount(len(prompts))
        for row_idx, row in enumerate(prompts):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row['id'])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row['prompt_text'][:50] + '...'))
            self.table.setItem(row_idx, 2, QTableWidgetItem(row['llm_used'] or ""))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(row['performance_score']) if row['performance_score'] is not None else ""))
            self.table.setItem(row_idx, 4, QTableWidgetItem(row['intended_use'] or ""))
            self.table.setItem(row_idx, 5, QTableWidgetItem(row['updated_at']))
        self.update_stats(prompts)

    def update_stats(self, prompts):
        total = len(prompts)
        scores = [p['performance_score'] for p in prompts if p['performance_score'] is not None]
        avg = sum(scores)/len(scores) if scores else None
        self.total_prompts_lbl.setText(str(total))
        self.avg_score_lbl.setText(f"{avg:.2f}" if avg is not None else "N/A")

    def get_selected_prompt_id(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "No selection", "Please select a prompt first.")
            return None
        prompt_id_item = self.table.item(selected, 0)
        return int(prompt_id_item.text())

    def create_prompt(self):
        dialog = PromptDialog(parent=self, user_id=self.user_row['id'])
        if dialog.exec_():
            data = dialog.get_prompt_data()
            insert_prompt(self.user_row['id'], data)
            self.refresh_table()

    def edit_prompt(self):
        prompt_id = self.get_selected_prompt_id()
        if prompt_id is None:
            return
        prompt_row = get_prompt_by_id(prompt_id)
        dialog = PromptDialog(parent=self, user_id=self.user_row['id'], prompt=prompt_row)
        if dialog.exec_():
            data = dialog.get_prompt_data()
            update_prompt(prompt_id, data)
            self.refresh_table()

    def delete_prompt(self):
        prompt_id = self.get_selected_prompt_id()
        if prompt_id is None:
            return
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this prompt?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            delete_prompt(prompt_id)
            self.refresh_table()

    def view_prompt(self):
        prompt_id = self.get_selected_prompt_id()
        if prompt_id is None:
            return
        prompt_row = get_prompt_by_id(prompt_id)
        detail = PromptDetail(prompt_row)
        detail.exec_()

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export CSV", "", "CSV Files (*.csv)")
        if not path:
            return
        prompts = get_prompts_for_user(self.user_row['id'])
        df = pd.DataFrame(prompts)
        df.to_csv(path, index=False)
        QMessageBox.information(self, "Exported", f"Prompts exported to {path}")
