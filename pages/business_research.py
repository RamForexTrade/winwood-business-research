"""
Business Research Page
=====================
AI-powered business research and contact information discovery.
"""

import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime
from typing import Dict, List, Optional


def enhanced_business_research_page():
    """Business Research page with AI-powered search functionality."""
    
    st.title("🔍 Business Research")
    st.markdown("**AI-Powered Business Intelligence & Contact Discovery**")
    st.info("✨ **Smart search** to find detailed business information and contact details!")
    
    # Initialize session state
    if 'research_results' not in st.session_state:
        st.session_state.research_results = {}
    
    if 'research_status' not in st.session_state:
        st.session_state.research_status = 'ready'
    
    if 'api_tested' not in st.session_state:
        st.session_state.api_tested = False
    
    # Load data from session state
    data = None
    data_source = ""
    
    # Try multiple data sources
    if 'enhanced_data' in st.session_state and st.session_state.enhanced_data is not None:
        data = st.session_state.enhanced_data
        data_source = "enhanced data with research results"
        st.info("🔄 **Using enhanced data with previous research results**")
    elif 'working_data' in st.session_state and st.session_state.working_data is not None:
        data = st.session_state.working_data
        data_source = "working data from session"
        st.info("📊 **Using working dataset from session**")
    else:
        # Try state management
        try:
            from state_management import get_state
            state = get_state()
            if hasattr(state, 'main_dataframe') and state.main_dataframe is not None:
                data = state.main_dataframe
                data_source = "main dataframe from state management"
                st.info("📊 **Using dataset from state management**")
        except Exception as e:
            st.warning(f"⚠️ Could not load from state management: {e}")
    
    # Show data source info
    if data is not None:
        st.caption(f"Data source: {data_source} | Shape: {data.shape}")
    
    # API Configuration
    with st.expander("🔧 API Configuration", expanded=not st.session_state.api_tested):
        st.write("**Configure API Keys for AI Research:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tavily_key = st.text_input("Tavily API Key", 
                                     type="password", 
                                     help="Get your key from tavily.com",
                                     key="tavily_key_input")
        
        with col2:
            groq_key = st.text_input("Groq API Key", 
                                   type="password", 
                                   help="Get your key from console.groq.com",
                                   key="groq_key_input")
        
        if st.button("🧪 Test API Connection"):
            if tavily_key and groq_key:
                # Set environment variables for testing
                import os
                os.environ['TAVILY_API_KEY'] = tavily_key
                os.environ['GROQ_API_KEY'] = groq_key
                
                try:
                    from services.web_scraper import WebScraper
                    scraper = WebScraper()
                    
                    with st.spinner("Testing API connections..."):
                        api_ok, api_message = scraper.test_api_connection()
                    
                    if api_ok:
                        st.success(f"✅ {api_message}")
                        st.session_state.api_tested = True
                    else:
                        st.error(f"❌ {api_message}")
                except Exception as e:
                    st.error(f"❌ Configuration Error: {e}")
                    # Enable demo mode
                    st.session_state.api_tested = True
                    st.warning("⚠️ API test failed - enabling demo mode")
            else:
                st.warning("⚠️ Please enter both API keys")
        
        # Show setup instructions
        if not st.session_state.api_tested:
            st.info("""
            **Setup Instructions:**
            1. Get Tavily API key from [tavily.com](https://tavily.com) (for web search)
            2. Get Groq API key from [console.groq.com](https://console.groq.com) (for AI extraction)
            3. Enter keys above and test connection
            4. Or click test with empty keys to use demo mode
            """)
    
    # Handle no data case
    if data is None or data.empty:
        st.warning("⚠️ No data found. Please upload your business data first.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("← Go to Upload", use_container_width=True):
                try:
                    from controllers import go_to_stage
                    go_to_stage('upload')
                except:
                    if 'current_stage' in st.session_state:
                        st.session_state.current_stage = 'upload'
                    st.rerun()
        
        with col2:
            # Create sample data for testing
            if st.button("🧪 Use Sample Data", use_container_width=True):
                sample_data = pd.DataFrame({
                    'Consignee Name': [
                        'Acme Timber Corporation',
                        'Global Wood Solutions',
                        'Teakwood Trading Inc',
                        'Premium Lumber LLC',
                        'Forest Products Co'
                    ],
                    'Product': ['Teak Wood', 'Plywood', 'Timber Logs', 'Lumber', 'Wood Panels'],
                    'Quantity': [100, 200, 150, 300, 75],
                    'Value': [10000, 25000, 18000, 45000, 8500],
                    'Consignee City': ['Mumbai', 'Delhi', 'Chennai', 'Bangalore', 'Kolkata']
                })
                
                st.session_state.working_data = sample_data
                st.success("✅ Sample timber business data loaded!")
                st.rerun()
        
        return
    
    # Data overview
    st.subheader("📊 Data Overview")
    
    # Find company column
    company_column = None
    for col in ['Consignee Name', 'Company Name', 'Company', 'Consignee', 'Business Name']:
        if col in data.columns:
            company_column = col
            break
    
    if not company_column:
        # Use first string column
        for col in data.columns:
            if data[col].dtype == 'object':
                company_column = col
                break
    
    # Find city column
    city_column = None
    for col in ['Consignee City', 'City', 'Location', 'Place']:
        if col in data.columns:
            city_column = col
            break
    
    if company_column:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Records", len(data))
        
        with col2:
            unique_companies = data[company_column].nunique()
            st.metric("Unique Companies", unique_companies)
        
        with col3:
            researched_count = len(st.session_state.research_results)
            st.metric("Researched", researched_count)
        
        with col4:
            pending_count = unique_companies - researched_count
            st.metric("Pending", max(0, pending_count))
        
        # Show data preview
        with st.expander("📋 Data Preview", expanded=False):
            st.dataframe(data.head(10), use_container_width=True)
        
        # Research Configuration
        st.subheader("⚙️ Research Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            batch_size = st.slider("Batch Size", 1, 10, 3, 
                                 help="Number of companies to research at once")
            search_delay = st.slider("Search Delay (seconds)", 1.0, 5.0, 2.0, 
                                   help="Delay between searches")
        
        with col2:
            enable_government_search = st.checkbox("Enable Government Sources", value=True)
            enable_industry_search = st.checkbox("Enable Industry Sources", value=True)
        
        # Show search strategy
        search_layers = ["General Business Search"]
        if enable_government_search:
            search_layers.append("Government Database Search")
        if enable_industry_search:
            search_layers.append("Timber Industry Directory Search")
        
        st.info(f"🎯 **Search Strategy**: {' + '.join(search_layers)}")
        
        # Research execution
        st.subheader("🚀 AI Research Execution")
        
        # Get companies to research
        all_companies = data[company_column].dropna().unique().tolist()
        researched_companies = set(st.session_state.research_results.keys())
        pending_companies = [c for c in all_companies if c not in researched_companies]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"📋 **Companies to research**: {len(pending_companies)}")
            
            if pending_companies:
                st.write("**Sample pending companies:**")
                for company in pending_companies[:3]:
                    if city_column:
                        city_info = data[data[company_column] == company][city_column].iloc[0] if len(data[data[company_column] == company]) > 0 else ""
                        st.write(f"• {company}" + (f" ({city_info})" if city_info else ""))
                    else:
                        st.write(f"• {company}")
                if len(pending_companies) > 3:
                    st.write(f"... and {len(pending_companies) - 3} more")
        
        with col2:
            st.info(f"⚙️ **Configuration**:")
            st.write(f"• Batch size: {batch_size}")
            st.write(f"• Search delay: {search_delay}s")
            st.write(f"• Government search: {'✅' if enable_government_search else '❌'}")
            st.write(f"• Industry search: {'✅' if enable_industry_search else '❌'}")
        
        # Research button
        if pending_companies and st.session_state.api_tested:
            if st.button("🔍 Start AI Research", type="primary", use_container_width=True):
                perform_batch_research(
                    pending_companies[:batch_size], 
                    search_delay, 
                    city_column, 
                    data, 
                    company_column
                )
        elif not st.session_state.api_tested:
            st.warning("⚠️ Please test API connection first")
        elif not pending_companies:
            st.success("✅ All companies have been researched!")
    
    else:
        st.error("❌ Could not identify company name column in your data")
    
    # Results section
    if st.session_state.research_results:
        st.subheader("📋 Research Results")
        
        # Results overview
        total = len(st.session_state.research_results)
        successful = len([r for r in st.session_state.research_results.values() if r['status'] == 'found'])
        success_rate = (successful / total * 100) if total > 0 else 0.0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Researched", total)
        with col2:
            st.metric("Successful", successful)
        with col3:
            st.metric("Success Rate", f"{success_rate:.1f}%")
        
        # Results table
        with st.expander("👁️ View Research Results", expanded=True):
            try:
                from services.web_scraper import ResearchResultsManager
                results_df = ResearchResultsManager.format_results_for_display(st.session_state.research_results)
                st.dataframe(results_df, use_container_width=True)
            except Exception as e:
                # Fallback display
                results_data = []
                for company, result in st.session_state.research_results.items():
                    if result['status'] == 'found':
                        contacts = result.get('contacts', [])
                        email = contacts[0]['email'] if contacts else 'No email'
                        description = result.get('description', 'No description')
                    else:
                        email = 'Not found'
                        description = result.get('description', 'Research failed')
                    
                    results_data.append({
                        'Company': company,
                        'Status': result['status'].title(),
                        'Email': email,
                        'Description': description
                    })
                
                results_df = pd.DataFrame(results_data)
                st.dataframe(results_df, use_container_width=True)
        
        # Export options
        st.subheader("📤 Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'results_df' in locals():
                results_csv = results_df.to_csv(index=False)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="📥 Download Research Results",
                    data=results_csv,
                    file_name=f"business_research_results_{timestamp}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with col2:
            # Export enhanced data
            try:
                from services.web_scraper import ResearchResultsManager
                enhanced_data = ResearchResultsManager.merge_with_original_data(data, st.session_state.research_results)
                
                # Save enhanced data to session
                st.session_state.enhanced_data = enhanced_data
                st.session_state.working_data = enhanced_data
                
                enhanced_csv = enhanced_data.to_csv(index=False)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                st.download_button(
                    label="📊 Download Enhanced Data",
                    data=enhanced_csv,
                    file_name=f"enhanced_business_data_{timestamp}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            except Exception as e:
                st.button("📊 Download Enhanced Data", disabled=True, help=f"Error: {e}")
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("← Upload", use_container_width=True):
            try:
                from controllers import go_to_stage
                go_to_stage('upload')
            except:
                st.session_state.current_stage = 'upload'
                st.rerun()
    
    with col2:
        if st.button("📊 Visualizations", use_container_width=True):
            try:
                from controllers import go_to_stage
                go_to_stage('visualizations')
            except:
                st.session_state.current_stage = 'visualizations'
                st.rerun()
    
    with col3:
        if st.session_state.research_results:
            if st.button("Email Outreach →", type="primary", use_container_width=True):
                try:
                    from controllers import go_to_stage
                    go_to_stage('analyze')
                except:
                    st.session_state.current_stage = 'analyze'
                    st.rerun()
        else:
            st.button("Complete Research First", disabled=True, use_container_width=True)


def perform_batch_research(companies: List[str], delay: float, city_column: Optional[str], 
                          data: pd.DataFrame, company_column: str):
    """Perform batch research on companies."""
    
    progress_bar = st.progress(0.0, text="Initializing research...")
    status_text = st.empty()
    
    try:
        from services.web_scraper import WebScraper
        scraper = WebScraper()
        
        for i, company in enumerate(companies):
            # Update progress
            progress = (i + 1) / len(companies)
            progress_bar.progress(progress, text=f"Researching {company}...")
            status_text.info(f"🔍 Researching: {company}")
            
            # Get city context if available
            expected_city = None
            if city_column:
                try:
                    city_data = data[data[company_column] == company][city_column]
                    expected_city = city_data.iloc[0] if len(city_data) > 0 else None
                except:
                    pass
            
            # Perform research
            try:
                result = scraper.research_company_contacts(company, expected_city)
                st.session_state.research_results[company] = result
                
                # Show live results
                if result['status'] == 'found':
                    contacts = result.get('contacts', [])
                    email = contacts[0]['email'] if contacts else 'No email'
                    status_text.success(f"✅ Found: {company} | Email: {email}")
                else:
                    status_text.warning(f"⚠️ Limited data: {company}")
                
            except Exception as e:
                st.session_state.research_results[company] = {
                    'status': 'error',
                    'contacts': [],
                    'description': f"Research error: {str(e)}",
                    'confidence_score': 0.0
                }
                status_text.error(f"❌ Error: {company}")
            
            # Delay between requests
            time.sleep(delay)
    
    except Exception as e:
        st.error(f"❌ Research error: {e}")
        return
    
    # Final status
    successful = len([r for r in st.session_state.research_results.values() if r['status'] == 'found'])
    total = len(companies)
    
    progress_bar.progress(1.0, text="Research completed!")
    status_text.success(f"🎉 Research completed! {successful}/{total} successful")
    
    st.session_state.research_status = 'completed'
    time.sleep(2)
    st.rerun()


# Entry points
def render():
    """Entry point for existing app structure"""
    enhanced_business_research_page()


def main():
    """Main entry point"""
    enhanced_business_research_page()


if __name__ == "__main__":
    st.set_page_config(
        page_title="Enhanced Business Research",
        page_icon="🔍", 
        layout="wide"
    )
    main()