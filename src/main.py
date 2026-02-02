from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlmodel import Session, select

from src.data.db import get_session, init_db, get_next_id
from src.models.motos import Moto


init_db()

app = FastAPI()

# Jinja2
templates = Jinja2Templates(directory="src/templates")

# Static
app.mount("/static", StaticFiles(directory="src/static"), name="static")


# ------------------------------
#   RUTAS WEB (HTML)
# ------------------------------

# INICIO
@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "mensaje": "Bienvenido a la App de Motos"}
    )


# LISTADO
@app.get("/motos", response_class=HTMLResponse)
async def lista_motos_web(
    request: Request,
    orden: str | None = None,
    session: Session = Depends(get_session)
):

    query = select(Moto)

    # Ordenación SQL
    if orden == "id_asc":
        query = query.order_by(Moto.id.asc())
    elif orden == "id_desc":
        query = query.order_by(Moto.id.desc())
    elif orden == "año_asc":
        query = query.order_by(Moto.año.asc())
    elif orden == "año_desc":
        query = query.order_by(Moto.año.desc())

    motos = session.exec(query).all()

    return templates.TemplateResponse(
        "motos.html",
        {"request": request, "motos": motos, "orden": orden}
    )


# ---------- CREAR ----------
@app.get("/motos/crear", response_class=HTMLResponse)
async def crear_moto_form(request: Request):
    return templates.TemplateResponse("crear_moto.html", {"request": request})


@app.post("/motos/crear")
async def crear_moto(
    marca: str = Form(...),
    modelo: str = Form(...),
    año: int = Form(...),
    nueva: str = Form(...),
    session: Session = Depends(get_session)
):
    # Obtener el siguiente ID disponible
    nuevo_id = get_next_id(session)

    # Crear la moto con ese ID
    moto = Moto(
        id=nuevo_id,
        marca=marca,
        modelo=modelo,
        año=año,
        nueva=(nueva == "true")
    )

    session.add(moto)
    session.commit()
    session.refresh(moto)

    return RedirectResponse("/motos?ok=creada", status_code=303)

# ---------- EDITAR ----------
@app.get("/motos/editar/{moto_id}", response_class=HTMLResponse)
async def editar_moto_form(
    request: Request,
    moto_id: int,
    session: Session = Depends(get_session)
):
    moto = session.get(Moto, moto_id)
    if not moto:
        raise HTTPException(404, "Moto no encontrada")

    return templates.TemplateResponse(
        "editar_moto.html",
        {"request": request, "moto": moto}
    )


@app.post("/motos/editar/{moto_id}")
async def editar_moto(
    moto_id: int,
    marca: str = Form(...),
    modelo: str = Form(...),
    año: int = Form(...),
    nueva: str = Form(...),
    session: Session = Depends(get_session)
):
    moto = session.get(Moto, moto_id)
    if not moto:
        raise HTTPException(404, "Moto no encontrada")

    moto.marca = marca
    moto.modelo = modelo
    moto.año = año
    moto.nueva = (nueva == "true")

    session.add(moto)
    session.commit()

    return RedirectResponse("/motos?ok=editada", status_code=303)


# ---------- ELIMINAR ----------
@app.get("/motos/eliminar/{moto_id}", response_class=HTMLResponse)
async def eliminar_moto_form(
    request: Request,
    moto_id: int,
    session: Session = Depends(get_session)
):
    moto = session.get(Moto, moto_id)
    return templates.TemplateResponse(
        "eliminar_moto.html",
        {"request": request, "moto": moto}
    )


@app.post("/motos/eliminar/{moto_id}")
async def eliminar_moto(
    moto_id: int,
    session: Session = Depends(get_session)
):
    moto = session.get(Moto, moto_id)
    if moto:
        session.delete(moto)
        session.commit()

    return RedirectResponse("/motos?ok=eliminada", status_code=303)


# ---------- DETALLE ----------
@app.get("/motos/{moto_id}", response_class=HTMLResponse)
async def detalle_moto(
    request: Request,
    moto_id: int,
    session: Session = Depends(get_session)
):
    moto = session.get(Moto, moto_id)
    if not moto:
        raise HTTPException(404, "Moto no encontrada")

    return templates.TemplateResponse(
        "moto_detalle.html",
        {"request": request, "moto": moto}
    )


# ------------------------------
#   API REST (JSON)
# ------------------------------

@app.get("/api/motos")
async def api_lista_motos(session: Session = Depends(get_session)):
    return session.exec(select(Moto)).all()


@app.post("/api/motos", status_code=201)
async def api_crear_moto(moto: Moto, session: Session = Depends(get_session)):
    session.add(moto)
    session.commit()
    session.refresh(moto)
    return moto


@app.put("/api/motos/{moto_id}")
async def api_actualizar_moto(
    moto_id: int,
    moto_actualizada: Moto,
    session: Session = Depends(get_session)
):
    moto = session.get(Moto, moto_id)
    if not moto:
        raise HTTPException(404, "Moto no encontrada")

    moto.marca = moto_actualizada.marca or moto.marca
    moto.modelo = moto_actualizada.modelo or moto.modelo
    moto.año = moto_actualizada.año or moto.año
    moto.nueva = (
        moto_actualizada.nueva
        if moto_actualizada.nueva is not None
        else moto.nueva
    )

    session.add(moto)
    session.commit()
    session.refresh(moto)

    return moto


@app.delete("/api/motos/{moto_id}", status_code=204)
async def api_eliminar_moto(
    moto_id: int,
    session: Session = Depends(get_session)
):
    moto = session.get(Moto, moto_id)
    if moto:
        session.delete(moto)
        session.commit()
    return None

