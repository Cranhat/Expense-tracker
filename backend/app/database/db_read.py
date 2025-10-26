def create_fetch(table, object = "*"):
    return f"""
        SELECT {object}
        FROM {table};
    """
    
def create_fetch_where(table, object = "*", condition = ""):
    return f"""
        SELECT {object}
        FROM {table}
        WHERE {condition};
    """