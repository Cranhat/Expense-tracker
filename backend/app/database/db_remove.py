def create_remove():
    return """
            DELETE FROM {0}
            WHERE {1};
            """     
