import http.client
import json

#-------------------------------------------------------------
# Set your Okta Org URL
# In future, use form. Be sure to strip http:// and https://
#-------------------------------------------------------------

url = 'DOMAIN.okta.com' # <--------------------------------  EDIT THIS VALUE <<<<<<<<<<<<<<<<

# Prompt via cli for username, print what was entered
username = input("Enter your username(email): ")

# Such security. Use Okta apikey here for simplicty.
apikey = "OKTA_ADMIN_API_KEY" # <--------------------------------  EDIT THIS VALUE <<<<<<<<<<<<<<<<

# Connection to Okta using url and apikey.
conn = http.client.HTTPSConnection(url)
payload = ''
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Authorization': 'SSWS ' + str(apikey)
}

# API request to find the user ID based on a CLI input username
# In the future this would be pulled from a form. should add error cehcking
conn.request("GET", "/api/v1/users?q=" + username, payload, headers)
res = conn.getresponse()
data = res.read()
dataDecode = data.decode("utf-8")

# Using json.loads to find the 'id' from the json returned by the API call, then listing the (user) id.
# Second for loop finds the profile attribute login and saves that to login variable

data_dict = json.loads(dataDecode)

for s in range(len(data_dict)):
  if data_dict[s]["id"]:
    uid = data_dict[s]["id"]
    #print(uid)

for s in range(len(data_dict)):
  if data_dict[s]["profile"]["login"]:
    login = data_dict[s]["profile"]["login"]
#-----------------------------------------
#   USER GROUP IDS
# API request to Okta org to get Group IDs based on userID
#-----------------------------------------
conn.request("GET", "/api/v1/users/" + uid + "/groups", payload, headers)
res = conn.getresponse()
data = res.read()
dataDecode = data.decode("utf-8")

data_dict = json.loads(dataDecode)
gidStr = []

for s in range(len(data_dict)):
  if data_dict[s]["id"]:
    gidStr.append(data_dict[s]["id"])

#-----------------------------------------
#   SIGN ON POLICIES
# API request to Okta org to get Okta Sign On policy Ids
#-----------------------------------------
conn.request("GET", "/api/v1/policies?type=OKTA_SIGN_ON", payload, headers)
res = conn.getresponse()
data = res.read()
dataDecode = data.decode("utf-8")

# List Okta Sign On policies
data_dict = json.loads(dataDecode)
pname = []
pidStr = []
# The json returned has a nested list, thus the name here
nested_pidgroupStr = []

for s in range(len(data_dict)):
  if data_dict[s]["name"]:
    pname.append(data_dict[s]["name"])

for s in range(len(data_dict)):
  if data_dict[s]["id"]:
    pidStr.append(data_dict[s]["id"])

for s in range(len(data_dict)):
  if data_dict[s]["conditions"]["people"]["groups"]["include"]:
    nested_pidgroupStr.append(data_dict[s]["conditions"]["people"]["groups"]["include"])

# This flattens the list. Turning the nested list into a regular list. Easier to work with.
pidgroupStr = []
for elem in nested_pidgroupStr:
  pidgroupStr.extend(elem)

pnameFull = pname

#-----------------------------------------
#   ENROLLMENT POLICIES
# API request to Okta org to get Okta Enrollment policies
#-----------------------------------------
conn.request("GET", "/api/v1/policies?type=MFA_ENROLL", payload, headers)
res = conn.getresponse()
data = res.read()
dataDecode = data.decode("utf-8")

# List Okta Sign On policies
data_dict = json.loads(dataDecode)
enrollName = []
enrollStr = []
# The json returned has a nested list, thus the name here
nested_enrollgroupStr = []

for s in range(len(data_dict)):
  if data_dict[s]["name"]:
    enrollName.append(data_dict[s]["name"])

for s in range(len(data_dict)):
  if data_dict[s]["id"]:
    enrollStr.append(data_dict[s]["id"])

for s in range(len(data_dict)):
  if data_dict[s]["conditions"]["people"]["groups"]["include"]:
    nested_enrollgroupStr.append(data_dict[s]["conditions"]["people"]["groups"]["include"])

# This flattens the list. Turning the nested list into a regular list. Easier to work with.
enrollgroupStr = []
for elem in nested_enrollgroupStr:
  enrollgroupStr.extend(elem)

print()
enrollnameFull = enrollName

#-----------------------------------------
#   LIST USER DATA
# Creating a class to store info in for the User
#-----------------------------------------

class User:
  "This is for the username entered"
  def __init__(self, uid="00u", u="@email", g="00g"):
    self.uid = uid
    self.user = u
    self.group = g

# Create object for current user, assign values from earlier data, print it

current = User(uid, login, gidStr)
print("Okta Username: " + current.user)
print("Okta UserId: " + current.uid)

#-----------------------------------------
# Checking for Matches
#-----------------------------------------

print("\nChecking Sign On policies...")
for s in range(len(pidgroupStr)):
  if pidgroupStr[s] in gidStr:
    print("Sign On Policy Used : " + pnameFull[s])
    break
  else:
    print(".")

print("\nChecking Enrollment policies...")
for s in range(len(enrollgroupStr)):
  if enrollgroupStr[s] in gidStr:
    print("Enrollment Policy Used : " + enrollnameFull[s])
    print("")
    break
  else:
    print(".")
