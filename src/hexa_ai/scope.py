import fnmatch

def is_in_scope(target, scope_list):
    """
    Checks if a target (URL or IP) is within the defined scope.
    Matches using Unix shell-style wildcards.
    """
    if not scope_list:
        return True # Default to True if no scope file is provided

    for pattern in scope_list:
        if fnmatch.fnmatch(target, pattern):
            return True
    return False

def load_scope(filepath):
    try:
        with open(filepath, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return []
