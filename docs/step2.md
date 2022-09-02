# Step 2 - Obtain Member Activity 
## Functions 
1) `getContributorList(orgName,repo_details_dir)`
   1) Input Paramaters
      1) **orgName** - Name of organisation (without `.json` extension) (`10gen`)
      2) **repo_details_dir** - Path of folder containing JSON files. The default path is _step1_obtainRepoDetails/data/repo_details/_
   2) Return Value
      1) **contributorList** - a sorted list that contains list of contributors, excluding users with key `login`
2) `getrepoForContributor(conributor, activityType)`
   1) INput Parameters
      1) **contributor** 
      2) **activityType**
## Input 
* orgName.json from `step1`
* 