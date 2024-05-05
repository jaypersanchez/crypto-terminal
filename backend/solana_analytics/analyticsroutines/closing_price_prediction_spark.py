# Based on Linear Regression
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator

# Initialize Spark Session
spark = SparkSession.builder.appName("SolanaPricePrediction").getOrCreate()

# Load the dataset /FileStore/tables/sol_exchange_data.csv
data_path = "../data/sol_exchange_data.csv"
df = spark.read.csv(data_path, header=True, inferSchema=True)

# Selecting the features (independent variables) and the label (dependent variable)
df = df.select("open_price", "close_price")

# Assembling the features into a feature vector
featureAssembler = VectorAssembler(inputCols=["open_price"], outputCol="features")
output = featureAssembler.transform(df)

# Finalize the data preparation for model training
finalized_data = output.select("features", "close_price")

# Split the data into training and test sets
train_data, test_data = finalized_data.randomSplit([0.7, 0.3])

# Initialize and train the linear regression model
lr = LinearRegression(featuresCol="features", labelCol="close_price")
lr_model = lr.fit(train_data)

# Make predictions on the test data
predictions = lr_model.transform(test_data)

# Evaluate the model
evaluator = RegressionEvaluator(labelCol="close_price", predictionCol="prediction", metricName="rmse")
rmse = evaluator.evaluate(predictions)
print(f"Root Mean Squared Error (RMSE) on test data: {rmse}")

# Show model coefficients
print(f"Coefficients: {lr_model.coefficients} Intercept: {lr_model.intercept}")

# Example of making a prediction
# Assuming you want to predict the closing price for an opening price of 60
new_data = spark.createDataFrame([(60,)], ["open_price"])
new_data = featureAssembler.transform(new_data)
new_prediction = lr_model.transform(new_data)
new_prediction.show()
