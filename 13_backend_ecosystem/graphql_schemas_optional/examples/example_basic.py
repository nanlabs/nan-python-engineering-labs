"""Basic example: select only requested fields."""
user = {'id': 7, 'name': 'Alice', 'email': 'alice@example.com', 'plan': 'pro'}

def execute(query):
    fields = [t for t in query.strip().strip('{}').split() if t.isidentifier()]
    return {'data': {'user': {f: user[f] for f in fields if f in user}}}

print(execute('{ id name plan }'))
