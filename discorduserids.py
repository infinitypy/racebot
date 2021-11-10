import writelbtosheet

sheet_mappings = writelbtosheet.user_data.get_values(f'A2:B{writelbtosheet.user_data.row_count}')
mappings = {}
for k, v in sheet_mappings:
    if v:
        mappings[v] = k


def get_id(d_id):
    d_id = str(d_id)
    for k, v in mappings.items():
        if d_id == v:
            return k
    return None


def set_id(u_id, d_id):
    if u_id not in mappings:
        return None
    d_id = str(d_id)
    replace = mappings[u_id] != ''
    mappings[u_id] = d_id
    write_mappings(u_id, d_id)
    return replace


def remove_id(d_id):
    d_id = str(d_id)
    for k, v in mappings.items():
        if d_id == v:
            mappings[k] = ''
            write_mappings(k, '')
            return True
    return False


def write_mappings(u_id, new_did):
    sheet_uids = writelbtosheet.user_data.range(2, 2, writelbtosheet.user_data.row_count, 2)
    for index, cell in enumerate(sheet_uids):
        if cell.value == u_id:
            writelbtosheet.user_data.update_cell(index + 2, 1, new_did)
            return True
    return False
