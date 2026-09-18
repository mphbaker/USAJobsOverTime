import requests
import time
import csv
from collections import defaultdict

# Fetch credentials securely from environment variables or fall back to prompts
API_KEY = os.getenv("USAJOBS_API_KEY", "YOUR_API_KEY_HERE")
EMAIL = os.getenv("USAJOBS_EMAIL", "your_email@example.com")HEADERS = {
    "Host": "data.usajobs.gov",
    "User-Agent": EMAIL,
    "Authorization-Key": API_KEY
}

def generate_date_chunks(start_year, start_month, num_months):
    """Generates 10-day date ranges for N months going backwards."""
    months = []
    curr_year, curr_month = start_year, start_month

    for _ in range(num_months):
        if curr_month in [1, 3, 5, 7, 8, 10, 12]:
            last_day = 31
        elif curr_month in [4, 6, 9, 11]:
            last_day = 30
        else:
            last_day = 29 if (curr_year % 4 == 0 and (curr_year % 100 != 0 or curr_year % 400 == 0)) else 28

        chunks = [
            (f"{curr_month:02d}-01-{curr_year}", f"{curr_month:02d}-10-{curr_year}"),
            (f"{curr_month:02d}-11-{curr_year}", f"{curr_month:02d}-20-{curr_year}"),
            (f"{curr_month:02d}-21-{curr_year}", f"{curr_month:02d}-{last_day:02d}-{curr_year}")
        ]

        months.append((f"{curr_year}-{curr_month:02d}", chunks))

        curr_month -= 1
        if curr_month == 0:
            curr_month = 12
            curr_year -= 1

    return list(reversed(months))

def fetch_data_with_retry(url, params):
    for attempt in range(4):
        try:
            res = requests.get(url, headers=HEADERS, params=params, timeout=15)
            if res.status_code == 200:
                return res.json()
            elif res.status_code == 204:
                return None
            elif res.status_code in [500, 502, 503, 504]:
                time.sleep(2 * (attempt + 1))
        except requests.RequestException:
            time.sleep(2 * (attempt + 1))
    return None

def is_open_to_public(job):
    """Checks hiringpaths array to see if 'The public' is listed."""
    hiring_paths = job.get("hiringpaths", [])
    if isinstance(hiring_paths, list):
        for path in hiring_paths:
            path_name = str(path.get("hiringPath", "")).lower()
            if "public" in path_name:
                return True
    return False

def get_job_category(job):
    """Extracts job series and title for job classification."""
    series = ""
    categories = job.get("jobcategories", [])
    if isinstance(categories, list) and len(categories) > 0:
        series = categories[0].get("series", "")
    
    title = job.get("positionTitle", "Unknown")
    return f"{title} (Series: {series})" if series else title

def process_timeframe(label_prefix, month_chunks, csv_writer):
    url = "https://data.usajobs.gov/api/historicjoa"

    for month_label, chunks in month_chunks:
        # Aggregation keys: (Agency, Job Title, Open To Public) -> Count
        stats = defaultdict(int)

        for start_date, end_date in chunks:
            continuation_token = None

            while True:
                params = {
                    "StartPositionOpenDate": start_date,
                    "EndPositionOpenDate": end_date
                }
                if continuation_token:
                    params["continuationtoken"] = continuation_token

                data = fetch_data_with_retry(url, params)
                if not data:
                    break

                jobs = data.get("data", [])
                for job in jobs:
                    agency = job.get("hiringAgencyName") or job.get("hiringDepartmentName") or "Unknown"
                    open_public = "Yes" if is_open_to_public(job) else "No"
                    job_cat = get_job_category(job)

                    stats[(agency, job_cat, open_public)] += 1

                continuation_token = data.get("paging", {}).get("metadata", {}).get("continuationToken")
                if not continuation_token:
                    break

                time.sleep(0.1)

        # Write results to CSV
        for (agency, job_cat, open_public), count in stats.items():
            csv_writer.writerow([label_prefix, month_label, agency, job_cat, open_public, count])

        print(f"Processed {label_prefix} - {month_label} ({len(stats)} distinct job categories)")

def main():
    output_file = "usajobs_18months_analysis.csv"
    
    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Period_Type", "Month", "Agency", "Job_Title_Series", "Open_To_Public", "Total_Listings"])

        # 1. Pre-Trump Baseline (April 2024 to Dec 2024 - 9 months)
        print("--- Fetching Pre-Trump Baseline Data (2024) ---")
        pre_trump_months = generate_date_chunks(2024, 12, 9)
        process_timeframe("Pre-Trump Baseline", pre_trump_months, writer)

        # 2. Main 18-Month Query (April 2025 to Sept 2026 - 18 months)
        print("\n--- Fetching 18-Month Historic Data (2025 - 2026) ---")
        post_trump_months = generate_date_chunks(2026, 9, 18)
        process_timeframe("Post-2025 Period", post_trump_months, writer)

    print(f"\nFinished! All data exported to {output_file}")

if __name__ == "__main__":
    main()
