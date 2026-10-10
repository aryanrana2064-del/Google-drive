"""Colour palettes and the application stylesheet (light and dark) - a clean, high-contrast, flat look.

Design rules: solid backgrounds (no see-through panels, so text is always easy to read), one accent colour for the
main action, bigger click targets (taller buttons, inputs and table rows), clear focus and selection states, and a
dark sidebar with a bright bar on the current page. The old ``glass_*`` entries are kept as the names of the solid
panel colours so nothing else in the app needs to change.
"""
from __future__ import annotations

import re

PALETTES: dict[str, dict[str, str]] = {
    "light": {
        "bg": "#f3f5f9", "surface": "#ffffff", "border": "#d9dfeb", "text": "#111827", "muted": "#566176",
        "primary": "#2c47cf", "primary_hover": "#243bb0", "primary_text": "#ffffff",
        "sidebar": "#14213d", "sidebar_text": "#dbe3f5", "sidebar_active": "#2b3f75", "sidebar_muted": "#9aa8c9",
        "danger": "#c62828", "success": "#17703f", "warning": "#a15c00",
        "row_alt": "#f7f9fc", "selection": "#dbe4ff", "input_bg": "#ffffff", "hover": "#eef2fb",
        "bar_udhaar": "#e0575b", "bar_jama": "#2fa36b",
        # ---- panel colours used by the style sheet (all solid)
        "bg_gradient": "#f3f5f9",
        "glass": "#ffffff", "glass_strong": "#ffffff",
        "glass_hover": "#eef2fb", "glass_input": "#ffffff",
        "glass_alt": "#f7f9fc", "glass_header": "#eef1f7",
        "glass_edge": "#d9dfeb", "glass_line": "#c9d1e0",
        "glass_selection": "#dbe4ff", "popup": "#ffffff",
        "sidebar_gradient": "#14213d",
        "nav_hover": "#1f2f55",
        "nav_active": "#2b3f75",
        "side_edge": "#14213d", "accent_bar": "#8aa0ff",
        "primary_gradient": "#2c47cf",
        "primary_gradient_hover": "#243bb0",
    },
    "dark": {
        "bg": "#0f1522", "surface": "#172033", "border": "#2b3752", "text": "#eef1f8", "muted": "#a3afc9",
        "primary": "#7b93ff", "primary_hover": "#93a7ff", "primary_text": "#0b1020",
        "sidebar": "#0a0f1d", "sidebar_text": "#c4cee6", "sidebar_active": "#1c2747", "sidebar_muted": "#8290b2",
        "danger": "#ff8585", "success": "#52d89b", "warning": "#f3bb55",
        "row_alt": "#141c2d", "selection": "#2a3e78", "input_bg": "#0f1626", "hover": "#1e2940",
        "bar_udhaar": "#ff8585", "bar_jama": "#52d89b",
        # ---- panel colours used by the style sheet (all solid)
        "bg_gradient": "#0f1522",
        "glass": "#172033", "glass_strong": "#1e2940",
        "glass_hover": "#24324f", "glass_input": "#0f1626",
        "glass_alt": "#141c2d", "glass_header": "#1c2639",
        "glass_edge": "#2b3752", "glass_line": "#38476a",
        "glass_selection": "#2a3e78", "popup": "#1c2639",
        "sidebar_gradient": "#0a0f1d",
        "nav_hover": "#141d36",
        "nav_active": "#1c2747",
        "side_edge": "#0a0f1d", "accent_bar": "#7b93ff",
        "primary_gradient": "#7b93ff",
        "primary_gradient_hover": "#93a7ff",
    },
}

_current = "light"


def current_name() -> str:
    return _current


def current() -> dict[str, str]:
    return PALETTES[_current]


def set_current(name: str) -> None:
    global _current
    _current = name if name in PALETTES else "light"


