import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('champions.csv')

plt.subplot(131)
df_fsm = df['First Skill Maxed'].value_counts()
plt.pie(df_fsm, labels=df_fsm.index, startangle=90, autopct='%1.1f%%')
plt.axis('equal')
plt.title('First Skill Maxed')

plt.subplot(132)
df_ssm = df['Second Skill Maxed'].value_counts()
plt.pie(df_ssm, labels=df_ssm.index, startangle=90, autopct='%1.1f%%')
plt.axis('equal')
plt.title('Second Skill Maxed')

plt.subplot(133)
df_tsm = df['Third Skill Maxed'].value_counts()
plt.pie(df_tsm, labels=df_tsm.index, startangle=90, autopct='%1.1f%%')
plt.axis('equal')
plt.title('Third Skill Maxed')

plt.show()
plt.pie(df['Skill Priority'].value_counts(), labels= df['Skill Priority'].value_counts().index, startangle=90,
        autopct='%1.1f%%')
plt.show()
