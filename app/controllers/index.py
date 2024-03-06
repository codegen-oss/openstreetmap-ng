from fastapi import APIRouter
from starlette.responses import HTMLResponse

from app.lib.render_response import render_response

router = APIRouter()


@router.get('/')
@router.get('/export')
@router.get('/directions')
@router.get('/search')
@router.get('/query')
@router.get('/history')
@router.get('/history/nearby')
@router.get('/history/friends')
@router.get('/user/{_:str}/history')
@router.get('/note/{_:int}')
@router.get('/changeset/{_:int}')
@router.get('/node/{_:int}')
@router.get('/node/{_:int}/history')
@router.get('/node/{_:int}/history/{__:int}')
@router.get('/way/{_:int}')
@router.get('/way/{_:int}/history')
@router.get('/way/{_:int}/history/{__:int}')
@router.get('/relation/{_:int}')
@router.get('/relation/{_:int}/history')
@router.get('/relation/{_:int}/history/{__:int}')
async def index() -> HTMLResponse:
    return render_response('index.jinja2')


@router.get('/copyright')
async def copyright() -> HTMLResponse:
    return render_response('copyright.jinja2')


@router.get('/help')
async def help() -> HTMLResponse:
    return render_response('help.jinja2')


@router.get('/about')
async def about() -> HTMLResponse:
    return render_response('about.jinja2')
