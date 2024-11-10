import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon

class WebGenieWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Main window setup
        self.setWindowTitle('Web Genie - Web Automation Assistant')
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""
        QMainWindow {
            background-color: #fce4ec;
        }
        QTextEdit {
            border: 1px solid #cccccc;
            border-radius: 8px;
            padding: 8px;
            font-size: 14px;
            background-color: #fce4ec;
            color: #333333;
        }
        QPushButton {
            border: none;
            border-radius: 4px;
            padding: 8px;
            font-size: 14px;
        }
        QLabel {
            color: #333333;
        }
    """)
        # Create main central widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top bar with logo and title
        top_bar = QWidget()
        top_bar.setStyleSheet("background-color: #eee8aa; border-bottom: 1px solid #e57373;")
        top_bar.setFixedHeight(120)  # Increase height to fit larger logo
        top_layout = QHBoxLayout(top_bar)

        # Add title and logo
        title_label = QLabel("Web Genie")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333333;")

        logo_label = QLabel()
        logo_pixmap = QPixmap("WebGenieLogo.png")  # Path to the logo
        scaled_pixmap = logo_pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setMinimumSize(100, 100)  # Ensure enough space for the logo
        logo_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Add widgets to layout
        top_layout.addWidget(title_label)
        top_layout.addStretch()
        top_layout.addWidget(logo_label)
        top_layout.setContentsMargins(40, 20, 40, 20)

       
        # Chat area
        chat_scroll = QScrollArea()
        chat_scroll.setWidgetResizable(True)
        chat_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color:  #ffffe0;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #2d2d3d;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #444444;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(chat_widget)
        chat_scroll.setWidget(chat_widget)

        # Welcome message
        welcome_widget = QFrame()
        welcome_widget.setStyleSheet("""
            QFrame {
                background-color: #2d2d3d;
                border-radius: 8px;
                padding: 20px;
                margin: 20px;
            }
            QLabel {
                color: #ffffff;
            }
        """)
        welcome_layout = QVBoxLayout(welcome_widget)
        welcome_title = QLabel("Welcome to Web Genie! 🧞")
        welcome_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        welcome_desc = QLabel(
            "I can help you automate web tasks. Try asking me to:\n"
            "• Fill out forms on websites\n"
            "• Extract data from web pages\n"
            "• Navigate through different pages\n"
            "• Search and collect information\n\n"
            "Just describe what you want to do in natural language!"
        )
        welcome_desc.setStyleSheet("font-size: 14px;")
        welcome_layout.addWidget(welcome_title)
        welcome_layout.addWidget(welcome_desc)
        self.chat_layout.addWidget(welcome_widget)
        self.chat_layout.addStretch()
        
        # Bottom bar with prompt input
        bottom_bar = QWidget()
        bottom_bar.setStyleSheet("background-color: #FFDD00; padding: 5px;")
        bottom_layout = QVBoxLayout(bottom_bar)
        
        # Prompt input area
        prompt_container = QWidget()
        prompt_layout = QHBoxLayout(prompt_container)
        prompt_layout.setContentsMargins(0, 0, 0, 0)
        
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Describe the web task you want to automate...")
        self.prompt_input.setFixedHeight(50)
        self.prompt_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #444444;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                background-color: #1e1e2e;
                color: #ffffff;
            }
        """)
        
        send_button = QPushButton("Run")
        send_button.setFixedSize(QSize(80, 50))
        send_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6a35a0;
            }
        """)
        send_button.clicked.connect(self.send_message)
        
        prompt_layout.addWidget(self.prompt_input)
        prompt_layout.addWidget(send_button)
        
        bottom_layout.addWidget(prompt_container)
        
        # Add status bar for showing automation progress
        status_bar = QWidget()
        status_layout = QHBoxLayout(status_bar)
        self.status_label = QLabel("Ready to automate")
        self.status_label.setStyleSheet("color: #1C1C1C; font-size: 24px;")
        status_layout.addWidget(self.status_label)
        bottom_layout.addWidget(status_bar)
        
        # Add all main sections to the main layout
        main_layout.addWidget(top_bar)
        main_layout.addWidget(chat_scroll)
        main_layout.addWidget(bottom_bar)

    def send_message(self):
        message = self.prompt_input.toPlainText().strip()
        if message:
            # User message
            message_widget = QFrame()
            message_widget.setStyleSheet("""
                QFrame {
                    background-color: #7f3fbf;
                    border-radius: 8px;
                    padding: 10px;
                    margin: 10px;
                }
            """)
            message_layout = QVBoxLayout(message_widget)
            message_label = QLabel(message)
            message_label.setStyleSheet("color: #ffffff;")
            message_label.setWordWrap(True)
            message_layout.addWidget(message_label)
            
            self.chat_layout.addWidget(message_widget)
            self.prompt_input.clear()
            
            # System response
            response_widget = QFrame()
            response_widget.setStyleSheet("""
                QFrame {
                    background-color: #008080;
                    border: 1px solid #444444;
                    border-radius: 8px;
                    padding: 10px;
                    margin: 10px;
                }
            """)

            response_layout = QVBoxLayout(response_widget)
            response_label = QLabel("Starting web automation task...")
            response_label.setStyleSheet("color: #ffffff;")
            response_label.setWordWrap(True)
            response_layout.addWidget(response_label)
            
            self.chat_layout.addWidget(response_widget)
            self.chat_layout.addStretch()
            
            # Update status
            self.status_label.setText("Executing web automation task...")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.send_message()

def main():
    app = QApplication(sys.argv)
    window = WebGenieWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()