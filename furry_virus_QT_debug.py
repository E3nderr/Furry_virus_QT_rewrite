import sys
import os
import base64
import random
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer, QRegExp, QThread
from PyQt5.QtGui import QPixmap, QFont, QRegExpValidator, QKeyEvent
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QWidget, QSpacerItem, QSizePolicy, QDialog
from resource_images import image_base64_data  # Import the generated base64 data
from multiprocessing import Process
from screeninfo import get_monitors
os.system('cls')
inst_file = "inst_file.txt"

def base64_to_pixmap(base64_str):
    # Convert the base64 string back to a QPixmap.
    image_data = base64.b64decode(base64_str)
    pixmap = QPixmap()
    pixmap.loadFromData(image_data)
    return pixmap

# Detects multiple monitors
def get_monitor_geometry(index=1):
    monitors = get_monitors()
    if len(monitors) > index:
        monitor = monitors[index]
        return monitor.x, monitor.y, monitor.width, monitor.height
    else:
        return 0, 0, 800, 600  # Default values if no second monitor
    
def create_funny_window_process(phrase):
            app = QApplication(sys.argv)  # Start a new QApplication for each process
            window = QMainWindow()         # Instantiate the window here
            
            # Set window title and size
            window.setWindowTitle(phrase)
            window.resize(200, 100)

            # Get available monitors using screeninfo
            monitors = get_monitors()

            def print_monitor_layout():
                monitors = get_monitors()
                for i, monitor in enumerate(monitors):
                    print(f"Monitor {i + 1}: x={monitor.x}, y={monitor.y}, width={monitor.width}, height={monitor.height}, primary={monitor.is_primary}")


                if monitors:
                    # Randomly select a monitor
                    monitor = random.choice(monitors)
                    monitor_x = monitor.x
                    monitor_y = monitor.y
                    screen_width = monitor.width
                    screen_height = monitor.height

                    # Set a random position within the selected monitor's dimensions
                    random_x = random.randint(0, screen_width - 200) + monitor_x
                    random_y = random.randint(0, screen_height - 100) + monitor_y

                    # Ensure the window stays within the monitor's bounds
                    window.setGeometry(random_x, random_y, 200, 100)
                else:
                    window.setGeometry(100, 100, 200, 100)  # Default placement if no monitors are detected

            # Print monitor layout for debugging 
            print_monitor_layout()

            # Set the label and display the window
            funny_label = QLabel(phrase)
            funny_label.setFont(QFont("Arial", 50))
            funny_label.setStyleSheet("color: #ff33ff;")
            funny_label.setAlignment(Qt.AlignCenter)

            central_widget = QWidget()
            layout = QVBoxLayout(central_widget)
            layout.addWidget(funny_label)
            window.setCentralWidget(central_widget)

            window.show()
            sys.exit(app.exec_())
    
def create_funny_windows(max_windows=15):
    phrases = ["uwu", "owo", "nya~", "meow", "TwT"]
    for i in range(max_windows):
        # Schedule the creation of each funny window with a delay
        QTimer.singleShot(i * 100, lambda phrase=random.choice(phrases): 
                           Process(target=create_funny_window_process, args=(phrase,)).start())

    
def inst_update(inst_file="inst_file.txt"):
    try:
        # Open the instance file and read the current count.
        with open(inst_file, 'r') as file:
            content = file.read().strip()
            # Handle cases where the content is not an integer.
            inst = int(content) if content.isdigit() else 0
    except (FileNotFoundError, ValueError):
        # Default to 0 if the file is not found or has invalid content.
        inst = 0

    # Increment the instance count.
    inst += 1

    # Write the updated instance count back to the file.
    with open(inst_file, 'w') as file:
        file.write(str(inst))

    return inst

# Function to reset the count file 
def reset_instance_count(inst_file="inst_file.txt"):
    
    try:
        with open(inst_file, 'w') as file:
            file.write("0")
        print(f"Instance count reset to 0.")
    except Exception as e:
        print(f"Error resetting instance count: {e}")

