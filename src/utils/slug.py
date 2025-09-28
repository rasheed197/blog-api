import re, uuid

def generate_slug(title):
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
    return f"{slug}-"
    # return f"{slug}-{uuid.uuid4().hex[:6]}"