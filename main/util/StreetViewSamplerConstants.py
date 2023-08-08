API_KEY = 'AIzaSyCome9MA6HFIVVZtQJy5Do8YQtOBvArgb0'
DEFAULT_DATASET_SIZE = 10000
DEFAULT_IMAGE_WIDTH = 640
DEFAULT_IMAGE_HEIGHT = 640
DEFAULT_IMAGE_SIZE = f'{DEFAULT_IMAGE_WIDTH}x{DEFAULT_IMAGE_HEIGHT}'
DEFAULT_FOV = 120
DEFAULT_METADATA_FILE_NAME = 'metadata.json'
DEFAULT_HEADINGS = [0, 90, 180, 270]
DEFAULT_PROMPTS = [
    'highways+in+Canada', 'roads+in+Canada', 'alleys+in+Canada',
    'highways+in+United+States', 'lanes+in+United+States', 'alleys+in+United+States', 'boulevards+in+United+States', 'trails+in+United+States', 'roads+in+United+States',
    'highways+in+California', 'lanes+in+California', 'alleys+in+California', 'boulevards+in+California', 'trails+in+California', 'roads+in+California',
    'highways+in+Texas', 'lanes+in+Texas', 'alleys+in+Texas', 'boulevards+in+Texas', 'trails+in+Texas', 'roads+in+Texas',
    'highways+in+Ohio', 'lanes+in+Ohio', 'alleys+in+Ohio', 'boulevards+in+Ohio', 'trails+in+Ohio', 'roads+in+Ohio',
    'highways+in+Alaska', 'lanes+in+Alaska', 'alleys+in+Alaska', 'boulevards+in+Alaska', 'trails+in+Alaska', 'roads+in+Alaska',
    'highways+in+Virginia', 'lanes+in+Virginia', 'alleys+in+Virginia', 'boulevards+in+Virginia', 'trails+in+Virginia', 'roads+in+Virginia',
    'highways+in+New+Jersey', 'lanes+in+New+Jerseys', 'alleys+in+New+Jersey', 'trails+in+New+Jersey', 'roads+in+New+Jersey',
    'highways+in+Florida', 'lanes+in+Florida', 'alleys+in+Florida', 'boulevards+in+Florida', 'trails+in+Florida', 'roads+in+Florida',
    'highways+in+Georgia', 'lanes+in+Georgia', 'alleys+in+Georgia', 'boulevards+in+Georgia', 'trails+in+Georgia', 'roads+in+Georgia',
    'highways+in+Washington', 'lanes+in+Washington', 'alleys+in+Washington', 'boulevards+in+Washington', 'trails+in+Washington', 'roads+in+Washington',
    'highways+in+Michigan', 'lanes+in+Michigan', 'alleys+in+Michigan', 'boulevards+in+Michigan', 'trails+in+Michigan', 'roads+in+Michigan',
    'highways+in+Illinois', 'lanes+in+Illinois', 'alleys+in+Illinois', 'boulevards+in+Illinois', 'trails+in+Illinois', 'roads+in+Illinois',
    'highways+in+Colorado', 'lanes+in+Colorado', 'alleys+in+Colorado', 'boulevards+in+Colorado', 'trails+in+Colorado', 'roads+in+Colorado',
    'highways+in+North+Carolina', 'lanes+in+North+Carolina', 'alleys+in+North+Carolina', 'boulevards+in+North+Carolina', 'trails+in+North+Carolina', 'roads+in+North+Carolina',
    'highways+in+Arizona', 'lanes+in+Arizona', 'alleys+in+Arizona', 'boulevards+in+Arizona', 'trails+in+Arizona', 'roads+in+Arizona',
    'highways+in+Arkansas', 'lanes+in+Arkansas', 'alleys+in+Arkansas', 'boulevards+in+Arkansas', 'trails+in+Arkansas', 'roads+in+Arkansas',
    'highways+in+Connecticut', 'lanes+in+Connecticut', 'alleys+in+Connecticut', 'boulevards+in+Connecticut', 'trails+in+Connecticut', 'roads+in+Connecticut',
    'highways+in+Iowa', 'lanes+in+Iowa', 'alleys+in+Iowa', 'boulevards+in+Iowa', 'trails+in+Iowa', 'roads+in+Iowa',
    'highways+in+Louisiana', 'lanes+in+Louisiana', 'alleys+in+Louisiana', 'boulevards+in+Louisiana', 'trails+in+Louisiana', 'roads+in+Louisiana',
    'highways+in+Kansas', 'lanes+in+Kansas', 'alleys+in+Kansas', 'boulevards+in+Kansas', 'trails+in+Kansas', 'roads+in+Kansas',
    'highways+in+Kentucky', 'lanes+in+Kentucky', 'alleys+in+Kentucky', 'boulevards+in+Kentucky', 'trails+in+Kentucky', 'roads+in+Kentucky',
    'highways+in+Maryland', 'lanes+in+Maryland', 'alleys+in+Maryland', 'boulevards+in+Maryland', 'trails+in+Maryland', 'roads+in+Maryland',
    'highways+in+Massachusetts', 'lanes+in+Massachusetts', 'alleys+in+Massachusetts', 'boulevards+in+Massachusetts', 'trails+in+Massachusetts', 'roads+in+Massachusetts',
    'highways+in+Maine', 'lanes+in+Maine', 'alleys+in+Maine', 'boulevards+in+Maine', 'trails+in+Maine', 'roads+in+Maine',
    'highways+in+Minnesota', 'lanes+in+Minnesota', 'alleys+in+Minnesota', 'boulevards+in+Minnesota', 'trails+in+Minnesota', 'roads+in+Minnesota',
    'highways+in+Missouri', 'lanes+in+Missouri', 'alleys+in+Missouri', 'boulevards+in+Missouri', 'trails+in+Missouri', 'roads+in+Missouri',
    'highways+in+Mississippi', 'lanes+in+Mississippi', 'alleys+in+Mississippi', 'boulevards+in+Mississippi', 'trails+in+Mississippi', 'roads+in+Mississippi',
    'highways+in+Nevada', 'lanes+in+Nevada', 'alleys+in+Nevada', 'boulevards+in+Nevada', 'trails+in+Nevada', 'roads+in+Nevada',
    'highways+in+Oklahoma', 'lanes+in+Oklahoma', 'alleys+in+Oklahoma', 'boulevards+in+Oklahoma', 'trails+in+Oklahoma', 'roads+in+Oklahoma',
    'highways+in+Indiana', 'lanes+in+Indiana', 'alleys+in+Indiana',  'trails+in+Indiana', 'roads+in+Indiana',
   
    'highways+in+Cuba', 'lanes+in+Cuba', 'alleys+in+Cuba',
    'highways+in+Mexico', 'lanes+in+Mexico', 'roads+in+Mexico',
    'highways+in+Brizil''lanes+in+Brizil', 'alleys+in+Brizil',
    'roads+in+Argentina', 'lanes+in+Argentina', 'streets+in+Argentina',
    'roads+in+Chile', 'lanes+in+Chile',
    'lanes+in+Peru', 'road+in+Peru', 'alleys+in+Peru',
    'alleys+in+Columbia', 'highways+in+Columbia', 'roads+in+Columbia', 'lanes+in+Columbia',

    'alleys+in+New+Zealand', 'roadsß+in+New+Zealand', 'highways+in+New+Zealand', 'lanes+in+New+Zealand',
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
    'roads+in+Heilongjiang', 'streets+in+Heilongjiang', 'highways+in+Heilongjiang',
    'roads+in+Hebei', 'streets+in+Hebei', 'highways+in+Hebei',
    'roads+in+Jiangsu', 'streets+in+Jiangsu', 'highways+in+Jiangsu',
    'roads+in+Henan', 'streets+in+Henan', 'highways+in+Henan',
    'roads+in+Hubei', 'streets+in+Hubei', 'highways+in+Hubei',
    'roads+in+Hunan', 'streets+in+Hunan', 'highways+in+Hunan',
    'roads+in+Anhui', 'streets+in+Anhui', 'highways+in+Anhui',
    'roads+in+Fujian', 'streets+in+Fujian', 'highways+in+Fujian',
    'roads+in+Gansu', 'streets+in+Gansu', 'highways+in+Gansu',
    'roads+in+Guangdong', 'streets+in+Guangdong', 'highways+in+Guangdong',
    'roads+in+Guizhou', 'streets+in+Guizhou', 'highways+in+Guizhou',
    'roads+in+Hainan', 'streets+in+Hainan', 'highways+in+Hainan',
    'roads+in+Jiangxi', 'streets+in+Jiangxi', 'highways+in+Jiangxi',
    'roads+in+Jilin', 'streets+in+Jilin', 'highways+in+Jilin',
    'roads+in+Liaoning', 'streets+in+Liaoning', 'highways+in+Liaoning',
    'roads+in+Qinghai', 'streets+in+Qinghai', 'highways+in+Qinghai',
    'roads+in+Shaanxi', 'streets+in+Shaanxi', 'highways+in+Shaanxi',
    'roads+in+Shandong', 'streets+in+Shandong', 'highways+in+Shandong',
    'roads+in+Shanxi', 'streets+in+Shanxi', 'highways+in+Shanxi',
    'roads+in+Sichuan', 'streets+in+Sichuan', 'highways+in+Sichuan',
    'roads+in+Yunnan', 'streets+in+Yunnan', 'highways+in+Yunnan',
    'roads+in+Zhejiang', 'streets+in+Zhejiang', 'highways+in+Zhejiang',
    'roads+in+Beijing', 'streets+in+Beijing', 'highways+in+Beijing',
    'roads+in+Shanghai', 'streets+in+Shanghai', 'highways+in+Shanghai',

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
    'roads+in+Moscow', 'streets+in+Moscow', 'lanes+in+Moscow',
    'roads+in+Saint+Petersburg', 'streets+in+Saint+Petersburg', 'lanes+in+Saint+Petersburg',
    'roads+in+Novosibirsk', 'streets+in+Novosibirsk', 'lanes+in+Novosibirsk',
    'roads+in+Yekaterinburg', 'streets+in+Yekaterinburg', 'lanes+in+Yekaterinburg',
    'roads+in+Kazan', 'streets+in+Kazan', 'lanes+in+Kazan',
    'roads+in+Nizhny+Novgorod', 'streets+in+Nizhny+Novgorod', 'lanes+in+Nizhny+Novgorod',
    'roads+in+Chelyabinsk', 'streets+in+Chelyabinsk', 'lanes+in+Chelyabinsk',

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
