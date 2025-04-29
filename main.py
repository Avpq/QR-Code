#from idlelib.colorizer import prog_group_name_to_tag

import  sys
import cv2
import qrcode

from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui


'''
This defines a new class called MyGUI.
It inherits from QMainWindow, which is a PyQt5 class that provides a main application window with menus, toolbars, and other UI elements.
'''
class MyGUI(QMainWindow): # we imported using the 'PyQt5.QtWidgets'

    def __init__(self): # constructor for MyGUI class
        super(MyGUI, self).__init__() #	Calls the constructor of the parent class (QMainWindow).

        '''
        uic.loadUI() is a function from PyQt5’s UI Compiler (uic) module.
		It loads a .ui file (created using Qt Designer) and applies it to the current PyQt5 application.
		2nd parameter, self ensures that the UI elements from "QRCodeGUI.ui" are loaded into the current instance (self).
	•	Without self, the UI won’t be connected to the main window.
        '''
        uic.loadUi("QRCodeGUI.ui", self)
        # self.show() displays the main window after loading the UI, without this line, the window would be created but not shown.
        self.show()

        '''
        Initializing current_file to an empty string indicates that no file has been loaded or selected at the GUI’s creation. This attribute stores the path or name of a file, such as one containing 
        QR code data or related to the QR code functionality. Setting up current_file during initialization allows other parts of the program to access or update it without checking its existence. 
        Later, when a user opens or saves a file, this variable can be updated to reflect the current file.
        '''
        self.current_file = ""

        # now we use the individual keywords to refer to individual UI elements
        # These lines are part of the initialization in the MyGUI class and use PyQt’s signals and slots mechanism to link UI events to the corresponding methods (or “slots”) in the code.
        self.actionLoad_2.triggered.connect(self.load_image)
        self.actionSave.triggered.connect(self.save_image)
        self.actionQUIT.triggered.connect(self.quit_program)
        self.pushButton_qr2text.clicked.connect(self.read_code)
        self.pushButton_text2qr.clicked.connect(self.generate_code)


    def load_image(self):
        '''
        The function (QFileDialog.getOpenFileName) opens a file selection dialog—a pop-up window that allows the user to navigate the file system and choose a file.
        This sets the current instance of the MyGUI class as the parent of the dialog. Having a parent means the dialog will be centered over or tied to the main window
        '''
        options = QFileDialog.Options()         # Creates an instance of options that can be passed to the file dialog. This lets you customize the dialog’s behavior if needed.

        '''
        Load File is the title of this dialog window, it tells the user, the purpose of the dialog  
        "" (empty string): -- This represents the initial directory. An empty string means the dialog will default to a standard location (often the last accessed directory or a system default).
		"All Files (*)": -- This is a file filter that tells the dialog which types of files to display. Here, "All Files (*)" means that the dialog should show every file, regardless of type.
		
		When you write options=options in the function call, you are telling Python: -- “For the options parameter of getOpenFileName, use the value stored in our local variable (at the beginning of this method) options.”
        
        The function returns a tuple with 2 elements. When the dialog is used, it not only returns the file path selected by the user (which gets stored in filename), 
        but it also returns the filter that was active at the time of selection. In this case, since you’ve specified "All Files (*)", that value would be returned as the second element of the tuple.

        Since the second value (the active filter) is not needed later in your program, it’s assigned to _, a common Python convention to indicate that this value is intentionally being ignored.
        '''
        filename, _ = QFileDialog.getOpenFileName(self, "Loada File", "", "All Files (*)", options=options)

        if filename != "":
            self.current_file = filename
            pixmap = QtGui.QPixmap(self.current_file)
            pixmap = pixmap.scaled(350, 350)
            self.label.setScaledContents(True)
            self.label.setPixmap(pixmap)


    def read_code(self):
        image = cv2.imread(self.current_file) # It uses OpenCV’s imread function to load an image from the file path stored in self.current_file.
        detector = cv2.QRCodeDetector() # It creates an instance of OpenCV’s QRCodeDetector class, this detector is a tool provided by OpenCV that can identify and decode QR codes from image data.
        '''
        data: Contains the decoded text (if a QR code is successfully detected and decoded).
		The two underscores (_) are placeholders for additional return values, such as the bounding box or other details that are not needed in this context, so they’re intentionally ignored.
        '''
        data, _, _ = detector.detectAndDecode(image)
        self.textEdit.setText(data) # It sets the decoded text (data) as the content of a text edit widget in the GUI.


    def generate_code(self):
        ''''
        Version:  The version determines the dimensions of the QR code rang is [1, 40].
        Error Correction: Adjusting it will change how much damage the QR code can tolerate versus how much data it can hold.
		Box Size: Changing it affects the pixel dimensions of each module, impacting the overall size and potentially the clarity of the QR code.
		Border: Modifying it changes the whitespace around the QR code, which can influence the ease of scanning.
        '''
        qr = qrcode.QRCode(version = 4, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size = 20, border = 2)

        qr.add_data(self.textEdit.toPlainText()) # self.textEdit.toPlainText() extracts the plain text from a text-edit widget and adds that text to the QR code object, which will be encoded into the QR code.

        qr.make(fit=True) # This tells the QR code generator to automatically choose the smallest possible version that can fit the provided data if the data size exceeds what the initially specified version CAN hold.

        image = qr.make_image(fill_color="black", back_color="white") # The make_image() method converts the generated QR code data into an image object.
        image.save("res.png")
        '''
        QtGui.QPixmap("res.png") loads the saved image file into a QPixmap object, which is used in PyQt for handling images.
        pixmap.scaled(350, 350) resizes the image to 350x350 pixels so it fits appropriately within the GUI.
        self.label.setPixmap(pixmap) sets the pixmap on a label widget in the GUI. This updates the interface so that the generated QR code is visible to the user.
        '''
        pixmap = QtGui.QPixmap("res.png")
        pixmap = pixmap.scaled(350, 350)
        self.label.setPixmap(pixmap)


    def save_image(self):
        options = QFileDialog.Options() # read in the load_image() function
        '''
        self: Sets the parent of the dialog to your main window (MyGUI instance). This ensures that the dialog is centered on your main window.
		"Save File": The title of the dialog window, which informs the user about the action.
		"": An empty string for the initial directory, meaning the dialog will default to a standard location.
		"PNG (*.png)": A filter that restricts the file types shown in the dialog. In this case, it shows only files with a .png extension.
		options=options: see the load_function()
        '''
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "PNG (*.png)", options = options)

        if filename != "":
            image = self.label.pixmap() # This line retrieves the current image (a QPixmap) displayed in the label widget (self.label) of your GUI.
            image.save(filename, "PNG")


    def quit_program(self):
        sys.exit(0)



def main(): # main() function, the entry-point of a GUI based program in Python
    '''
    app is a reference to the object of the QApplication class
    QApplication class is part of the PyQt5 framework, specifically within the PyQt5.QtWidgets module. The QApplication class is crucial for any PyQt-based GUI application
    [] mimics command-line arguments, since this application desent need any command-line arguments, the list is empty
    '''
    app = QApplication([])
    window = MyGUI() #This line creates an instance of the MyGUI class.
    app.exec_() # starts and keeps the application running
    '''
    exec is a reserved keyword in Python (used for dynamically executing code).
	To avoid a naming conflict with the Python keyword, PyQt uses exec_().
    '''

'''
These lines ensure that the main() function is called only when the script is executed directly, not when it is imported as a module into another script.
This condition checks if the module’s name is "__main__", which is true if the script is run directly, if the condition is met, the main() function is called, which starts the PyQt application.
'''
if __name__ == "__main__":
    main()
