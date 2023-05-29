import api
from fastapi.responses import FileResponse
from datetime import date
from starlette.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

wrapper = api.ApiWrapper()
config = api.Config(wrapper)


def __create_html__(template: str, filters: dict, data: dict):
    return templates.TemplateResponse(template, {"request": filters['request'], "filters": filters, "data": data})


def load_settings_list(arr_filters: dict):
    arr_filters['top'] = arr_filters['top'] if 'top' in arr_filters else 10
    arr_filters['skip'] = arr_filters['skip'] if 'skip' in arr_filters else 0
    response = config.list_settings(arr_filters)

    data = response["data"] if not response is None else []
    return __create_html__("home.html", arr_filters, data)


def get_setting(setting_id: str):
    return config.get_setting(setting_id)


def mock_settings_list(arr_filters: dict):
    arr_filters['top'] = arr_filters['top'] if 'top' in arr_filters else 10
    arr_filters['skip'] = arr_filters['skip'] if 'skip' in arr_filters else 0
    response = {
        "data": []
    }
    response["data"].append({
                "id": 123, 
                "name": "setting 123"
            })
    response["data"].append({
                "id": 456, 
                "name": "setting 456"
            })
    response["data"].append({
                "id": 789, 
                "name": "setting 789"
            })

    data = response["data"] if not response is None else []
    return __create_html__("home.html", arr_filters, data)