def create_update():
    return """
            UPDATE {0} 
            SET {1}
            WHERE {2};
            """