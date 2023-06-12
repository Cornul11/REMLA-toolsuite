import sys

import matplotlib.pyplot as plt
import pandas as pd

# print python executable used to run this script
print("Python executable: ", )

if len(sys.argv) < 2:
    print("Usage: ", sys.executable, " ", sys.argv[0], " <filename>")
    sys.exit(1)

filename = sys.argv[1]

df = pd.read_csv(filename)

# filter only finished submissions
df = df[df['Submissionreview submitted'] == True]

multivar_score_dict = {"Insufficient": 0, "Sufficient": 1,
                       "Good": 2, "Very Good": 3, "Excellent": 4}

binary_score_dict = {"Fail": 0, "Pass": 5}

# select columns starting with "R" and a number and a dot
score_columns = df.filter(regex='^R[0-9]+\.', axis=1).columns

# the columns we will use to compute the average score
mean_columns = []

# replace categorical scores with numerical ones and calculate the average score
for col in score_columns:
    if 'R9.' not in col and 'R12.' not in col:
        mean_columns.append(col)
        score_dict = multivar_score_dict if 'R10.' in col or 'R11.' in col else binary_score_dict
        # extract the score part of the answer
        df[col] = df[col].apply(lambda x: str(x).split(')')[1].split()[0] if pd.notnull(x) and ')' in str(x) else x)
        df[col] = df[col].replace(score_dict)
        df[col] = pd.to_numeric(df[col], errors='coerce')  # turn into numeric

# create a new column for the average score
df['average_score'] = df[mean_columns].mean(axis=1, skipna=True)

# Plotting the average score
plt.scatter(df.id, df['average_score'])
plt.title('Scatter plot of average scores')
plt.xlabel('Index')  # this can be changed to something more meaningful, but for now does well
plt.ylabel('Average score')
plt.show()
