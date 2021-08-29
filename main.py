import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="darkgrid")

df = pd.read_csv("911.csv")
# Check the info() of the df
print(df.info())
# Check the head of df
print(df.head(3))

# ---------------
# Basic Questions
# ---------------

# What are the top 5 zipcodes for 911 calls?
grouped_by = df.groupby("zip").sum()
print(grouped_by.sort_values("e").iloc[::-1].head(5)["e"])

# What are the top 5 townships (twp) for 911 calls?
grouped_by = df.groupby("twp").sum()
print(grouped_by.sort_values("e").iloc[::-1].head(5)["e"])

# Take a look at the 'title' column, how many unique title codes are there?
print(df["title"].nunique())


# ---------------
# Creating new features
# ---------------

# In the titles column there are "Reasons/Departments" specified before the title code. These are EMS, Fire,
# and Traffic. Use .apply() with a custom lambda expression to create a new column called "Reason" that contains this
# string value.
#
# For example, if the title column value is EMS: BACK PAINS/INJURY , the Reason column value would be EMS.
df["Reason"] = df["title"].apply(lambda element: element.split(":")[0])
print(df["Reason"])

# What is the most common Reason for a 911 call based off of this new column?
print(df["Reason"].value_counts())

# Now use seaborn to create a countplot of 911 calls by Reason.
sns.set_context("notebook")
reason_plot = sns.displot(x="Reason", data=df, palette="flare")
reason_plot.figure.savefig("Plots/reason_plot.png")
plt.clf()

# What is the data type of the objects in the timeStamp column
print(df.dtypes)
# Use pd.to_datetime to convert the column from strings to DateTime objects.
df["timeStamp"] = pd.to_datetime(df["timeStamp"])
# Now that the timestamp column are actually DateTime objects, use .apply() to create 3 new columns called Hour,
# Month, and Day of Week. You will create these columns based off of the timeStamp column, reference the solutions if
# you get stuck on this step.
df["Hour"] = df["timeStamp"].dt.hour
df["Month"] = df["timeStamp"].dt.month
df["DayOfWeek"] = df["timeStamp"].dt.dayofweek

# Use the .map() with this dictionary to map the actual string names to the day of the week:
day_map = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
df["DayOfWeek"] = df["DayOfWeek"].map(day_map)

# Now use seaborn to create a countplot of the Day of Week column with the hue based off of the Reason column.
# sns.countplot(x="DayOfWeek", hue="Reason", data=df)
# Now do the same for Month:
month_plot = sns.countplot(x="Month", hue="Reason", data=df)
month_plot.figure.savefig("Plots/month_figure.png")
plt.clf()
# Now create a gropuby object called byMonth, where you group the DataFrame by the month column and use the count()
# method for aggregation. Use the head() method on this returned DataFrame
grouped_by = df.groupby("Month").count()
print(grouped_by.head(5))

# Now create a simple plot off of the dataframe indicating the count of calls per month.
x = grouped_by.index.values
y = grouped_by["e"]
fig, ax = plt.subplots()
ax.plot(x, y)
fig.savefig("Plots/count_of_calls_per_month.png")
plt.clf()
# Use seaborn's lmplot() to create a linear fit on the number of calls per month. Keep in mind you may need to reset
# the index to a column.
df_reset = grouped_by.reset_index()
reg_plot = sns.lmplot(x="Month", y="e", data=df_reset)
plt.ylabel("Suma")
reg_plot.figure.savefig("Plots/regression_lmplot.png")
plt.clf()

# Create a new column called 'Date' that contains the date from the timeStamp column.
df["Date"] = df["timeStamp"].apply(lambda element: element.date())
# Now groupby this Date column with the count() aggregate and create a plot of counts of 911 calls.
grouped_by = df.groupby("Date").count()
plt.figure(figsize=(20, 10))
lineplot = sns.lineplot(x="Date", y="e", data=grouped_by)
lineplot.figure.savefig("Plots/lineplot.png")

# Now recreate this plot but create 3 separate plots with each plot representing a Reason for the 911 call
for sub_plot in df["Reason"].unique():
    filtered_df = df[df["Reason"] == sub_plot]
    grouped_by = filtered_df.groupby("Date").count()
    plt.figure(figsize=(15, 10))
    lineplot = sns.lineplot(x="Date", y="e", data=grouped_by).set_title("{}".format(sub_plot))
    lineplot.figure.savefig("Plots/{}.png".format(sub_plot))
    plt.clf()

# Restructure the dataframe so that the columns become the Hours and the Index becomes the Day of the Week
multilevel = df.groupby(by=["DayOfWeek", "Hour"]).count()["Reason"].unstack()
# Create a HeatMap using this new DataFrame
heat_map = sns.heatmap(multilevel)
heat_map.figure.savefig("Plots/heatmap_day.png")
plt.clf()

# Create a clustermap using this DataFrame
cluster_map = sns.clustermap(multilevel)
cluster_map.figure.savefig("Plots/clustermap.png")

plt.clf()
# Repeat these same plots and operations, for a DataFrame that shows the Month as the column.
multilevel_month = df.groupby(by=["DayOfWeek", "Month"]).count()["Reason"].unstack()
new_heatmap = sns.heatmap(multilevel_month)
new_heatmap.figure.savefig("Plots/heatmap2.png")
plt.clf()
cluster_map = sns.clustermap(multilevel_month)
cluster_map.figure.savefig("Plots/clustermap2.png")
plt.clf()
