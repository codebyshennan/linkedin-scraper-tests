"""
Tests for the LinkedIn scraper.
"""
import os
import pytest
from src.scraper import LinkedInScraper

@pytest.fixture
def scraper():
    """Create a scraper instance for testing."""
    scraper = LinkedInScraper(headless=True)
    yield scraper
    scraper.close()

def test_scraper_initialization(scraper):
    """Test that the scraper initializes correctly."""
    assert scraper.driver is not None
    assert scraper.wait is not None

def test_login_without_credentials(scraper):
    """Test that login fails when no credentials are provided."""
    # Temporarily unset environment variables
    email = os.environ.pop('LINKEDIN_EMAIL', None)
    password = os.environ.pop('LINKEDIN_PASSWORD', None)
    
    with pytest.raises(ValueError):
        scraper.login()
    
    # Restore environment variables
    if email:
        os.environ['LINKEDIN_EMAIL'] = email
    if password:
        os.environ['LINKEDIN_PASSWORD'] = password

def test_login_with_invalid_credentials(scraper):
    """Test that login fails with invalid credentials."""
    result = scraper.login(
        email="invalid@example.com",
        password="invalidpassword"
    )
    assert not result

@pytest.mark.skipif(
    not os.getenv('LINKEDIN_EMAIL') or not os.getenv('LINKEDIN_PASSWORD'),
    reason="LinkedIn credentials not available"
)
def test_login_with_valid_credentials(scraper):
    """Test login with valid credentials from environment variables."""
    result = scraper.login()
    assert result

@pytest.mark.skipif(
    not os.getenv('LINKEDIN_EMAIL') or not os.getenv('LINKEDIN_PASSWORD'),
    reason="LinkedIn credentials not available"
)
def test_get_profile_info(scraper):
    """Test profile information retrieval."""
    # Login first
    scraper.login()
    
    # Test with a public profile
    profile_info = scraper.get_profile_info(
        "https://www.linkedin.com/in/williamhgates/"
    )
    
    assert isinstance(profile_info, dict)
    assert "name" in profile_info
    assert "headline" in profile_info
    assert "location" in profile_info
    assert "profile_url" in profile_info