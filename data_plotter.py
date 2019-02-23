import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import os

def plot_pie_chart(df_val_counts, title):
    global plt_number
    plt.figure(plt_number)
    if len(set(df_val_counts.index).intersection(['Q', 'W', 'E'])):
        color_dict = coldic
    else:
        color_dict = coldic_2
    plt.pie(df_val_counts, labels=df_val_counts.index, colors=[color_dict[x] for x in df_val_counts.index],
            startangle=90, autopct='%1.1f%%', pctdistance=0.85)
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    plt.axis('equal')
    plt.gca().add_artist(centre_circle)
    plt.title(title)
    plt.savefig('Charts/{}.png'.format(title), transparent=True)
    plt_number += 1


def plot_donut(data_frame, title):
    global plt_number
    df_fsm = data_frame['First Skill Maxed'].value_counts()
    df_lp = data_frame['Skill Priority'].value_counts()
    df_fsm.sort_index(inplace=True)
    df_lp.sort_index(inplace=True)
    plt.figure(plt_number)
    plt.pie(df_fsm, labels=df_fsm.index, colors=[coldic[x] for x in df_fsm.index],
            startangle=90, autopct='%1.1f%%', pctdistance=0.85)
    plt.pie(df_lp, labels=df_lp.index, colors=[coldic_2[x] for x in df_lp.index], radius=0.75, rotatelabels=45,
            startangle=90, autopct='%1.1f%%', pctdistance=0.85, labeldistance=0.35, textprops={'fontsize': 'small'})
    centre_circle = plt.Circle((0, 0), 0.5, fc='white')
    plt.axis('equal')
    plt.gca().add_artist(centre_circle)
    plt.title(title)
    plt.savefig('Charts/{}.png'.format(title), transparent=True)
    plt_number += 1


def complete_info(value_counts, year):
    for y in range(2009, year):
        if y not in value_counts:
            value_counts[y] = 0


def plot_stacked_bars(data_frame, criterion, title):
    global plt_number
    plt.figure(plt_number)
    year = datetime.datetime.now().year + 1
    ind = np.arange(year - 2009)
    df_e = data_frame[data_frame['First Skill Maxed'] == 'E'][criterion].value_counts()
    df_q = data_frame[data_frame['First Skill Maxed'] == 'Q'][criterion].value_counts()
    df_w = data_frame[data_frame['First Skill Maxed'] == 'W'][criterion].value_counts()

    complete_info(df_e, year)
    complete_info(df_q, year)
    complete_info(df_w, year)

    df_e.sort_index(inplace=True)
    df_q.sort_index(inplace=True)
    df_w.sort_index(inplace=True)

    e_vals = list(df_e.values)
    q_vals = list(df_q.values)
    p1 = plt.bar(ind, e_vals, color=coldic['E'], zorder=3)
    p2 = plt.bar(ind, list(df_q.values), bottom=e_vals, color=coldic['Q'], zorder=3)
    p3 = plt.bar(ind, list(df_w.values), bottom=[i + j for (i,j) in zip(e_vals, q_vals)], color=coldic['W'], zorder=3)
    plt.xticks(ind, np.arange(2009, year), rotation=45)
    plt.legend((p1[0], p2[0], p3[0]), ('E', 'Q', 'W'))
    plt.grid(axis='y', zorder=0, alpha=0.5)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.title(title)
    plt.savefig('Charts/{}.png'.format(title), transparent=True)
    plt_number += 1


def main():
    df = pd.read_csv('champions.csv')

    global coldic
    global coldic_2

    subclasses = {'Controller': ['Enchanter', 'Catcher'],
                  'Fighter': ['Diver', 'Juggernaut'],
                  'Mage': ['Burst', 'Battlemage', 'Artillery'],
                  'Slayer': ['Assassin', 'Skirmisher'],
                  'Tank': ['Vanguard', 'Warden']}

    if not os.path.exists('Charts'):
        os.mkdir('Charts')

    plt.rcParams.update({'figure.max_open_warning': 0})
    # General plot that shows how many champions max E, Q or W and the six possible skill-maxing sequences
    plot_donut(df, 'General skill priority')

    # Plot what skill champions choose at level 1
    df_f = df['First Skill'].value_counts()
    plot_pie_chart(df_f, 'Skill chosen at level 1')

    # Plot what skill is first maxed for each champion class
    for class_ in ['Controller', 'Fighter', 'Mage', 'Marksman', 'Slayer', 'Tank', 'Specialist']:
        df_g = df[df['Class'] == class_]
        plot_donut(df_g, 'Skill priority for {}'.format(class_))

        if class_ in subclasses.keys():
            for subclass in subclasses[class_]:
                df_g3 = df[df['Subclass'] == subclass]
                plot_donut(df_g3, 'Skill priority for {}'.format(subclass))

    # Bar plot of first skill maxed first according to champion release year
    plot_stacked_bars(df, 'Release Date', 'First skill maxed by champions according to year of release')

    # Bar plot of first skill maxed first according to champion release year or full VGU
    plot_stacked_bars(df, 'Release Date (VGU)', 'First skill maxed by champions according to year of release or VGU')


if __name__ == '__main__':
    plt_number = 0
    coldic = {'Q': '#75b4ea',
              'W': '#dd8585',
              'E': '#98dd85'}

    coldic_2 = {'QWE': '#9097f1',
                'QEW': '#75d0ea',
                'WEQ': '#e6e385',
                'WQE': '#ddb385',
                'EQW': '#a7eb95',
                'EWQ': '#c1dd85'}

    main()

