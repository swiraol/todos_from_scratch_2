def error_for_title(title, title_type=None, lists=None):
    if not 0 < len(title) < 160:
        return "The title must be between 0 and 160 characters"
    
    if title_type == 'list':
        for lst in lists:
            if title.casefold() == lst['title'].casefold():
                return "The list title already exists"
    
    return None