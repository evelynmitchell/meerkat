import rich

import meerkat as mk

IMAGE_COLUMN = "img"
EMBED_COLUMN = "img_clip"

rich.print(
    "[bold red]This script uses CLIP to embed images. "
    "This will take some time to download the model. "
    "Please be patient.[/bold red]"
)

df = mk.get("imagenette", version="160px")
# Download the precomupted CLIP embeddings for imagenette.
# You can also embed the images yourself with mk.embed. This will take some time.
# To embed: df = mk.embed(df, input=IMAGE_COLUMN, out_col=EMBED_COLUMN, encoder="clip").
df_clip = mk.DataFrame.read(
    "https://huggingface.co/datasets/meerkat-ml/meerkat-dataframes/resolve/main/embeddings/imagenette_160px.mk.tar.gz",  # noqa: E501
    overwrite=False,
)
df = df.merge(df_clip[["img_id", "img_clip"]], on="img_id")

match = mk.gui.Match(df=df, against=EMBED_COLUMN)

df = df.mark()
# Get the name of the match criterion in a reactive way.
with mk.magic():
    criterion_name = match.criterion.name

# Sort
df_sorted = mk.sort(data=df, by=criterion_name, ascending=False)

# Gallery
gallery = mk.gui.Gallery(df_sorted, main_column=IMAGE_COLUMN)

page = mk.gui.Page(
    component=mk.gui.html.flexcol([match, gallery]),
    id="match",
)
page.launch()
