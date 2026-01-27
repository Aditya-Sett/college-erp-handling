def semester_name(n: int) -> str:
    if n == 1:
        return "1st Sem"
    elif n == 2:
        return "2nd Sem"
    elif n == 3:
        return "3rd Sem"
    else:
        return f"{n}th Sem"
