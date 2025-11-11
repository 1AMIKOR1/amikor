from sqladmin import ModelView

from app.models.products import ProductsModel
from app.models.users import UsersModel


class UsersView(ModelView, model=UsersModel):
    column_list = [UsersModel.email, UsersModel.name]
    # column_details_list = [User.id, User.name, User.email, User.created_at]
    column_details_exclude_list = [UsersModel.hashed_password]
    can_delete = False
    name = "User"  # Display name (default: model class name)
    name_plural = "Users"  # Plural name (default: name + "s")
    icon = "fa-solid fa-user"  # Icon for sidebar
    category = "People"  # Group in sidebar
    category_icon = "fa-solid fa-users"  # Icon for category
    column_searchable_list = [UsersModel.name, UsersModel.email, UsersModel.role]


class ProductsView(ModelView, model=ProductsModel):
    column_list = [ProductsModel.title, ProductsModel.quantity, ProductsModel.price]
    can_delete = False
    name = "Product"  # Display name (default: model class name)
    name_plural = "Products"  # Plural name (default: name + "s")
    icon = "fa-solid fa-user"  # Icon for sidebar
    category = "Products"  # Group in sidebar
    category_icon = "fa-solid fa-users"  # Icon for category
    column_searchable_list = [ProductsModel.title, ProductsModel.price]
