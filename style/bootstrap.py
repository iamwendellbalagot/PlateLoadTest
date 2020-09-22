
class Bootstrap:
    def __init__(self):
        pass
    def getStylesheet(self):
        external_stylesheets = [
            'https://codepen.io/chriddyp/pen/bWLwgP.css',
            {
                'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
                'rel': 'stylesheet',
                'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
                'crossorigin': 'anonymous'
            }
        ]
        return external_stylesheets
        
    def getScripts(self):
        external_scripts = [
            'https://www.google-analytics.com/analytics.js',
            {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
            {
                'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
                'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
                'crossorigin': 'anonymous'
            }
        ]
        
        return external_scripts
