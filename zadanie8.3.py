import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("fatal-police-shootings-data.csv")
df_population = pd.read_excel("Dane dotyczące populacji w poszczególnych stanach USA.xlsx")
df_states = pd.read_excel("Dane dotyczące skrotów poszczególnych stanów.xlsx")

mental_illness_pivot = pd.pivot_table(
    df,
    values='id',
    index='race',
    columns='signs_of_mental_illness',
    aggfunc='count',
    fill_value=0
)

mental_illness_pivot['mental_illness_percentage'] = mental_illness_pivot.apply(
    lambda row: (row[True] / row.sum()) * 100 if row.sum() > 0 else 0,
    axis=1
)

max_race = mental_illness_pivot['mental_illness_percentage'].idxmax()
max_percentage = mental_illness_pivot['mental_illness_percentage'].max()
print(f"\nRasa z najwyższym odsetkiem oznak choroby psychicznej: {max_race} ({max_percentage:.2f}%)")

df['date'] = pd.to_datetime(df['date'])
df['weekday'] = df['date'].dt.day_name()

days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
interventions_by_day = df['weekday'].value_counts().reindex(days_order)

plt.figure(figsize=(10, 6))
interventions_by_day.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title("Liczba śmiertelnych interwencji policji w USA wg dnia tygodnia")
plt.xlabel("Dzień tygodnia")
plt.ylabel("Liczba interwencji")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("interwencje_dzien_tygodnia.png")
plt.show()

mental_illness_pivot.to_csv("zestawienie_rasa_choroba_psychiczna.csv", encoding="utf-8-sig")

print("\nKolumny w df_states:", df_states.columns.tolist())
print("Kolumny w df_population:", df_population.columns.tolist())

df_population = df_population[['State', 'Census population, April 1, 2020']]
df_population.columns = ['State', 'Population'] 

full_name_col = df_states.columns[0] 
abbrev_col = [col for col in df_states.columns if 'USPS' in str(col)][0]

df_states = df_states[[full_name_col, abbrev_col]]
df_states.columns = ['State', 'Abbreviation']

shootings_by_state = df['state'].value_counts().reset_index()
shootings_by_state.columns = ['Abbreviation', 'Shootings']


state_info = pd.merge(df_states, df_population, on='State')

merged = pd.merge(shootings_by_state, state_info, on='Abbreviation')

merged['Shootings_per_1000'] = (merged['Shootings'] / merged['Population']) * 1000

merged_sorted = merged.sort_values(by='Shootings_per_1000', ascending=False)
merged_sorted.to_csv("interwencje_na_1000_mieszkancow.csv", index=False, encoding="utf-8-sig")

print("\nTop 10 stanów wg liczby interwencji na 1000 mieszkańców:")
print(merged_sorted[['State', 'Shootings', 'Population', 'Shootings_per_1000']].head(10))

