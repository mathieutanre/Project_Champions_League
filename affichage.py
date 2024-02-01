import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Lire les données
df = pd.read_csv("match_schedule_test.csv")

# Créer un plot pour chaque journée
for day in df['Day'].unique():
    df_day = df[df['Day'] == day]
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Team1", y="Team2", data=df_day)
    plt.title(f"Matches for Day {day}")
    plt.xlabel("Team 1")
    plt.ylabel("Team 2")
    plt.show()pip

