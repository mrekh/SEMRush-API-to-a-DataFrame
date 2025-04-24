"""The main script that converts your SEMRush API request to a DataFrame."""

import requests
import pandas as pd
import os
from dotenv import load_dotenv
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables from .env file
load_dotenv()


def fetch_semrush_data(
    report_type: str, domain: str, api_key: str | None = None
) -> pd.DataFrame | None:
    """Fetches data from the SEMrush API and returns it as a Pandas DataFrame.

    Args:
        report_type: The type of SEMrush report to request.
        domain: The domain name to investigate.
        api_key: SEMrush API key. If None, attempts to load from SEMRUSH_API_KEY environment variable.

    Returns:
        A Pandas DataFrame containing the report data, or None if an error occurs.
    """
    if api_key is None:
        api_key = os.getenv("SEMRUSH_API_KEY")

    if not api_key:
        logging.error("SEMRUSH_API_KEY not found in environment variables or provided.")
        return None

    if not report_type:
        logging.error("Report type cannot be empty.")
        return None

    if not domain:
        logging.error("Domain cannot be empty.")
        return None

    # Construct the API request URL
    # Note: export_escape=1 ensures special characters in the response are properly escaped.
    # Depending on the report_type, other parameters like 'database' might be required.
    # Refer to SEMrush API documentation for specific report requirements.
    base_url = "https://api.semrush.com/"
    params = {
        "type": report_type,
        "key": api_key,
        "domain": domain,
        "export_escape": 1,
        # Add other necessary parameters based on report_type here, e.g., 'database': 'us'
    }

    try:
        logging.info(f"Requesting report '{report_type}' for domain '{domain}'...")
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        logging.info("API request successful.")

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        # Check if the response text provides more detail (SEMrush often returns error messages in the body)
        if hasattr(e, "response") and e.response is not None:
            logging.error(f"SEMrush API Error Response: {e.response.text.strip()}")
        return None

    # Process the response text (assuming CSV-like format separated by semicolons)
    response_text = response.text.strip()
    if not response_text:
        logging.warning("Received empty response from API.")
        return pd.DataFrame()  # Return empty DataFrame for empty response

    lines = response_text.split("\n")

    if not lines or len(lines) < 1:
        logging.warning("Response format unexpected (no header line).")
        return pd.DataFrame()  # Return empty DataFrame

    # SEMrush CSV often has double quotes around fields and uses ';' as delimiter
    header = lines[0].strip().split(";")
    data_rows = []

    # Start from the second line (index 1) for data
    for line in lines[1:]:
        line = line.strip()
        if not line:  # Skip empty lines which might occur at the end
            continue
        # Simple parsing assuming fields are ";"-separated and potentially quoted
        # This might need refinement based on actual SEMrush output variations
        # It assumes quotes are only at the very beginning and end if present
        if line.startswith('"') and line.endswith('"'):
            line = line[1:-1]
        fields = line.split('";"')  # Split fields separated by '";"'
        data_rows.append(fields)

    if not data_rows:
        logging.warning("No data rows found after header.")
        # Return DataFrame with columns but no data
        return pd.DataFrame(columns=header)

    try:
        df = pd.DataFrame(data_rows, columns=header)
        logging.info(f"Successfully created DataFrame with shape {df.shape}")
        return df
    except ValueError as e:
        logging.error(f"Error creating DataFrame: {e}")
        logging.error(f"Header: {header}")
        logging.error(
            f"First data row (attempted): {data_rows[0] if data_rows else 'N/A'}"
        )
        return None


if __name__ == "__main__":
    # Example usage:
    # Ensure you have a .env file with SEMRUSH_API_KEY="YOUR_KEY"
    # Or pass the key directly: fetch_semrush_data(report_type='domain_rank', domain='example.com', api_key='YOUR_KEY')

    # You might want to get these from command-line arguments instead
    example_report_type = "domain_rank"  # Replace with a valid report type
    example_domain = "google.com"  # Replace with the domain you want to analyze

    df_result = fetch_semrush_data(
        report_type=example_report_type, domain=example_domain
    )

    if df_result is not None:
        print("\n--- SEMrush Data ---")
        print(df_result.head())
        # Example: Save to CSV
        # output_filename = f"{example_domain}_{example_report_type}_report.csv"
        # try:
        #     df_result.to_csv(output_filename, index=False)
        #     logging.info(f"Report saved to {output_filename}")
        # except Exception as e:
        #     logging.error(f"Failed to save report to CSV: {e}")
    else:
        print("\nFailed to fetch data.")
        sys.exit(1)  # Exit with error code if fetching failed
