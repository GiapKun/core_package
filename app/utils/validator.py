import re

from bson import ObjectId

from app.utils.value import DataFormat
import tldextract


def check_object_id(_id: str) -> bool:
    """
    Checks if a given string is a valid ObjectId.

    Args:
        _id (str): The string to check.

    Returns:
        is_valid (bool): True if the string is a valid ObjectId, False otherwise.
    """
    if ObjectId.is_valid(_id):
        return True
    return False


def check_email(email):
    """
    Checks if a given string is a valid email address based on the defined regex pattern.

    Args:
        email (str): The email address to check.

    Returns:
        is_valid (bool): True if the email matches the regex pattern, False otherwise.
    """
    pattern = DataFormat.EMAIL_REGEX.value
    if re.match(pattern, email):
        return True
    return False


def check_phone(phone):
    """
    Checks if a given string is a valid phone number based on the defined regex pattern.

    Args:
        phone (str): The phone number to check.

    Returns:
        is_valid (bool): True if the phone number matches the regex pattern, False otherwise.
    """
    pattern = DataFormat.PHONE_REGEX.value
    if re.match(pattern, phone):
        return True
    return False

def check_domain(domain: str):
    """
    Checks if the given domain is valid and contains a "registered domain".

    - Uses the `tldextract` library to split the domain into components:
        + Subdomain (if any)
        + Main domain (e.g., "example")
        + Suffix (e.g., "com", "org")
    - The `registered_domain` combines the main domain and the suffix (e.g., "example.com").

    Args:
        domain (str): The domain name to check.

    Returns:
        str: The registered domain (e.g., "example.com") if valid.
        bool: Returns `False` if no registered domain is found.
    """
    extract = tldextract.extract(domain)
    if extract.registered_domain:  # Check if a registered domain exists
        return extract.registered_domain  # Return the registered domain (e.g., "example.com")
    else:
        return False  # Invalid domain
    
def get_main_domain(domain: str):
    """
    Extracts the main domain (excluding subdomain and suffix) from a given domain.

    - Uses `tldextract` to parse the domain.
    - The main domain (e.g., "example") is often used to identify the organization.

    Args:
        domain (str): The domain name to extract the main domain from.

    Returns:
        str: The main domain (e.g., "example") if valid.
        bool: Returns `False` if the domain is invalid or does not have a main domain.
    """
    extract = tldextract.extract(domain)
    if extract.domain:  # Check if a main domain exists
        return extract.domain  # Return the main domain (e.g., "example")
    else:
        return False  # Invalid domain
    
def get_suffix_domain(domain: str, include_first_dot: bool = True):
    """
    Retrieves the suffix (e.g., "com", "org") of a domain.

    - Uses `tldextract` to parse the domain and extract the suffix.
    - Optionally adds a leading dot (`.`) before the suffix, controlled by `include_first_dot`.

    Args:
        domain (str): The domain name to extract the suffix from.
        include_first_dot (bool): 
            - If `True`, includes a leading dot (`.`) before the suffix (default).
            - If `False`, returns the suffix without the leading dot (e.g., "com").

    Returns:
        str: The suffix (e.g., ".com" or "com" depending on `include_first_dot`) if valid.
        bool: Returns `False` if the domain is invalid or does not have a suffix.
    """
    extract = tldextract.extract(domain)
    if extract.suffix:  # Check if a suffix exists
        suffix = f".{extract.suffix}" if include_first_dot else extract.suffix
        return suffix  # Return the suffix (e.g., ".com" or "com")
    else:
        return False  # Invalid domain or no suffix
