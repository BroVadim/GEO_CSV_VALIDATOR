import pandas as pd
import numpy as np
from typing import List
import traceback

def columns_validator(
    method :str,
    columns : List[str]
    )->bool:
    method_columns = {
        'markers':['lat1','lon1','popup1','marker_size','marker_color'],
        'route':['lat1', 'lon1', 'lat2','lon2','popup1','popup2','line_width','line_color'],
        'polygon':['lat1','lon1'],
        'heatMap':['lat1','lon1','marker_size']
    }
    try:
        pattern_columns = set(method_columns[method])
        #issubset не подходит, если в фрейме меньше нужных колонок но остальные подходят
        result = set(columns) & pattern_columns == pattern_columns
    except:
        print(f'Error - {traceback.format_exc()}')
        result  = False
    finally:
        return result

def column_type_validator(
    method :str,
    df:pd.DataFrame
    ) -> bool:
    markers_method = [
        ('lat1', float),('lon1', float),
        ('popup1',str),('marker_size','int64')
    ]
    route_method = [
            ('lat1',float),('lon1',float),
            ('lat2',float),('lon2',float),
            ('popup1',str),('popup2',str),
            ('line_width','int64'),('line_color',str),
    ]
    polygon_method = [
        ('lat1',float),('lon1',float)
    ]
    heatMap_method = [
        ('lat1', float),('lon1', float),
        ('marker_size','int64')
    ]
    methods_dfs = {
        'markers': pd.DataFrame(
            {k: pd.Series(dtype=t) for k, t in markers_method}
        ),
        'route': pd.DataFrame(
            {k: pd.Series(dtype=t) for k, t in route_method}
        ),
        'polygon': pd.DataFrame(
            {k: pd.Series(dtype=t) for k,t in polygon_method}
        ),
        'heatMap': pd.DataFrame(
            {k: pd.Series(dtype=t) for k,t in heatMap_method}
        )
    }
    try:
        #our_df-создает словарь имя_колонки:тип_данных для входного фрейма
        our_df = dict(df[methods_dfs[method].columns].dtypes)
        # method_df-создает словарь имя_колонки:тип_данных для фрейма методов
        method_df = dict(methods_dfs[method].dtypes)
        result = (our_df == method_df)
    except:
        result = False
        print(f'Произошла ошибка: {traceback.format_exc()}')
    finally:
        return result

def column_nan_validator(
    df:pd.DataFrame
    )->bool:
    try:
        result = all(
            df.replace('', np.nan).notna().all()
        )
    except:
        result = False
        print(f'Произошла ошибка {traceback.format_exc()}')
    finally:
        return result

def coordinates_validator(
    method:str,
    df:pd.DataFrame
    )->bool:
    # ЕЩЕ РАЗ ПРОВЕРИТЬ ИНТЕРВАЛЫ ДЛЯ ДОЛГОТЫ И ШИРОТЫ
    def latlng_validator(latlngs, type_coord):
        #если значение широта,оно должно быть в интервале [-90,90]
        if type_coord == 'lat':
            Llim, Rlim = -90, 90
        #если значение долгота,оно должно быть в интервале [-180,180]
        elif type_coord =='lon':
            Llim, Rlim = -180, 180
        latlng_validation = []
        for latlng in latlngs:
            # с помощью lambda-выражения проверяем элементы списка на принадлежность заданному интервалу
            validation = list(
                map(
                    lambda x: True if x >= Llim and x <= Rlim else False,
                    latlng
                )
            )
            latlng_validation.append(all(validation))
        return all(latlng_validation)
    
    if method in ['markers','heatmap','polygon']:
        cols_count = 2
    elif method in ['route']:
        cols_count = 4
    else:
        raise TypeError
    try:
        if cols_count == 2:
            lat1, lon1 = df['lat1'].tolist(), df['lon1'].tolist()
            result_validation = [
                latlng_validator([lat1],'lat'),
                latlng_validator([lon1], 'lon')
            ]
        elif cols_count== 4:
            lat1, lon1 = df['lat1'].tolist(), df['lon1'].tolist()
            lat2, lon2 = df['lat2'].tolist(), df['lon2'].tolist()
            result_validation = [
                latlng_validator([lat1, lat2],'lat'),
                latlng_validator([lon1, lon2],'lon')
            ]
        else:
            raise TypeError
        result = all(result_validation)
    except:
        result = False
        print(f'В ходе работы произошла ошибка {traceback.format_exc()}')
    finally:
        return result