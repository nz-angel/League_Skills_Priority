import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('champions.csv')
subplots_pos = [131, 132, 133]

plt.figure(0)
for idx, skill in enumerate(list(df.keys()[1:4])):
        plt.subplot(subplots_pos[idx])
        df_fsm = df[skill].value_counts()
        plt.pie(df_fsm, labels=df_fsm.index, startangle=90, autopct='%1.1f%%')
        plt.axis('equal')
        plt.title(skill)



plt.figure(1)
plt.pie(df['Skill Priority'].value_counts(), labels= df['Skill Priority'].value_counts().index, startangle=90,
        autopct='%1.1f%%')
plt.axis('equal')
plt.show()
