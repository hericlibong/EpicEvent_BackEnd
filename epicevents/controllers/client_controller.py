# controllers/client_controller.py
from utils.decorators import requires_role
from utils.roles import UserRole

@requires_role(UserRole.COMMERCIAL)
def create_client():
    # logique pour créer un client
    pass
