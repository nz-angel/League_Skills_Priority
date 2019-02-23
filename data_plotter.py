import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('champions.csv')
coldic = {'Q': 'xkcd:bright blue',
          'W': 'xkcd:scarlet',
          'E': 'xkcd:apple green'}

coldic_2 = {'QWE': 'xkcd:denim blue',
            'QEW': 'xkcd:teal blue',
            'WEQ': 'xkcd:reddish',
            'WQE': 'xkcd:wine red',
            'EQW': 'xkcd:light forest green',
            'EWQ': 'xkcd:dark lime green'}

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
                          loc='bottom', cellLoc='center', colWidths=[0.25]*4)
        plt.title(skill, pad=-20)

# Plot showing how many champions use each of the six possible skill orders
plt.figure(1)
df_sp = df['Skill Priority'].value_counts()
plt.pie(df_sp, labels=df_sp.index, colors=[coldic_2[x] for x in df_sp.index], startangle=90, autopct='%1.1f%%')
plt.table(cellText=[list(df_sp.values)+[sum(df_sp.values)]],
          colLabels=list(df_sp.index)+['Total'],
          loc='bottom', cellLoc='center')
plt.axis('equal')
plt.title('Leveling priority')

# Plot what skill champions choose at level 1
plt.figure(2)
df_f = df['First Skill'].value_counts()
plt.pie(df_f, labels=df_f.index, startangle=90, colors=[coldic[x] for x in df_f.index], autopct='%1.1f%%')
plt.table(cellText=[list(df_f.values)+[sum(df_f.values)]],
          colLabels=list(df_f.index)+['Total'],
          loc='bottom', cellLoc='center')
plt.axis('equal')
plt.title('Skill chosen at level 1')

# Plot what skill is first maxed for each champion class
i = 3
for class_ in ['Controller', 'Fighter', 'Mage', 'Marksman', 'Slayer', 'Tank', 'Specialist']:
    plt.figure(i)
    df_g = df[df['Class'] == class_]['First Skill Maxed'].value_counts()
    plt.pie(df_g, labels=df_g.index, startangle=90, colors=[coldic[x] for x in df_g.index], autopct='%1.1f%%')
    plt.axis('equal')
    plt.title('Max priority for {}'.format(class_))
    i += 1

    plt.figure(i)
    df_g2 = df[df['Class'] == class_]['Skill Priority'].value_counts()
    plt.pie(df_g2, labels=df_g2.index, startangle=90, colors=[coldic_2[x] for x in df_g2.index], autopct='%1.1f%%')
    plt.axis('equal')
    plt.title('Skill maxing order for {}'.format(class_))
    i += 1

plt.show()

