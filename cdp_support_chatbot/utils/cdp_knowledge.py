import requests
from bs4 import BeautifulSoup
import re
import os
import json
import time

class CDPKnowledgeBase:
    """Class for managing CDP documentation and knowledge"""
    
    def __init__(self):
        """Initialize the CDP knowledge base"""
        self.platforms = ["Segment", "mParticle", "Lytics", "Zeotap"]
        self.doc_urls = {
            "Segment": "https://segment.com/docs/",
            "mParticle": "https://docs.mparticle.com/",
            "Lytics": "https://docs.lytics.com/",
            "Zeotap": "https://docs.zeotap.com/home/en-us/"
        }
        
        # Dictionary of platform documentation
        self.documentation = {}
        
        # Load or fetch documentation
        self._load_documentation()
        
        # Keywords and phrases related to CDPs
        self.cdp_keywords = [
            "customer data platform", "cdp", "segment", "mparticle", "lytics", "zeotap",
            "data source", "integration", "audience", "user profile", "event tracking",
            "identity resolution", "data collection", "analytics", "attribution",
            "marketing", "personalization", "campaign", "customer journey", "data sync",
            "webhook", "api", "sdk", "tracking", "user data", "segmentation"
        ]
    
    def _load_documentation(self):
        """Load documentation from cache or fetch from websites"""
        cache_file = "cdp_documentation_cache.json"
        
        # Check if cached documentation exists
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                self.documentation = json.load(f)
            print("Loaded documentation from cache.")
        else:
            # For production, you would implement actual web scraping here
            # For this assignment, we're using placeholder documentation
            self._create_placeholder_documentation()
            
            # Save to cache
            with open(cache_file, 'w') as f:
                json.dump(self.documentation, f)
    
    def _create_placeholder_documentation(self):
        """Create placeholder documentation for each platform"""
        self.documentation = {
            "Segment": [
                "Setting up a new source in Segment: 1. Log in to your Segment workspace. 2. Navigate to Sources in the left sidebar. 3. Click 'Add Source'. 4. Select the type of source you want to add. 5. Follow the configuration instructions specific to your chosen source.",
                "Segment provides various SDKs for different platforms: JavaScript, iOS, Android, Node.js, etc. To implement tracking: 1. Install the appropriate SDK. 2. Initialize with your write key. 3. Track events using the track() method.",
                "To create a new destination in Segment: 1. Go to the Destinations page. 2. Click 'Add Destination'. 3. Search for your desired integration. 4. Follow the configuration steps to connect your data.",
                "Segment Protocols help maintain data quality. To set up: 1. Go to Protocols in your workspace. 2. Define tracking plans with expected events and properties. 3. Enable enforcement to validate incoming data against your plan."
            ],
            "mParticle": [
                "Creating a user profile in mParticle: 1. Implement the mParticle SDK in your application. 2. Use the identify() method to create a user profile with a unique ID. 3. Add user attributes with the setUserAttribute() method.",
                "Setting up a new input in mParticle: 1. Navigate to Setup > Inputs. 2. Select the platform for your input. 3. Follow the configuration steps for your specific input type. 4. Obtain your API credentials for implementation.",
                "To create an audience in mParticle: 1. Go to Audiences in the left sidebar. 2. Click 'New Audience'. 3. Define your audience criteria using attributes and behaviors. 4. Save and activate your audience.",
                "mParticle's Identity Resolution: 1. Configure identity strategy in Setup > Identity. 2. Set up identity priorities. 3. Implement identity linking in your app or website."
            ],
            "Lytics": [
                "Building an audience segment in Lytics: 1. Navigate to Segments in the main menu. 2. Click 'Create New Segment'. 3. Use the segment builder to define your criteria. 4. Add behavioral triggers and user attributes. 5. Save and publish your segment.",
                "Setting up a data collection in Lytics: 1. Go to Collect > Sources in the navigation. 2. Select 'Add New Source'. 3. Choose your source type. 4. Configure connection settings and mapping.",
                "Lytics personalization implementation: 1. Create content recommendations in the Experience section. 2. Define audience targeting rules. 3. Use the Lytics JavaScript tag to deliver personalized content.",
                "Implementing Lytics JavaScript tag: 1. Go to Implementation section. 2. Copy your unique tag code. 3. Add to your website's header or tag manager. 4. Verify installation with the tag assistant."
            ],
            "Zeotap": [
                "Integrating your data with Zeotap: 1. Log in to the Zeotap platform. 2. Navigate to Integrations in the main menu. 3. Select 'Add New Integration'. 4. Choose from available connectors or use the API option. 5. Configure data mapping and scheduling.",
                "Creating a unified customer view in Zeotap: 1. Set up identity resolution settings in Data Management. 2. Define matching rules for customer records. 3. Review and approve identity links.",
                "Building segments in Zeotap: 1. Go to Audience Manager. 2. Click 'Create Segment'. 3. Use the visual builder to define audience criteria. 4. Add behavioral and demographic filters. 5. Save and activate.",
                "Activating Zeotap audiences: 1. Navigate to Activation section. 2. Select destination platforms. 3. Map your segments to the destination. 4. Configure sync settings and frequency."
            ]
        }
    
    def is_cdp_related(self, query):
        """
        Determine if the query is related to CDPs
        
        Args:
            query (str): The user query
            
        Returns:
            bool: True if the query is CDP-related, False otherwise
        """
        query_lower = query.lower()
        
        # Check for CDP platform names
        for platform in self.platforms:
            if platform.lower() in query_lower:
                return True
        
        # Check for CDP-related keywords
        for keyword in self.cdp_keywords:
            if keyword in query_lower:
                return True
                
        # Check for "how to" questions related to data platforms
        how_to_pattern = re.compile(r"how (do|can|to|would|should) (i|we|you).*")
        if how_to_pattern.search(query_lower):
            # If it's a how-to question, check if it might be related to data platforms
            data_related_terms = ["data", "user", "customer", "profile", "segment", "audience", "track", "integration"]
            for term in data_related_terms:
                if term in query_lower:
                    return True
        
        return False
    
    def get_documentation(self, platform):
        """
        Get the documentation for a specific platform
        
        Args:
            platform (str): The CDP platform name
            
        Returns:
            list: List of documentation snippets for the platform
        """
        if platform in self.documentation:
            return self.documentation[platform]
        return []