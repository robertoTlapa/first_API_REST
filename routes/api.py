from fastapi import APIRouter
from endpoints import usuario, evento, charla, confirmar_charla, confirma_evento

router = APIRouter()
router.include_router(usuario.router)
router.include_router(evento.router)
router.include_router(charla.router)
router.include_router(confirmar_charla.router)
router.include_router(confirma_evento.router)
