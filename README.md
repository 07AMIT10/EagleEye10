# EagleEye10

# FMCG Product Analyzer and Tracker

A web-based OCR solution that analyzes FMCG product images to extract and track essential product information using the advanced Qwen-2 2B VL vision model.

## Features

- Automated extraction of product information from packaging images
- Real-time analysis of product details (brand name, manufacturing date, expiry date, quantity, MRP)
- Intelligent inventory tracking system with duplicate detection
- Streamlined data extraction pipeline
- Clean and responsive user interface

## Technologies Used

- Frontend: Streamlit, HTML
- Backend: Python, Regex
- Cloud Infrastructure: Google Cloud Platform (GCP), Vertex AI
- Vision Model: Qwen-2 2B VL
- Image Processing: Pillow (PIL)
- Data Management: Pandas
- Version Control: Git, GitHub

## Installation & Setup

1. Clone this repository
```bash
git clone https://github.com/yourusername/fmcg-product-analyzer.git
cd fmcg-product-analyzer
```

2. Create a virtual environment and activate it
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure GCP Credentials
- Create a service account in Google Cloud Console
- Download the JSON key file
- Set up environment variables:
  ```bash
  export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
  export GOOGLE_CLOUD_PROJECT="your-project-id"
  ```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open the provided URL in your web browser
3. Upload an FMCG product image
4. Click "Analyze Image" to process
5. View extracted information and inventory tracking

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
