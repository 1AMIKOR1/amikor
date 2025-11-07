from sqladmin import ModelView

from app.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name, User.last_name]
    # column_details_list = [User.id, User.name, User.email, User.created_at]
    column_details_exclude_list = [User.password]
    can_delete = False
    name = "User"  # Display name (default: model class name)
    name_plural = "Users"  # Plural name (default: name + "s")
    icon = "fa-solid fa-user"  # Icon for sidebar
    category = "People"  # Group in sidebar
    category_icon = "fa-solid fa-users"  # Icon for category
    column_searchable_list = [User.name, User.email]


