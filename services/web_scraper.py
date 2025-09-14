"""
Web Scraper Service for Business Contact Research
Enhanced with Tavily + Groq Integration for Timber/Wood Business Research
"""

import pandas as pd
import time
import streamlit as st
from typing import Dict, List, Tuple, Optional, Callable
import random
import json
from datetime import datetime
import os
import asyncio
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraper:
    """Enhanced web scraper with Tavily and Groq integration."""
    
    def __init__(self):
        """Initialize the web scraper with API configurations."""
        self.tavily_key = os.getenv('TAVILY_API_KEY')
        self.groq_key = os.getenv('GROQ_API_KEY')
        self.researcher = None
        
        # Initialize researcher if keys are available
        if self.tavily_key and self.groq_key:
            try:
                from tavily import TavilyClient
                self.researcher = TavilyClient(api_key=self.tavily_key)
                logger.info("WebScraper initialized with Tavily and Groq")
            except ImportError:
                logger.warning("Tavily not available - using fallback mode")
            except Exception as e:
                logger.error(f"Error initializing researcher: {e}")
        else:
            logger.warning("API keys not found - using demo mode")
    
    def test_api_connection(self) -> Tuple[bool, str]:
        """Test API connections."""
        if not self.tavily_key or not self.groq_key:
            return False, "API keys not configured"
        
        try:
            # Test Tavily
            if self.researcher:
                test_result = self.researcher.search("test query", max_results=1)
                if test_result:
                    return True, "API connections successful"
            
            return False, "API test failed"
        except Exception as e:
            return False, f"API test error: {str(e)}"
    
    def research_company_contacts(self, company_name: str, expected_city: Optional[str] = None) -> Dict:
        """Research company contact information."""
        if not self.researcher:
            return self.create_demo_result(company_name)
        
        try:
            # Construct search query
            search_query = f"{company_name} contact email phone"
            if expected_city:
                search_query += f" {expected_city}"
            
            # Search with Tavily
            search_results = self.researcher.search(
                search_query,
                max_results=5,
                search_depth="advanced"
            )
            
            # Extract contact information using Groq
            if search_results and 'results' in search_results:
                contacts = self.extract_contacts_with_groq(search_results['results'], company_name)
                
                if contacts:
                    return {
                        'status': 'found',
                        'contacts': contacts,
                        'description': f"Contact information found for {company_name}",
                        'confidence_score': 0.8,
                        'search_results': len(search_results['results'])
                    }
            
            return {
                'status': 'not_found',
                'contacts': [],
                'description': f"Limited information found for {company_name}",
                'confidence_score': 0.2,
                'search_results': 0
            }
            
        except Exception as e:
            logger.error(f"Research error for {company_name}: {e}")
            return self.create_fallback_result(company_name, str(e))
    
    def extract_contacts_with_groq(self, search_results: List[Dict], company_name: str) -> List[Dict]:
        """Extract contact information using Groq AI."""
        try:
            import groq
            client = groq.Groq(api_key=self.groq_key)
            
            # Prepare context from search results
            context = "\\n".join([
                f"Title: {result.get('title', '')}\\nContent: {result.get('content', '')[:500]}"
                for result in search_results[:3]
            ])
            
            prompt = f"""
            Extract contact information for the company "{company_name}" from the following search results:
            
            {context}
            
            Please extract and return ONLY valid contact information in JSON format:
            {{
                "email": "valid_email@domain.com or null",
                "phone": "valid_phone_number or null",
                "website": "valid_website_url or null"
            }}
            
            Return only the JSON, no additional text.
            """
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=200
            )
            
            # Parse response
            result_text = response.choices[0].message.content.strip()
            
            # Clean and parse JSON
            if result_text.startswith('```json'):
                result_text = result_text.replace('```json', '').replace('```', '').strip()
            
            contact_data = json.loads(result_text)
            
            # Validate and format
            contacts = []
            if contact_data.get('email') and '@' in str(contact_data['email']):
                contacts.append({
                    'email': contact_data['email'],
                    'phone': contact_data.get('phone'),
                    'website': contact_data.get('website')
                })
            
            return contacts
            
        except Exception as e:
            logger.error(f"Groq extraction error: {e}")
            return []
    
    def create_demo_result(self, company_name: str) -> Dict:
        """Create demo result for companies."""
        # Generate realistic demo data
        demo_emails = [
            f"info@{company_name.lower().replace(' ', '').replace('corporation', 'corp').replace('limited', 'ltd')[:15]}.com",
            f"contact@{company_name.lower().replace(' ', '')[:10]}.in",
            f"sales@{company_name.lower().replace(' ', '').replace('&', 'and')[:12]}.co.in"
        ]
        
        demo_phones = [
            "+91-22-" + str(random.randint(2000, 9999)) + "-" + str(random.randint(1000, 9999)),
            "+91-11-" + str(random.randint(4000, 9999)) + "-" + str(random.randint(1000, 9999)),
            "+91-80-" + str(random.randint(2000, 9999)) + "-" + str(random.randint(1000, 9999))
        ]
        
        # Random success rate for demo
        success_rate = random.random()
        
        if success_rate > 0.3:  # 70% success rate for demo
            return {
                'status': 'found',
                'contacts': [{
                    'email': random.choice(demo_emails),
                    'phone': random.choice(demo_phones),
                    'website': f"www.{company_name.lower().replace(' ', '')[:10]}.com"
                }],
                'description': f"Demo: {company_name} - Timber and wood processing company",
                'confidence_score': random.uniform(0.7, 0.9),
                'search_results': random.randint(3, 8)
            }
        else:
            return {
                'status': 'not_found',
                'contacts': [],
                'description': f"Demo: Limited information available for {company_name}",
                'confidence_score': random.uniform(0.1, 0.3),
                'search_results': random.randint(0, 2)
            }
    
    def create_fallback_result(self, company_name: str, error_msg: str) -> Dict:
        """Create fallback result for errors."""
        return {
            'status': 'error',
            'contacts': [],
            'description': f"Research error: {error_msg[:100]}",
            'confidence_score': 0.0,
            'search_results': 0
        }


