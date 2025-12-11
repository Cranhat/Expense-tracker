def create_remove():
    return """
            DELETE FROM {0}
            WHERE {1};
            """     

def create_remove_member():
    return """
            DELETE FROM {0}
            WHERE {1} AND {2};
            """     
