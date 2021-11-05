# community-datasets

### Script
There are two methods, one to extract the metadata and the other to store that metadata.

```get_datasets``` takes in 2 arguments - ```pages``` and ```page_size```.\
```pages``` is the page number of search results and ```page_size``` is the number of results per page.

```store``` takes in two arguments - ```data``` and ```filename```. It stores the data as csv.\
```data``` is the metadata returned from ```get_datasets``` and ```filename``` is the name of file where you want to store the data.

Please have a look at the first few lines of the following XML file before running the script. It'll help in understanding the schema and thereby deciding the parameters.\
https://api.openaire.eu/search/datasets?sortBy=resultdateofacceptance,descending&size=50&keywords=covid-19&page=1

Please note that the number of total results returned by one query is limited to 10,000. For accessing the whole graph, use [OpenAIRE Research Graph dumps](https://develop.openaire.eu/graph-dumps.html). 

### API Documentation
The description of some entities is mentioned below.\
```Title```: the titles of the Result, each with a typology represented by a Qualifier and Provenance information\
```Description```: contains the Abstract of the Result\
```Collected From```: a Datasource from which metadata of this instance has been collected (e.g. an aggregator of institutional repositories)\
```DOI```: unique and persistent identifier used to identify the result together with the relative identification agency

For more information about the data model, visit the following link.\
https://zenodo.org/record/2643199#.YYVP5L1BxQI

For API documentation, visit the link below.\
https://develop.openaire.eu/api.html#datasets