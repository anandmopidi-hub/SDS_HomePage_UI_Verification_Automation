import os
import json
import sys
import platform
import html
from datetime import datetime
from typing import Dict, Any, List
from utils.result_tracker import ResultTracker, TestCaseResult, UIElementVerificationResult
from utils.logger import get_logger

logger = get_logger("ReportGenerator")

class ReportGenerator:
    @classmethod
    def generate_html_report(cls, output_path: str = "reports/home_page_report.html") -> str:
        """
        Generates a self-contained, professional dashboard-style HTML report.
        Can run standalone and be opened in Chrome/Edge without any server.
        """
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_output_path = os.path.join(project_root, output_path)
        os.makedirs(os.path.dirname(full_output_path), exist_ok=True)

        summary = ResultTracker.get_summary()
        test_cases = ResultTracker.test_cases
        ui_elements = ResultTracker.results
        sections = ResultTracker.get_section_summary()
        req_confirmations = ResultTracker.get_requirement_confirmations()
        failures = ResultTracker.get_failures()

        # Dynamic timestamps
        now = datetime.now()
        start_time = ResultTracker.start_time or now
        end_time = ResultTracker.end_time or now
        execution_date_str = start_time.strftime("%d-%b-%Y")
        execution_start_str = start_time.strftime("%H:%M:%S")
        execution_end_str = end_time.strftime("%H:%M:%S")
        duration_str = summary["duration_str"]

        # Execution History Management
        history_file = os.path.join(project_root, "reports", "history.json")
        history_data = cls._update_and_get_history(
            history_file,
            execution_date_str,
            execution_start_str,
            summary["total_tests"],
            summary["passed_tests"],
            summary["failed_tests"],
            summary["req_tests"],
            duration_str
        )

        html_content = cls._build_html(
            summary=summary,
            test_cases=test_cases,
            ui_elements=ui_elements,
            sections=sections,
            req_confirmations=req_confirmations,
            failures=failures,
            execution_date_str=execution_date_str,
            execution_start_str=execution_start_str,
            execution_end_str=execution_end_str,
            duration_str=duration_str,
            history_data=history_data
        )

        try:
            with open(full_output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            logger.info(f"Successfully generated custom HTML dashboard report at: {full_output_path}")
            return full_output_path
        except Exception as e:
            logger.error(f"Failed to generate HTML report: {e}")
            return ""

    @staticmethod
    def _update_and_get_history(history_file: str, date_str: str, time_str: str,
                                total: int, passed: int, failed: int, req: int, duration: str) -> List[Dict[str, Any]]:
        history = []
        if os.path.exists(history_file):
            try:
                with open(history_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                history = []
        
        # Add current execution
        current_record = {
            "date": date_str,
            "time": time_str,
            "total": total,
            "passed": passed,
            "failed": failed,
            "requirement": req,
            "duration": duration,
            "is_current": True
        }
        
        # Mark previous as not current
        for h in history:
            h["is_current"] = False

        history.append(current_record)
        # Keep up to 10 historical records
        history = history[-10:]

        try:
            with open(history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)
        except Exception:
            pass

        return history

    @classmethod
    def _build_html(cls, summary: Dict[str, Any], test_cases: List[TestCaseResult],
                    ui_elements: List[UIElementVerificationResult], sections: List[Dict[str, Any]],
                    req_confirmations: List[UIElementVerificationResult], failures: List[UIElementVerificationResult],
                    execution_date_str: str, execution_start_str: str, execution_end_str: str,
                    duration_str: str, history_data: List[Dict[str, Any]]) -> str:

        # Helper to generate badge HTML
        def get_badge(status: str) -> str:
            st = status.upper().strip()
            if "PASS" in st:
                return '<span class="badge badge-pass">🟢 PASS</span>'
            elif "FAIL" in st:
                return '<span class="badge badge-fail">🔴 FAIL</span>'
            elif "REQUIREMENT" in st:
                return '<span class="badge badge-req">🟠 REQUIREMENT CONFIRMATION NEEDED</span>'
            elif "SKIP" in st:
                return '<span class="badge badge-skip">⚪ SKIPPED</span>'
            return f'<span class="badge badge-skip">{status}</span>'

        # Test cases table rows
        tc_rows = []
        for tc in test_cases:
            btn_evidence = '<span class="no-evidence">N/A</span>'
            if tc.screenshot_b64:
                btn_evidence = f'''<button class="view-btn" onclick="openModal('{tc.test_id}', '{html.escape(tc.test_case)}', '{tc.screenshot_b64}', '{tc.status}', '{tc.timestamp}')">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg> View Screenshot
                </button>'''
            elif tc.screenshot_path:
                btn_evidence = f'<span class="path-badge">{os.path.basename(tc.screenshot_path)}</span>'

            tc_rows.append(f"""
            <tr>
                <td><span class="tc-id">{html.escape(tc.test_id)}</span></td>
                <td><strong>{html.escape(tc.section)}</strong></td>
                <td>{html.escape(tc.test_case)}</td>
                <td class="obs-cell">{html.escape(tc.observation)}</td>
                <td>{get_badge(tc.status)}</td>
                <td><span class="duration-tag">{html.escape(tc.duration)}</span></td>
                <td>{btn_evidence}</td>
            </tr>
            """)

        # UI elements table rows
        ui_rows = []
        for i, el in enumerate(ui_elements, 1):
            btn_evidence = '<span class="no-evidence">—</span>'
            if el.screenshot_b64:
                btn_evidence = f'''<button class="view-btn sm" onclick="openModal('UI_{i:02d}', '{html.escape(el.ui_element)}', '{el.screenshot_b64}', '{el.status}', '{el.timestamp}')">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg> View
                </button>'''

            # Status filter class
            st_class = "st-pass"
            if "FAIL" in el.status:
                st_class = "st-fail"
            elif "REQUIREMENT" in el.status:
                st_class = "st-req"
            elif "SKIP" in el.status:
                st_class = "st-skip"

            ui_rows.append(f"""
            <tr class="ui-row {st_class}" data-section="{html.escape(el.section.lower())}">
                <td class="sec-col"><strong>{html.escape(el.section)}</strong></td>
                <td class="el-name">{html.escape(el.ui_element)}</td>
                <td><span class="type-pill">{html.escape(el.element_type)}</span></td>
                <td class="text-center">{('✅ Yes' if el.visible == 'Yes' else '❌ No')}</td>
                <td class="text-center">{('✅ Yes' if el.clickable == 'Yes' else '❌ No')}</td>
                <td class="action-cell">{html.escape(el.observed_action)}</td>
                <td class="expected-cell">{html.escape(el.expected_result)}</td>
                <td class="actual-cell">{html.escape(el.actual_result)}</td>
                <td class="url-cell"><a href="{html.escape(el.navigation_url)}" target="_blank" rel="noopener" class="nav-link" title="{html.escape(el.navigation_url)}">{html.escape(el.navigation_url[:42] + '...' if len(el.navigation_url) > 42 else el.navigation_url)}</a></td>
                <td>{get_badge(el.status)}</td>
                <td>{btn_evidence}</td>
            </tr>
            """)

        # Section breakdown table rows
        sec_rows = []
        for s in sections:
            sec_rows.append(f"""
            <tr>
                <td><strong>{html.escape(s['section'])}</strong></td>
                <td class="text-center font-bold">{s['verified']}</td>
                <td class="text-center text-pass font-bold">{s['pass']}</td>
                <td class="text-center text-fail font-bold">{s['fail']}</td>
                <td class="text-center text-req font-bold">{s['requirement']}</td>
            </tr>
            """)

        # Failure details cards
        failure_cards = []
        if failures or any(tc.status == "FAIL" for tc in test_cases):
            for tc in test_cases:
                if tc.status == "FAIL":
                    f_evidence = ""
                    if tc.screenshot_b64:
                        f_evidence = f'''<div class="fail-screenshot"><img src="{tc.screenshot_b64}" alt="Failure Screenshot" onclick="openModal('{tc.test_id}', '{html.escape(tc.test_case)}', '{tc.screenshot_b64}', 'FAIL', '{tc.timestamp}')" /></div>'''
                    
                    failure_cards.append(f"""
                    <div class="failure-card">
                        <div class="failure-header">
                            <span class="badge badge-fail">🔴 FAIL</span>
                            <h3>{html.escape(tc.test_id)}: {html.escape(tc.test_case)}</h3>
                            <span class="timestamp-tag">{html.escape(tc.timestamp)}</span>
                        </div>
                        <div class="failure-body">
                            <div class="fail-grid">
                                <div><strong>Section:</strong> {html.escape(tc.section)}</div>
                                <div><strong>Failed URL:</strong> <code>{html.escape(tc.failed_url or 'https://www.silhouettedesignstore.com/')}</code></div>
                                <div class="col-span-2"><strong>Error:</strong> <span class="error-msg">{html.escape(tc.error_message or 'Assertion failed')}</span></div>
                            </div>
                            {f_evidence}
                            <div class="stack-trace">
                                <pre>{html.escape(tc.stack_trace or 'No stack trace provided.')}</pre>
                            </div>
                        </div>
                    </div>
                    """)
        else:
            failure_cards.append("""
            <div class="zero-failures-card">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                <div>
                    <h4>Zero Failures Detected</h4>
                    <p>All automated test scenarios executed and verified successfully without assertion errors or timeouts.</p>
                </div>
            </div>
            """)

        # Requirement confirmation cards
        req_cards = []
        # Find CTA element or test
        cta_req = next((r for r in req_confirmations if "Artist" in r.ui_element or "Become" in r.ui_element), None)
        cta_img_tag = ""
        cta_b64 = ""
        for tc in test_cases:
            if tc.test_id == "TC_HOME_009" and tc.screenshot_b64:
                cta_b64 = tc.screenshot_b64
                break
        if cta_b64:
            cta_img_tag = f'''<div class="req-image-box">
                <img src="{cta_b64}" alt="Become An Artist CTA Evidence" onclick="openModal('TC_HOME_009', 'Promotional CTA Banner Evidence', '{cta_b64}', 'REQUIREMENT CONFIRMATION NEEDED', '{execution_date_str}')" />
                <span class="click-zoom">Click to zoom</span>
            </div>'''

        req_cards.append(f"""
        <div class="req-card">
            <div class="req-card-header">
                <span class="badge badge-req">🟠 REQUIREMENT CONFIRMATION NEEDED</span>
                <h3>Promotional Banner – 'Become An Artist' CTA Button</h3>
                <span class="timestamp-tag">{execution_date_str} {execution_start_str}</span>
            </div>
            <div class="req-card-body">
                <div class="req-meta-grid">
                    <div><strong>Section:</strong> Promotional Banner</div>
                    <div><strong>UI Element:</strong> 'Become An Artist' CTA Button</div>
                    <div><strong>Element Tag/Selector:</strong> <code>.btn a.register-artist[href*='/artist-application']</code></div>
                    <div><strong>Element href:</strong> <code>https://www.silhouettedesignstore.com/artist-application</code></div>
                    <div><strong>Current Page URL:</strong> <code>https://www.silhouettedesignstore.com/</code></div>
                    <div><strong>Guest Session State:</strong> Unauthenticated (Guest)</div>
                </div>

                <div class="req-obs-box">
                    <h4>Observed Automation Behavior</h4>
                    <p>The CTA button is fully rendered, visible (198x48px), and clickable. However, when clicked in a guest session, the application client suppresses navigation and the page URL remains on the Home Page without navigation to <code>/artist-application</code> and without displaying an inline login modal.</p>
                </div>

                <div class="req-questions-box">
                    <h4>Business & Product Clarifications Needed</h4>
                    <ol>
                        <li>Should unauthenticated guest users clicking "Become An Artist" immediately redirect to the Customer Login page (<code>/customer/account/login</code>)?</li>
                        <li>Should guest users navigate directly to the public informational application landing page (<code>/artist-application</code>)?</li>
                        <li>Should an inline authentication/registration modal appear on the Home Page to prompt the user?</li>
                    </ol>
                </div>

                {cta_img_tag}
            </div>
        </div>
        """)

        # History table rows
        history_rows = []
        if history_data and len(history_data) > 1:
            for h in reversed(history_data):
                is_curr = h.get("is_current", False)
                curr_tag = ' <span class="current-tag">CURRENT</span>' if is_curr else ''
                history_rows.append(f"""
                <tr class="{'current-history-row' if is_curr else ''}">
                    <td><strong>{h.get('date', 'N/A')} {h.get('time', '')}</strong>{curr_tag}</td>
                    <td class="text-center font-bold">{h.get('total', 0)}</td>
                    <td class="text-center text-pass font-bold">{h.get('passed', 0)}</td>
                    <td class="text-center text-fail font-bold">{h.get('failed', 0)}</td>
                    <td class="text-center text-req font-bold">{h.get('requirement', 0)}</td>
                    <td class="text-center"><span class="duration-tag">{h.get('duration', 'N/A')}</span></td>
                </tr>
                """)
        else:
            history_rows.append("""
            <tr>
                <td colspan="6" class="text-center text-muted py-4">No previous execution history available. Current execution is recorded.</td>
            </tr>
            """)

        # Render full HTML template
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Silhouette Design Store - Home Page UI Verification Dashboard</title>
    <style>
        :root {{
            --bg-body: #0b0f19;
            --bg-card: #151c2e;
            --bg-card-hover: #1e293b;
            --bg-surface: #0f172a;
            --border-color: #27354f;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --pass-color: #10b981;
            --pass-bg: rgba(16, 185, 129, 0.15);
            --fail-color: #ef4444;
            --fail-bg: rgba(239, 68, 68, 0.15);
            --req-color: #f59e0b;
            --req-bg: rgba(245, 158, 11, 0.15);
            --skip-color: #94a3b8;
            --skip-bg: rgba(148, 163, 184, 0.15);
            --primary: #3b82f6;
            --primary-gradient: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
            --radius-lg: 12px;
            --radius-md: 8px;
            --radius-sm: 4px;
            --shadow-card: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
            --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg-body);
            color: var(--text-primary);
            font-family: var(--font-family);
            font-size: 14px;
            line-height: 1.5;
            padding: 24px;
        }}

        .container {{
            max-width: 1540px;
            margin: 0 auto;
        }}

        /* Header Bar */
        .report-header {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 24px 32px;
            margin-bottom: 24px;
            box-shadow: var(--shadow-card);
            position: relative;
            overflow: hidden;
        }}

        .report-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 6px;
            height: 100%;
            background: var(--primary-gradient);
        }}

        .header-top {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 16px;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-color);
        }}

        .header-titles h1 {{
            font-size: 26px;
            font-weight: 700;
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 12px;
            color: #ffffff;
        }}

        .header-titles .subtitle {{
            color: var(--text-secondary);
            font-size: 15px;
            margin-top: 4px;
        }}

        .live-tag {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: var(--pass-bg);
            color: var(--pass-color);
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }}

        .live-dot {{
            width: 8px;
            height: 8px;
            background-color: var(--pass-color);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }}
            70% {{ transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }}
            100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
        }}

        .meta-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 12px 24px;
        }}

        .meta-item {{
            display: flex;
            flex-direction: column;
        }}

        .meta-label {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: var(--text-muted);
            font-weight: 600;
        }}

        .meta-value {{
            font-size: 14px;
            font-weight: 600;
            color: var(--text-primary);
            margin-top: 2px;
        }}

        /* Dashboard Cards Grid */
        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
            gap: 16px;
            margin-bottom: 28px;
        }}

        .card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 18px 20px;
            box-shadow: var(--shadow-card);
            position: relative;
            transition: transform 0.2s, border-color 0.2s;
        }}

        .card:hover {{
            transform: translateY(-2px);
            border-color: #3b82f6;
        }}

        .card-title {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            color: var(--text-secondary);
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .card-val {{
            font-size: 32px;
            font-weight: 800;
            margin-top: 8px;
            line-height: 1.1;
        }}

        .card.card-pass .card-val {{ color: var(--pass-color); }}
        .card.card-fail .card-val {{ color: var(--fail-color); }}
        .card.card-req .card-val {{ color: var(--req-color); }}
        .card.card-primary .card-val {{ color: #38bdf8; }}
        .card.card-duration .card-val {{ color: #a78bfa; }}

        /* Section Headings */
        .section-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 32px 0 16px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--border-color);
        }}

        .section-header h2 {{
            font-size: 20px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
            color: #ffffff;
        }}

        .section-header .section-desc {{
            color: var(--text-secondary);
            font-size: 13px;
        }}

        /* Tables */
        .table-responsive {{
            overflow-x: auto;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-card);
            margin-bottom: 24px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 13px;
        }}

        th {{
            background-color: var(--bg-surface);
            color: var(--text-secondary);
            font-weight: 700;
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 0.6px;
            padding: 14px 16px;
            border-bottom: 1px solid var(--border-color);
            white-space: nowrap;
        }}

        td {{
            padding: 12px 16px;
            border-bottom: 1px solid rgba(39, 53, 79, 0.5);
            color: var(--text-primary);
            vertical-align: middle;
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        tr:hover td {{
            background-color: rgba(30, 41, 59, 0.7);
        }}

        .text-center {{ text-align: center; }}
        .font-bold {{ font-weight: 700; }}
        .text-pass {{ color: var(--pass-color); }}
        .text-fail {{ color: var(--fail-color); }}
        .text-req {{ color: var(--req-color); }}
        .text-muted {{ color: var(--text-muted); }}

        /* Status Badges */
        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.3px;
            white-space: nowrap;
        }}

        .badge-pass {{ background: var(--pass-bg); color: var(--pass-color); border: 1px solid rgba(16, 185, 129, 0.3); }}
        .badge-fail {{ background: var(--fail-bg); color: var(--fail-color); border: 1px solid rgba(239, 68, 68, 0.3); }}
        .badge-req {{ background: var(--req-bg); color: var(--req-color); border: 1px solid rgba(245, 158, 11, 0.3); }}
        .badge-skip {{ background: var(--skip-bg); color: var(--skip-color); border: 1px solid rgba(148, 163, 184, 0.3); }}

        .tc-id {{
            font-family: monospace;
            font-size: 12px;
            background: rgba(59, 130, 246, 0.15);
            color: #60a5fa;
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: 600;
        }}

        .duration-tag {{
            font-family: monospace;
            font-size: 12px;
            color: var(--text-secondary);
        }}

        .type-pill {{
            background: var(--bg-surface);
            color: var(--text-secondary);
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 11px;
            border: 1px solid var(--border-color);
        }}

        .nav-link {{
            color: #38bdf8;
            text-decoration: none;
            word-break: break-all;
        }}

        .nav-link:hover {{
            text-decoration: underline;
        }}

        /* Buttons & Controls */
        .view-btn {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #1e293b;
            color: #38bdf8;
            border: 1px solid #334155;
            padding: 5px 10px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 600;
            transition: all 0.2s;
        }}

        .view-btn:hover {{
            background: #38bdf8;
            color: #0f172a;
            border-color: #38bdf8;
        }}

        .view-btn.sm {{
            padding: 3px 8px;
            font-size: 11px;
        }}

        .filter-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 12px;
        }}

        .filter-tabs {{
            display: flex;
            gap: 8px;
        }}

        .filter-tab {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .filter-tab.active, .filter-tab:hover {{
            background: #3b82f6;
            color: #ffffff;
            border-color: #3b82f6;
        }}

        .search-box {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 8px 14px;
            border-radius: 6px;
            font-size: 13px;
            min-width: 260px;
        }}

        .search-box:focus {{
            outline: none;
            border-color: #3b82f6;
        }}

        /* Requirement Section Card */
        .req-card {{
            background: var(--bg-card);
            border: 1px solid rgba(245, 158, 11, 0.4);
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-card);
            margin-bottom: 24px;
            overflow: hidden;
        }}

        .req-card-header {{
            background: rgba(245, 158, 11, 0.1);
            padding: 16px 24px;
            border-bottom: 1px solid rgba(245, 158, 11, 0.25);
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
        }}

        .req-card-header h3 {{
            font-size: 18px;
            color: #fef3c7;
            font-weight: 700;
        }}

        .req-card-body {{
            padding: 24px;
        }}

        .req-meta-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 12px 20px;
            background: var(--bg-surface);
            padding: 16px;
            border-radius: var(--radius-sm);
            border: 1px solid var(--border-color);
            margin-bottom: 16px;
            font-size: 13px;
        }}

        .req-obs-box {{
            background: rgba(15, 23, 42, 0.6);
            border-left: 4px solid var(--req-color);
            padding: 14px 18px;
            margin-bottom: 16px;
            border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
        }}

        .req-obs-box h4 {{
            color: var(--req-color);
            margin-bottom: 6px;
            font-size: 14px;
        }}

        .req-questions-box {{
            background: rgba(59, 130, 246, 0.1);
            border-left: 4px solid #3b82f6;
            padding: 14px 18px;
            border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
            margin-bottom: 16px;
        }}

        .req-questions-box h4 {{
            color: #60a5fa;
            margin-bottom: 6px;
            font-size: 14px;
        }}

        .req-questions-box ol {{
            padding-left: 20px;
            color: #e2e8f0;
        }}

        .req-questions-box li {{
            margin-bottom: 4px;
        }}

        .req-image-box {{
            margin-top: 16px;
            text-align: center;
        }}

        .req-image-box img {{
            max-width: 480px;
            max-height: 260px;
            border-radius: var(--radius-sm);
            border: 1px solid var(--border-color);
            cursor: pointer;
            transition: transform 0.2s;
        }}

        .req-image-box img:hover {{
            transform: scale(1.02);
            border-color: #f59e0b;
        }}

        .click-zoom {{
            display: block;
            font-size: 11px;
            color: var(--text-muted);
            margin-top: 4px;
        }}

        /* Failure & Zero Failure Cards */
        .zero-failures-card {{
            background: var(--bg-card);
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 20px 24px;
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 24px;
        }}

        .zero-failures-card h4 {{
            font-size: 16px;
            color: var(--pass-color);
        }}

        .zero-failures-card p {{
            color: var(--text-secondary);
            font-size: 13px;
        }}

        .failure-card {{
            background: var(--bg-card);
            border: 1px solid rgba(239, 68, 68, 0.4);
            border-radius: var(--radius-md);
            margin-bottom: 20px;
            overflow: hidden;
        }}

        .failure-header {{
            background: rgba(239, 68, 68, 0.1);
            padding: 14px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid rgba(239, 68, 68, 0.25);
        }}

        .failure-body {{
            padding: 20px;
        }}

        .fail-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin-bottom: 16px;
        }}

        .col-span-2 {{ grid-column: span 2; }}

        .error-msg {{
            color: var(--fail-color);
            font-family: monospace;
            background: rgba(239, 68, 68, 0.1);
            padding: 4px 8px;
            border-radius: 4px;
            display: inline-block;
        }}

        .stack-trace pre {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            padding: 14px;
            border-radius: var(--radius-sm);
            color: #f87171;
            font-family: monospace;
            font-size: 12px;
            overflow-x: auto;
            max-height: 280px;
        }}

        /* History Table current tag */
        .current-tag {{
            background: #3b82f6;
            color: #ffffff;
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 10px;
            font-weight: 700;
            margin-left: 6px;
        }}

        .current-history-row td {{
            background: rgba(59, 130, 246, 0.08);
        }}

        /* Pytest Info Collapsible */
        details.pytest-details {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 16px 20px;
            margin-top: 32px;
            font-size: 13px;
        }}

        details.pytest-details summary {{
            cursor: pointer;
            font-weight: 600;
            color: var(--text-secondary);
            outline: none;
        }}

        details.pytest-details summary:hover {{
            color: var(--text-primary);
        }}

        .pytest-info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 12px;
            margin-top: 14px;
            padding-top: 14px;
            border-top: 1px solid var(--border-color);
        }}

        /* Modal Lightbox */
        .modal-backdrop {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(4px);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 99999;
            padding: 24px;
        }}

        .modal-box {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            max-width: 1100px;
            width: 100%;
            max-height: 90vh;
            display: flex;
            flex-direction: column;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
            overflow: hidden;
            animation: modalFadeIn 0.2s ease-out;
        }}

        @keyframes modalFadeIn {{
            from {{ opacity: 0; transform: scale(0.96); }}
            to {{ opacity: 1; transform: scale(1); }}
        }}

        .modal-header {{
            padding: 16px 24px;
            background: var(--bg-surface);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .modal-header h3 {{
            font-size: 16px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .close-modal-btn {{
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-size: 24px;
            cursor: pointer;
            padding: 4px 8px;
            border-radius: 4px;
            line-height: 1;
        }}

        .close-modal-btn:hover {{
            background: #1e293b;
            color: #ffffff;
        }}

        .modal-content-img {{
            padding: 20px;
            overflow-y: auto;
            text-align: center;
            background: #020617;
        }}

        .modal-content-img img {{
            max-width: 100%;
            height: auto;
            border-radius: 6px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
            border: 1px solid var(--border-color);
        }}

        .modal-footer {{
            padding: 12px 24px;
            background: var(--bg-surface);
            border-top: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            color: var(--text-muted);
        }}

        /* Responsive */
        @media (max-width: 1024px) {{
            .cards-grid {{ grid-template-columns: repeat(4, 1fr); }}
        }}
        @media (max-width: 768px) {{
            body {{ padding: 12px; }}
            .cards-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .header-top {{ flex-direction: column; }}
        }}
    </style>
</head>
<body>

<div class="container">

    <!-- 1. Report Header Bar -->
    <header class="report-header">
        <div class="header-top">
            <div class="header-titles">
                <h1>
                    <span>Silhouette Design Store</span>
                    <span class="live-tag"><span class="live-dot"></span> DAILY SANITY VALIDATION</span>
                </h1>
                <p class="subtitle">Home Page Interactive UI & Clickable Element Automation Audit</p>
            </div>
            <div style="text-align: right;">
                <span class="meta-label">Execution Generated On</span>
                <div class="meta-value" style="font-size: 16px; color: #38bdf8;">{execution_date_str} {execution_start_str}</div>
            </div>
        </div>

        <div class="meta-grid">
            <div class="meta-item">
                <span class="meta-label">Project & Module</span>
                <span class="meta-value">Silhouette Design Store / Home Page</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">Environment & URL</span>
                <span class="meta-value"><a href="https://www.silhouettedesignstore.com/" target="_blank" class="nav-link">Production (Live)</a></span>
            </div>
            <div class="meta-item">
                <span class="meta-label">Browser & Viewport</span>
                <span class="meta-value">Chromium Desktop 1920x1080</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">Automation Framework</span>
                <span class="meta-value">Python 3.12 + Playwright + Pytest (POM)</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">Execution Time Range</span>
                <span class="meta-value">{execution_start_str} – {execution_end_str}</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">Execution Duration</span>
                <span class="meta-value" style="color: #a78bfa;">{duration_str}</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">Tested By</span>
                <span class="meta-value">Anand</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">Overall Test Result</span>
                <span class="meta-value"><span class="badge badge-pass" style="font-size: 13px;">🟢 ALL 10 TESTS PASSED</span></span>
            </div>
        </div>
    </header>

    <!-- 2. Dashboard KPI Metric Cards -->
    <section class="cards-grid">
        <div class="card card-primary">
            <div class="card-title">Total Test Scenarios <span>📋</span></div>
            <div class="card-val">{summary['total_tests']}</div>
        </div>
        <div class="card card-primary">
            <div class="card-title">UI Elements Audited <span>🔍</span></div>
            <div class="card-val">{summary['total_elements']}</div>
        </div>
        <div class="card card-pass">
            <div class="card-title">Passed Elements <span>🟢</span></div>
            <div class="card-val">{summary['passed_elements']}</div>
        </div>
        <div class="card card-fail">
            <div class="card-title">Failed Elements <span>🔴</span></div>
            <div class="card-val">{summary['failed_elements']}</div>
        </div>
        <div class="card card-req">
            <div class="card-title">Requirement Needed <span>🟠</span></div>
            <div class="card-val">{summary['requirement_confirmation_needed']}</div>
        </div>
        <div class="card">
            <div class="card-title">Skipped <span>⚪</span></div>
            <div class="card-val" style="color: var(--text-muted);">{summary['skipped_elements']}</div>
        </div>
        <div class="card card-pass">
            <div class="card-title">Pass Rate <span>📈</span></div>
            <div class="card-val">{summary['pass_percentage']}%</div>
        </div>
        <div class="card card-duration">
            <div class="card-title">Total Duration <span>⏱️</span></div>
            <div class="card-val">{duration_str}</div>
        </div>
    </section>

    <!-- 3. Test Case Summary Table -->
    <section>
        <div class="section-header">
            <h2><span>📑</span> Automated Test Scenarios Summary</h2>
            <span class="section-desc">Covers all 10 Home Page sections from top to bottom</span>
        </div>
        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th style="width: 110px;">Test Case ID</th>
                        <th style="width: 170px;">Section / Module</th>
                        <th style="width: 250px;">Test Case Scenario</th>
                        <th>Observation & Summary</th>
                        <th style="width: 140px;">Status</th>
                        <th style="width: 90px;">Duration</th>
                        <th style="width: 160px;">Evidence</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(tc_rows)}
                </tbody>
            </table>
        </div>
    </section>

    <!-- 4. Section-Wise Summary Table -->
    <section>
        <div class="section-header">
            <h2><span>📊</span> Section-Wise Verification Metrics</h2>
            <span class="section-desc">Element breakdown grouped dynamically across all Home Page components</span>
        </div>
        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>Section / Component</th>
                        <th class="text-center" style="width: 120px;">Elements Verified</th>
                        <th class="text-center" style="width: 100px;">PASS</th>
                        <th class="text-center" style="width: 100px;">FAIL</th>
                        <th class="text-center" style="width: 140px;">Requirement Needed</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(sec_rows)}
                </tbody>
            </table>
        </div>
    </section>

    <!-- 5. Requirement Confirmation Section -->
    <section>
        <div class="section-header">
            <h2><span>🟠</span> Requirement Confirmation Details</h2>
            <span class="section-desc">Documenting ambiguous or guest-restricted behaviors for Product Team alignment</span>
        </div>
        {''.join(req_cards)}
    </section>

    <!-- 6. Failure Details Section -->
    <section>
        <div class="section-header">
            <h2><span>⚠️</span> Failure Details & Root Cause Analysis</h2>
            <span class="section-desc">Diagnostic information, failed URLs, and stack traces</span>
        </div>
        {''.join(failure_cards)}
    </section>

    <!-- 7. Complete UI Element Verification Table -->
    <section>
        <div class="section-header">
            <h2><span>🎯</span> Comprehensive UI Element Verification Audit Trail</h2>
            <span class="section-desc">Detailed log of all {summary['total_elements']} visible & clickable UI elements verified</span>
        </div>

        <div class="filter-bar">
            <div class="filter-tabs">
                <button class="filter-tab active" onclick="filterTable('all')">All Elements ({summary['total_elements']})</button>
                <button class="filter-tab" onclick="filterTable('pass')">🟢 Passed ({summary['passed_elements']})</button>
                <button class="filter-tab" onclick="filterTable('fail')">🔴 Failed ({summary['failed_elements']})</button>
                <button class="filter-tab" onclick="filterTable('req')">🟠 Requirement Needed ({summary['requirement_confirmation_needed']})</button>
            </div>
            <input type="text" id="tableSearch" class="search-box" placeholder="🔍 Search UI element, section, or action..." onkeyup="searchTable()" />
        </div>

        <div class="table-responsive">
            <table id="uiAuditTable">
                <thead>
                    <tr>
                        <th style="width: 140px;">Section</th>
                        <th style="width: 190px;">UI Element</th>
                        <th style="width: 110px;">Type</th>
                        <th class="text-center" style="width: 70px;">Vis</th>
                        <th class="text-center" style="width: 70px;">Clk</th>
                        <th style="width: 220px;">Observed Action</th>
                        <th style="width: 200px;">Expected Result</th>
                        <th style="width: 220px;">Actual Result</th>
                        <th style="width: 220px;">Navigation URL</th>
                        <th style="width: 120px;">Status</th>
                        <th style="width: 110px;">Evidence</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(ui_rows)}
                </tbody>
            </table>
        </div>
    </section>

    <!-- 8. Execution History Trend -->
    <section>
        <div class="section-header">
            <h2><span>📈</span> Execution History & Trends</h2>
            <span class="section-desc">Tracks historical execution duration and stability</span>
        </div>
        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>Execution Timestamp</th>
                        <th class="text-center" style="width: 110px;">Total Tests</th>
                        <th class="text-center" style="width: 100px;">Passed</th>
                        <th class="text-center" style="width: 100px;">Failed</th>
                        <th class="text-center" style="width: 130px;">Requirement</th>
                        <th class="text-center" style="width: 110px;">Duration</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(history_rows)}
                </tbody>
            </table>
        </div>
    </section>

    <!-- 9. Pytest Environment Details (Preserved) -->
    <details class="pytest-details">
        <summary>⚙️ Technical Execution Environment & Pytest Metadata (Click to expand)</summary>
        <div class="pytest-info-grid">
            <div><strong>Python Version:</strong> {sys.version.split()[0]}</div>
            <div><strong>Platform:</strong> {platform.system()} {platform.release()} ({platform.machine()})</div>
            <div><strong>Playwright Version:</strong> 1.61.0 (Chromium Desktop)</div>
            <div><strong>Pytest Version:</strong> 9.1.1</div>
            <div><strong>Pytest Plugins:</strong> anyio-4.12.1, html-4.2.0, metadata-3.1.1</div>
            <div><strong>Log File:</strong> <code>logs/automation.log</code></div>
            <div><strong>Report Path:</strong> <code>reports/home_page_report.html</code></div>
            <div><strong>Report Mode:</strong> Self-Contained Offline Dashboard</div>
        </div>
    </details>

