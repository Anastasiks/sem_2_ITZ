import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go


np.random.seed(42)

n_rows = 700

data = {
    "brand": np.random.choice(
        ["BMW", "Audi", "Toyota", "Kia", "Ford"],
        n_rows
    ),

    "price_usd": np.random.normal(
        35000,
        10000,
        n_rows
    ).clip(10000, 90000),

    "engine_volume": np.random.choice(
        [1.4, 1.6, 2.0, 2.5, 3.0],
        n_rows
    ),

    "horsepower": np.random.randint(
        90,
        450,
        n_rows
    ),

    "rating": np.random.uniform(
        3.0,
        5.0,
        n_rows
    ),

    "fuel_type": np.random.choice(
        ["Petrol", "Diesel", "Hybrid"],
        n_rows
    )
}

df = pd.DataFrame(data)


df["brand"] = df["brand"].astype("category")
df["fuel_type"] = df["fuel_type"].astype("category")

print(df.info())
print(df.isna().sum())
print(df.duplicated().sum())


sns.set_theme(style="whitegrid")

fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1 HIST
sns.histplot(
    df["price_usd"],
    kde=True,
    color="skyblue",
    ax=axes[0, 0]
)

axes[0, 0].set_title("Распределение цен автомобилей")

# 2 SCATTER
sns.scatterplot(
    data=df,
    x="horsepower",
    y="price_usd",
    hue="brand",
    ax=axes[0, 1]
)

axes[0, 1].set_title("Мощность и цена")

# 3 BOXPLOT
sns.boxplot(
    data=df,
    x="brand",
    y="price_usd",
    hue="fuel_type",
    ax=axes[1, 0]
)

axes[1, 0].set_title("Цены по брендам")

# 4 HEATMAP
corr = df.select_dtypes(include=["number"]).corr()

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    ax=axes[1, 1]
)

axes[1, 1].set_title("Корреляции")

plt.tight_layout()
plt.show()


# 1 Scatter
fig1 = px.scatter(
    df,
    x="horsepower",
    y="price_usd",
    color="brand",
    title="Цена и мощность"
)

fig1.show()

# 2 Line
avg_price = df.groupby(
    "brand",
    observed=True
)["price_usd"].mean().reset_index()

fig2 = px.line(
    avg_price,
    x="brand",
    y="price_usd",
    markers=True,
    title="Средняя цена по брендам"
)

fig2.show()

# 3 Bar
fuel_count = df.groupby(
    ["brand", "fuel_type"],
    observed=True
).size().reset_index(name="count")

fig3 = px.bar(
    fuel_count,
    x="brand",
    y="count",
    color="fuel_type",
    barmode="group",
    title="Тип топлива"
)

fig3.show()

# 4 Heatmap
fig4 = px.imshow(
    corr,
    text_auto=True,
    title="Матрица корреляций"
)

fig4.show()

# 5 Dropdown
brands = sorted(df["brand"].unique())

fig_drop = go.Figure()

for brand in brands:

    brand_df = df[df["brand"] == brand]

    fig_drop.add_trace(
        go.Histogram(
            x=brand_df["price_usd"],
            name=brand,
            visible=True
        )
    )

buttons = []

buttons.append(
    dict(
        method="update",
        label="Все",
        args=[
            {"visible": [True] * len(brands)},
            {"title": "Все бренды"}
        ]
    )
)

for i, brand in enumerate(brands):

    visible = [False] * len(brands)
    visible[i] = True

    buttons.append(
        dict(
            method="update",
            label=brand,
            args=[
                {"visible": visible},
                {"title": f"Бренд: {brand}"}
            ]
        )
    )

fig_drop.update_layout(
    updatemenus=[
        dict(
            buttons=buttons,
            direction="down",
            x=1.1,
            y=1.1
        )
    ],
    title="Фильтрация цен по брендам"
)

fig_drop.show()
print(df.info())