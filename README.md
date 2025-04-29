# QR-Code

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This is my __1st Project__ ever project. 

The motivation behind this project was for rising popularity of QR codes all over the world, in India qr codes are used day to day
in order to implement the [UPI Payment method](https://en.wikipedia.org/wiki/Unified_Payments_Interface)

<br> Then i read read [this paper] (https://www.researchgate.net/publication/318125149_An_Introduction_to_QR_Code_Technology)
about the technology and how it works on the basic building blocks of computers ie 0|1, i was also ammused by how this perfectly aligns with the black and white printing used on paper to represent these QR codes where in 1 is represnted by the black color and white is used for 0.
<br> One day in the 2nd year of college, i with my friend [Ankit] (https://github.com/basakankit) were tinkering with a QR code, using a website and seeing how the QR code maze ;) changes when we modify the text. This fascianted me into building one of my own.
<br> I found out that their was no __easily accessible way__ to read these QR codes on computers, just as there is on mobile devices using the camera app.  
    Hence i thought of building my very own desktop-app.

<br>
## QR Code Generator Application
A simple desktop application built with Python and PyQt5 for generating and reading QR codes.

###🛠️ Features

Generate QR Codes: Create QR codes.
Read QR Codes: Scan and decode existing QR codes.
Save & Export: Save generated QR codes as image files (PNG).

###📦 Prerequisites

Python 3.6 or higher

Libraries:
- PyQt5 (for GUI)
- qrcode (for QR code generation)
- opencv-python (for reading QR codes)


### ⚙️ Installation

__ 1.) Clone the repository:__
<br>
'git clone https://github.com/yourusername/your-repo.git'
cd your-repo
<br>

__2.) Create & activate a virtual environment (optional but recommended):__
'''
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\\Scripts\\activate   # Windows
'''
<br>

__3.) Install dependencies:__
'pip install -r requirements.txt'


###🚀 Usage

1.) Ensure the UI file (QRCodeGUI.ui) is in the same directory as main.py (or update the path in the code).
2.) Run the application:
'python main.py'

The main window will open—use the buttons to generate or read QR codes.


###📁 Project Structure
'''
├── main.py            # Application entry point and UI logic
├── QRCodeGUI.ui       # Qt Designer UI file
├── requirements.txt   # Python dependencies
├── LICENSE            # License file
└── README.md          # This documentation
'''

###📝 Configuration & Customization

- To change default QR settings (version, box size, border), edit the parameters in the qrcode.QRCode(...) constructor inside main.py.
- To style the GUI further, open QRCodeGUI.ui in Qt Designer and make adjustments then save.

###🤝 Contributing

Feel free to open issues or submit pull requests. For major changes, please discuss what you’d like to change via an issue first.


###📜 License

This project is licensed under the MIT License. See the LICENSE file for details

<br>
PS --> This is my 1st project and so has more of comments than code ;))
