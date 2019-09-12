from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import uvicorn
import io
import Image

templates = Jinja2Templates(directory='templates')

app = Starlette(debug=True)
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.route('/')
async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.route("/upload", methods=["POST"])
async def upload(request):
    data = await request.form()
    bytes = await (data["file"].read())
    return predict_flower_class(bytes)

def predict_flower_class(bytes):
    img = Image.open(io.BytesIO(bytes))
    # ImageDataBunch.single_from_classes()
    # create_cnn()
    learn = load('export.pkl')
    _, class_, losses = learn.predict(img)
    return JSONResponse({
        "prediction": class_,
        "losses":losses
    })
    
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)