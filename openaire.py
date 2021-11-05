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
                # print(result['description']['$'])
                # break
                result = hit['metadata']['oaf:entity']['oaf:result']
                # IN USE
                title = ''
                if 'title' in result:
                    if isinstance(result['title'], list):
                        for val in result['title']:
                            title += val['$']
                            title += ' | '
                        title = doi.rstrip(' | ')
                    else:
                        title = result['title']['$']

                abstract = ''
                if 'description' in result:
                    if isinstance(result['description'], list):
                        for val in result['description']:
                            abstract += val['$']
                            abstract += ' | '
                        abstract = abstract.rstrip(' | ')
                    else:
                        abstract = result['description']['$']

                publisher = ''
                if 'publisher' in result:
                    publisher = result['publisher']['$']

                date_of_acceptance = ''
                if 'dateofacceptance' in result:
                    date_of_acceptance = result['dateofacceptance']['$']

                collected_from = ''
                if 'collectedfrom' in result:
                    if isinstance(result['collectedfrom'], list):
                        for val in result['collectedfrom']:
                            collected_from += val['@name']
                            collected_from += ' | '
                        collected_from = collected_from.rstrip(' | ')
                    else:
                        collected_from = result['collectedfrom']['@name']

                doi = ''
                if 'pid' in result:
                    if isinstance(result['pid'], list):
                        for val in result['pid']:
                            doi += val['$']
                            doi += ' | '
                        doi = doi.rstrip(' | ')
                    else:
                        doi = result['pid']['$']
                        
                        
                # NOT IN USE
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

                original_id = ''
                if isinstance(result['originalId'], list):
                    original_id = result['originalId'][0]['$']
                else:
                    original_id = result['originalId']['$']

                best_access_right = result['bestaccessright']['@classid']


                keywords = ''
                if 'subject' in result:
                    if isinstance(result['subject'], list):
                        for keyword in result['subject']:
                            keywords += keyword['$']
                            keywords += ','
                        keywords = keywords.rstrip(',')
                    else:
                        keywords = result['subject']['$']

                language = result['language']['@classname']

                result_type = result['resulttype']['@classname']
                resource_type = result['resourcetype']['@classname']

                # context = result['context']['@type']

                # linked_collected_from = ''
                # linked_publisher = ''
                # linked_doa = ''
                # linked_title = ''
                # linked_pid = ''
                #
                # if 'result' in result['children']:
                #     for child in result['children']['result']:
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


                rd = ''
                # if 'relevantdate' in result:
                #     for relevant_date in result['relevantdate']:
                #         rd += relevant_date['@classname'] + ':' + relevant_date['$'] + ','
                #     rd = rd.rstrip(',')

                row = [n, title, abstract, publisher, date_of_acceptance, collected_from, doi]
                rows.append(row)

                n += 1

        except Exception as e:
            print(e)

    return rows

def store(data, filename):
    heading = ['S.No.', 'Title', 'Abstract', 'Publisher', 'Date of Acceptance', 'Collected From', 'DOI']
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(heading)
        csvwriter.writerows(data)

data = get_datasets(200, 50)

store(data, 'openaire_research_datasets.csv')
print('DONE')
