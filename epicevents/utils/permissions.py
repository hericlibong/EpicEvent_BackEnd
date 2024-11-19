# utils/permissions.py

DEPARTMENT_PERMISSIONS = {
    'Gestion': {
        'can_manage_users': True,
        'can_create_contracts': True,
        'can_modify_all_contracts': True,
        'can_assign_support': True,
        'can_modify_all_events': True,
        'can_filter_events': True,
        'can_filter_contracts': True,
    },
    'Commercial': {
        'can_create_clients': True,
        'can_modify_own_clients': True,
        'can_modify_own_contracts': True,
        'can_create_events': True,
        'can_filter_contracts': True,
    },
    'Support': {
        'can_modify_own_events': True,
        'can_filter_events': True,
    },
}

def has_permission(user_department, permission):
    """
    Vérifie si l'utilisateur a les permissions requises pour effectuer une action.
    """
    permissions = DEPARTMENT_PERMISSIONS.get(user_department, {})
    return permissions.get(permission, False)