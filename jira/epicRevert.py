## Simple script to revert a bulk change to a specific epic

import requests
import json

## Your info here. Note "site" is the part before "atlassian.net"
epic = "EPIC_NUM"
site = "YOU_SITE"
token = "TOKEN_HERE"


headers = {
  "Accept": "application/json",
  "Content-Type": "application/json",
  "Authorization": "Basic %s"%token
}


## Get Issues in an Epic
def getIssues(epic):
    url = "https://{}.atlassian.net/rest/api/3/search?jql=parent={}".format(site, epic)
    # +order+by+key&startAt=100
    response = requests.request(
       "GET",
       url,
       headers=headers
    )

    json_epic = json.loads(response.text)
    keys = []

    for issue in json_epic["issues"]:
        keys.append(issue["key"])

    print(keys)
    return(keys)

## Update Issue's Parent
def updateParent(key,change):
    print("Updating parent of {} to {}".format(key, change))
    url = "https://{}.atlassian.net/rest/api/3/issue/{}".format(site, key)

    payload = json.dumps({
        "fields": {
            "parent": {
                "id": change}
        }})
    response = requests.request(
        "PUT",
        url,
        data=payload,
        headers=headers,
    )
    print(response.text)


## Get Previous Epic (and then call updateParent())
def getChanges(keys):
    for key in keys:
        url = "https://{}.atlassian.net/rest/api/2/issue/{}/changelog".format(site, key)
        response = requests.request(
           "GET",
           url,
           headers=headers
        )
        json_issue = json.loads(response.text)
        change = [0,0]
        for entry in json_issue["values"]:
            id = entry["id"]
            for item in entry["items"]:
                field = item["field"]
                if field == "IssueParentAssociation" and type(item["fromString"]) == str:
                    if int(id) > int(change[0]):
                         change = [id, item["fromString"]]
        if change[1] != 0:
            print(key,change[1])
            updateParent(key,change[1])


getChanges(getIssues(epic))
