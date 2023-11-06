from fastapi.middleware.cors import CORSMiddleware


def get_cors_middleware():
    allow_all = ['*']

    return CORSMiddleware(
        allow_origins=allow_all,
        allow_credentials=True,
        allow_methods=allow_all,
        allow_headers=allow_all,
    )
