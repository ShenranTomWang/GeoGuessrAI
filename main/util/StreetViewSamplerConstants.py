API_KEY = 'AIzaSyCome9MA6HFIVVZtQJy5Do8YQtOBvArgb0'
DEFAULT_DATASET_SIZE = 10000
DEFAULT_IMAGE_WIDTH = 640
DEFAULT_IMAGE_HEIGHT = 640
DEFAULT_IMAGE_SIZE = f'{DEFAULT_IMAGE_WIDTH}x{DEFAULT_IMAGE_HEIGHT}'
DEFAULT_FOV = 120
DEFAULT_METADATA_FILE_NAME = 'metadata.json'
DEFAULT_HEADINGS = [0, 90, 180, 270]
DEFAULT_PROMPTS = [
    'highways+in+Canada', 'road+in+Canada', 'alleys+in+Canada',
    'highways+in+United+States', 'lanes+in+United+States', 'alleys+in+United+States', 'boulevards+in+United+States', 'trails+in+United+States', 'road+in+United+States',
    'highways+in+Cuba', 'lanes+in+Cuba', 'alley+in+Cuba',
    'highways+in+Mexico', 'lanes+in+Mexico', 'road+in+Mexico',
    'highways+in+Brizil''lanes+in+Brizil', 'alleys+in+Brizil',
    'road+in+Argentina', 'lanes+in+Argentina', 'street+in+Argentina',
    'road+in+Chile', 'lanes+in+Chile',
    'lanes+in+Peru', 'road+in+Peru', 'alleys+in+Peru',
    'alleys+in+Columbia', 'highways+in+Columbia', 'road+in+Columbia', 'lanes+in+Columbia',

    'alleys+in+New+Zealand', 'road+in+New+Zealand', 'highways+in+New+Zealand', 'lanes+in+New+Zealand',
    'lanes+in+Australia', 'highways+in+Australia', 'streets+in+Australia', 'roads+in+Australia',

    'roads+in+Madagascar', 'streets+in+Madagascar', 'lanes+in+Madagascar',
    'lanes+in+South+Africa', 'highways+in+South+Africa', 'streets+in+South+Africa',
    'streets+in+Namibia', 'lanes+in+Namibia',
    'roads+in+Angola', 'highways+in+Angola',
    'highways+in+Zambia', 'streets+in+Zambia', 'roads+in+Zambia',
    'highways+in+Mozambique', 'streets+in+Mozambique',
    'streets+in+Tanzania', 'highways+in+Tanzania', 'roads+in+Tanzania',
    'streets+in+Congo', 'lanes+in+Congo', 'highways+in+democratic+republic+of+congo', 'streets+in+democratic+republic+of+congo',
    'roads+in+Ethiopia', 'highways+in+Ethiopia',
    'streets+in+Uganda', 'highways+in+Uganda', 'roads+in+Uganda',
    'roads+in+Morocco', 'lanes+in+Morocco',
    'lanes+in+Egypt', 'streets+in+Egypt', 'roads+in+Egypt',
    'roads+in+Japan', 'streets+in+Japan', 'highways+in+Japan',
    'roads+in+South+Korea', 'streets+in+South+Korea', 'highways+in+South+Korea',
    'alleys+in+North+Korea', 'lanes+in+North+Korea',
    'roads+in+China', 'streets+in+China', 'highways+in+China',
    'roads+in+Philippines', 'streets+in+Philippines', 'highways+in+Philippines',
    'roads+in+Indonesia', 'streets+in+Indonesia', 'highways+in+Indonesia',
    'roads+in+Malaysia', 'streets+in+Malaysia', 'highways+in+Malaysia',
    'roads+in+Singapore', 'streets+in+Singapore', 'lanes+in+Singapore',
    'roads+in+Thailand', 'streets+in+Thailand', 'highways+in+Thailand',
    'roads+in+India', 'streets+in+India', 'highways+in+India',
    'roads+in+Burma', 'streets+in+Burma', 'highways+in+Burma',
    'roads+in+Laos', 'streets+in+Laos', 'lanes+in+Laos',
    'roads+in+Vietnam', 'streets+in+Vietnam', 'highways+in+Vietnam',
    'roads+in+Nepal', 'streets+in+Nepal', 'highways+in+Nepal',
    'roads+in+Bangladesh', 'streets+in+Bangladesh', 'highways+in+Bangladesh',
    'roads+in+Iran', 'streets+in+Iran', 'highways+in+Iran',
    'roads+in+Saudi+Arabia', 'streets+in+Saudi+Arabia', 'highways+in+Saudi+Arabia',
    'roads+in+Israel', 'streets+in+Israel', 'highways+in+Israel',
    'roads+in+The+United+Arab+Emirates', 'streets+in+The+United+Arab+Emirates', 'highways+in+The+United+Arab+Emirates',
    'roads+in+Yemen', 'streets+in+Yemen', 'highways+in+Yemen',
    'roads+in+Pakistan', 'streets+in+Pakistan', 'highways+in+Pakistan',
    'roads+in+Afghanistan', 'streets+in+Afghanistan', 'highways+in+Afghanistan',
    'roads+in+Kazakhstan', 'streets+in+Kazakhstan', 'lanes+in+Kazakhstan',
    'roads+in+Mongolia', 'streets+in+Mongolia', 'lanes+in+Mongolia',

    'roads+in+Georgia', 'streets+in+Georgia', 'highways+in+Georgia',
    'roads+in+Turkey', 'streets+in+Turkey', 'highways+in+Turkey',
    'roads+in+Russia', 'streets+in+Russia', 'lanes+in+Russia',
    'roads+in+Ukraine', 'streets+in+Ukraine', 'lanes+in+Ukraine',
    'roads+in+Slovakia', 'streets+in+Slovakia', 'lanes+in+Slovakia',
    'roads+in+Slovenia', 'streets+in+Slovenia', 'lanes+in+Slovenia',
    'roads+in+Serbia', 'streets+in+Serbia', 'lanes+in+Serbia',
    'roads+in+Poland', 'streets+in+Poland', 'highways+in+Poland',
    'roads+in+Spain', 'streets+in+Spain', 'highways+in+Spain',
    'alleys+in+Portugal', 'streets+in+Portugal', 'highways+in+Portugal', 'lanes+in+Portugal'
    'roads+in+Croatia', 'streets+in+Croatia', 'lanes+in+Croatia',
    'roads+in+Switzerland', 'streets+in+Switzerland', 'highways+in+Switzerland',
    'roads+in+Sweden', 'streets+in+Sweden', 'highways+in+Sweden',
    'roads+in+Norway', 'streets+in+Norway', 'highways+in+Norway',
    'roads+in+Finland', 'avenue+in+Finland', 'highways+in+Finland', 'alleys+in+Finland'
    'roads+in+Denmark', 'avenue+in+Denmark', 'highways+in+Denmark', 'alleys+in+Denmark'
    'roads+in+Netherlands', 'streets+in+Netherlands', 'highways+in+Netherlands',
    'roads+in+Italy', 'streets+in+Italy', 'highways+in+Italy',
    'roads+in+Iceland', 'streets+in+Iceland', 'highways+in+Iceland',
    'roads+in+Greece', 'streets+in+Greece', 'lanes+in+Greece',
    'roads+in+Germany', 'streets+in+Germany', 'highways+in+Germany',
    'roads+in+France', 'streets+in+France', 'highways+in+France',
    'roads+in+Ireland', 'streets+in+Ireland', 'highways+in+Ireland',
    'roads+in+United+Kingdom', 'streets+in+United+Kingdom', 'highways+in+United+Kingdom',
    'roads+in+Czech', 'streets+in+Czech', 'lanes+in+Czech',
    'roads+in+Belgium', 'streets+in+Belgium', 'highways+in+Belgium',
    'roads+in+Hungary', 'streets+in+Hungary', 'lanes+in+Hungary',
    'roads+in+Austria', 'streets+in+Austria', 'highways+in+Austria',
    'alleys+in+Rumania', 'lanes+in+Rumania'
]
