import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from utils import readData, getAgent

def analyze_data_types(df):
    num_numeric = df.select_dtypes(include=['int64', 'float64']).shape[1]
    num_categorical = df.select_dtypes(include=['object', 'category']).shape[1]
    return num_numeric, num_categorical

st.set_page_config(
    page_title="DataBot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for code display only
if 'show_code' not in st.session_state:
    st.session_state.show_code = False

# Single sidebar control for code display
with st.sidebar:
    st.markdown("<h1 style='color: white;'>Settings</h1>", unsafe_allow_html=True)
    show_code = st.checkbox('Show Python Code', 
                          value=st.session_state.show_code,
                          key='code_toggle_single')

# Set dark mode directly
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    .stSidebar {
        background-color: #000000;
        color: #FFFFFF;
    }
    header[data-testid="stHeader"] {
        background-color: #000000;
    }
    .stButton button {
        background-color: #4A4A4A;
        color: #FFFFFF;
        border: 1px solid #404040;
    }
    .dataframe {
        background-color: #000000; /* Black background for tables */
        color: #FFFFFF;
        border: 1px solid #404040;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, 
    .stMarkdown h5, .stMarkdown h6 {
        color: #FFFFFF;
    }
    .stTextInput input, .stSelectbox select {
        background-color: #333333;
        color: #FFFFFF;
        border: 1px solid #404040;
    }
    .stFileUploader {
        background-color: #000000; /* Black background for drag-and-drop */
        color: #FFFFFF;
        border: 1px solid #808080; /* Grey border */
    }
    .stCheckbox > div:first-child {
        color: #FFFFFF;
    }
    .stChatMessage {
        background-color: #808080; /* Grey background for text responses */
        color: #FFFFFF;
        border-radius: 8px;
        padding: 8px 12px;
    }
    .stChatMessage-user {
        background-color: #808080; /* Grey background for user responses */
        color: #FFFFFF;
        align-self: flex-end;
    }
    .stChatMessage-assistant {
        background-color: #808080; /* Grey background for assistant responses */
        color: #FFFFFF;
        align-self: flex-start;
    }
    .stChatInput {
        background-color: #808080; /* Grey background for chat input */
        color: #FFFFFF;
        border: 1px solid #404040;
    }
    .stSlider > div > div > div {
        background-color: #4A4A4A;
    }
    .element-container {
        background-color: #000000 !important; /* Black background for plots */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Single main title
st.markdown("<h1 style='color: white;'>DataBot: Your AI-Driven Data Analyst 😊</h1>", unsafe_allow_html=True)

# Function to update code display
def update_code_display(code_snippet, section_key):
    if show_code:
        st.sidebar.code(code_snippet, language="python", key=f'code_section_{section_key}')

# Theme and Code Display Configuration
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
    st.session_state.show_code = False
    st.session_state.current_code = ""

# Define tabs first
# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    try:
        df = readData(uploaded_file)
        num_numeric, num_categorical = analyze_data_types(df)
        
        # Sidebar stats
        st.sidebar.markdown("<h1 style='color: white;'>Data Overview 📊</h1>", unsafe_allow_html=True)
        st.sidebar.write(f"Total columns: {df.shape[1]}")
        st.sidebar.write(f"Total rows: {df.shape[0]}")
        st.sidebar.write(f"Numeric columns: {num_numeric}")
        st.sidebar.write(f"Categorical columns: {num_categorical}")

        if num_numeric <= 1:
            st.warning("This dataset is mostly descriptive. Limited statistical analysis available.")
            st.write("Data Preview:")
            st.dataframe(df.head())
            st.write("Data Types:")
            st.write(df.dtypes)
        else:
            # Define tabs after file upload
            tabs = st.tabs(["Analysis", "Visualization", "Chat"])
            
            with tabs[0]:
                st.header("Data Analysis")
                st.dataframe(df.head())
                if num_numeric > 0:
                    st.write("Statistical Summary:")
                    st.write(df.describe())
                
            # Visualization section with multiple column selection
            with tabs[1]:
                st.header("Data Visualization")
                if num_numeric > 1:
                    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        plot_type = st.selectbox("Select Plot Type", ["Bar", "Scatter", "Histogram", "Box", "Line"])
                        selected_columns = st.multiselect("Select Columns to Visualize", numeric_cols, default=numeric_cols[0])
                    
                    with col2:
                        fig_width = st.slider("Plot width", 4, 12, 6)
                        fig_height = st.slider("Plot height", 3, 8, 4)
                        if plot_type == "Bar":
                            n_bars = st.slider("Number of bars", 5, 50, 20)
                        
                    if st.button("Generate Plot", key='gen_plot'):
                        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
                        
                        if plot_type == "Bar":
                            data_subset = df[selected_columns].head(n_bars)
                            data_subset.plot(kind='bar', ax=ax)
                        elif plot_type == "Scatter":
                            if len(selected_columns) >= 2:
                                sns.scatterplot(data=df, x=selected_columns[0], y=selected_columns[1], ax=ax)
                        elif plot_type == "Box":
                            df[selected_columns].boxplot(ax=ax)
                        elif plot_type == "Line":
                            df[selected_columns].plot(ax=ax)
                        elif plot_type == "Histogram":
                            df[selected_columns].hist(ax=ax)
                        
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        st.pyplot(fig)
                else:
                    st.info("Not enough numerical columns for visualization")
                    
            # Chat Interface
            def format_response(response):
                if isinstance(response, pd.DataFrame):
                    return response.to_html()
                elif isinstance(response, str):
                    if 'Action Input:' in response:
                        output_start = response.find('Action Input:') + len('Action Input:')
                        return response[output_start:].strip()
                    return response
                return str(response)

            with tabs[2]:
                st.header("Chat with your Data")
                
                if "messages" not in st.session_state:
                    st.session_state.messages = []

                # Display chat history
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        if message["role"] == "assistant" and st.session_state.show_code:
                            st.code(message["content"], language="python")
                        else:
                            st.markdown(f"<span style='background-color: #808080; color: white;'>{message['content']}</span>", unsafe_allow_html=True)

                # Chat input and response
                if prompt := st.chat_input("Ask about your data"):
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(f"<span style='background-color: #808080; color: white;'>{prompt}</span>", unsafe_allow_html=True)

                    with st.chat_message("assistant"):
                        try:
                            agent = getAgent(df)
                            response = agent.run(prompt)
                            formatted_response = format_response(response)
                            
                            if st.session_state.show_code:
                                st.code(formatted_response, language="python")
                            else:
                                st.markdown(f"<span style='background-color: #808080; color: white;'>{formatted_response}</span>", unsafe_allow_html=True)
                            
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": formatted_response
                            })
                            analysis_code = "agent.run(prompt)"
                            update_code_display(analysis_code, "chat")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                        
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
else:
    st.info("Please upload a CSV file to begin analysis")
