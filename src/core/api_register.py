from fastapi import FastAPI

from ..api.v1.city.controller import router as city_router
from ..api.v1.spot.controller import router as spot_router
from ..api.v1.tag.controller import router as tag_router
from ..api.v1.spot_type.controller import router as spot_type_router
from ..api.v1.feedback.controller import router as feedback_router
from ..api.v1.media.controller import router as media_router, spot_media_file_router
from ..api.v1.user.controller import router as user_router
from ..api.v1.role_permission.controller import router as role_router
from ..api.v1.user_spot.controller import router as user_spots_router
from ..api.v1.spot_attribute.controller import router as spot_attribute_router

from ..api.v1.auth.controller import router  as auth_router


V1_PREFIX = "/api/v1"


def regis_api_v1(app : FastAPI):
    app.include_router(city_router, prefix=V1_PREFIX)
    app.include_router(spot_router, prefix=V1_PREFIX)
    app.include_router(spot_attribute_router, prefix=V1_PREFIX)
    app.include_router(tag_router, prefix=V1_PREFIX)
    app.include_router(spot_type_router, prefix=V1_PREFIX)
    app.include_router(feedback_router, prefix=V1_PREFIX)
    app.include_router(media_router, prefix=V1_PREFIX)
    app.include_router(user_router, prefix=V1_PREFIX)
    app.include_router(role_router, prefix=V1_PREFIX)
    app.include_router(spot_type_router, prefix=V1_PREFIX)
    app.include_router(user_spots_router, prefix=V1_PREFIX)
    app.include_router(spot_media_file_router, prefix=V1_PREFIX)
    app.include_router(auth_router, prefix=V1_PREFIX)

