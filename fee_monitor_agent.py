import os
import pandas as pd
import logging
import traceback

# ==================== CONFIG ====================
EXCEL_FILE_PATH = os.path.expanduser("~/Downloads/winterseason2025Test.xlsx")
OUTPUT_FILE_PATH = os.path.expanduser("~/Downloads/CricketTeamFeesPendingReport.xlsx")
LOG_FILE = "fee_monitor.log"

# ==================== LOGGER ====================
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# ==================== FEE ANALYZER ====================
class FeeAnalyzer:
    def __init__(self, df):
        self.df = df

    def analyze(self):
        try:
            # Compute balance
            self.df["Balance"] = self.df["Total Fee"] - self.df["Paid Amount"]
            # Filter players with pending balance
            pending_df = self.df[self.df["Balance"] > 0]
            total_balance = pending_df["Balance"].sum()
            total_expense = self.df["Total Fee"].sum()
            logging.info("Fee analysis completed successfully.")
            return pending_df, total_balance, total_expense
        except Exception as e:
            logging.error("Error analyzing fee data: %s", str(e))
            raise

# ==================== MAIN PROCESS ====================
def main():
    logging.info("=== Fee Monitor Agent started ===")
    try:
        if not os.path.exists(EXCEL_FILE_PATH):
            logging.error("Excel file not found at %s", EXCEL_FILE_PATH)
            print(f"Excel file not found at {EXCEL_FILE_PATH}")
            return

        # Read Excel file
        df = pd.read_excel(EXCEL_FILE_PATH)
        logging.info("Excel file read successfully from %s", EXCEL_FILE_PATH)

        # Analyze fees
        analyzer = FeeAnalyzer(df)
        pending_df, total_balance, total_expense = analyzer.analyze()

        # Prepare summary row
        summary_df = pd.DataFrame({
            "Player Name": ["Total Balance / Expense"],
            "Total Fee": [total_expense],
            "Paid Amount": [total_expense - total_balance],
            "Balance": [total_balance]
        })

        # Concatenate pending players with summary row
        if not pending_df.empty:
            final_df = pd.concat([pending_df, summary_df], ignore_index=True)
        else:
            final_df = summary_df

        # Write output Excel
        final_df.to_excel(OUTPUT_FILE_PATH, index=False)
        logging.info("Pending report generated successfully at %s", OUTPUT_FILE_PATH)
        print(f"Pending report generated successfully: {OUTPUT_FILE_PATH}")

    except Exception as e:
        logging.error("Fatal Error: %s", traceback.format_exc())
        print("An error occurred. Check log for details.")

# ==================== RUN ====================
if __name__ == "__main__":
    main()
