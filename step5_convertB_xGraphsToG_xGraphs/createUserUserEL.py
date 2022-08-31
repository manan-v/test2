import pandas as pd
import itertools
import os


def createEL(org, activityType, source='../step3_convertJSONToMatrix/data/matrix_user_repo/', dest='../step4_convertMatrixToB_xGraphs/data/gml/user-user-EL/'):
    
    if os.path.exists(dest+org+'_'+activityType+'.edgelist'):
        pass
    else:
        source = source+activityType+'/'+org+'.csv'
        df = pd.read_csv(source)

        df_ = pd.DataFrame(index=df.iloc[:, 0].values,
                        columns=df.iloc[:, 0].values)
        df_ = df_.fillna(0)  # with 0s rather than NaNs

        # df without the first column
        df1 = df.iloc[:, 1:]
        with open(dest+org+'_'+activityType+'.edgelist','a') as elFile:
            for column in df1:
                # Get the indices in the column with 1 entries
                indices = [i for i, x in enumerate(df1[column].values) if x == 1]

                # Create combinations of the indices (as edgelist) - only once - if (i,j) is there, (j,i) won't be present
                for a, b in itertools.combinations(indices, 2):
                    edge=(df.iloc[:, 0][a], df.iloc[:, 0][b])
                    # df.to_csv(elFile, header=None, index=None, sep='\n', mode='a')
                    edge=str(edge)
                    edge=edge.replace('(','').replace("'","").replace(',','').replace(')','')
                    elFile.write(''.join(edge)+'\n')
                    # print(edge)
createEL('10gen','starred')