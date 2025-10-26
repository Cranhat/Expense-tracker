def create_update(table, values, condition):
    return f"""
            UPDATE {table} 
            SET {values}
            WHERE {condition};
            """