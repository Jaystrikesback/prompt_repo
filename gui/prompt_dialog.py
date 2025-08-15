# gui/prompt_dialog.py
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit,
                             QTextEdit, QSpinBox, QDialogButtonBox, QLabel)
from PyQt5.QtCore import Qt

class PromptDialog(QDialog):
    def __init__(self, parent=None, user_id=None, prompt=None):
        super().__init__(parent)
        self.user_id = user_id
        self.prompt = prompt
        self.setWindowTitle("Create Prompt" if prompt is None else "Edit Prompt")
        self.resize(500, 600)

        layout = QVBoxLayout()
        form = QFormLayout()

        self.prompt_text_edit = QTextEdit()
        self.intended_use_edit = QLineEdit()
        self.llm_used_edit = QLineEdit()
        self.performance_spin = QSpinBox()
        self.performance_spin.setRange(0, 10)
        self.performance_spin.setSpecialValueText("Not set")
        self.performance_spin.setValue(-1)
        self.outcome_edit = QTextEdit()
        self.notes_edit = QTextEdit()

        form.addRow("Prompt Text:", self.prompt_text_edit)
        form.addRow("Intended Use:", self.intended_use_edit)
        form.addRow("LLM Used:", self.llm_used_edit)
        form.addRow("Performance Score (0‑10):", self.performance_spin)
        form.addRow("Outcome:", self.outcome_edit)
        form.addRow("Notes:", self.notes_edit)

        layout.addLayout(form)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

        if self.prompt:
            self.load_prompt()

    def load_prompt(self):
        self.prompt_text_edit.setPlainText(self.prompt['prompt_text'])
        self.intended_use_edit.setText(self.prompt['intended_use'])# if 'intended_use' in self.prompt else "")
        self.llm_used_edit.setText(self.prompt['llm_used'])# if 'llm_used' in self.prompt else '') #.get('llm_used') or "")
        ps = self.prompt['performance_score']# if 'performance_score' in self.prompt else None #.get('performance_score')
        if ps is not None:
            self.performance_spin.setValue(ps)
        else:
            self.performance_spin.setSpecialValueText("Not set")
        self.outcome_edit.setPlainText(self.prompt['outcome'])# if 'outcome' in self.prompt else '') #.get('outcome') or "")
        self.notes_edit.setPlainText(self.prompt['notes'])# if 'notes' in self.prompt else '') #.get('notes') or "")

    def get_prompt_data(self):
        data = {
            'prompt_text': self.prompt_text_edit.toPlainText(),
            'intended_use': self.intended_use_edit.text(),
            'llm_used': self.llm_used_edit.text(),
            'performance_score': self.performance_spin.value() if self.performance_spin.value() != -1 else None,
            'outcome': self.outcome_edit.toPlainText(),
            'notes': self.notes_edit.toPlainText()
        }
        return data
