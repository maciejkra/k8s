"""
   Application entry
"""
from api.info import APP


if __name__ == '__main__':
    APP.run(debug=False, host='0.0.0.0', port='5002')
