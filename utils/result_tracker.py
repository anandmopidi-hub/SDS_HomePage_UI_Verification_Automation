import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
from utils.logger import get_logger

logger = get_logger("ResultTracker")

@dataclass
class UIElementVerificationResult:
    section: str
    ui_element: str
    element_type: str
    visible: str  # "Yes" / "No"
    clickable: str  # "Yes" / "No"
    observed_action: str
    expected_result: str
    actual_result: str
    navigation_url: str
    status: str  # "PASS" / "FAIL" / "REQUIREMENT CONFIRMATION NEEDED" / "SKIPPED"
    evidence: str = "View Screenshot"
    screenshot_path: str = ""
    screenshot_b64: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@dataclass
class TestCaseResult:
    test_id: str  # e.g., "TC_HOME_001"
    test_name: str  # e.g., "test_01_cookie_bar_elements"
    section: str  # e.g., "Cookie Consent"
    test_case: str  # e.g., "Cookie Bar Verification"
    observation: str  # e.g., "All cookie bar actions verified successfully"
    status: str  # "PASS" / "FAIL" / "REQUIREMENT CONFIRMATION NEEDED" / "SKIPPED"
    duration: str  # "00:08"
    duration_sec: float = 0.0
    screenshot_path: str = ""
    screenshot_b64: str = ""
    error_message: str = ""
    stack_trace: str = ""
    failed_url: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

