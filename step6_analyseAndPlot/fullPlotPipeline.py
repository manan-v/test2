'''
Input: user-repo CSV
PreReq: 
1) For P1-P4: orgName_starred.gml AND orgName_subscriptions.gml in gml/user-repo-GML/
2) For P7-P8: orgName_starred.csv AND orgName_subscriptions.csv in matrix_user_repo/starred/adjacency/ and matrix_user_repo/subscriptions/adjacency/
'''
import degreeDistribution
import createUserUserEL
import createGML
import louvain
import clusteringCoefficient

import os, time  
start=time.time()
def fullPlotPipeline(org):
    startOrg = time.time()
    try:
        # Create GML from CSV
        # createGML.createFromCSV(org, activityType='starred')
        # createGML.createFromCSV(org, activityType='subscriptions')

        if not os.path.exists('latest-matrix-plots/'+org):
            os.makedirs('latest-matrix-plots/'+org)
        # Generate user-user edgeList; Input: user-repo GML
        # createUserUserEL.createEL(org, 'starred')
        # createUserUserEL.createEL(org, 'subscriptions')

        # # Generate user-user GML; Input: user-user edgeList
        # createGML.createFromEL(org, activityType='starred')
        # createGML.createFromEL(org, activityType='subscriptions')
        # Clustering Coefficient plots
        # clusteringCoefficient.calcClusteringCoefficient(
        #     org, activityType='starred')
        # clusteringCoefficient.calcClusteringCoefficient(
        #     org, activityType='subscriptions')
        # # Plot P7-P8; Input: user-user GML
        
        # louvain.findCommunity(org, activityType='starred')
        # louvain.findCommunity(org, activityType='subscriptions')
        # degreeDistribution.P7toP8(org, activityType='starred')
        # degreeDistribution.P7toP8(org, activityType='subscriptions')

        
        # # Generate P1-P4 + P9-P12
        degreeDistribution.allForOrg(org+'_starred')
        degreeDistribution.allForOrg(org+'_subscriptions')

        # # Plot P5-P6; Input: user-user GML
        # # Manually from Gephi

        
    except:
        print("err for "+org)

    endOrg = time.time()
    print("Time taken for "+org+": "+str(round(endOrg-startOrg))+" sec")


orgList = ['10gen','a2c','acknet','cappuccino','codemonkeylabs','cogenda','cohesive','defensio','elevatedrails','flywheelnet','fs','gnip','handlino','lrug','mangos','reddit','salesforce','yahoo','yeebase']
# orgList=['a2c']
orgList.sort()
for org in orgList:
    org=org.replace('.csv','')
    print(org)
    fullPlotPipeline(org)
    # break
end=time.time()
print("Total time for "+str(len(orgList))+" orgs: "+str(round(end-start))+" sec")
