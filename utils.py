import pandas as pd
import fitz  # PyMuPDF

PASSING_GRADES = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', '通過']
FAILING_GRADES = ['D', 'E', '未通過']

def parse_pdf(file) -> pd.DataFrame:
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    
    lines = text.splitlines()
    data = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 3:
            try:
                credit = int(parts[-2])
                grade = parts[-1]
                course = " ".join(parts[:-2])
                data.append((course, credit, grade))
            except:
                continue

    df = pd.DataFrame(data, columns=["course", "credit", "gpa"])
    return df

def calculate_credits(df: pd.DataFrame):
    df["credit"] = pd.to_numeric(df["credit"], errors="coerce")
    passed = df[df["gpa"].isin(PASSING_GRADES) & (df["credit"] > 0)]
    failed = df[df["gpa"].isin(FAILING_GRADES) & (df["credit"] > 0)]
    zero_credit = df[df["credit"] == 0]
    return {
        "total_passed_credits": passed["credit"].sum(),
        "failed_courses": failed.reset_index(drop=True),
        "zero_credit_courses": zero_credit.reset_index(drop=True)
    }
