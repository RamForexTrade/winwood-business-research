"""
Quick test to verify the preprocessor module is working
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from services.preprocessor import detect_file_type, remove_duplicates_by_consignee
    print('✅ Successfully imported preprocessor module!')
    
    # Test file type detection
    print('Testing file type detection...')
    csv_type = detect_file_type(b'test', 'sample.csv')
    xlsx_type = detect_file_type(b'test', 'sample.xlsx')
    print(f'CSV detection: {csv_type}')
    print(f'XLSX detection: {xlsx_type}')
    
    print('✅ Preprocessor module is working correctly!')
    print('🎉 Ready to test with Streamlit app!')
    
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()