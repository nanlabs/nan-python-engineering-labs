"""Exercise: Parametrize.

Goal:
Create `my_solution/email_tools.py`.

Requirements:
- `normalize_email(value)` trims whitespace and lowercases the input.
- `extract_domain(value)` returns the part after `@` and raises `ValueError` for invalid addresses.
- `is_company_email(value, company_domain="company.dev")` returns `True` only when the normalized domain matches.

Hint:
The tests use multiple cases through `@pytest.mark.parametrize`. Think about edge cases up front.
"""
