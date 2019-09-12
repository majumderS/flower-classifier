from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse, JSONResponse
import uvicorn
import io
import Image
import aiohttp
import asyncio

templates = Jinja2Templates(directory='templates')
export_file_url = 'https://drive.google.com/uc?export=download&id=1RQqmYqnS_U4xYQcis7xZXfKJY9xA3zxc'
export_file_name = 'export.pkl'

app = Starlette(debug=True)
app.mount('/static', StaticFiles(directory='static'), name='static')


classes = ['alpine sea holly', 'anthurium', 'artichoke', 'azalea', 'ball moss', 'balloon flower', 'barbeton daisy', 'bearded iris', 
 'bee balm', 'bird of paradise', 'bishop of llandaff', 'black-eyed susan', 'blackberry lily', 'blanket flower', 'bolero deep blue',
 'bougainvillea', 'bromelia', 'king protea', 'lenten rose', 'lotus', 'love in the mist', 'magnolia', 'mallow', 'marigold', 
 'mexican aster', 'mexican petunia', 'monkshood', 'moon orchid', 'morning glory', 'orange dahlia', 'osteospermum', 'oxeye daisy', 
 'passion flower', 'pelargonium', 'buttercup', 'california poppy', 'camellia', 'canna lily', 'canterbury bells', 'cape flower', 
 'carnation', 'cautleya spicata', 'clematis', "colt's foot", 'columbine', 'common dandelion', 'corn poppy', 'cyclamen ', 'daffodil',
 'desert-rose', 'english marigold', 'peruvian lily', 'petunia', 'pincushion flower', 'pink primrose', 'pink-yellow dahlia?', 
 'poinsettia', 'primula', 'prince of wales feathers', 'purple coneflower', 'red ginger', 'rose', 'ruby-lipped cattleya', 
 'siam tulip', 'silverbush', 'snapdragon', 'spear thistle', 'spring crocus', 'fire lily', 'foxglove', 'frangipani', 'fritillary',
 'garden phlox', 'gaura', 'gazania', 'geranium', 'giant white arum lily', 'globe thistle', 'globe-flower', 'grape hyacinth',
 'great masterwort', 'hard-leaved pocket orchid', 'hibiscus', 'hippeastrum ', 'japanese anemone', 'stemless gentian', 'sunflower',
 'sweet pea', 'sweet william', 'sword lily', 'thorn apple', 'tiger lily', 'toad lily', 'tree mallow', 
 'tree poppy', 'trumpet creeper', 'wallflower', 'water lily', 'watercress', 'wild pansy', 'windflower', 'yellow iris']

async def setup_learner():
    await download_file(export_file_url, path / export_file_name)
    try:
        learn = load_learner(path, export_file_name)
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise

def predict_flower_class(bytes):
    img = open_image(io.BytesIO(bytes))
    class = learn.predict(img)[0]
    return JSONResponse({
        "prediction": class,
    })

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close(

@app.route('/')
async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.route("/upload", methods=["POST"])
async def upload(request):
    data = await request.form()
    bytes = await (data["file"].read())
    return predict_flower_class(bytes)


    
if __name__ == '__main__':
        if 'serve' in sys.argv:
            uvicorn.run(app, host='0.0.0.0', port=5000, log_level='info')
