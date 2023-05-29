from fastapi import Request, APIRouter
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from services import (
    get_setting,
    load_settings_list,
    mock_settings_list
)

router = APIRouter()

@router.get("/")
def root():
    return RedirectResponse("/api/mock")

@router.get("/api/mock")
def mock(request: Request, response_class=HTMLResponse):
    arr_filters = dict(request.query_params.items())
    arr_filters['request'] = request
    return mock_settings_list(arr_filters)

@router.get("/api/config")
def config(request: Request):
    arr_filters = dict(request.query_params.items())
    return load_settings_list(arr_filters)

@router.get("/api/settings/{setting_id}")
def settings(setting_id: str):
    return get_setting(setting_id)
