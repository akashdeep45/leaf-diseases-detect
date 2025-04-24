import streamlit as st
import cv2 as cv
import numpy as np
import keras
from PIL import Image
import tensorflow as tf
import io
import traceback

# Define label names at the top
label_name = ['Apple scab','Apple Black rot', 'Apple Cedar apple rust', 'Apple healthy', 'Cherry Powdery mildew',
'Cherry healthy','Corn Cercospora leaf spot Gray leaf spot', 'Corn Common rust', 'Corn Northern Leaf Blight','Corn healthy', 
'Grape Black rot', 'Grape Esca', 'Grape Leaf blight', 'Grape healthy','Peach Bacterial spot','Peach healthy', 'Pepper bell Bacterial spot', 
'Pepper bell healthy', 'Potato Early blight', 'Potato Late blight', 'Potato healthy', 'Strawberry Leaf scorch', 'Strawberry healthy',
'Tomato Bacterial spot', 'Tomato Early blight', 'Tomato Late blight', 'Tomato Leaf Mold', 'Tomato Septoria leaf spot',
'Tomato Spider mites', 'Tomato Target Spot', 'Tomato Yellow Leaf Curl Virus', 'Tomato mosaic virus', 'Tomato healthy']

# Set page configuration
st.set_page_config(
    page_title="Plant Disease Detection 🌿",
    page_icon="🍃",
    layout="wide"
)

