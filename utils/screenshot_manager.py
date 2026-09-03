import os
import re
import base64
from datetime import datetime
from typing import Tuple
from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger("ScreenshotManager")

class ScreenshotManager:
    @staticmethod
    def capture(page: Page, name: str, status: str = "PASS") -> Tuple[str, str]:
        """
        Captures a screenshot with an execution-specific timestamp.
        Example: TC_HOME_001_cookie_bar_PASS_20260903_143000.png
        
        Returns:
            Tuple[str, str]: (absolute_file_path, base64_data_uri)
        """
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        screenshots_dir = os.path.join(project_root, "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:19]  # e.g., 20260903_143000_123
        clean_name = re.sub(r'[^a-zA-Z0-9_-]', '_', name).strip('_')
        filename = f"{clean_name}_{status.upper()}_{timestamp}.png"
        filepath = os.path.join(screenshots_dir, filename)
        
        b64_uri = ""
        try:
            # Capture viewport screenshot
            png_bytes = page.screenshot(path=filepath, full_page=False)
            b64_str = base64.b64encode(png_bytes).decode("utf-8")
            b64_uri = f"data:image/png;base64,{b64_str}"
            logger.info(f"Captured screenshot: {filepath}")
            return filepath, b64_uri
        except Exception as e:
            logger.error(f"Failed to capture screenshot {filename}: {e}")
            # Fallback if file was written but bytes read failed
            if os.path.exists(filepath):
                try:
                    with open(filepath, "rb") as f:
                        b64_str = base64.b64encode(f.read()).decode("utf-8")
                        b64_uri = f"data:image/png;base64,{b64_str}"
                except Exception:
                    pass
            return filepath, b64_uri

    @staticmethod
    def file_to_base64(filepath: str) -> str:
        """Converts an existing image file on disk to a base64 data URI."""
        if not filepath or not os.path.exists(filepath):
            return ""
        try:
            with open(filepath, "rb") as img_file:
                b64 = base64.b64encode(img_file.read()).decode("utf-8")
                return f"data:image/png;base64,{b64}"
        except Exception as e:
            logger.warning(f"Failed converting {filepath} to base64: {e}")
            return ""
