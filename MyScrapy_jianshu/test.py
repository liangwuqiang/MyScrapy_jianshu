import re

content = """
dsfsdf
<div class="image-container-fill" style="padding-bottom: 60.75000000000001%;"></div>
dsfsdf
<div class="image-container-fill" style="padding-bottom: 33.25%;"></div>
dfsdf
<div class="image-container-fill" style="padding-bottom: 85.25%;"></div>
dsfsdf
"""
pattern = '<div class="image-container-fill" style="padding-bottom: \d+\.\d+%;"></div>'
content = re.sub(pattern=pattern, repl='@@@', string=content)
print(content)