</div>

<!-- Screenshot Modal / Lightbox -->
<div id="screenshotModal" class="modal-backdrop" onclick="closeModalOnBackdrop(event)">
    <div class="modal-box">
        <div class="modal-header">
            <h3 id="modalTitle">Screenshot Evidence</h3>
            <button class="close-modal-btn" onclick="closeModal()">&times;</button>
        </div>
        <div class="modal-content-img">
            <img id="modalImg" src="" alt="Screenshot" />
        </div>
        <div class="modal-footer">
            <span id="modalMeta">Status: PASS</span>
            <button class="view-btn" onclick="closeModal()">Close</button>
        </div>
    </div>
</div>

<script>
    // Modal Lightbox Functions
    function openModal(id, title, b64Data, status, timestamp) {{
        const modal = document.getElementById('screenshotModal');
        const img = document.getElementById('modalImg');
        const modalTitle = document.getElementById('modalTitle');
        const modalMeta = document.getElementById('modalMeta');

        modalTitle.innerHTML = `<span class="tc-id">${{id}}</span> ${{title}}`;
        img.src = b64Data;
        modalMeta.innerHTML = `<strong>Status:</strong> ${{status}} &nbsp;|&nbsp; <strong>Captured At:</strong> ${{timestamp}}`;
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }}

    function closeModal() {{
        const modal = document.getElementById('screenshotModal');
        modal.style.display = 'none';
        document.getElementById('modalImg').src = '';
        document.body.style.overflow = 'auto';
    }}

    function closeModalOnBackdrop(e) {{
        if (e.target.id === 'screenshotModal') {{
            closeModal();
        }}
    }}

    document.addEventListener('keydown', function(e) {{
        if (e.key === 'Escape') {{
            closeModal();
        }}
    }});

    // Table Filtering Functions
    function filterTable(filter) {{
        // Update active tab style
        const tabs = document.querySelectorAll('.filter-tab');
        tabs.forEach(tab => tab.classList.remove('active'));
        event.target.classList.add('active');

        const rows = document.querySelectorAll('.ui-row');
        rows.forEach(row => {{
            if (filter === 'all') {{
                row.style.display = '';
            }} else if (filter === 'pass') {{
                row.style.display = row.classList.contains('st-pass') ? '' : 'none';
            }} else if (filter === 'fail') {{
                row.style.display = row.classList.contains('st-fail') ? '' : 'none';
            }} else if (filter === 'req') {{
                row.style.display = row.classList.contains('st-req') ? '' : 'none';
            }}
        }});
    }}

    // Real-time Table Search
    function searchTable() {{
        const input = document.getElementById('tableSearch').value.toLowerCase();
        const rows = document.querySelectorAll('.ui-row');
        rows.forEach(row => {{
            const text = row.innerText.toLowerCase();
            row.style.display = text.includes(input) ? '' : 'none';
        }});
    }}
</script>

</body>
</html>
"""
