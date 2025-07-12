from src.generate_data import generate_business_data
from src.eda import run_eda
from src.anomaly_detector import detect_anomalies_zscore, detect_anomalies_iforest
from src.pdf_report import generate_pdf_report

if __name__ == "__main__":
    generate_business_data()
    run_eda()
    detect_anomalies_zscore()
    detect_anomalies_iforest()
    generate_pdf_report()