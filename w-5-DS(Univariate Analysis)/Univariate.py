class UnivariateBuilder():
    def quanQualFinder(dataset):
        quan=[]
        qual=[]
        for colName in dataset.columns:
            if dataset[colName].dtype =='O':
                qual.append(colName)
            else:
                quan.append(colName)
        return quan,qual 

    def createFreqTable(dataset,colName):
        freqTable = pd.DataFrame(columns=['Unique_values','Frequency','Relative_Frequency',"CumSum"])
        freqTable['Unique_values']=dataset[colName].value_counts().index
        freqTable['Frequency']=dataset[colName].value_counts().values
        freqTable['Relative_Frequency']=( freqTable['Frequency'] / len(dataset[colName].value_counts()))
        freqTable['CumSum']=freqTable['Relative_Frequency'].cumsum()
        return freqTable


    def Univariate(dataset,quan):
        descriptive = pd.DataFrame(index = ["Mean","Median","Mode","Q1:25%",
                                        "Q2:50%","Q3:75%","99%","Q4:100%","IQR","1.5Rule","Lesser","Grather","Min","Max","skew","kurtosis"                              
                                       ],columns=quan)
        for colName in quan:
            descriptive[colName]['Mean'] = dataset[colName].mean()
            descriptive[colName]['Median'] = dataset[colName].median()
            descriptive[colName]['Mode'] = dataset[colName].mode()[0]
            descriptive[colName]['Q1:25%'] = dataset.describe()[colName]["25%"]
            descriptive[colName]['Q2:50%'] = dataset.describe()[colName]["50%"]
            descriptive[colName]['Q3:75%'] = dataset.describe()[colName]["75%"]
            descriptive[colName]['99%'] = np.percentile(dataset[colName],99)
            descriptive[colName]['Q4:100%'] = dataset.describe()[colName]["max"]
            descriptive[colName]['IQR'] = descriptive[colName]['Q3:75%'] - descriptive[colName]['Q1:25%']
            descriptive[colName]['1.5Rule'] = 1.5 * descriptive[colName]['IQR']
            descriptive[colName]['Lesser'] = descriptive[colName]['Q1:25%'] - descriptive[colName]['1.5Rule'] #Q1-1.5*IQR = Q1-descriptive[colName]['1.5Rule']
            descriptive[colName]['Grather'] = descriptive[colName]['Q3:75%'] + descriptive[colName]['1.5Rule'] #Q3+1.5*IQR = Q1-descriptive[colName]['1.5Rule']
            descriptive[colName]['Min'] = dataset[colName].min() #Min values have to calc from dataset
            descriptive[colName]['Max'] = dataset[colName].max() #Max values have to calc from dataset
            descriptive[colName]['skew'] = dataset[colName].skew()
            descriptive[colName]['kurtosis'] = dataset[colName].kurtosis()
        return descriptive


    def FindOutlierCol(quan):
        lessorCol=[]
        greaterCol=[]    
        for colName in quan:
            if(descriptive[colName]["Lesser"] >  descriptive[colName]["Min"]):
                lessorCol.append(colName)
        
            if(descriptive[colName]["Grather"] <  descriptive[colName]["Max"]):
             greaterCol.append(colName)
    
        return lessorCol,greaterCol


    def ReplacingOutliers(dataset,lessorCol,greaterCol):
        for colName in lessorCol:
            dataset[colName][dataset[colName] < descriptive[colName]["Lesser"]] =  descriptive[colName]["Lesser"]
         
        for colName in greaterCol:
            dataset[colName][dataset[colName] > descriptive[colName]["Grather"]] =  descriptive[colName]["Grather"] 
        return dataset