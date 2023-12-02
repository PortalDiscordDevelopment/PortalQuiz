"""a file to store all the db schemas lol"""
schemas = [
    """CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY,
    category TEXT NOT NULL,
    question TEXT NOT NULL,
    correct TEXT NOT NULL,
    wrong_one TEXT NOT NULL,
    wrong_two TEXT NOT NULL,
    wrong_three TEXT NOT NULL
)"""
]
