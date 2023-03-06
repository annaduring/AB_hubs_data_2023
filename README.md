## Data Assignment deliverables

- Code required to arrive at the final solution. 
- Architecture diagram with the transformation pipeline and the ERD of the data.
- Basic insights on the holes’ data. | Insights.ipynb
- Basic insights on the size, structure and volume of data. | Insights.ipynb

## Approach:
I kept the apprach fairly simple:
- explore the dataset in a Jupyter notebook, to get some idea of the dataset and the holes’ data.
- extract the parquet file and run some transformation in pandas and arrive to 2 dataframes:
    - parts: it contains the uuid, some timestamp columns and the status of the job
    - part_measures: it contains the radius and lenght info form the uuid with a center
- load thesethe csv to a postgres database
- join the tables and arrive at the final solution. 



## Caveats:
- I believe pandas works fine with a small dataset, for a bigger dataset the in-memory package might not be sufficient
- pandas tends to guess the data type so some data type corrections need to explicit (it would be if I were to use C anyway..) <- which I don't..

## Run the code
To run the code, run the filerunfile.bat

### Using pyspark/Spark
I tried this approach as well and I am adding the line-by-line code too. It will require pyspark/Spark/Hadoop setup

### Architecture
![alt text](https://github.com/annaduring/AB_hubs_data_2023/blob/main/architecture.PNG?raw=true)

### ERD of the data
![alt text](https://github.com/annaduring/AB_hubs_data_2023/blob/main/ab_ERD_hubs.png?raw=true)


