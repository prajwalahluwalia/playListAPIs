# playListAPIs

Data Storage - The data is stored in the form of dataframe locally and used in the code.

************************How to use************************

1. Take a pull from branch, open the folder using your preferred code editor.

2. create a virtual environment, activate it and do "pip install -r requirements.txt"

3. do `flask run --port={port_number}` in cmd and open `http://127.0.0.1:{port-number}/` to access the application. Default port flask operates in is 5000.

************************Extra points************************

The search bar can fetch the records present in the store.

For starters the ratings will be `NA` but you can give ratings to the song by clicking on it and selecting preferred radio button, ratings can be given from range 1-5. left most being 1 and right most being 5.

Lyrics functionality is not working as third party APIs are not functional. provided the feature as it seemed really cool to have a lyrics section as well.