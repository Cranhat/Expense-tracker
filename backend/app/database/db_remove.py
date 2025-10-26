def create_remove(table, condition):
    return f"""
            DELETE FROM {table}
            WHERE {condition};
            """     



