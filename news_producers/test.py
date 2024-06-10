import pandas as pd

# Sample DataFrame
data = {
    'title': ['Title 1', 'Title 2', 'Title 3'],
    'content': ['Some text', 'Another text with [Removed]', 'https://removed.com'],
    'url': ['url1', 'url2', 'url3'],
    'description': ['Desc 1', '[Removed]', 'Desc 3']
}
df = pd.DataFrame(data)

# Replacements dictionary
replacements = {
    
        '[Removed]': None,  # Remove [Removed]
        'https://removed.com': None  # Remove https://removed.com
    
}

df.replace(replacements, inplace=True)

print(df)
