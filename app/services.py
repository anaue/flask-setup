import api
from fastapi.responses import FileResponse
from datetime import date
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
config_api = api.Config()


def __create_html__(template: str, filters: dict, data: dict):
    return templates.TemplateResponse(template, {"request": filters['request'], "filters": filters, "data": data})


def load_settings_list(arr_filters: dict):
    arr_filters['top'] = arr_filters['top'] if 'top' in arr_filters else 10
    arr_filters['skip'] = arr_filters['skip'] if 'skip' in arr_filters else 0
    response = config_api.list_settings(arr_filters)

    data = response["data"] if not response is None else []
    return __create_html__("home.html", arr_filters, data)


def get_setting(setting_id: str):
    return config_api.get_setting(setting_id)


def settings_list_mock(arr_filters: dict):
    arr_filters['top'] = arr_filters['top'] if 'top' in arr_filters else 10
    arr_filters['skip'] = arr_filters['skip'] if 'skip' in arr_filters else 0
    response = {
        "data": [
            {
                "id": 123,
                "name": "setting 123"
            },{
                "id": 456,
                "name": "setting 456"
            },{
                "id": 789,
                "name": "setting 7890"
            }
        ]
    }
    data = response["data"] if not response is None else []
    return __create_html__("home.html", arr_filters, data)