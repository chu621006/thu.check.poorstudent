import pandas as pd
import fitz  # PyMuPDF
import re

PASSING_GRADES = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', '通過']
FAILING_GRADES = ['D', 'E', '未通過']

def parse_pdf(file) -> pd.DataFrame:
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    
    # 彈性正則匹配學分與 GPA，並倒推出課程名稱
    pattern = re.compile(rf"(.+?)\s+(\d+)\s+(A\+|A-|A|B\+|B-|B|C\+|C-|C|D|E|通過|未通過)")
    data = []
    for line in text.splitlines():
        match = pattern.search(line.strip())
        if match:
            course = match.group(1).strip()
            credit = int(match.group(2))
            gpa = match.group(3).strip()
            data.append((course, credit, gpa))
    
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
