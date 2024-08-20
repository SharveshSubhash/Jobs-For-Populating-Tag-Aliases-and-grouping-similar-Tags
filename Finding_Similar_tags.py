from fuzzywuzzy import fuzz
from collections import defaultdict

def normalize_tag(tag):
    return tag.lower().replace('-', ' ').replace('_', ' ')

def are_similar(tag1, tag2, threshold=85):
    return fuzz.ratio(tag1, tag2) >= threshold

def group_similar_tags(tags):
    normalized_tags = {tag: normalize_tag(tag) for tag in tags}
    grouped_tags = defaultdict(list)
    
    # I though of adding a list to keep track of tags that we have already been grouped
    visited_tags = set()
    
    for tag in tags:
        if tag in visited_tags:
            continue
        
        grouped_tags[tag].append(tag)
        visited_tags.add(tag)
        
        for other_tag in tags:
            if other_tag == tag or other_tag in visited_tags:
                continue
            
            if are_similar(normalized_tags[tag], normalized_tags[other_tag]):
                grouped_tags[tag].append(other_tag)
                visited_tags.add(other_tag)
    
    return dict(grouped_tags)

new_tags = [ "Artificial Intelligence", "AI", "A.I.", "Machine Learning", "ML", "Deep Learning","deep-learning", "Data Science", "data_science" ]
grouped_tags = group_similar_tags(new_tags)
print("Grouped Tags:")
for key, group in grouped_tags.items():
    print(f"{key}: {group}")
