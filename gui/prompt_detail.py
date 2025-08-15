# gui/prompt_detail.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class PromptDetail(QDialog):
    def __init__(self, prompt_row):
        super().__init__()
        self.setWindowTitle(f"Prompt Detail - ID {prompt_row['id']}")
        self.resize(600, 700)
        layout = QVBoxLayout()

        fields = [
            ("Prompt Text", prompt_row['prompt_text']),
            ("Intended Use", prompt_row['intended_use']),
            ("LLM Used", prompt_row['llm_used']),
            ("Performance Score", str(prompt_row['performance_score']) if prompt_row['performance_score'] is not None else "Not set"),
            ("Outcome", prompt_row['outcome']),
            ("Notes", prompt_row['notes']),
            ("Created At", prompt_row['created_at']),
            ("Updated At", prompt_row['updated_at'])
        ]

        for label_text, value in fields:
            lbl = QLabel(f"<b>{label_text}:</b>")
            txt = QTextEdit()
            txt.setReadOnly(True)
            txt.setPlainText(value if value else "")
            layout.addWidget(lbl)
            layout.addWidget(txt)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)