_TEMPLATE = """
* { font-size: 14px; }

/* ---- window and pages ---------------------------------------------------------------------------- */
QMainWindow, QDialog { background: @bg_gradient@; color: @text@; }
QStackedWidget { background: transparent; }
QWidget#page { background: transparent; }
QScrollArea { background: transparent; border: none; }
QScrollArea > QWidget > QWidget { background: transparent; }
QLabel { color: @text@; background: transparent; }
QLabel#h1 { font-size: 24px; font-weight: 700; }
QLabel#h2 { font-size: 16px; font-weight: 600; }
QLabel#muted, QLabel[muted="true"] { color: @muted@; }
QLabel#kpiValue { font-size: 26px; font-weight: 700; }
QLabel#kpiTitle { color: @muted@; font-size: 12px; font-weight: 700; letter-spacing: 1px; }
QLabel#kpiCaption { color: @muted@; font-size: 12px; }
QLabel[kind="danger"] { color: @danger@; font-weight: 600; }
QLabel[kind="success"] { color: @success@; font-weight: 600; }
QLabel[kind="warning"] { color: @warning@; font-weight: 600; }

/* ---- sidebar: solid dark, bright bar on the current page ----------------------------------------- */
QFrame#sidebar { background: @sidebar_gradient@; border-right: 1px solid @side_edge@; }
QLabel#brand { color: #ffffff; font-size: 18px; font-weight: 800; letter-spacing: 1px; background: transparent; }
QLabel#brandSub { color: @sidebar_muted@; font-size: 12px; background: transparent; }
QLabel#sideNote { color: @sidebar_muted@; font-size: 12px; background: transparent; }
QPushButton#nav { background: transparent; color: @sidebar_text@; border: none; border-left: 4px solid transparent;
                  border-radius: 8px; text-align: left; padding: 11px 14px; font-size: 14px; }
QPushButton#nav:hover { background: @nav_hover@; color: #ffffff; }
QPushButton#nav:checked { background: @nav_active@; color: #ffffff; font-weight: 700; border-left: 4px solid @accent_bar@; }
QPushButton#sideTool { background: @nav_hover@; color: @sidebar_text@; border: 1px solid @nav_active@;
                       border-radius: 8px; padding: 8px 10px; }
QPushButton#sideTool:hover { background: @nav_active@; color: #ffffff; }

/* ---- cards and group boxes ----------------------------------------------------------------------- */
QFrame#card { background: @glass@; border: 1px solid @glass_edge@; border-radius: 12px; }
QFrame#card QLabel { background: transparent; }
QGroupBox { background: @glass@; border: 1px solid @glass_edge@; border-radius: 12px; margin-top: 16px;
            padding: 16px 12px 10px 12px; font-weight: 600; }
QGroupBox::title { subcontrol-origin: margin; left: 14px; padding: 0 6px; color: @muted@; }

/* ---- buttons: one clear main action, quiet secondary ones ---------------------------------------- */
QPushButton { background: @glass_strong@; color: @text@; border: 1px solid @glass_line@; border-radius: 8px;
              padding: 8px 16px; min-height: 20px; }
QPushButton:hover { background: @glass_hover@; border: 1px solid @primary@; }
QPushButton:pressed { background: @glass_header@; }
QPushButton:focus { border: 2px solid @primary@; }
QPushButton:disabled { color: @muted@; background: @glass_alt@; border: 1px solid @glass_edge@; }
QPushButton#primary { background: @primary_gradient@; color: @primary_text@; border: 1px solid @primary@; font-weight: 600; }
QPushButton#primary:hover { background: @primary_gradient_hover@; border: 1px solid @primary_hover@; }
QPushButton#primary:disabled { background: @glass_alt@; color: @muted@; border: 1px solid @glass_edge@; }
QPushButton#danger { color: @danger@; border: 1px solid @danger@; }
QPushButton#danger:hover { background: @glass_hover@; }
QToolButton { background: @glass_input@; color: @text@; border: 1px solid @glass_line@; border-radius: 8px; padding: 6px 10px; }
QToolButton:hover { background: @glass_hover@; border: 1px solid @primary@; }

/* ---- inputs -------------------------------------------------------------------------------------- */
QLineEdit, QComboBox, QDateEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox {
    background: @glass_input@; color: @text@; border: 1px solid @glass_line@; border-radius: 8px; padding: 8px 10px;
    min-height: 20px; selection-background-color: @glass_selection@; selection-color: @text@; }
QLineEdit:hover, QComboBox:hover, QDateEdit:hover, QPlainTextEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover {
    border: 1px solid @muted@; }
QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border: 2px solid @primary@; padding: 7px 9px; }
QLineEdit[invalid="true"] { border: 2px solid @danger@; padding: 7px 9px; }
QLineEdit:read-only { background: @glass_alt@; }
QLineEdit:disabled, QComboBox:disabled, QDateEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled { color: @muted@; background: @glass_alt@; }
QComboBox QAbstractItemView, QCompleter QAbstractItemView { background: @popup@; color: @text@; border: 1px solid @glass_line@;
                              selection-background-color: @selection@; selection-color: @text@; outline: 0; }
QMenu { background: @popup@; color: @text@; border: 1px solid @glass_line@; border-radius: 8px; padding: 4px; }
QMenu::item { padding: 8px 20px; border-radius: 6px; }
QMenu::item:selected { background: @selection@; }
QCalendarWidget QWidget { background: @popup@; color: @text@; }

/* ---- tables: readable rows, strong selection ----------------------------------------------------- */
QTableWidget { background: @glass@; alternate-background-color: @glass_alt@; color: @text@;
               border: 1px solid @glass_edge@; border-radius: 10px; gridline-color: transparent;
               selection-background-color: @glass_selection@; selection-color: @text@; }
QTableWidget::item { padding: 4px 10px; border: none; }
QTableWidget::item:hover { background: @hover@; }
QTableWidget::item:selected { background: @glass_selection@; color: @text@; }
QHeaderView { background: transparent; }
QHeaderView::section { background: @glass_header@; color: @text@; border: none; border-bottom: 2px solid @glass_line@;
                       padding: 9px 10px; font-weight: 700; font-size: 13px; }
QTableCornerButton::section { background: @glass_header@; border: none; }

/* ---- tabs ---------------------------------------------------------------------------------------- */
QTabWidget::pane { border: 1px solid @glass_edge@; border-radius: 10px; background: @glass@; top: -1px; }
QTabBar::tab { background: transparent; color: @muted@; padding: 10px 18px; border: none; border-bottom: 3px solid transparent;
               font-weight: 600; }
QTabBar::tab:hover { color: @text@; }
QTabBar::tab:selected { color: @primary@; border-bottom: 3px solid @primary@; }

/* ---- bars, scrollbars ---------------------------------------------------------------------------- */
QProgressBar { background: @glass_line@; border: none; border-radius: 4px; height: 8px; text-align: center; color: transparent; }
QProgressBar::chunk { background: @primary_gradient@; border-radius: 4px; }
QProgressBar[state="warn"]::chunk { background: @warning@; }
QProgressBar[state="over"]::chunk { background: @danger@; }

QScrollBar:vertical { background: transparent; width: 12px; margin: 2px; }
QScrollBar::handle:vertical { background: @glass_line@; border-radius: 5px; min-height: 36px; }
QScrollBar::handle:vertical:hover { background: @muted@; }
QScrollBar::add-line, QScrollBar::sub-line { height: 0; width: 0; }
QScrollBar:horizontal { background: transparent; height: 12px; margin: 2px; }
QScrollBar::handle:horizontal { background: @glass_line@; border-radius: 5px; min-width: 36px; }
QScrollBar::handle:horizontal:hover { background: @muted@; }

QStatusBar { background: @glass@; color: @muted@; border-top: 1px solid @glass_edge@; }
QToolTip { background: @popup@; color: @text@; border: 1px solid @glass_line@; border-radius: 6px; padding: 5px; }
QMessageBox { background: @bg_gradient@; }
QCheckBox, QRadioButton { color: @text@; spacing: 8px; background: transparent; }
"""


def build_stylesheet(name: str) -> str:
    palette = PALETTES.get(name, PALETTES["light"])
    return re.sub(r"@(\w+)@", lambda m: palette[m.group(1)], _TEMPLATE)
