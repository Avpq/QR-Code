# QR-Code

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This is my __1st Project__ ever project. 

The motivation behind this project was for rising popularity of QR codes all over the world, in India qr codes are used day to day
in order to implement the [UPI Payment method](https://en.wikipedia.org/wiki/Unified_Payments_Interface)

Then i read read [this paper](https://www.researchgate.net/publication/318125149_An_Introduction_to_QR_Code_Technology) about the technology and how it works on the basic building blocks of computers ie 0|1, i was also ammused by how this perfevtly aligns with the black and white printing used on paper to represent these QR codes where in 1 is represnted by the black color and white is used for 0.

One day in the 2nd year of college, i with my friend [Ankit](https://github.com/basakankit) were tinkering with a QR code, using a website and seeing how the QR code maze 🤣 changes when we modify the text. This fascianted me into building one of my own.

I found out that their was no __easily accessible way__ to read these QR codes on computers, just as there is on mobile devices using the camera app.  

<br>Hence i thought of building my very own desktop-app.
<br>


# QR Code Generator Application

A simple desktop application built with Python and PyQt5 for generating and reading QR codes.

## 🛠️ Features

- **Generate QR Codes**: Create QR codes.
- **Read QR Codes**: Scan and decode existing QR codes with OpenCV.
- **Save & Export**: Save generated QR codes as image files (PNG).

## 📦 Prerequisites

- **Python** 3.6 or higher
- **Libraries**:
  - `PyQt5` (for GUI)  
  - `qrcode` (for QR code generation)  
  - `opencv-python` (for reading QR codes)

## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Avpq/QR-Code.git
   cd QR-Code
   ```

2. **Create & activate a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate   # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

1. **Ensure** the UI file (`QRCodeGUI.ui`) is in the same directory as `main.py` (or update the path in the code).
2. **Run** the application:
   ```bash
   python main.py
   ```
3. The main window will open—use the buttons to generate or read QR codes.
<div align="center">
<p align="center">
  <img src="assets/image_programme.png" width="600" height ="400" alt="Project Logo"/>
</p>
</div>

4. Text to QR
- Enter the text you wish to convert
- Click on the __text to QR button__, the QR code will be generated
- Now Go To File \< Save (alternatively on macOS use the shortcut ^S), now enter the filename and the location you wish to save the image in
<div align="center">
<img src="https://github.com/Avpq/QR-Code/blob/main/assets/text2qr.gif" width="800" height ="390"/>
</div>

5. QR to Text
- Open a PNG file, using the load option (alternatively on macOS use the shortcut ^L)
- Click on the __QR to Text Button__, and you will get the text out of the image
<div align="center">
<img src="https://github.com/Avpq/QR-Code/blob/main/assets/qr2text%20(1).gif" width="800" height ="390"/>
<br>
<img src="https://github.com/Avpq/QR-Code/blob/main/assets/qr2text%20(2).gif" width="800" height ="390"/>
</div>

## 📁 Project Structure

```text
├── assests            # Contains the sample images used during demonstration
├── LICENSE            # License file
├── QRCodeGUI.ui       # Qt Designer UI file
├── README.md          # This documentation
├── main.py            # Application entry point and UI logic
└── requirements.txt   # Python dependencies
``` 

## 📝 Configuration & Customization

- To change default QR settings edit the parameters in the `qrcode.QRCode(...)` constructor inside `main.py`.
- To style the GUI further, open `QRCodeGUI.ui` in Qt Designer and make adjustments then save.

## 🤝 Contributing

Feel free to open issues or submit pull requests. For major changes, please discuss what you’d like to change via an issue first or send me an [e-mail](mailto:avisahai96@gmail.com?subject=Contribute&body=Write%20how%20you%20will%20contribute%20here)


## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


<br>
PS --> This is my 1st project and so has more of comments than code ;))
