import requests
import logging
import json
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_ollama_running() -> bool:
    """Check if the Ollama server is running locally."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def process_with_yield_navigator(content: str, timeout: int = 30) -> Optional[str]:
    """
    Process text with the Yield Navigator model via Ollama API.

    Args:
        content (str): The input text
        timeout (int): Request timeout in seconds

    Returns:
        Optional[str]: The processed text, or None if failed
    """
    if not content or not isinstance(content, str) or len(content.strip()) == 0:
        logger.warning("Invalid or empty content provided.")
        return None

    if not is_ollama_running():
        logger.error("Ollama is not running. Start it with 'ollama serve'.")
        return None

    try:
        logger.info("Sending content to Yield Navigator model...")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "YConcept/yield-navigator",
                "prompt": (
                    f"Rewrite the following text for a blog post. "
                    f"Begin with a strong position or hook and end with an engaging close:\n\n{content}"
                ),
                "stream": False
            },
            timeout=timeout,
            headers={"Content-Type": "application/json"}
        )

        response.raise_for_status()
        data = response.json()
        result = data.get("response", "")

        if result:
            logger.info("Successfully processed content.")
            return result
        else:
            logger.warning("The model returned no output.")
            return None

    except requests.exceptions.RequestException as e:
        logger.error("Request error: %s", str(e))
        return None
    except json.JSONDecodeError as e:
        logger.error("Response parse error: %s", str(e))
        return None

# Test block runs if you execute `python3 yield_navigator.py`
if __name__ == "__main__":
    test_content = "Artificial intelligence is transforming how businesses make decisions."
    result = process_with_yield_navigator(test_content)
    if result:
        print("\nProcessed content:\n")
        print(result)
    else:
        print("\nFailed to process content. Check if Ollama is running and the model is pulled.\n")
