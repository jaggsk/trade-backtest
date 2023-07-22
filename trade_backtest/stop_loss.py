import pandas as pd
import pandas_ta as pta

def donchian_stop(df, lookback :int = None, pip_buffer = None, percent_buffer = None, pip_location = None):
    '''
    Function to create Donchian channel window on ohlc dataset.
    https://www.investopedia.com/terms/d/donchianchannels.asp

    (pd dataframe)(int)(int)(int)(int)->(pd dataframe)

    lookback = number of units over which to calculate the rolling min and max of price data 
    Requires am imput dataframe with Open High Low Close columns - note upper case first letter
    pip_buffer = window of number of pips above and below channels 
    pip_location = indicates decimal place resolution of pip
    percent_buffer = % window above and below channels 

    PRECONDITION: supplied dataframe has minimum High and Low columns
    KJAGGS JUly 2023

    '''
    assert isinstance(lookback, int), 'Function donchian_stop - lookback must be an integer'
    
    if pip_buffer is not None and percent_buffer is not None:
        raise Exception("Only one method of pip_buffer or percent buffer can be selected")
    
    if pip_buffer is not None:
        assert isinstance(pip_buffer, int), 'Function donchian_stop - pip_buffer must be an integer'
        
        if pip_location is not None:
            assert isinstance(pip_location, int) , 'Function donchian_stop - pip_location must be an integer'
     
            df['Donchian high'] = df['High'].rolling(lookback).max() + (1*(10**pip_location))
            df['Donchian low'] = df['Low'].rolling(lookback).min() - (1*(10**pip_location))
            
            return df
            
        else:
            raise Exception("Function donchian_stop -pip_location integer value required")
    
    if percent_buffer is not None:
        assert isinstance(percent_buffer, int) or isinstance(percent_buffer, float), 'Function donchian_stop - percent_buffer must be an integer'
        
        df['Donchian high'] = df['High'].rolling(lookback).max() * (100+percent_buffer)/100
        df['Donchian low'] = df['Low'].rolling(lookback).min() * (100-percent_buffer)/100
    
    
    return df

def atr_stop(df, atr_len :int = None, atr_mult = None, percent_buffer = None, pip_buffer = None ,pip_location : int= None):
    '''
    Function to create Average True Range (ATR) channel window on ohlc dataset.
    https://www.investopedia.com/terms/a/atr.asp

    (pd dataframe)(int)(int)(int)(int)->(pd dataframe)

    atr_len = number of units over which to calculate the average true range of price data 
    atr_mult = scalar applied to atr value
    Requires am imput dataframe with Open High Low Close columns - note upper case first letter
    pip_buffer = window of number of pips above and below channels 
    pip_location = indicates decimal place resolution of pip
    percent_buffer = % window above and below channels 

    PRECONDITION: supplied dataframe has a minimum of High and Low columns
    KJAGGS JUly 2023

    '''
    assert isinstance(atr_len, int), 'Function atr_stop - lookback atr period must be an integer'
    assert isinstance(atr_mult, (int,float)), 'Function atr_stop - atr_mult must be a float'
    
    if pip_buffer is not None and percent_buffer is not None:
        raise Exception("Function atr_stop - Only one method of pip_buffer or percent buffer can be selected")
    
    if pip_buffer is not None:
        assert isinstance(pip_buffer, int), 'Function atr_stop - pip_buffer must be an integer'
        
        if pip_location is not None:
            assert isinstance(pip_location, int) , 'Function atr_stop - pip_location must be an integer'
     
            df['ATR'] = pta.atr(df['High'],df['Low'],df['Close'],length = atr_len,mamode="RMA") 
    
            df['ATR High'] = df['High'] + (df['ATR'] * atr_mult) + (1*(10**pip_location))
            df['ATR Low'] = df['Low'] - (df['ATR'] * atr_mult) - (1*(10**pip_location))
            
            return df
            
        else:
            raise Exception("Function atr_stop - pip_location integer value required")
    
    elif percent_buffer is not None:
        assert isinstance(percent_buffer, int) or isinstance(percent_buffer, float), 'Function atr_stop - percent_buffer must be an integer'
        
        df['ATR'] = pta.atr(df['High'],df['Low'],df['Close'],length = atr_len,mamode="RMA") * atr_mult
        
        df['ATR High'] = (df['High'] + df['ATR']) * (100+percent_buffer)/100
        df['ATR Low'] = (df['Low'] - df['ATR']) * (100-percent_buffer)/100
    
    else:
        #no buffer on atr
        df['ATR'] = pta.atr(df['High'],df['Low'],df['Close'],length = atr_len,mamode="RMA") * atr_mult
        
        df['ATR High'] = (df['High'] + df['ATR'])
        df['ATR Low'] = (df['Low'] - df['ATR'])
    
    return df


def fixed_stop(df, percent_stop = None, pip_stop = None ,pip_location : int= None):
    '''
    Function to create fixed stop loss values on ohlc dataset.

    (pd dataframe)(int:float)(int)(int)->(pd dataframe)

    Requires am imput dataframe with Open High Low Close columns - note upper case first letter
    pip_buffer = window of number of pips above and below price 
    pip_location = indicates decimal place resolution of pip
    percent_buffer = % window above and below price 

    PRECONDITION: supplied dataframe has a minimum of High and Low columns
    KJAGGS JUly 2023

    '''

    if pip_stop is None and percent_stop is None:
        raise Exception("Function fixed_stop - One of pip_stop or percent_stop must be selected")
 
    if pip_stop is not None and percent_stop is not None:
        raise Exception("Function fixed_stop - Only one method of pip_stop or percent_stop can be selected")
    
    if pip_stop is not None:
        assert isinstance(pip_stop, int), 'Function fixed_stop - pip_stop must be an integer'
        
        if pip_location is not None:
            assert isinstance(pip_location, int) , 'Function fixed_stop - pip_location must be an integer'
     
            df['Pip High'] = df['High'] + (pip_stop*(10**pip_location))
            df['Pip Low'] = df['Low'] - (pip_stop*(10**pip_location))
            
            return df
            
        else:
            raise Exception("Function fixed_stop - pip_location integer value required")
    
    if percent_stop is not None:
        assert isinstance(percent_stop, int) or isinstance(percent_stop, float), 'Function fixed_stop - percent_buffer must be an integer'
        

        df['Percent High'] = (df['High']) * (100+percent_stop)/100
        df['Percent Low'] = (df['Low']) * (100-percent_stop)/100
    
    
    
    return df
