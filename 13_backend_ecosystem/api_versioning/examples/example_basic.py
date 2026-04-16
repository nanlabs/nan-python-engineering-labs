"""Basic example: behavior switch by API version."""
def profile_v1(uid):
    return {'id': uid, 'name': 'Alice'}

def profile_v2(uid):
    return {'id': uid, 'full_name': 'Alice Doe', 'plan': 'pro'}

def dispatch(version, uid):
    if version == '1':
        return profile_v1(uid)
    if version == '2':
        return profile_v2(uid)
    raise ValueError('unsupported version')

print(dispatch('1', 7))
print(dispatch('2', 7))
