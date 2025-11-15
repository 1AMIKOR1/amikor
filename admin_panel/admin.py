import io
from typing import Any

from sqladmin import Admin
from starlette.datastructures import FormData, UploadFile
from starlette.requests import Request


class CustomAdmin(Admin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    async def _handle_form_data(self, request: Request, obj: Any = None) -> FormData:
        """
        Handle form data and modify in case of UploadFile.
        This is needed since in edit page
        there's no way to show current file of object.
        """

        form = await request.form()
        form_data: list[tuple[str, str | UploadFile]] = []

        for key, value in form.multi_items():

            if not isinstance(value, UploadFile):
                form_data.append((key, value))
                continue

            should_clear = form.get(key + "_checkbox")
            empty_upload = len(await value.read(1)) != 1
            await value.seek(0)
            if should_clear:
                form_data.append((key, UploadFile(io.BytesIO(b""))))
            elif empty_upload and getattr(obj, key, None):
                f = getattr(obj, key)  # In case of update, imitate UploadFile
                if hasattr(f, 'name') and hasattr(f, 'open'):
                    form_data.append((key, UploadFile(filename=f.name, file=f.open())))
            else:
                form_data.append((key, value))
        return FormData(form_data)