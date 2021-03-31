#%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# %%
#All files downloaded from social explorer, the txt file associated with each file is the data dictionary provided by social explorer.
us_tracts = pd.read_csv('../data/R12789222_SL140.csv')
us_counties = pd.read_csv('../data/R12789106_SL050.csv')

# %%
#column lables from social explorer file R12782267.txt
total_over65_cols = ['ACS19_5yr_B01001020', 'ACS19_5yr_B01001021', 'ACS19_5yr_B01001022', 'ACS19_5yr_B01001023', 'ACS19_5yr_B01001024', 'ACS19_5yr_B01001025']
total_over65_white_cols = ['ACS19_5yr_B01001A014', 'ACS19_5yr_B01001A015' ,'ACS19_5yr_B01001A016', 'ACS19_5yr_B01001A029', 'ACS19_5yr_B01001A030' ,'ACS19_5yr_B01001A031']
total_over65_hispanic_cols = ['ACS19_5yr_B01001I014', 'ACS19_5yr_B01001I015', 'ACS19_5yr_B01001I016', 'ACS19_5yr_B01001I029', 'ACS19_5yr_B01001I030', 'ACS19_5yr_B01001I031']
total_over65_black_cols =  ['ACS19_5yr_B01001B014', 'ACS19_5yr_B01001B015', 'ACS19_5yr_B01001B016', 'ACS19_5yr_B01001B029', 'ACS19_5yr_B01001B030', 'ACS19_5yr_B01001B031']
total_over65_asian_cols =  ['ACS19_5yr_B01001D014', 'ACS19_5yr_B01001D015', 'ACS19_5yr_B01001D016', 'ACS19_5yr_B01001D029', 'ACS19_5yr_B01001D030', 'ACS19_5yr_B01001D031']
total_over65_pi_cols =  ['ACS19_5yr_B01001E014', 'ACS19_5yr_B01001E015', 'ACS19_5yr_B01001E016', 'ACS19_5yr_B01001E029', 'ACS19_5yr_B01001E030', 'ACS19_5yr_B01001E031']
total_over65_aian_cols =  ['ACS19_5yr_B01001C014', 'ACS19_5yr_B01001C015', 'ACS19_5yr_B01001C016', 'ACS19_5yr_B01001C029', 'ACS19_5yr_B01001C030', 'ACS19_5yr_B01001C031']

#%%

def create_composite_est_moe(a_column_list):
    a_moe_col_list = [i + 's' for i in a_column_list]
    estimates = us_tracts.loc[:,a_column_list].sum(axis=1)
    moes = us_tracts.loc[:,a_moe_col_list].mul(1.645, axis = 1).pow(2, axis=1).sum(axis=1).pow(0.5)
    return estimates, moes

total_pop = us_tracts.ACS19_5yr_B01001001
total_pop_moe = us_tracts.ACS19_5yr_B01001001s * 1.645

total_over65, total_over65_moe = create_composite_est_moe(total_over65_cols)
total_over65_white, total_white_over65_moe = create_composite_est_moe(total_over65_white_cols)
total_over65_hispanic, total_hispanic_over65_moe = create_composite_est_moe(total_over65_hispanic_cols)
total_over65_black, total_black_over65_moe = create_composite_est_moe(total_over65_black_cols)
total_over65_asian, total_asian_over65_moe = create_composite_est_moe(total_over65_asian_cols)
total_over65_nhpi, total_nhpi_over65_moe = create_composite_est_moe(total_over65_pi_cols)
total_over65_aian, total_aian_over65_moe = create_composite_est_moe(total_over65_aian_cols)

#%%
def se_to_moe_tract(a_column):
    moe_col = a_column + 's'
    est = us_tracts.loc[:,a_column]
    moes = us_tracts.loc[:,moe_col].mul(1.645)
    return est, moes

total_white, total_white_moe = se_to_moe_tract('ACS19_5yr_B02001002')
total_black, total_black_moe = se_to_moe_tract('ACS19_5yr_B02001003')
total_hisp, total_hisp_moe =  se_to_moe_tract('ACS19_5yr_B01001I001')
total_asian, total_asian_moe = se_to_moe_tract('ACS19_5yr_B02001005')
total_nhpi, total_nhpi_moe =  se_to_moe_tract('ACS19_5yr_B02001006')
total_aian, total_aian_moe =  se_to_moe_tract('ACS19_5yr_B02001004')

# %%
def make_scatterplot(estimate, moe, title:str, ptile = 0.99):
    sns.set_theme()
    baseplot = sns.scatterplot(x= estimate, y = moe, alpha = 0.3, palette='colorblind')
    plot_max = estimate.quantile(ptile)
    baseplot.set_xlim(0, plot_max)
    baseplot.set_ylim(0, plot_max)
    baseplot.axline((0, 0), slope=1, color="red")
    baseplot.axline((0, 0), slope=.5, color="yellow")
    baseplot.axline((0, 0), slope=.1, color="green")
    baseplot.set_title('Margin of Error and Estimate\n'+title+': All US Census Tracts 2019 ACS')
    return baseplot

# %%