# Custom CSS with improved visibility
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #2e7d32;
        color: white;
        border: none;
        padding: 0.5rem;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
    }
    .title-container {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #1b5e20, #2e7d32);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .prevention-card {
        background-color: white;
        padding: 1.2rem;
        border-radius: 8px;
        margin: 0.8rem 0;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .prevention-card strong {
        color: #1b5e20;
        font-size: 1.1rem;
        display: block;
        margin-bottom: 0.5rem;
    }
    .prevention-card-text {
        color: #333333;
        font-size: 0.95rem;
        line-height: 1.4;
    }
    .upload-section {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        border: 2px dashed #2e7d32;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .prevention-title {
        color: #1b5e20;
        font-weight: bold;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to detect if image is a plant/leaf
def is_plant_image(img, threshold=0.3):
    """
    Analyze image to determine if it likely contains a plant or leaf.
    Uses color and texture features to make this determination.
    
    Args:
        img: The OpenCV image
        threshold: Green ratio threshold (0-1)
        
    Returns:
        boolean: True if the image likely contains a plant, False otherwise
    """
    try:
        # 1. Check color distribution (plants are typically green)
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        
        # Define range for green color in HSV
        lower_green = np.array([25, 40, 40])
        upper_green = np.array([95, 255, 255])
        
        # Create mask for green areas
        green_mask = cv.inRange(hsv, lower_green, upper_green)
        green_ratio = np.sum(green_mask > 0) / (img.shape[0] * img.shape[1])
        
        # 2. Check texture features (edges characteristic of leaves)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        blurred = cv.GaussianBlur(gray, (5, 5), 0)
        edges = cv.Canny(blurred, 50, 150)
        edge_ratio = np.sum(edges > 0) / (img.shape[0] * img.shape[1])
        
        # Combine features for decision
        if green_ratio > threshold or (green_ratio > 0.15 and edge_ratio > 0.05):
            return True
        return False
    except Exception as e:
        st.error(f"Error in plant detection: {str(e)}")
        return True  # Default to True on error to allow further processing

# Title Section
st.markdown("""
    <div class="title-container">
        <h1 style='color: white;'>🍃 Plant Disease Detection 🍃</h1>
        <p style='color: #e8f5e9;'>AI-Powered Plant Disease Detection System</p>
    </div>
""", unsafe_allow_html=True)

# Create three columns for layout
col1, col2, col3 = st.columns([1, 1.5, 1])

# Column 1: Why Detect Plant Diseases?
with col1:
    st.markdown("### Why Detect Plant Diseases?")
    st.markdown("""
    Early detection of plant diseases is crucial for:
    
    * 🌱 **Preventing crop losses**
    * 💊 **Optimizing treatment effectiveness**
    * 🌿 **Reducing pesticide use**
    * 🌾 **Ensuring food security**
    * 🍃 **Protecting plant health**
    * 💰 **Maximizing crop yield**
    * 🌍 **Supporting sustainable farming**
    """)

# Column 2: Upload and Analysis Section
with col2:
    st.markdown("### Upload Plant Image")
    
    # Create upload section with custom styling
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    
    # Add supported formats information
    st.markdown("""
    ℹ️ **Supported Plants:**
    - Apple, Cherry, Corn, Grape
    - Peach, Pepper, Potato
    - Strawberry, Tomato
    
    📸 **Supported formats:** JPG, JPEG, PNG
    """)
    
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
    
    # Camera input option
    camera_input = st.camera_input("Or take a picture")
    
    input_image = uploaded_file if uploaded_file is not None else camera_input
    
    if input_image is not None:
        try:
            # Try to handle the file with PIL first to better handle various image formats
            pil_image = Image.open(input_image)
            
            # Convert PIL image to bytes for OpenCV
            img_byte_arr = io.BytesIO()
            pil_image.save(img_byte_arr, format=pil_image.format if pil_image.format else 'JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Now process with OpenCV
            img = cv.imdecode(np.frombuffer(img_byte_arr, dtype=np.uint8), cv.IMREAD_COLOR)
            
            if img is None:
                st.error("⚠️ OpenCV couldn't decode the image. Please try another format like JPG or PNG.")
            else:
                # Display the uploaded image - without use_container_width parameter
                st.image(img_byte_arr, caption="Uploaded Image")
                
                # First check if it's a plant image
                is_plant = is_plant_image(img)
                
                # Add analyze button with custom styling
                if st.button("🔍 Analyze Plant"):
                    with st.spinner("Analyzing image..."):
                        # First check if the image appears to be a plant/leaf
                        if not is_plant:
                            st.error("❌ This doesn't appear to be a plant or leaf image. Please upload an image of a plant leaf.")
                            st.info("For accurate results, please upload a clear image of a plant leaf against a simple background.")
                        else:
                            try:
                                # Image preprocessing
                                normalized_image = np.expand_dims(
                                    cv.resize(cv.cvtColor(img, cv.COLOR_BGR2RGB), (150, 150)), 
                                    axis=0
                                )
                                
                                # Load model and make prediction
                                model = keras.models.load_model('Training/model/Leaf Deases(96,88).h5')
                                predictions = model.predict(normalized_image)
                                confidence = predictions[0][np.argmax(predictions)] * 100
                                
                                # Extra validation: If all class probabilities are similar, it might not be a valid leaf
                                prediction_std = np.std(predictions[0])
                                if prediction_std < 0.02:  # If standard deviation is low, predictions are uncertain
                                    st.error("❌ This doesn't appear to be one of the supported plant types.")
                                    st.info("Please upload an image of a leaf from one of the supported plant types listed above.")
                                else:
                                    # Display results with proper formatting
                                    st.markdown("### Analysis Results")
                                    if confidence >= 80:
                                        result = label_name[np.argmax(predictions)]
                                        st.success(f"**Detected Disease:** {result}")
                                        st.info(f"**Confidence:** {confidence:.2f}%")
                                        
                                        # Add treatment recommendations based on detected disease
                                        st.markdown("### Treatment Recommendations")
                                        st.markdown("""
                                        Based on the detected condition, here are some recommendations:
                                        1. Isolate affected plants
                                        2. Remove infected leaves
                                        3. Apply appropriate treatment
                                        4. Monitor plant recovery
                                        """)
                                    else:
                                        st.warning(f"⚠️ Confidence too low ({confidence:.2f}%). Please ensure the image is clear and well-lit.")
                            except Exception as e:
                                st.error(f"⚠️ Analysis failed: {str(e)}")
                                st.info("Please make sure the image is clear and contains a leaf from one of the supported plants.")
        except Exception as e:
            st.error(f"⚠️ Failed to process the image: {str(e)}")
            st.info("Troubleshooting tips: Try a JPG or PNG format, ensure the image isn't corrupted, and keep the image size under 5MB.")
            
            # For development - show the full error trace
            with st.expander("Technical error details"):
                st.code(traceback.format_exc())
    
    st.markdown('</div>', unsafe_allow_html=True)

# Column 3: Prevention Tips
with col3:
    st.markdown('<p class="prevention-title">### Prevention Tips</p>', unsafe_allow_html=True)
    
    prevention_tips = [
        ("🔍 Regular Monitoring", "Check plants weekly for signs of disease"),
        ("💧 Proper Watering", "Avoid overwatering and water at base"),
        ("🌪️ Good Air Circulation", "Space plants properly"),
        ("🧹 Clean Garden Tools", "Sanitize tools between uses"),
        ("🌱 Healthy Soil", "Maintain proper soil pH and nutrients"),
        ("🛡️ Disease-Resistant Varieties", "Choose resistant plant varieties"),
        ("📏 Proper Plant Spacing", "Allow adequate space between plants"),
        ("🌡️ Climate Control", "Maintain appropriate temperature and humidity")
    ]
    
    for title, description in prevention_tips:
        st.markdown(f"""
        <div class="prevention-card">
            <strong>{title}</strong>
            <div class="prevention-card-text">{description}</div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; padding: 2rem 0; color: #333333;'>
    <p>Developed with ❤️ for Sustainable Agriculture</p>
</div>
""", unsafe_allow_html=True)
