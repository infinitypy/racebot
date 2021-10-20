f = open('savedids.txt', 'r', encoding='utf8')
mappings = {entry.split('\t')[0]: entry.split('\t')[1].strip() for entry in f.readlines()}
f.close()


def get_id(d_id):
    d_id = str(d_id)
    return mappings[d_id] if d_id in mappings else None


def set_id(d_id, u_id):
    d_id = str(d_id)
    replace = d_id in mappings
    mappings[d_id] = u_id
    write_mappings()
    return replace


def remove_id(d_id):
    d_id = str(d_id)
    remove = d_id in mappings
    if remove:
        del mappings[d_id]
    return remove


def write_mappings():
    f1 = open('savedids.txt', 'r+')
    f1.truncate(0)
    f1.seek(0)
    for d_id, u_id in mappings.items():
        f1.write('{}\t{}\n'.format(d_id, u_id))
    f1.close()
