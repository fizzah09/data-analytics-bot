import os
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def format_agent_output(output):
    if isinstance(output, pd.DataFrame):
        return output
    elif isinstance(output, str):
        if 'DataFrame' in output or 'describe' in output:
            return pd.DataFrame(eval(output.split('Input:')[-1].strip()))
        return output
    return str(output)

def readData(path):
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        raise Exception(f"Error reading data: {str(e)}")

def getAgent(data):
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.5,
            google_api_key=os.environ.get("GOOGLE_API_KEY")
        )
        
        agent = create_pandas_dataframe_agent(
            llm, 
            data,
            verbose=True,
            handle_parsing_errors=True,
            allow_dangerous_code=True  # Enable code execution
        )
        return agent
    except Exception as e:
        raise Exception(f"Error creating agent: {str(e)}")