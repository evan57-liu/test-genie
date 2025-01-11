import uvicorn

from test_genie.core.configs import config
from test_genie.core.log import setup_logging


def main():
    setup_logging()
    uvicorn.run(
        app="test_genie.app.server:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True,
        workers=1,
    )


if __name__ == "__main__":
    main()
