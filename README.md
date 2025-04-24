# SEMrush API to DataFrame

This script fetches data from the SEMrush API for a specified report type and domain, then converts the response into a Pandas DataFrame.

## Features

*   Fetches data from SEMrush API based on report type and domain.
*   Parses the CSV-like response into a Pandas DataFrame.
*   Handles API key securely using environment variables (`.env` file).
*   Includes basic error handling and logging.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd SEMRush-API-to-a-DataFrame
    ```

2.  **Create a virtual environment (using uv):**
    ```bash
    # Install uv if you haven't already: https://docs.astral.sh/uv/
    uv venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3.  **Install dependencies (using uv):**
    ```bash
    uv pip sync requirements.txt
    ```

4.  **Configure API Key:**
    *   Copy the sample environment file: `cp env.sample .env`
    *   Edit the `.env` file and add your SEMrush API key:
        ```dotenv
        SEMRUSH_API_KEY="YOUR_ACTUAL_SEMRUSH_API_KEY"
        ```
    *   **Important:** The `.env` file is included in `.gitignore` to prevent accidentally committing your API key.

## Usage

Modify the `if __name__ == "__main__":` block in `main.py` to set your desired `report_type` and `domain`:

```python
if __name__ == "__main__":
    # --- Configuration ---
    # Find valid report types in the SEMrush API documentation.
    report_type = 'domain_rank'  # Example: Get domain ranking report
    domain = 'google.com'        # Example: Analyze google.com
    # -------------------

    df_result = fetch_semrush_data(report_type=report_type, domain=domain)

    if df_result is not None:
        print("\n--- SEMrush Data ---")
        print(df_result.head())
        # Optionally, save the DataFrame to a CSV file
        # output_filename = f"{domain}_{report_type}_report.csv"
        # try:
        #     df_result.to_csv(output_filename, index=False)
        #     print(f"\nReport saved to {output_filename}")
        # except Exception as e:
        #     print(f"\nError saving report to CSV: {e}")
    else:
        print("\nFailed to fetch or process data.")
        # Indicate failure
        exit(1)

```

Then, run the script:

```bash
uv run main.py
```

The script will print the first few rows of the resulting DataFrame to the console.

## Customization

*   **API Parameters:** Some SEMrush reports require additional parameters (e.g., `database`). You can add these to the `params` dictionary within the `fetch_semrush_data` function in `main.py`.
*   **Output:** Uncomment and modify the file saving logic in the `if __name__ == "__main__":` block to save the DataFrame to a CSV file.

## SEMrush API Documentation

Refer to the official [SEMrush API documentation](https://developer.semrush.com/api/basics/introduction/) for details on available reports, required parameters, and API usage limits.
