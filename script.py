import pandas as pd
from matplotlib import pyplot as plt
import humanfriendly
from matplotlib.ticker import FuncFormatter
import ballpark
from matplotlib import rcParams

params = {
   'axes.labelsize': 18,
   'font.size': 18,
   'font.family': 'Times New Roman',
   'legend.fontsize': 16,
   'xtick.labelsize': 16,
   'ytick.labelsize': 16,
   'text.usetex': False,
   'figure.figsize': [9, 7]
   }

rcParams.update(params)
plt.axes(frameon=0)
# plt.grid()


# plt.figure(figsize=(20, 10))
ax = plt.gca()



langs = ['bn', 'en', 'hi', 'ur', 'ml', 'ta', 'te']
d = {}
df = None
for lang in langs:
    fname = '{}.csv'.format(lang)
    d[lang] = pd.read_csv(fname, parse_dates=['month'])
    d[lang].columns = ['year', lang]
    if df is None:
        df = d[lang]
    else:
        df = df.merge(d[lang], on='year')
        # df = pd.concat([df, d[lang][lang]], axis=0)

print(df["year"].dt.date)
# del df["en"]
print(df.head())
print(df.iloc[-1])

idxs = df["year"].dt.year >= 2008
df = df[idxs]

def formatter(value, pos):
    # print(value, pos)
    b = ballpark.ballpark
    multiplier = -1 if value < 0 else 1
    bpv = b(value * multiplier)
    sign = '-' if value < 0 else ''
    s = '{}{}'.format(sign, bpv)
    return s

formatter = FuncFormatter(formatter)
ax.yaxis.set_major_formatter(formatter)

# langs.remove('en')
for lang in langs:
    df.plot(kind='line', x='year', y=lang, ax=ax)

plt.ylabel('#(wikipedia-pages)')
ax.grid(b=True, axis='y', color="0.9", linestyle='-', linewidth=1,
        which='both')
plt.savefig('wiki-growth.pdf')
plt.show()
