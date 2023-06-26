

from fastapi import APIRouter
from fastapi import Depends

from tendril.authn.users import auth_spec
from tendril.authn.users import authn_dependency
from tendril.authn.users import AuthUserModel

from tendril.caching.tokens import GenericTokenTModel
from tendril.caching.tokens import read

from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)


tokens_router = APIRouter(prefix='/tokens',
                          tags=["Tokens API"],
                          dependencies=[Depends(authn_dependency),
                                        auth_spec(scopes=['interests:common'])]
                          )


@tokens_router.get("/{namespace}/{key}",
                   response_model=GenericTokenTModel)
async def get_token(namespace: str, key: str):
    return read(namespace=namespace, key=key)


routers = [
    tokens_router
]
