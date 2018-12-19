import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('champions.csv')
coldic = {'Q': 'xkcd:bright blue', 'W': 'xkcd:scarlet', 'E': 'xkcd:apple green'}

# General plot comparing what skills are maxed first, second and third
subplots_pos = [131, 132, 133]
plt.figure(0)
for idx, skill in enumerate(list(df.keys()[1:4])):
        plt.subplot(subplots_pos[idx])
        df_fsm = df[skill].value_counts()
        plt.pie(df_fsm, labels=df_fsm.index, colors=[coldic[x] for x in df_fsm.index], startangle=90, autopct='%1.1f%%')
        plt.axis('equal')
        table = plt.table(cellText=[list(df_fsm.values)+[sum(df_fsm.values)]],
                          colLabels=list(df_fsm.index)+['Total'],
                          rowLabels=['Champions'],
                          loc='bottom', cellLoc='center', colWidths=[0.25]*4)
        # for key, cell in table.get_celld().items():
        #         cell.set_linewidth(0)
        plt.title(skill, pad=-20)

# Plot showing what is the second skill maxed in the case of champions who max Q first
plt.figure(1)
df_ssm = df[df['First Skill Maxed'] == 'Q']['Second Skill Maxed'].value_counts()
plt.pie(df_ssm, labels=df_ssm.index, colors=[coldic[x] for x in df_ssm.index], startangle=90, autopct='%1.1f%%')
plt.table(cellText=[list(df_ssm.values)+[sum(df_ssm.values)]],
          colLabels=list(df_ssm.index)+['Total'],
          loc='bottom', cellLoc='center')
plt.axis('equal')
plt.title('Skill maxed after maxing Q')

# Plot showing how many champions use each of the six possible skill orders
plt.figure(2)
df_sp = df['Skill Priority'].value_counts()
plt.pie(df_sp, labels=df_sp.index, startangle=90, autopct='%1.1f%%')
plt.table(cellText=[list(df_sp.values)+[sum(df_sp.values)]],
          colLabels=list(df_sp.index)+['Total'],
          loc='bottom', cellLoc='center')
plt.axis('equal')
plt.title('Skill-leveling priority')

# Plot what skill champions choose at level 1
plt.figure(3)
df_f = df['First Skill'].value_counts()
plt.pie(df_f, labels=df_f.index, startangle=90, colors=[coldic[x] for x in df_f.index], autopct='%1.1f%%')
plt.table(cellText=[list(df_f.values)+[sum(df_f.values)]],
          colLabels=list(df_f.index)+['Total'],
          loc='bottom', cellLoc='center')
plt.axis('equal')
plt.title('Skill chosen at level 1')

plt.show()
