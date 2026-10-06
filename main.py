from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Jira Ticket Validator")


REQUIRED_SECTIONS = {
    "problem_as_is": [
        "Problem (As-is)",
        "Problem:",
        "As-is:"
    ],
    "expected_to_be": [
        "Expected (To-be)",
        "Expected:",
        "To-be:"
    ],
    "acceptance_criteria": [
        "Acceptance criteria:",
        "Acceptance criteria"
    ],
    "screen_module": [
        "Screen / module:",
        "Screen / Module:",
        "Screen:"
    ],
    "environment": [
        "Environment:"
    ],
    "tenant_saas_id": [
        "Tenant / SaaS ID:",
        "Tenant:",
        "SaaS ID:"
    ],
    "company_branch": [
        "Company & branch:",
        "Company:",
        "Branch:"
    ],
    "test_data": [
        "Test data:",
        "Test Data:"
    ],
    "steps_to_verify": [
        "Steps to verify:",
        "Steps to Verify:"
    ],
    "country_locale_rules": [
        "Country / locale rules:",
        "Country / Locale Rules:",
        "Country:"
    ],
}


class TicketRequest(BaseModel):
    description: str = ""


def section_exists(description: str, variations: list[str]) -> bool:
    description_lower = description.lower()

    for variation in variations:
        if variation.lower() in description_lower:
            return True

    return False


def validate_ticket(description: str):

    checks = {}

    for field, variations in REQUIRED_SECTIONS.items():
        checks[field] = section_exists(description, variations)

    passed = sum(checks.values())
    total = len(checks)

    missing = [
        field
        for field, passed_check in checks.items()
        if not passed_check
    ]

    return {
        "valid": passed == total,
        "passed": passed,
        "total": total,
        "checks": checks,
        "missing": missing,
        "message": (
            "Ticket can be created"
            if passed == total
            else f"Ticket rejected: {total - passed} requirement(s) missing"
        )
    }


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "jira-ticket-validator"
    }


@app.post("/validate")
def validate(request: TicketRequest):
    return validate_ticket(request.description)