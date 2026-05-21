from dataclasses import dataclass, field
from typing import Literal


@dataclass
class Issue:
    criterion: str          # e.g. "1.1.1"
    criterion_name: str     # e.g. "Non-text Content"
    level: Literal["A", "AA", "AAA"]
    severity: Literal["error", "warning"]
    title: str
    description: str
    fix: str
    snippet: str = ""

    def to_dict(self) -> dict:
        return {
            "criterion": self.criterion,
            "criterion_name": self.criterion_name,
            "level": self.level,
            "severity": self.severity,
            "title": self.title,
            "description": self.description,
            "fix": self.fix,
            "snippet": self.snippet,
        }


MANUAL_CHECKS = [
    {
        "criterion": "2.4.1",
        "criterion_name": "Bypass Blocks",
        "level": "A",
        "title": "Skip navigation / bypass mechanism",
        "description": (
            "There must be a way to skip repeated blocks (e.g. navigation) and reach "
            "the main content directly. Skip links are often JavaScript-rendered or "
            "visually hidden until focused, so presence cannot be verified from static "
            "HTML alone. Test by pressing Tab on page load — a skip link should appear "
            "as the first focusable element."
        ),
    },
    {
        "criterion": "1.4.3",
        "criterion_name": "Contrast (Minimum)",
        "level": "AA",
        "title": "Colour contrast",
        "description": (
            "Text must have a contrast ratio of at least 4.5:1 (3:1 for large text). "
            "This requires rendering the page with computed CSS values and cannot be "
            "reliably checked without a browser engine."
        ),
    },
    {
        "criterion": "2.1.2",
        "criterion_name": "No Keyboard Trap",
        "level": "A",
        "title": "Keyboard trap",
        "description": (
            "Ensure users can navigate away from all interactive components using "
            "only the keyboard. Requires manual interaction testing."
        ),
    },
    {
        "criterion": "2.4.3",
        "criterion_name": "Focus Order",
        "level": "A",
        "title": "Focus order is logical",
        "description": (
            "Tab order should follow a meaningful sequence. Requires visual "
            "assessment while tabbing through the page."
        ),
    },
    {
        "criterion": "1.2.2",
        "criterion_name": "Captions (Prerecorded)",
        "level": "A",
        "title": "Video/audio captions quality",
        "description": (
            "Captions must be accurate and synchronised. Presence of a <track> "
            "element can be detected automatically but caption quality cannot."
        ),
    },
    {
        "criterion": "1.4.13",
        "criterion_name": "Content on Hover or Focus",
        "level": "AA",
        "title": "Content on hover or focus",
        "description": (
            "Tooltips and other content that appears on hover/focus must be "
            "dismissible, hoverable, and persistent. Requires interaction testing."
        ),
    },
    {
        "criterion": "3.3.1",
        "criterion_name": "Error Identification",
        "level": "A",
        "title": "Form error identification",
        "description": (
            "When a form error occurs, the item in error must be identified and "
            "described. Requires form submission testing."
        ),
    },
    {
        "criterion": "1.3.2",
        "criterion_name": "Meaningful Sequence",
        "level": "A",
        "title": "Meaningful reading sequence",
        "description": (
            "Content order in the DOM should match the intended reading order. "
            "Requires human judgment about visual layout vs. DOM order."
        ),
    },
    {
        "criterion": "1.4.5",
        "criterion_name": "Images of Text",
        "level": "AA",
        "title": "Images of text",
        "description": (
            "Images that contain text (other than logos) should be replaced with "
            "real text. Images can be detected but whether they contain text cannot "
            "be determined without visual inspection or OCR."
        ),
    },
]
