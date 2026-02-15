"""Logger setup module for fitness advisor chatbot.

Configures logging with file output for tracking application events and errors.
"""

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="settings/logs-fitness-chatbot.log",
)
