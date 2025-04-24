# 🌿 Plant Disease Detection System

An AI-powered web application that detects plant diseases from leaf images using deep learning. The system can identify 33 different types of plant diseases across various crops.

## 🌟 Features

- Real-time plant disease detection
- Support for 33 different plant diseases
- Camera and file upload options
- Detailed treatment recommendations
- Prevention tips and best practices
- User-friendly interface
- High accuracy predictions (96.88%)

## 🛠️ Technologies Used

### Programming Languages
- Python 3.8+

### Core Libraries
- **Streamlit**: Web application framework
- **TensorFlow/Keras**: Deep learning framework
- **OpenCV**: Image processing
- **NumPy**: Numerical computations
- **PIL**: Image handling

### Machine Learning
- **Model Type**: Convolutional Neural Network (CNN)
- **Architecture**: Transfer Learning based
- **Accuracy**: 96.88%
- **Input Size**: 150x150 pixels
- **Output Classes**: 33 different plant diseases

### Supported Plants
- Apple
- Cherry
- Corn
- Grape
- Peach
- Pepper
- Potato
- Strawberry
- Tomato

## 📋 Prerequisites

1. Python 3.8 or higher
2. pip (Python package installer)
3. Git (optional, for cloning the repository)

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/leaf-diseases-detect.git
cd leaf-diseases-detect
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Install required packages:
```bash
pip install -r requirements.txt
```

## 💻 Running the Application

### Method 1: Using the Batch File (Windows)
1. Double-click `run_app.bat`
2. Wait for the application to start
3. Open your browser and go to http://localhost:8501

### Method 2: Using Command Line
1. Open terminal/command prompt
2. Navigate to project directory
3. Run:
```bash
streamlit run main.py
```
4. Open your browser and go to http://localhost:8501

## 📸 Using the Application

1. **Upload Image**:
   - Click "Choose an image" to upload a leaf image
   - Or use the camera option to take a picture

2. **Analysis**:
   - Click "Analyze Plant" button
   - Wait for the analysis to complete
   - View the results and recommendations

3. **Results**:
   - Disease name (if detected)
   - Confidence score
   - Treatment recommendations
   - Prevention tips

## 📚 Project Structure

```
leaf-diseases-detect/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── run_app.bat         # Windows batch file
├── README.md           # Project documentation
├── Training/
│   ├── model/         # Trained model files
│   └── Leaf_Deases.ipynb  # Training notebook
└── Media/             # Media files
```

## 🧠 Model Details

- **Architecture**: CNN with transfer learning
- **Training Data**: 33 different plant diseases
- **Input Processing**: 
  - Resize to 150x150
  - RGB conversion
  - Normalization
- **Output**: Disease classification with confidence score
- **Confidence Threshold**: 80%

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Dataset providers
- Open-source community
- Contributors and maintainers

## 📧 Contact

For any queries or support, please open an issue in the repository.
