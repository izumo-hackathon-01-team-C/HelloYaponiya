from fastapi import APIRouter, Request, HTTPException, status


router = APIRouter()


@router.get(path='/translations/{lang}')
def get_translations(request: Request, lang: str) -> dict[str, str]:
    if translations := request.app.state.translation_fixtures.get(lang):
        return translations
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Translation not found'
        )
