.💸 Wallet Raider (지갑털이범) 
🛒"The ultimate shopping companion designed to raid the best deals for your wallet."Wallet Raider is a high-performance price comparison web application built with Streamlit. By leveraging the Naver Shopping API, it provides real-time price tracking, advanced data visualization, and a premium user experience inspired by professional shopping portals.✨ Key Features🔍 Real-time Lowest Price Search: Fetch accurate product data and filter results instantly using the Naver Shopping API.📊 Data-Driven Insights: Automatic generation of price distribution histograms, average price metrics, and "lowest vs. highest" comparisons.⚖️ Smart Compare Pool: Add multiple products to a comparison list to analyze specs and price differences via interactive bar charts.❤️ Wishlist & Quick Filters: Save your favorite items in-session and navigate through trending categories (Laptops, Smartphones, GPUs) with a single click.🎨 Premium UI/UX: A clean, "Danawa PRO" inspired layout with responsive product cards and intuitive navigation.🛠 Tech StackCategoryTechnologyFrontend / FrameworkStreamlitData AnalysisPandas, NumPyVisualizationPlotly ExpressAPI / NetworkingRequests, Naver Search APILanguagePython 3.9+🚀 Getting Started1. PrerequisitesYou need a Client ID and Client Secret from the Naver Developers Center.2. InstallationBash# Clone the repository
git clone https://github.com/your-username/wallet-raider.git
cd wallet-raider

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
3. Environment Setup (Secrets)Create a .streamlit/secrets.toml file in your project root and add your API keys:Ini, TOMLNAVER_CLIENT_ID = "YOUR_CLIENT_ID"
NAVER_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
📸 Preview1️⃣ Advanced Search & ResultsVisualizes product images, mall information, and manufacturers in a clean, professional grid.2️⃣ Price Distribution ReportA Plotly-powered histogram shows where the current price sits compared to the market average, helping you decide if it's the right time to buy.📂 Project StructurePlaintext.
├── .streamlit/
│   └── secrets.toml      # API Key management (Keep this private!)
├── app.py                # Main application logic
├── requirements.txt      # List of Python dependencies
└── README.md             # Documentation
🤝 ContributingContributions, issues, and feature requests are welcome! Feel free to check the Issues tab.
