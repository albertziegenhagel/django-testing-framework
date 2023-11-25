from dtf.models import Project, TestReference

def create_reference_query(project, query_params):
    queries = {}
    for prop in project.properties.all():
        if prop.influence_reference:
            prop_value = query_params.get(prop.name, None)
            if not prop_value is None:
                queries['property_values__' + prop.name] = prop_value
    return queries

def get_project_by_id(project_id, queryset):
    """
    Retrieve a project by its Id. Returns None if no project is found.
    """
    try:
        return queryset.get(pk=project_id)
    except Project.DoesNotExist:
        return None

def get_project_by_slug(project_slug, queryset):
    """
    Retrieve a project by its slug. Returns None if no project is found.
    """
    try:
        return queryset.get(slug=project_slug)
    except Project.DoesNotExist:
        return None

def get_project_by_id_or_slug(id, queryset):
    """
    Retrieve a project by its ID or slug. Returns None if no project is found.
    """
    if id.isdigit():
        project = get_project_by_id(int(id), queryset)
    else:
        project = None

    if project is None:
        project = get_project_by_slug(id, queryset)

    return project

def get_object_or_none(klass, *args, **kwargs):
    if hasattr(klass, '_default_manager'):
        queryset = klass._default_manager.all()
    else:
        queryset = klass
    try:
        return queryset.get(*args, **kwargs)
    except klass.model.DoesNotExist:
        return None
