import csv
import pandas as pd
from datetime import datetime

class ExportManager:
    @staticmethod
    def to_csv(applications, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"job_applications_{timestamp}.csv"
        
        df = pd.DataFrame(applications)
        df.to_csv(filename, index=False)
        return filename
    
    @staticmethod
    def to_excel(applications, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"job_applications_{timestamp}.xlsx"
        
        df = pd.DataFrame(applications)
        df.to_excel(filename, index=False)
        return filename