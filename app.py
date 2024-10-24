import streamlit as st
from google.cloud import aiplatform
import pandas as pd
from PIL import Image
import io
import json
import re
from google.oauth2 import service_account

# Initialize Streamlit page configuration
st.set_page_config(
    page_title="FMCG Product Analyzer",
    layout="wide",
    page_icon="🛍"
)

# Custom CSS for better UI
st.markdown("""
    <style>
   .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
    }
   .stButton>button:hover {
        background-color: #45a049;
    }
   .reportview-container {
        background: #fafafa;
    }
   .main {
        padding: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Load Google Cloud credentials
try:
    credentials_info = json.loads(st.secrets["GOOGLE_APPLICATION_CREDENTIALS"])
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    project_id = st.secrets["GOOGLE_CLOUD_PROJECT"]
    
    # Initialize Vertex AI
    aiplatform.init(project=project_id, location="us-central1", credentials=credentials)
    
    # Initialize the Qwen-2 2B VL model
    model_resource_name = "projects/{}/locations/us-central1/models/{}".format(project_id, "your-qwen-2-2b-vl-model-id")
    st.success("Model loaded successfully")

except Exception as e:
    st.error(f"Error loading credentials: {str(e)}")
    st.stop()

# Initialize session state for product tracking
if 'product_data' not in st.session_state:
    st.session_state.product_data = []

def analyze_image(image):
    # Assuming Qwen-2 2B VL model is a Vertex AI Image Classification/Annotation model
    # You might need to adjust this to match your model's prediction call
    client = aiplatform.PredictionClient(credentials=credentials)
    with io.BytesIO() as buffered_image:
        image.save(buffered_image, format='PNG')
        buffered_image.seek(0)
        response = client.predict(
            endpoint=model_resource_name,
            instances=[{"content": buffered_image.getvalue()}],
            parameters={}
        ).predictions
    
    # Parse response to extract relevant information
    # This part heavily depends on the model's output format, adjust accordingly
    analysis = []
    for prediction in response:
        for annotation in prediction:
            if annotation.display_name in ["Brand Name", "Date of Manufacturing", "Date of Expiry", "Quantity", "MRP", "Basic Details"]:
                analysis.append(f"{annotation.display_name}:{annotation.text}")
    
    return "\n".join(analysis)

def parse_product_details(analysis):
    details = {
        "Brand Name": "Not identified",
        "Date of Manufacturing": "Not specified",
        "Date of Expiry": "Not specified",
        "Quantity": "Not specified",
        "MRP": "Not specified",
        "Basic Details": "Not provided"
    }
    
    if analysis:
        lines = analysis.split('\n')
        for line in lines:
            if 'Brand Name:' in line:
                details["Brand Name"] = line.split(':', 1)[1].strip()
            elif 'Date of Manufacturing:' in line:
                details["Date of Manufacturing"] = line.split(':', 1)[1].strip()
            elif 'Date of Expiry:' in line:
                details["Date of Expiry"] = line.split(':', 1)[1].strip()
            elif 'Quantity:' in line:
                details["Quantity"] = line.split(':', 1)[1].strip()
            elif 'MRP:' in line:
                details["MRP"] = line.split(':', 1)[1].strip()
            elif 'Basic Details:' in line:
                details["Basic Details"] = line.split(':', 1)[1].strip()
    
    return details

def update_product_data(details):
    # Check if product already exists
    for product in st.session_state.product_data:
        if (product['Brand Name'].lower() == details['Brand Name'].lower() and
            product['Quantity'] == details['Quantity'] and
            product['MRP'] == details['MRP']):
            # Update existing entry
            product['Count'] += 1
            return
    
    # Add new entry if not found
    details['Count'] = 1
    st.session_state.product_data.append(details)

def main():
    st.title("FMCG Product Analyzer and Tracker")
    
    uploaded_file = st.file_uploader("Choose an image of an FMCG product", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        # Resize image for display
        max_width = 300
        ratio = max_width / image.width
        new_size = (max_width, int(image.height * ratio))
        resized_image = image.resize(new_size)
        
        # Display resized image
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(resized_image, caption="Uploaded Image", use_column_width=True)
        
        with col2:
            if st.button("Analyze Image"):
                with st.spinner("Analyzing image..."):
                    analysis = analyze_image(image)
                    if analysis:
                        details = parse_product_details(analysis)
                        update_product_data(details)
                    
                        st.subheader("Product Details:")
                        for key, value in details.items():
                            if key!= 'Count':
                                st.write(f"{key}:** {value}")
                    else:
                        st.error("Unable to analyze the image. Please try again with a different image.")
    
    st.subheader("Product Inventory")
    if st.session_state.product_data:
        df = pd.DataFrame(st.session_state.product_data)
        
        # Reorder columns
        columns_order = ['Brand Name', 'Date of Manufacturing', 'Date of Expiry', 'Quantity', 'MRP', 'Basic Details', 'Count']
        df = df[columns_order]
        
        # Style the dataframe
        styled_df = df.style.set_properties({'text-align': 'left'})
        styled_df = styled_df.set_table_styles([
            {'selector': 'th', 'props': [('font-weight', 'bold'), ('text-align', 'left')]},
            {'selector': 'td', 'props': [('max-width', '200px'), ('white-space', 'normal')]}
        ])
        
        st.write(styled_df.to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.write("No products scanned yet.")

if __name__ == "__main__":
    main()
