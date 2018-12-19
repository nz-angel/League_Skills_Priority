import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('champions.csv')

subplots_pos = [131, 132, 133]
coldic = {'Q': 'xkcd:bright blue', 'W': 'xkcd:scarlet', 'E': 'xkcd:apple green'}

# General plot comparing what skills are maxed first, second and third
plt.figure(0)
for idx, skill in enumerate(list(df.keys()[1:4])):
        plt.subplot(subplots_pos[idx])
        df_fsm = df[skill].value_counts()
        plt.pie(df_fsm, labels=df_fsm.index, colors=[coldic[x] for x in df_fsm.index], startangle=90, autopct='%1.1f%%')
        plt.axis('equal')
        plt.title(skill)

# Plot showing what is the second skill maxed in the case of champions who max Q first
plt.figure(1)
df_ssm = df[df['First Skill Maxed'] == 'Q']['Second Skill Maxed'].value_counts()
plt.pie(df_ssm, labels=df_ssm.index, colors=[coldic[x] for x in df_ssm.index], startangle=90, autopct='%1.1f%%')
plt.axis('equal')
plt.title('Skill maxed after maxing Q')

# Plot showing how many champions use each of the six possible skill orders
plt.figure(2)
plt.pie(df['Skill Priority'].value_counts(), labels= df['Skill Priority'].value_counts().index, startangle=90,
        autopct='%1.1f%%')
plt.axis('equal')
plt.title('Combination of skill leveling')
plt.show()
