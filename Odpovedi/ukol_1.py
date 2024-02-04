# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt

data_github = "https://raw.githubusercontent.com/gerdant/prakticky_test_Repromeda/main/Data/transfery.csv"
data = pd.read_csv(data_github)
pd.set_option('display.max_columns', None)

#A
data['vek_mother'] = pd.to_numeric(data['vek_mother'], errors='coerce')
bins = [0, 30, 35, 40, np.inf]
age_categories = ['do 29', '30-34', '35-39', '40+']
age_category_series = pd.cut(data['vek_mother'], bins=bins, labels=age_categories, right=False)

age_groups = data.groupby(age_category_series)['clinical_gravidity'].mean().reset_index()
age_groups = age_groups.dropna()
age_groups['clinical_gravidity'] = age_groups['clinical_gravidity'] * 100
age_groups['clinical_gravidity'] = age_groups['clinical_gravidity'].round(2)
age_groups['clinical_gravidity'] = age_groups['clinical_gravidity'].astype(str) + '%'
tabulka_1 = age_groups.rename(columns={'vek_mother': 'všechny věkové kategorie', 'clinical_gravidity': 'x%'})
print(tabulka_1.T)


#B
data_cleaned = data.dropna(subset=['vek_mother', 'clinical_gravidity'])
X = sm.add_constant(data_cleaned['vek_mother'])
y = data_cleaned['clinical_gravidity']
model = sm.Logit(y, X)
result = model.fit()
print(result.summary())
if result.pvalues['vek_mother'] <= 0.05:
    print("Mother's age is statistically significant for the success of the transfer.")
else:
    print("Mother's age is not statistically significant for the success of the transfer.")



#C1
data['vek_embryo'] = pd.to_numeric(data['vek_embryo'], errors='coerce')
no_donor_data = data[data['f_donor'] != 1]
age_category_embryo = pd.cut(no_donor_data['vek_embryo'], bins=bins, labels=age_categories, right=False)
age_groups_em = no_donor_data.groupby(age_category_embryo)['clinical_gravidity'].mean().reset_index()
age_groups_em = age_groups_em.dropna()
age_groups_em['clinical_gravidity'] = age_groups_em['clinical_gravidity'] * 100
age_groups_em['clinical_gravidity'] = age_groups_em['clinical_gravidity'].round(2)
age_groups_em['clinical_gravidity'] = age_groups_em['clinical_gravidity'].astype(str) + '%'
tabulka_2 = age_groups_em.rename(columns={'vek_embryo': 'všechny věkové kategorie', 'clinical_gravidity': 'x%'})
print(tabulka_2.T)

#C2
data_embryo_cleaned = no_donor_data.dropna(subset=['vek_embryo', 'clinical_gravidity'])
X = sm.add_constant(data_embryo_cleaned['vek_embryo'])
y = data_embryo_cleaned['clinical_gravidity']
model = sm.Logit(y, X)
result = model.fit()
print(result.summary())
if result.pvalues['vek_embryo'] <= 0.05:
    print("Embryo's age is statistically significant for the success of the transfer.")
else:
    print("Embryo's age is not statistically significant for the success of the transfer.")



#D
def gen_metody(genetic_method):
    if genetic_method == 'PGT-A':
        return 'PGT-A'
    elif genetic_method == 'PGT-SR':
        return 'PGT-SR'
    elif genetic_method == 'Karyomapping':
        return 'Karyomapping'
    elif genetic_method == 'OneGene':
        return 'OneGene'
    elif pd.isna(genetic_method):  # Handle missing values
        return 'bez genetické metody'
    else:
        return 'ostatní'

# Appling the above function to the 'genetic_method' column
data['method_category'] = data['genetic_method'].apply(gen_metody)
# Creating a table with value counts for each category
vysledky = pd.DataFrame(data['method_category'].value_counts())
vysledky.columns = ['počet']
print(vysledky.T)

#E
contingency_table = pd.crosstab(data['sex'], data['clinical_gravidity'])
#here I am only interested in chi2 and p values, therefore I add an underscore to the 3rd and 4th values
chi2, p, _, _ = chi2_contingency(contingency_table)
print("Chi-squared statistic:", chi2)
print("P-value:", p)

if p < 0.05:
    print("Pohlaví embrya je statisticky významné na úspěch klinické gravidity.")
else:
    print("Pohlaví embrya není statisticky významné na úspěch klinické gravidity.")

#F
#plot A
age_groups = age_groups.sort_values(by='clinical_gravidity')
plt.bar(age_groups['vek_mother'], age_groups['clinical_gravidity'], color='gray')
plt.xlabel('všechny věkové kategorie')
plt.ylabel('x%')
plt.title('Úspěšnosti embryotransferu dle věku matky')
plt.savefig(r'C:\Users\irina\OneDrive\Documents\Programming\Prakticky ukol\plot_A.png')
plt.show()

#plot D
plt.figure(figsize=(8, 6))
vysledky.plot(kind='bar', color='skyblue', legend=False)
plt.xlabel('Method Category')
plt.ylabel('Count')
plt.title('Distribution of Genetic Methods')
for i, value in enumerate(vysledky['počet']):
    plt.text(i, value + 1, str(value), ha='center', va='bottom')
plt.savefig(r'C:\Users\irina\OneDrive\Documents\Programming\Prakticky ukol\plot_D.png')
plt.show()

