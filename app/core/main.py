import os

from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

router = APIRouter()

current_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(current_dir, "..", "templates")

templates = Jinja2Templates(directory=template_dir)


@router.get("/", response_class=HTMLResponse)
async def serve_home_page(request: Request):
    context = {"request": request, "page_title": "Welcome to Kyrgyz Adventure!"}
    return templates.TemplateResponse("index.html", context)
