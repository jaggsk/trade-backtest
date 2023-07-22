import pandas as pd

def donchian_stop(df, lookback :int = None, pip_buffer = None, percent_buffer = None, pip_location = None):
    '''
    Function to create Donchian channel window on ohlc dataset.
    https://www.investopedia.com/terms/d/donchianchannels.asp

    lookback = number of units over which to calculate the rolling min and max of price data 
    Requires am imput dataframe with OPen High Low Close columns
    pip_buffer = window of number of pips above and below channels 
    pip_location = indicates decimal place resolution of pip
    percent_buffer = % window above and below channels 

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
            raise Exception("pip_location integer value required")
    
    if percent_buffer is not None:
        assert isinstance(percent_buffer, int) or isinstance(percent_buffer, float), 'Function donchian_stop - percent_buffer must be an integer'
        
        df['Donchian high'] = df['High'].rolling(lookback).max() * (100+percent_buffer)/100
        df['Donchian low'] = df['Low'].rolling(lookback).min() * (100-percent_buffer)/100
    
    
    return df