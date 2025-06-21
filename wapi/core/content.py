def validate_and_fix_content(content, default_content):
    if not (isinstance(content.get('size'), list) and len(content['size']) == 2 and
            all(isinstance(x, (int, float)) and x > 0 for x in content['size'])):
        content['size'] = default_content['size']
    if not isinstance(content.get('html'), str):
        content['html'] = default_content['html']
    if not isinstance(content.get('css'), str):
        content['css'] = default_content['css']
    if not isinstance(content.get('js'), str):
        content['js'] = default_content['js']
    if not isinstance(content.get('movable'), bool):
        content['movable'] = default_content['movable']
    if not isinstance(content.get('transparent'), bool):
        content['transparent'] = default_content['transparent']
    opacity = content.get('opacity')
    if not (isinstance(opacity, (int, float)) and 0 < opacity <= 1):
        content['opacity'] = default_content['opacity']
    second_opacity = content.get('second_opacity')
    if not (isinstance(second_opacity, (int, float)) and 0 < second_opacity <= 1):
        content['second_opacity'] = default_content['second_opacity']
    block_size = content.get('block_size')
    if not (isinstance(block_size, int) and block_size > 0):
        content['block_size'] = default_content['block_size']
    padding = content.get('padding')
    if not (isinstance(padding, int) and padding >= 0):
        content['padding'] = default_content['padding']
    if not (isinstance(content.get('position'), list) and len(content['position']) == 2 and
            all(isinstance(x, (int, float)) and x >= 0 for x in content['position'])):
        content['position'] = default_content['position']
    return content

def is_content_valid(content, default):
    try:
        test = content.copy()
        _ = validate_and_fix_content(test, default)
        return True
    except:
        return False
