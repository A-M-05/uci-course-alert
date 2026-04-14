import requests
from bs4 import BeautifulSoup

WEBREG_URL = "https://www.reg.uci.edu/perl/WebSoc"

def fetch_course(term: str, course_code: str) -> dict | None:
    """
    Fetches course info from UCI WebSoc for a given term and course code.
    Returns a dict with availability info or None on failure.
    """
    params = {
        "YearTerm": term,
        "CourseCodes": course_code,
        "ShowFinals": "0",
        "ShowComments": "0",
        "Submit" : "Display Web Results",
        "Breadth" : "ANY",
        "Division" : "ANY",
        "ClassType" : "ALL",
        "FullCourses": "ANY",
        "CancelledCourses": "Exclude"
    }

    try:
        response = requests.post(WEBREG_URL, data=params, timeout=10)
        response.raise_for_status()
        return parse_html(response.text, course_code)
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch course {course_code}: {e}")
        return None


def parse_html(html: str, course_code: str) -> dict | None:
    """
    Parses WebSoc HTML and extracts enrollment status for the course code.
    """
    soup = BeautifulSoup(html, "html.parser")

    # WebSoc returns a table and finds the row matching the course code
    rows = soup.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) > 8 and course_code in row.get_text():
            return {
                "code": course_code,
                "enrolled": cells[11].get_text(strip=True),
                "status": cells[15].get_text(strip=True),
                "waitlist": cells[10].get_text(strip=True) if len(cells) > 9 else "N/A",
            }

    return None
