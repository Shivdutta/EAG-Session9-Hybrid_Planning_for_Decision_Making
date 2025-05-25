import unittest
from typing import Tuple, List

# Constants and mocked validation logic for demonstration
MAX_INPUT_LENGTH = 500

def validate_input_length(text: str) -> Tuple[bool, str]:
    return (len(text) <= MAX_INPUT_LENGTH, "Input too long" if len(text) > MAX_INPUT_LENGTH else "")

def validate_urls(text: str) -> Tuple[bool, str, str]:
    if "http://" in text or "https://" in text:
        return False, "URLs are not allowed", text.replace("http://", "[REDACTED_URL]").replace("https://", "[REDACTED_URL]")
    return True, "", ""

def validate_no_nsfw(text: str) -> Tuple[bool, str]:
    if "nsfw" in text.lower():
        return False, "NSFW content detected"
    return True, ""

def validate_email_format(text: str) -> Tuple[bool, str, str]:
    if "@" in text and not text.endswith(".com"):
        return False, "Invalid email format", text.replace("@", "[at]")
    return True, "", ""

def validate_llm_input(text: str) -> Tuple[bool, List[str], str]:
    is_valid = True
    error_messages = []
    fixed_text = text
    
    length_valid, length_error = validate_input_length(text)
    if not length_valid:
        is_valid = False
        error_messages.append(length_error)
        if len(text) > MAX_INPUT_LENGTH:
            fixed_text = text[:MAX_INPUT_LENGTH - 100] + "... [truncated]"
    
    urls_valid, urls_error, urls_fixed = validate_urls(fixed_text)
    if not urls_valid:
        is_valid = False
        error_messages.append(urls_error)
    elif urls_fixed:
        fixed_text = urls_fixed
    
    nsfw_valid, nsfw_error = validate_no_nsfw(fixed_text)
    if not nsfw_valid:
        is_valid = False
        error_messages.append(nsfw_error)
    
    email_valid, email_error, email_fixed = validate_email_format(fixed_text)
    if not email_valid:
        is_valid = False
        error_messages.append(email_error)
    elif email_fixed:
        fixed_text = email_fixed
    
    return is_valid, error_messages, fixed_text


class TestValidateLLMInput(unittest.TestCase):

    # ==== PASSING CASES ====

    def test_valid_short_clean_input(self):
        text = "Hello, this is a valid input with no issues. Email: user@example.com"
        is_valid, errors, fixed = validate_llm_input(text)
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])
        self.assertEqual(fixed, text)

    def test_valid_with_email(self):
        text = "You can email me at person@example.com for more info."
        is_valid, errors, fixed = validate_llm_input(text)
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])
    
    # ==== FAILING CASES ====

    def test_input_too_long(self):
        text = "x" * 600
        is_valid, errors, fixed = validate_llm_input(text)
        self.assertFalse(is_valid)
        self.assertIn("Input too long", errors)
        self.assertTrue(fixed.endswith("... [truncated]"))

    def test_input_with_url(self):
        text = "Visit my site at http://example.com"
        is_valid, errors, fixed = validate_llm_input(text)
        self.assertFalse(is_valid)
        self.assertIn("URLs are not allowed", errors)
        self.assertIn("[REDACTED_URL]", fixed)

    def test_input_with_nsfw_content(self):
        text = "This has NSFW words in it."
        is_valid, errors, fixed = validate_llm_input(text)
        self.assertFalse(is_valid)
        self.assertIn("NSFW content detected", errors)

    def test_input_with_invalid_email(self):
        text = "Contact me at someone@example"  # missing .com
        is_valid, errors, fixed = validate_llm_input(text)
        self.assertFalse(is_valid)
        self.assertIn("Invalid email format", errors)
        self.assertIn("[at]", fixed)

    def test_multiple_issues(self):
        text = "NSFW content and a bad email someone@example and a link http://example.com " + "x" * 600
        is_valid, errors, fixed = validate_llm_input(text)
        self.assertFalse(is_valid)
        self.assertIn("Input too long", errors)
        self.assertIn("URLs are not allowed", errors)
        self.assertIn("Invalid email format", errors)
        self.assertIn("NSFW content detected", errors)

if __name__ == '__main__':
    unittest.main()