class ResearchResultsManager:
    """Manage research results and data merging."""
    
    @staticmethod
    def format_results_for_display(research_results: Dict) -> pd.DataFrame:
        """Format research results for display."""
        results_data = []
        
        for company, result in research_results.items():
            if result['status'] == 'found':
                contacts = result.get('contacts', [])
                primary_email = contacts[0]['email'] if contacts else 'No email'
                phone = contacts[0].get('phone', 'No phone') if contacts else 'No phone'
                website = result.get('website', contacts[0].get('website', 'No website')) if contacts else 'No website'
                description = result.get('description', 'No description')
                confidence = f"{result.get('confidence_score', 0):.0%}"
            else:
                primary_email = phone = website = 'Not found'
                description = result.get('description', 'Research failed')
                confidence = f"{result.get('confidence_score', 0):.0%}"
            
            results_data.append({
                'Company': company,
                'Status': result['status'].title(),
                'Email': primary_email,
                'Phone': phone,
                'Website': website,
                'Description': description,
                'Confidence': confidence
            })
        
        return pd.DataFrame(results_data)
    
    @staticmethod
    def merge_with_original_data(original_data: pd.DataFrame, research_results: Dict) -> pd.DataFrame:
        """Merge research results with original data."""
        enhanced_data = original_data.copy()
        
        # Find company column
        company_column = None
        for col in ['Consignee Name', 'Company Name', 'Company', 'Consignee', 'Business Name']:
            if col in enhanced_data.columns:
                company_column = col
                break
        
        if not company_column:
            return enhanced_data
        
        # Add research result columns
        enhanced_data['Research_Status'] = 'pending'
        enhanced_data['Research_Email'] = ''
        enhanced_data['Research_Phone'] = ''
        enhanced_data['Research_Website'] = ''
        enhanced_data['Research_Description'] = ''
        enhanced_data['Research_Confidence'] = 0.0
        
        # Merge results
        for company, result in research_results.items():
            mask = enhanced_data[company_column] == company
            
            enhanced_data.loc[mask, 'Research_Status'] = result['status']
            
            if result['status'] == 'found' and result.get('contacts'):
                contact = result['contacts'][0]
                enhanced_data.loc[mask, 'Research_Email'] = contact.get('email', '')
                enhanced_data.loc[mask, 'Research_Phone'] = contact.get('phone', '')
                enhanced_data.loc[mask, 'Research_Website'] = contact.get('website', '')
            
            enhanced_data.loc[mask, 'Research_Description'] = result.get('description', '')
            enhanced_data.loc[mask, 'Research_Confidence'] = result.get('confidence_score', 0.0)
        
        return enhanced_data


# Global scraper instance
_scraper_instance = None

def get_web_scraper() -> WebScraper:
    """Get global web scraper instance."""
    global _scraper_instance
    if _scraper_instance is None:
        _scraper_instance = WebScraper()
    return _scraper_instance
