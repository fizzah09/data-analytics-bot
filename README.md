# DataBot: AI-Driven Data Analyst

An interactive data analysis application built with Streamlit and LangChain that helps users analyze and visualize data through natural language conversations.

## Project Structure

```
data-analytics-bot/
├── app.py            # Main application
├── utils.py          # Helper functions
├── requirements.txt  # Dependencies
├── .gitignore       # Git ignore file
└── README.md        # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd data-analytics-bot-1
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables in the `.env` file.

## Usage

1. Start the web server:
   ```
   python server.py
   ```

2. Access the bot through your web browser at `http://localhost:8000`.

## Features

- **Dark Mode Interface**: Clean, modern dark theme for comfortable viewing
- **Data Analysis**:
  - CSV file upload and processing
  - Basic statistical analysis
  - Pattern recognition
  - Data type detection
  
- **Interactive Visualizations**:
  - Bar charts
  - Scatter plots
  - Line graphs
  - Histograms
  - Box plots
  - Heat maps
  - Pair plots
  
- **AI-Powered Chat**:
  - Natural language queries
  - Data insights generation
  - Pattern analysis
  - Statistical summaries

## Importance in the Market

The Data Analytics Bot leverages the power of LangChain and Python packages such as Pandas, Matplotlib, and Seaborn to provide robust data analysis capabilities. In today's data-driven world, the ability to quickly and efficiently analyze data is crucial for businesses and researchers alike. This bot simplifies the process, making it accessible to users with varying levels of technical expertise.

## Minimum Viable Product (MVP)

The MVP of the Data Analytics Bot includes the following functionalities:
- Upload and process CSV files.
- Perform basic statistical analysis.
- Generate visualizations such as bar plots, scatter plots, and histograms.
- Interactive chat interface for querying data.

## Dev Challenge Reference

This project was developed as part of the [GitHub Dev Challenge](https://dev.to/challenges/github). The challenge prompts inspired the creation of a tool that not only showcases technical skills but also addresses real-world data analysis needs. By participating in this challenge, we aimed to demonstrate the practical applications of LangChain and Python in building a user-friendly data analytics solution.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.