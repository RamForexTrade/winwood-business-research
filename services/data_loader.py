"""
Enhanced Data Loader Service  
===========================
Data loading, parsing, and persistence with session management.
STAGE 2: Session Management System Integration
"""
import pandas as pd
import streamlit as st
from io import BytesIO
from typing import Optional, Tuple, Dict, Any
import os
from datetime import datetime

# Import from utils.data_utils if available, otherwise provide fallback
try:
    from utils.data_utils import clean_dataframe_for_arrow
except ImportError:
    def clean_dataframe_for_arrow(df):
        return df

# Import from state_management if available, otherwise provide fallback
try:
    from state_management import add_data_checkpoint, update_stage_progress
except ImportError:
    def add_data_checkpoint(description, data=None):
        pass
    def update_stage_progress(stage, completed=True):
        pass


@st.cache_data(show_spinner="Loading CSV...")
def load_csv(file_bytes: bytes) -> pd.DataFrame:
    """Load CSV data from uploaded bytes. Cached for speed."""
    try:
        # Try different encodings if UTF-8 fails
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        df = None
        
        for encoding in encodings:
            try:
                # Convert bytes to BytesIO for pandas
                file_io = BytesIO(file_bytes)
                df = pd.read_csv(file_io, encoding=encoding)
                break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                if encoding == encodings[-1]:  # Last encoding attempt
                    raise e
                continue
        
        if df is None:
            raise ValueError("Could not decode file with any supported encoding")
        
        # Basic validation
        if df.empty:
            st.warning("CSV file is empty")
            return pd.DataFrame()
        
        if len(df.columns) == 0:
            st.error("CSV file has no columns")
            return pd.DataFrame()
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Basic cleaning
        df = clean_dataframe_for_arrow(df)
        
        st.success(f"Loaded CSV: {len(df)} rows × {len(df.columns)} columns")
        return df
        
    except Exception as e:
        st.error(f"Error loading CSV: {str(e)}")
        return pd.DataFrame()


def load_excel(file_bytes: bytes, sheet_name: Optional[str] = None) -> pd.DataFrame:
    """Load Excel data from uploaded bytes."""
    try:
        file_io = BytesIO(file_bytes)
        
        # Load specific sheet or first sheet
        if sheet_name:
            df = pd.read_excel(file_io, sheet_name=sheet_name, engine='openpyxl')
        else:
            df = pd.read_excel(file_io, engine='openpyxl')
        
        # Basic validation
        if df.empty:
            st.warning("Excel file is empty")
            return pd.DataFrame()
        
        if len(df.columns) == 0:
            st.error("Excel file has no columns")
            return pd.DataFrame()
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Basic cleaning
        df = clean_dataframe_for_arrow(df)
        
        st.success(f"Loaded Excel: {len(df)} rows × {len(df.columns)} columns")
        return df
        
    except Exception as e:
        st.error(f"Error loading Excel: {str(e)}")
        return pd.DataFrame()


def detect_file_type(file_bytes: bytes, filename: str) -> str:
    """Detect file type from filename and content."""
    filename_lower = filename.lower()
    
    if filename_lower.endswith('.csv'):
        return 'csv'
    elif filename_lower.endswith(('.xlsx', '.xls')):
        return 'excel'
    else:
        return 'unknown'


def load_file(file_bytes: bytes, filename: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
    """Load file based on type detection."""
    file_type = detect_file_type(file_bytes, filename)
    
    if file_type == 'csv':
        return load_csv(file_bytes)
    elif file_type == 'excel':
        return load_excel(file_bytes, sheet_name)
    else:
        st.error(f"Unsupported file type: {filename}")
        return pd.DataFrame()


def save_dataframe_to_session(df: pd.DataFrame, name: str = "main_data") -> bool:
    """Save dataframe to session state."""
    try:
        if f"df_{name}" not in st.session_state:
            st.session_state[f"df_{name}"] = df.copy()
            add_data_checkpoint(f"Saved dataframe: {name}", df)
            return True
        return False
    except Exception as e:
        st.error(f"Error saving dataframe to session: {str(e)}")
        return False


def load_dataframe_from_session(name: str = "main_data") -> Optional[pd.DataFrame]:
    """Load dataframe from session state."""
    try:
        session_key = f"df_{name}"
        if session_key in st.session_state:
            return st.session_state[session_key].copy()
        return None
    except Exception as e:
        st.error(f"Error loading dataframe from session: {str(e)}")
        return None
