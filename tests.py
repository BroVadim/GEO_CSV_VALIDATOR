
import pytest
from validator import *

@pytest.mark.parametrize(
    'method, columns, expected_result',
    [
        ('markers',['lat1','lon1','popup1','marker_size','marker_color'],True),
        ('markers',['lat1', 'lon1', 'lat2','lon2','popup1','popup2','line_width','line_color'],False),
        ('markers',['lat1', 'lon1','marker_size','lat2','lon2','popup1','popup2','marker_color','line_width','line_color'],True),
        ('markers',['lat1','lon1'],False),
        ('markers',['lat','lon','marker_size'],False),
        ('markers',[1,2,3,4],False),
        ('markers',[None,None,None,None],False),
        ('markers',True,False),
        ('markers',False,False),
        ('markers',0,False),
        ('markers',[],False),
        ('markers',None,False),
        ('markers','',False),

        ('route',['lat1','lon1','popup1','marker_size'],False),
        ('route',['lat1', 'lon1', 'lat2','lon2','popup1','popup2','line_width','line_color'],True),
        ('route',['lat1','lon1'],False),
        ('route',['lat','lon','marker_size'],False),
        ('route',[1,2,3,4],False),
        ('route',[None,None,None,None],False),
        ('route',True,False),
        ('route',False,False),
        ('route',0,False),
        ('route',[],False),
        ('route',None,False),
        ('route','',False),

        ('polygon',['lat1','lon1'], True),
        ('polygon',['lat1', 'lon1', 'lat2','lon2','popup1','popup2','line_width','line_color'],True),
        ('polygon',[None,None],False),
        ('polygon',True,False),
        ('polygon',False,False),
        ('polygon',0,False),
        ('polygon',[],False),
        ('polygon',None,False),
        ('polygon','',False),
        ('polygon',['lat','lon'],False),
        ('polygon',[1,2,3,4],False),


        ('heatMap',['lat1','lon1','marker_size'], True),
        ('heatMap',['lat1', 'lon1', 'lat2','lon2','popup1','popup2','line_width','line_color','marker_size'],True),
        ('heatMap',[None,None,None],False),
        ('heatMap',True,False),
        ('heatMap',False,False),
        ('heatMap',0,False),
        ('heatMap',[],False),
        ('heatMap',None,False),
        ('heatMap','',False),
        ('heatMap',['lat','lon','marker_size'],False),
        ('heatMap',[1,2,3,4],False),
    ]
)
def test_columns_validator(method,columns,expected_result):
    assert columns_validator(method, columns)== expected_result, f'Произошла ошибка в комбинации {method}:{columns}:{expected_result}'

markers_method = [
    ('lat1', float),('lon1', float),
    ('popup1',str),('marker_size','int64')
]
route_method = [
    ('lat1',float),('lon1',float),
    ('lat2',float),('lon2',float),
    ('popup1',str),('popup2',str),
    ('line_width','int64'),('line_color',str)
]

#неверные типы данных для полей метода markers
test1 = [
    ('lat1','int64'),('lon1',float),
    ('popup1',str),('marker_size',str)
]

#неверные типы данных для полей метода route
test2 = [
    ('lat1','int64'),('lon1',float),
    ('lat2',float),('lon2',float),
    ('popup1',str),('popup2',str),
    ('line_width',str),('line_color',str)
]

def create_test_frame(data):
    df = pd.DataFrame({k: pd.Series(dtype=t) for k,t in data})
    return df

@pytest.mark.parametrize(
    'method, df, expected_result',
    [
        ('markers',create_test_frame(markers_method),True),
        ('markers',create_test_frame(test1),False),
        ('markers',None,False),
        ('markers','text_data',False),
        ('markers',0,False),
        ('markers',pd.DataFrame(), False),
        ('markers', pd.DataFrame(columns=['lat1','lon1','popup1','popup2','marker_size']), False),
        ('route',pd.DataFrame(), False),
        ('route',0,False),
        ('route','text_data',False),
        ('route',None,False),
        ('route',create_test_frame(test2),False),
        ('route',create_test_frame(route_method),True),
        ('route', pd.DataFrame(columns=['lat1','lon1','lat2','lon2','popup1','popup2','line_width','line_color']), False)
    ]
)
def test_column_type_validator(method, df,expected_result):
    assert column_type_validator(method, df) == expected_result, f'Проблема в наборе {method}:\n{df[:5]}:{expected_result}'

