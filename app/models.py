class User:
    def __init__(self, id, first_name, last_name, email, total_reactions=0, posts=[]):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = total_reactions
        self.posts = posts


class Post:
    def __init__(self, id: int, author_id: int, text: str, reactions=[]):
        self.id = id
        self.author_id = author_id
        self.text = text
        self.reactions = reactions