# Handles the count inside the inst file
def update_file(inst_file="inst_file.txt"):
    
    try:
        # Open the instance file and read the current count
        with open(inst_file, 'r') as file:
            content = file.read().strip()
            # Ensure content is a valid integer
            inst = int(content) if content.isdigit() else 0
    except (FileNotFoundError, ValueError):
        # Default to 0 if file not found or invalid content
        inst = 0

    # Increment the count
    inst += 1

    # Write the updated count back to the file
    with open(inst_file, 'w') as file:
        file.write(str(inst))

    print(f"Updated instance count: {inst}")  # Debugging output
    return inst

         
inst = inst_update()  # Update the instance count at the start of the program
print(f"Instances attempted: {inst}")

if inst >= 4:
    
    create_funny_windows(max_windows=5)  # Call the original function
    reset_instance_count(inst_file)  # Reset count to 0 if >= 4
else:
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Totally Not Malware")
            self.setFixedSize(1060, 500)
            self.center_window()
            
            
            # Main layout
            main_widget = QWidget()
            main_layout = QHBoxLayout(main_widget)
            self.setCentralWidget(main_widget)

            class CustomLineEdit(QLineEdit):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.setFont(QFont("Arial", 20))  # Set font size
                    self.setStyleSheet("border: 2px solid gray;")  # Default border color

                def focusInEvent(self, event):
                    self.setStyleSheet("border: 2px solid blue;")  # Change border color to blue on focus
                    super().focusInEvent(event)

                def focusOutEvent(self, event):
                    self.setStyleSheet("border: 2px solid gray;")  # Revert border color to gray when focus is lost
                    super().focusOutEvent(event)

            class ExpiryDateLineEdit(CustomLineEdit):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.setMaxLength(10)  # MM/DD/YYYY format has 10 characters
                    # Only allow numbers and slashes
                    reg_exp = QRegExp(r'[0-9/]*')  # Regex to allow only digits and slashes
                    validator = QRegExpValidator(reg_exp)
                    self.setValidator(validator)

                    # Set placeholder text for empty field with gray color
                    self.setPlaceholderText("MM/DD/YYYY")
                    self.setStyleSheet("color: gray; border: 2px solid gray;")  # Placeholder text in gray color

                def keyPressEvent(self, event: QKeyEvent):
                    current_text = self.text()
                    key = event.text()

                    # Only process numeric keys
                    if key.isdigit():
                        # Check if a slash needs to be added after every second keypress
                        new_text = current_text + key

                        if len(new_text) == 2 or len(new_text) == 5:
                            new_text = new_text + '/'  # Append slash after 2nd and 5th digits

                        self.setText(new_text)
                        self.setCursorPosition(len(self.text()))  # Move cursor after the added slash
                        return  # Prevent the default handling

                    # Call the default keyPressEvent if not a digit
                    super().keyPressEvent(event)


            class SecurityCodeLineEdit(CustomLineEdit):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    # restrict input to digits
                    reg_exp = QRegExp(r'\d*')  # Regex to allow only digits
                    validator = QRegExpValidator(reg_exp)
                    self.setValidator(validator)

            # Form layout for input fields
            form_layout = QVBoxLayout()

            greeting_label = QLabel("H-hi there...\nDo you th-think I could have your\ncredit card information, p-please?")
            greeting_label.setFont(QFont("Arial", 23))
            greeting_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            form_layout.addWidget(greeting_label)

            form = QFormLayout()
            font = QFont("Arial", 20)  # Create a QFont object with Arial and size 20

            # Create and set font for input fields
            self.card_number_input = CustomLineEdit()
            self.card_number_input.setFixedWidth(300)  # Set the physical width (in pixels)

            self.expiry_date_input = ExpiryDateLineEdit()  # Custom input for expiry date
            self.expiry_date_input.setFixedWidth(300)  # Set a smaller width for expiry date

            self.security_code_input = SecurityCodeLineEdit()  # Custom input for security code
            self.security_code_input.setFixedWidth(300)  # Set a smaller width for security code
            self.security_code_input.setEchoMode(QLineEdit.Password)

            # Create and set font and center alignment for labels
            card_number_label = QLabel("Card number:")
            card_number_label.setFont(font)
            card_number_label.setAlignment(Qt.AlignCenter)  # Center-align text

            expiry_date_label = QLabel("Expiry date:")
            expiry_date_label.setFont(font)
            expiry_date_label.setAlignment(Qt.AlignCenter)  # Center-align text

            
            security_code_label = QLabel("Security code:")
            security_code_label.setFont(font)
            security_code_label.setAlignment(Qt.AlignCenter)  # Center-align text
            

            # Add fields to the form layout
            form.addRow(card_number_label, self.card_number_input)
            form.addRow(expiry_date_label, self.expiry_date_input)
            form.addRow(security_code_label, self.security_code_input)

            # Add the form layout directly to the main layout (no canvas needed here)
            form_layout.addLayout(form)

            # Assuming `self` is your QWidget or QMainWindow, set this layout as the main layout
            self.setLayout(form_layout)

            # Button to submit
            submit_button = QPushButton("Th-thanks")
            submit_button.setFixedSize(200, 100)
            submit_button.clicked.connect(self.thanks_clicked)

            # Set the font to Arial with size 20
            submit_button.setFont(QFont("Arial", 20))

            submit_button.setStyleSheet("margin-top: 20px;")  # Optional, for spacing if needed

            # Center the button
            form_layout.addWidget(submit_button, alignment=Qt.AlignHCenter)

            
            # Display image
            image_label = QLabel(self)
            pixmap = base64_to_pixmap(image_base64_data["goober.jpg"])
            image_label.setPixmap(pixmap.scaled(420, 500))
            image_label.setStyleSheet("border: 2px solid #d93b38;")
            main_layout.addWidget(image_label)
            main_layout.addLayout(form_layout)
            
        # Connect the aboutToQuit signal to the update function
            QApplication.instance().aboutToQuit.connect(lambda: update_file())
            
        def handle_about_to_quit(self):
            # Now call the external update_file function
            update_file(self)

        def center_window(self):
            screen = QDesktopWidget().availableGeometry().center()
            qt_rectangle = self.frameGeometry()
            qt_rectangle.moveCenter(screen)
            self.move(qt_rectangle.topLeft())

        def thanks_clicked(self):
            if self.card_number_input.text() and self.expiry_date_input.text() and self.security_code_input.text():
                self.close()
                self.thank_you_window = ThankYouWindow()

    class ThankYouWindow(QDialog):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Thankuuu!!!")
            self.setFixedSize(550, 400)
            self.center_window()

            layout = QVBoxLayout()

            # Create a pink label with the text
            label = QLabel("Th-Thankuu~ uwu")
            label.setFont(QFont("Arial", 38))  # Adjusted font size for better fit
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: #ff33ff;")  # Set the text color to pink
            layout.addWidget(label)

            # Display the image
            pixmap = base64_to_pixmap(image_base64_data["goober2.jpg"])
            image_label = QLabel(self)
            image_label.setPixmap(pixmap.scaled(540, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Adjusted image size
            layout.addWidget(image_label)

            self.setLayout(layout)
            self.show()

            # Schedule the opening of the BTW window
            QTimer.singleShot(2000, self.open_btw_window)

        def center_window(self):
            # Centers the window on the screen."""
            qt_rectangle = self.frameGeometry()
            center_point = QDesktopWidget().availableGeometry().center()
            qt_rectangle.moveCenter(center_point)
            self.move(qt_rectangle.topLeft())

        def open_btw_window(self):
            # Opens the BTW window."""
            self.close()  # Close this window before opening the next
            btw_window = BTWWindow()
            btw_window.exec_()  # Display the new window

    class BTWWindow(QDialog):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Oh, btw...")
            self.setFixedSize(550, 600)
            self.center_window()

            layout = QVBoxLayout()
            label = QLabel("Oh, b-btw...\nYour computer\nhas virus owo")
            label.setFont(QFont("Arial", 45))
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: #ff33ff;")  # Set the text color to pink
            layout.addWidget(label)

            pixmap = base64_to_pixmap(image_base64_data["goober3.jpg"])
            image_label = QLabel(self)
            image_label.setPixmap(pixmap.scaled(540, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            layout.addWidget(image_label)

            self.setLayout(layout)
            self.show()
            QTimer.singleShot(500, self.create_funny_windows)

        def center_window(self):
            screen = QDesktopWidget().availableGeometry().center()
            qt_rectangle = self.frameGeometry()
            qt_rectangle.moveCenter(screen)
            self.move(qt_rectangle.topLeft())

        def create_funny_windows(self):
            create_funny_windows(0)
            
        

    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())


