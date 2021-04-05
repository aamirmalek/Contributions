import requests
import json
import yaml
import os

apiKey= input("Enter API Key:")

query=""" 
{
  actor {
    entitySearch(queryBuilder: {type: DASHBOARD}) {
      results {
        entities {
          ... on DashboardEntityOutline {
            guid
            name
          }
        }
      }
    }
  }
}
"""

query1=""" 
{
  actor {
    entity(guid: "%s") {
      ... on DashboardEntity {
        pages {
          name
          widgets {
            visualization { id }
            title
            layout { row width height column }
            rawConfiguration
          }
        }
      }
    }
  }
}
"""

url = "https://api.newrelic.com/graphql"
headers = {"content-type": "application/yaml", "Accept-Charset": "UTF-8","Api-Key": "%s" %apiKey}
headers1 = {"content-type": "application/json", "Accept-Charset": "UTF-8","Api-Key": "%s" %apiKey} 
r = requests.get(url, data=query, headers=headers)
listOfAllDashboard = r.text


path = os.getcwd()+'\\new-relic-repo\\dashboards'
os.chdir(path)

with open('listOfAllDashboard.yaml','w') as yaml_file:
    
    list1 = yaml.load(listOfAllDashboard, Loader=yaml.FullLoader)
    result= (list1["data"]["actor"]["entitySearch"]["results"]["entities"])
    array_length=len(result)
    yaml_file.close()
    os.remove("listOfAllDashboard.yaml")


for i in range(array_length):
    guidList=(result[i]["guid"])
    nameList=(result[i]["name"])
    print(guidList)
    print(nameList)

    if not ' / ' in nameList:

        r1 = requests.get(url, data=query1 %guidList, headers=headers1)
        dashaboardData = r1.json()
        result1= (dashaboardData["data"]["actor"]["entity"]["pages"][0])

        with open('%s.json' %nameList, 'w')  as f:
            json.dump(result1,f,indent=2)
            f.close()