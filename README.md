# community-datasets

There are two methods, one to extract the metadata and the other to store that metadata.

```get_datasets``` takes in 2 arguments - ```pages``` and ```page_size```.\
```pages``` is the page number of search results and ```page_size``` is the number of results per page.

```store``` takes in two arguments - ```data``` and ```filename```. It stores the data as csv.\
```data``` is the metadata returned from ```get_datasets``` and ```filename``` is the name of file where you want to store the data.

Please have a look at the first few lines of the following XML file before running the script. It'll help in understanding the schema and thereby deciding the parameters.\
https://api.openaire.eu/search/datasets?sortBy=resultdateofacceptance,descending&size=50&keywords=covid-19&page=1
