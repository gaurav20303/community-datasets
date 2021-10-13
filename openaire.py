from urllib.request import urlopen
import csv
import json
import datetime

def get_datasets(pages, page_size):
    n = 1
    rows = []
    for i in range(1, pages+1):
        print(f"page{i}")
        try:
            url = f"https://api.openaire.eu/search/datasets?sortBy=resultdateofacceptance,descending&size={page_size}&keywords=covid-19&page={i}&format=json"
            response = urlopen(url)
            response = response.read()
            data_json = json.loads(response)

            for hit in data_json['response']['results']['result']:
                # print(hit['metadata']['oaf:entity']['oaf:result']['description']['$'])
                # break

                date_of_collection = hit['header']['dri:dateOfCollection']['$']
                # print(date_of_collection)
                if 'Z' in date_of_collection:
                    date_of_collection = date_of_collection[:19]
                else:
                    date_of_collection = date_of_collection[:-2] + ':' + '00'

                date_of_collection = datetime.datetime.fromisoformat(date_of_collection)
                date_of_collection = date_of_collection.strftime('%Y-%m-%d %H:%M:%S')

                date_of_transformation = ''
                if hit['header']['dri:dateOfTransformation'] != None:
                    date_of_transformation = hit['header']['dri:dateOfTransformation']['$']
                    # print(date_of_transformation)
                    if 'Z' in date_of_transformation:
                        date_of_transformation = date_of_transformation[:19]
                    else:
                        date_of_transformation = date_of_transformation[:-2] + ':' + '00'

                    date_of_transformation = datetime.datetime.fromisoformat(date_of_transformation)
                    date_of_transformation = date_of_transformation.strftime('%Y-%m-%d %H:%M:%S')

                if isinstance(hit['metadata']['oaf:entity']['oaf:result']['collectedfrom'], list):
                    collected_from = hit['metadata']['oaf:entity']['oaf:result']['collectedfrom'][0]['@name']
                else:
                    collected_from = hit['metadata']['oaf:entity']['oaf:result']['collectedfrom']['@name']

                original_id = ''
                if isinstance(hit['metadata']['oaf:entity']['oaf:result']['originalId'], list):
                    original_id = hit['metadata']['oaf:entity']['oaf:result']['originalId'][0]['$']
                else:
                    original_id = hit['metadata']['oaf:entity']['oaf:result']['originalId']['$']

                p_id = ''
                if 'pid' in hit['metadata']['oaf:entity']['oaf:result']:
                    if isinstance(hit['metadata']['oaf:entity']['oaf:result']['pid'], list):
                        p_id = hit['metadata']['oaf:entity']['oaf:result']['pid'][0]['$']
                    else:
                        p_id = hit['metadata']['oaf:entity']['oaf:result']['pid']['$']

                if isinstance(hit['metadata']['oaf:entity']['oaf:result']['title'], list):
                    title = hit['metadata']['oaf:entity']['oaf:result']['title'][0]['$']
                else:
                    title = hit['metadata']['oaf:entity']['oaf:result']['title']['$']

                best_access_right = hit['metadata']['oaf:entity']['oaf:result']['bestaccessright']['@classid']

                date_of_acceptance = hit['metadata']['oaf:entity']['oaf:result']['dateofacceptance']['$']

                keywords = ''
                if 'subject' in hit['metadata']['oaf:entity']['oaf:result']:
                    if isinstance(hit['metadata']['oaf:entity']['oaf:result']['subject'], list):
                        for keyword in hit['metadata']['oaf:entity']['oaf:result']['subject']:
                            keywords += keyword['$']
                            keywords += ','
                        keywords = keywords.rstrip(',')
                    else:
                        keywords = hit['metadata']['oaf:entity']['oaf:result']['subject']['$']

                language = hit['metadata']['oaf:entity']['oaf:result']['language']['@classname']

                if 'publisher' in hit['metadata']['oaf:entity']['oaf:result']:
                    publisher = hit['metadata']['oaf:entity']['oaf:result']['publisher']['$']
                else:
                    publisher = ''

                result_type = hit['metadata']['oaf:entity']['oaf:result']['resulttype']['@classname']
                resource_type = hit['metadata']['oaf:entity']['oaf:result']['resourcetype']['@classname']

                # context = hit['metadata']['oaf:entity']['oaf:result']['context']['@type']

                # linked_collected_from = ''
                # linked_publisher = ''
                # linked_doa = ''
                # linked_title = ''
                # linked_pid = ''
                #
                # if 'result' in hit['metadata']['oaf:entity']['oaf:result']['children']:
                #     for child in hit['metadata']['oaf:entity']['oaf:result']['children']['result']:
                #         linked_collected_from += child['collectedfrom'] + '|'
                #         linked_publisher += child['publisher'] + '|'
                #         linked_doa += child['dateofacceptance'] + '|'
                #         linked_title += child['title']['$'] + '|'
                #         linked_pid += child['pid']['$'] + '|'
                #     linked_collected_from = linked_collected_from.rstrip('|')
                #     linked_publisher = linked_publisher.rstrip('|')
                #     linked_doa = linked_doa.rstrip('|')
                #     linked_title = linked_title.rstrip('|')
                #     linked_pid = linked_pid.rstrip('|')

                if 'description' in hit['metadata']['oaf:entity']['oaf:result']:
                    if isinstance(hit['metadata']['oaf:entity']['oaf:result']['description'], list):
                        abstract = hit['metadata']['oaf:entity']['oaf:result']['description'][0]['$']
                    else:
                        abstract = hit['metadata']['oaf:entity']['oaf:result']['description']['$']
                else:
                    abstract = ''

                rd = ''
                # if 'relevantdate' in hit['metadata']['oaf:entity']['oaf:result']:
                #     for relevant_date in hit['metadata']['oaf:entity']['oaf:result']['relevantdate']:
                #         rd += relevant_date['@classname'] + ':' + relevant_date['$'] + ','
                #     rd = rd.rstrip(',')

                row = [n, title, abstract, publisher, date_of_acceptance, collected_from]
                rows.append(row)

                n += 1

        except Exception as e:
            print(e)

    return rows

def store(data, filename):
    heading = ['S.No.', 'Title', 'Abstract', 'Publisher', 'Date of Acceptance', 'Collected From']
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(heading)
        csvwriter.writerows(data)

data = get_datasets(200, 50)

store(data, 'openaire_research_datasets.csv')
print('DONE')
