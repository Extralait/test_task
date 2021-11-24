def get_no_files_fields(model):
    return [f.name for f in model._meta.fields if not f.__dict__.get('upload_to')]