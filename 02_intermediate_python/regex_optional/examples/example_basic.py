"""Working example of regular expressions."""

import re

EMAIL_PATTERN = re.compile(r'[\w.-]+@[\w.-]+')


def extract_emails(text: str) -> list[str]:
    """Extract email addresses from free text."""
    return EMAIL_PATTERN.findall(text)


def anonymize_emails(text: str) -> str:
    """Replace email addresses with a placeholder."""
    return EMAIL_PATTERN.sub('[hidden-email]', text)


def main() -> None:
    sample = 'Contact ada@example.com and lin@test.dev for details.'
    print(extract_emails(sample))
    print(anonymize_emails(sample))


if __name__ == '__main__':
    main()
