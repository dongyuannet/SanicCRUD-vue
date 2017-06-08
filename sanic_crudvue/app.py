from sanic import Sanic
from sanic_cors import CORS

from crud import crud_bp, db, ShanghaiPersonInfo
from config import base_config

app = Sanic(__name__)

# but due to not support http `options` method in sanic core (https://github.com/channelcat/sanic/issues/251).
# So have to use third package extension for Sanic-Cors. Thank you @ashleysommer!

CORS(app,
     automatic_options=True)  # resolve pre-flight request problem (https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request)


@app.middleware('response')
async def custom_banner(request, response):
    response.headers["content-type"] = "application/json"


app.blueprint(crud_bp)
app.config.from_object(base_config)

db.create_tables([ShanghaiPersonInfo], safe=True)

app.run(host='0.0.0.0', port=8000, debug=True)