class ResultTracker:
    _instance = None
    results: List[UIElementVerificationResult] = []
    test_cases: List[TestCaseResult] = []
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResultTracker, cls).__new__(cls)
            cls._instance.results = []
            cls._instance.test_cases = []
            cls._instance.start_time = datetime.now()
            cls._instance.end_time = None
        return cls._instance

    @classmethod
    def set_start_time(cls, dt: Optional[datetime] = None):
        cls.start_time = dt or datetime.now()

    @classmethod
    def set_end_time(cls, dt: Optional[datetime] = None):
        cls.end_time = dt or datetime.now()

    @classmethod
    def get_duration_str(cls) -> str:
        if not cls.start_time:
            return "00:00"
        end = cls.end_time or datetime.now()
        total_sec = int((end - cls.start_time).total_seconds())
        mins, secs = divmod(max(0, total_sec), 60)
        return f"{mins:02d}:{secs:02d}"

    @classmethod
    def record(cls, section: str, ui_element: str, element_type: str, visible: bool, clickable: bool,
               observed_action: str, actual_result: str, navigation_url: str, status: str,
               evidence: str = "View Screenshot", expected_result: Optional[str] = None,
               screenshot_path: str = "", screenshot_b64: str = ""):
        """
        Records an individual UI element verification result.
        Maintains backwards compatibility with existing test calls.
        """
        if expected_result is None:
            expected_result = f"Element is visible, enabled, and executes '{observed_action}'"

        item = UIElementVerificationResult(
            section=section,
            ui_element=ui_element,
            element_type=element_type,
            visible="Yes" if visible else "No",
            clickable="Yes" if clickable else "No",
            observed_action=observed_action,
            expected_result=expected_result,
            actual_result=actual_result,
            navigation_url=navigation_url,
            status=status,
            evidence=evidence,
            screenshot_path=screenshot_path,
            screenshot_b64=screenshot_b64
        )
        cls.results.append(item)
        logger.info(f"[{status}] {section} > {ui_element} ({element_type}): {actual_result}")

    @classmethod
    def record_test_case(cls, test_id: str, test_name: str, section: str, test_case: str,
                         observation: str, status: str, duration_sec: float,
                         screenshot_path: str = "", screenshot_b64: str = "",
                         error_message: str = "", stack_trace: str = "", failed_url: str = ""):
        """Records a high-level test case scenario result."""
        mins, secs = divmod(int(duration_sec), 60)
        duration_str = f"{mins:02d}:{secs:02d}"

        tc = TestCaseResult(
            test_id=test_id,
            test_name=test_name,
            section=section,
            test_case=test_case,
            observation=observation,
            status=status,
            duration=duration_str,
            duration_sec=duration_sec,
            screenshot_path=screenshot_path,
            screenshot_b64=screenshot_b64,
            error_message=error_message,
            stack_trace=stack_trace,
            failed_url=failed_url
        )
        cls.test_cases.append(tc)
        logger.info(f"Test Case [{test_id}] {test_case} completed with status: {status} ({duration_str})")

    @classmethod
    def attach_screenshot_to_section(cls, section_name: str, screenshot_path: str, screenshot_b64: str):
        """Attaches screenshot evidence to elements in this section that lack screenshots."""
        for r in cls.results:
            if not r.screenshot_b64:
                # Match section name flexibly
                r_sec = r.section.lower()
                s_sec = section_name.lower()
                if (r_sec in s_sec) or (s_sec in r_sec) or ("cookie" in r_sec and "cookie" in s_sec) or ("artist" in r_sec and "artist" in s_sec) or ("bundle" in r_sec and "bundle" in s_sec) or ("filter" in r_sec and "filter" in s_sec):
                    r.screenshot_path = screenshot_path
                    r.screenshot_b64 = screenshot_b64

    @classmethod
    def get_summary(cls) -> Dict[str, Any]:
        total_elements = len(cls.results)
        passed_elements = sum(1 for r in cls.results if r.status == "PASS")
        failed_elements = sum(1 for r in cls.results if r.status == "FAIL")
        req_elements = sum(1 for r in cls.results if r.status == "REQUIREMENT CONFIRMATION NEEDED")
        skipped_elements = sum(1 for r in cls.results if r.status == "SKIPPED")

        total_tests = len(cls.test_cases)
        passed_tests = sum(1 for t in cls.test_cases if t.status == "PASS")
        failed_tests = sum(1 for t in cls.test_cases if t.status == "FAIL")
        req_tests = sum(1 for t in cls.test_cases if t.status == "REQUIREMENT CONFIRMATION NEEDED")
        skipped_tests = sum(1 for t in cls.test_cases if t.status == "SKIPPED")

        pass_pct = 0.0
        if total_elements > 0:
            pass_pct = round((passed_elements / total_elements) * 100, 1)

        return {
            "total_elements": total_elements,
            "passed_elements": passed_elements,
            "failed_elements": failed_elements,
            "requirement_confirmation_needed": req_elements,
            "skipped_elements": skipped_elements,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "req_tests": req_tests,
            "skipped_tests": skipped_tests,
            "pass_percentage": pass_pct,
            "duration_str": cls.get_duration_str()
        }

    @classmethod
    def get_section_summary(cls) -> List[Dict[str, Any]]:
        """Dynamically aggregates verification results by section."""
        sections_order = [
            "Cookie Bar", "Cookie Consent",
            "Header",
            "Main Navigation",
            "Hero Carousel",
            "Discovery & Filters",
            "Featured Products",
            "Design Store Artists",
            "Design Bundles",
            "Promotional Banner",
            "Footer",
            "Floating Widgets"
        ]
        
        # Group by section name preserving canonical order
        grouped: Dict[str, Dict[str, Any]] = {}
        for r in cls.results:
            sec = r.section
            if sec not in grouped:
                grouped[sec] = {"section": sec, "verified": 0, "pass": 0, "fail": 0, "requirement": 0, "skipped": 0}
            grouped[sec]["verified"] += 1
            if r.status == "PASS":
                grouped[sec]["pass"] += 1
            elif r.status == "FAIL":
                grouped[sec]["fail"] += 1
            elif r.status == "REQUIREMENT CONFIRMATION NEEDED":
                grouped[sec]["requirement"] += 1
            elif r.status == "SKIPPED":
                grouped[sec]["skipped"] += 1

        ordered_list = []
        for s in sections_order:
            if s in grouped:
                ordered_list.append(grouped.pop(s))
        # Append any remaining
        for remaining in grouped.values():
            ordered_list.append(remaining)

        return ordered_list

    @classmethod
    def get_requirement_confirmations(cls) -> List[UIElementVerificationResult]:
        return [r for r in cls.results if r.status == "REQUIREMENT CONFIRMATION NEEDED"]

    @classmethod
    def get_failures(cls) -> List[UIElementVerificationResult]:
        return [r for r in cls.results if r.status == "FAIL"]

    @classmethod
    def print_table(cls):
        summary = cls.get_summary()
        header = f"{'Section':<20} | {'UI Element':<32} | {'Type':<12} | {'Vis':<4} | {'Clk':<4} | {'Status':<32} | {'Navigation URL'}"
        sep = "-" * len(header)
        lines = ["\n" + sep, "HOME PAGE UI VERIFICATION AUDIT TRAIL", sep, header, sep]
        for r in cls.results:
            lines.append(f"{r.section:<20} | {r.ui_element:<32} | {r.element_type:<12} | {r.visible:<4} | {r.clickable:<4} | {r.status:<32} | {r.navigation_url}")
        lines.append(sep)
        lines.append(f"TOTAL: {summary['total_elements']} | PASSED: {summary['passed_elements']} | FAILED: {summary['failed_elements']} | REQUIREMENT CONFIRMATION NEEDED: {summary['requirement_confirmation_needed']}")
        lines.append(sep + "\n")
        table_text = "\n".join(lines)
        print(table_text)
        return table_text