plt.figure()
make_scatterplot(total_pop, total_pop_moe, title= 'Total Population').figure.savefig('total_pop.png', dpi = 300)
plt.figure()
make_scatterplot(total_white, total_white_moe, title= 'White Population').figure.savefig('white_pop.png', dpi = 300)
plt.figure()
make_scatterplot(total_black, total_black_moe, title= 'African-American Population').figure.savefig('black_pop.png', dpi = 300)
plt.figure()
make_scatterplot(total_hisp, total_hisp_moe, title= 'Hispanic Population').figure.savefig('hisp_pop.png', dpi = 300)
plt.figure()
make_scatterplot(total_asian, total_asian_moe, title= 'Asian Population', ptile = 0.999).figure.savefig('asian_pop.png', dpi = 300)
plt.figure()
make_scatterplot(total_nhpi, total_nhpi_moe, title= 'Native Hawaiian/Pacific Islander',ptile = 0.999).figure.savefig('nhpi_pop.png', dpi = 300)
plt.figure()
make_scatterplot(total_aian, total_aian_moe, title= 'American Indian/Alaska Native',ptile = 0.999).figure.savefig('aian_pop.png', dpi = 300)

# %%
def se_to_moe_county(a_column):
    moe_col = a_column + 's'
    est = us_counties.loc[:,a_column]
    moes = us_counties.loc[:,moe_col].mul(1.645)
    return est, moes

total_white_county, total_white_moe_county = se_to_moe_county('ACS19_5yr_B02001002')
total_black_county, total_black_moe_county = se_to_moe_county('ACS19_5yr_B02001003')
total_hisp_county, total_hisp_moe_county =  se_to_moe_county('ACS19_5yr_B01001I001')
total_asian_county, total_asian_moe_county = se_to_moe_county('ACS19_5yr_B02001005')
total_nhpi_county, total_nhpi_moe_county =  se_to_moe_county('ACS19_5yr_B02001006')
total_aian_county, total_aian_moe_county =  se_to_moe_county('ACS19_5yr_B02001004')

#%%
def make_scatterplot_county(estimate, moe, title:str, ptile = 0.99):
    sns.set_theme()
    baseplot = sns.scatterplot(x= estimate, y = moe, alpha = 0.3, palette='colorblind')
    plot_max = estimate.quantile(ptile)
    baseplot.set_xlim(0, plot_max)
    baseplot.set_ylim(0, plot_max)
    baseplot.axline((0, 0), slope=1, color="red")
    baseplot.axline((0, 0), slope=.5, color="yellow")
    baseplot.axline((0, 0), slope=.1, color="green")
    baseplot.set_title('Margin of Error and Estimate\n'+title+': All US Counties 2019 ACS 5-Year')
    return baseplot

# %%

plt.figure()
make_scatterplot_county(total_pop_county, total_pop_moe_county, title= 'Total Population').figure.savefig('total_pop_county.png', dpi = 300)
plt.figure()
make_scatterplot_county(total_white_county, total_white_moe_county, title= 'White Population').figure.savefig('white_pop_county.png', dpi = 300)
plt.figure()
make_scatterplot_county(total_black_county, total_black_moe_county, title= 'African-American Population').figure.savefig('black_pop_county.png', dpi = 300)
plt.figure()
make_scatterplot_county(total_hisp_county, total_hisp_moe_county, title= 'Hispanic Population').figure.savefig('hisp_pop_county.png', dpi = 300)
plt.figure()
make_scatterplot_county(total_asian_county, total_asian_moe_county, title= 'Asian Population', ptile = 0.999).figure.savefig('asian_pop_county.png', dpi = 300)
plt.figure()
make_scatterplot_county(total_nhpi_county, total_nhpi_moe_county, title= 'Native Hawaiian/Pacific Islander',ptile = 0.999).figure.savefig('nhpi_pop_county.png', dpi = 300)
plt.figure()
make_scatterplot_county(total_aian_county, total_aian_moe_county, title= 'American Indian/Alaska Native',ptile = 0.999).figure.savefig('aian_pop_county.png', dpi = 300)

#%%

def calculate_breaks(moe, est):
    estimate_moe_ratio = moe/est
    print(f'moe > 100% of estimate:  {round((sum(estimate_moe_ratio > 1)/len(estimate_moe_ratio)), 4) * 100}% of tracts')
    print(f'moe > 50% of estimate:  {round((sum(estimate_moe_ratio > .5)/len(estimate_moe_ratio)), 4) * 100}% of tracts')
    print(f'moe > 10% of estimate:  {round((sum(estimate_moe_ratio > .1)/len(estimate_moe_ratio)), 4) * 100}% of tracts')



calculate_breaks(total_pop_moe[total_pop > 0], total_pop[total_pop > 0])
calculate_breaks(total_hisp_moe, total_hisp)
calculate_breaks(total_hisp_moe[total_hisp > 0], total_hisp[total_hisp > 0])
calculate_breaks(total_black_moe[total_black > 0], total_black[total_black > 0])
calculate_breaks(total_asian_moe[total_asian > 0], total_asian[total_asian > 0])
calculate_breaks(total_nhpi_moe[total_nhpi > 0], total_nhpi[total_nhpi > 0])
calculate_breaks(total_aian_moe[total_aian > 0], total_aian[total_aian > 0])
calculate_breaks(total_aian_moe, total_aian)
calculate_breaks(total_hisp_moe_county, total_hisp_county)
# %%
msa_xwlk = pd.read_csv('../data/cbsa2fipsxw.csv', dtype=str)
us_tracts['st_cnty_code'] = us_tracts.Geo_GEOID.str.slice(7,12)
msa_xwlk['st_cnty_code'] = msa_xwlk['fipsstatecode']+msa_xwlk['fipscountycode']
us_tracts.st_cnty_code = us_tracts.st_cnty_code.astype(str)
msa_xwlk.st_cnty_code = msa_xwlk.st_cnty_code.astype(str)
us_tracts_msa = us_tracts.join(msa_xwlk, on = 'st_cnty_code')