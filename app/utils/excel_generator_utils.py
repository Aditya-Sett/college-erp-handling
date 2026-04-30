import pandas as pd
import io

def generate_excel(report):

    df = pd.DataFrame(report)

    # Column ordering
    fixed_cols = ["studentId", "collegeRoll", "username"]
    session_cols = [c for c in df.columns if c not in fixed_cols + ["percentage"]]

    df = df[fixed_cols + session_cols + ["percentage"]]

    output = io.BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)

    return output