list of packages used:  
Flask  
Flask-Cors  
numpy  
scikit-learn  
xgboost  
fake-useragent  
selenium  
pytube  
webdriver-manager  
httpie

to test api in (venv)    
`http post http://127.0.0.1:8888 url=https://www.youtube.com/watch?v=Hu3Q9t6H4yw format=MP3`

adjustment made to pytube cipher.py due to changes from YouTube's end (2023-07-01)

added Procfile for deployment in Railway  

```python
# old
def get_throttling_function_name(js: str) -> str:
    # ...
    function_patterns = [
        # ...
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*'
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
    ]    
    # ...
    
# new
def get_throttling_function_name(js: str) -> str:
    # ...
    function_patterns = [
        # ...
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&.*?\|\|\s*([a-z]+)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
    ]
    # ...
```