# Фрейм с валидными данными
nan_frame_test1 = pd.DataFrame({
    'lat1': [34.2914, 19.2355, 12.2552],
    'lon1': [56.9679, 41.1556, 10.4367],
    'popup1':['test1','test2','test3'],
    'marker_size':[4,6,3]
})
# Фреймы с невалидными данными
# пустое значение в данных с координатами
nan_frame_test2 = pd.DataFrame({
    'lat1': [34.2914, None, 12.2552],
    'lon1': [56.9679, 41.1556, 10.4367],
    'popup1':['test1','test2','test3'],
    'marker_size':[4,6,3]
})
# пустое значение в текстовых данных
nan_frame_test3 = pd.DataFrame({
    'lat1': [34.2914, 19.2355, 12.2552],
    'lon1': [56.9679, 41.1556, 10.4367],
    'popup1':['test1','','test3'],
    'marker_size':[4,6,3]
})

@pytest.mark.parametrize(
    'df, expected_result',
    [
        (nan_frame_test1,True),
        (nan_frame_test2,False),
        (nan_frame_test3,False)
    ]
)
def test_column_nan_validator(df, expected_result):
   assert column_nan_validator(df)==expected_result,f'Ошибка в данных {df}\n{expected_result}'

@pytest.mark.parametrize(
        'method, lat1, lon1, lat2, lon2, expected_result',
        [('markers', 34.5612, 30.4356, None, None, True),    # true values
        ('markers', -120.2345, 30.4356, None, None, False), # lat1 < -90
        ('markers',  120.2345, 30.4356, None, None, False), # lat1 > 90
        ('markers', None, 30.4356, None, None, False),      # lat1 = None
        ('markers','string', 30.4356, None, None, False),   # lat1 = str
        ('markers',[], 30.4356, None, None, False),         # lat1 = []
        ('markers', 10.2345, -191.4356, None, None, False), # lon1 < -180
        ('markers', 20.2345,  191.4356, None, None, False), # lon1 > 180
        ('markers', 20.2345, None, None, None, False),      # lon1 = None
        ('markers', 20.2345, 'string', None, None, False),  # lon1 = str
        ('markers', 20.2345, [], None, None, False),        # lon1 = []
        ('route', 34.5612, 30.4356, 30.4356, 34.5612, True),    # true values+
        ('route', 34.5612, 30.4356, -120.2345, 34.5612, False), # lat2 < -90 +
        ('route', 34.5612, 30.4356, 120.2345, None, False),     # lat2 > 90 +
        ('route', 34.5612, 30.4356, None, 34.5612, False),      # lat2 = None+
        ('route', 34.5612, 30.4356, 'string', None, False),     # lat2 = str+
        ('route', 34.5612, 30.4356, [], None, False),           # lat2 = []+
        ('route', 34.5612, 30.4356, None, -191.4356, False),    # lon2 < -180+
        ('route', 34.5612, 30.4356, 30.4356, 191.4356, False),  # lon2 > 180+
        ('route', 34.5612, 30.4356, 30.4356, None, False),      # lon2 = None
        ('route', 34.5612, 30.4356, 30.4356, 'string', False),  # lon2 = str+
        ('route', 34.5612, 30.4356, None, [], False)]            # lon2 = [] +
)
def test_coordinates_validator(method, lat1,lon1, lat2,lon2, expected_result):
    test_data = {
        'lat1': [lat1],'lon1': [lon1],
        'lat2': [lat2],'lon2': [lon2]
    }
    test_df = pd.DataFrame(test_data)
    assert coordinates_validator(method,test_df) == expected_result