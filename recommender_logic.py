from pathlib import Path
import pandas as pd, numpy as np, joblib
from sklearn.feature_extraction.text import (
    TfidfVectorizer,
    HashingVectorizer,
)
from collections import Counter
import chunkdot.cosine_similarity_top_k as cstk
import pickle

# New Preprocessed Dataset
md = pd.read_feather("./movies_final.feather")

feats = ["Genres", "Actors", "Keywords", "Name", "Director", "DescriptionLemma"]

combined_feats = ""
combined_feats += md["Genres"].apply(lambda x: " ".join(i for i in x) + " ") * 2
combined_feats += md["Keywords"].apply(lambda x: " ".join(i for i in x) + " ") * 4
combined_feats += md["Actors"].apply(
    lambda x: " ".join(i.replace(" ", "") for i in x) + " "
)
combined_feats += md["Name"].apply(lambda x: x.replace(" ", "") + " ") * 2
combined_feats += md["Director"].apply(lambda x: x.replace(" ", "") + " ") * 2
combined_feats += (md["DescriptionLemma"] + " ") * 7
# combined_feats+=md['Genres'].apply(lambda x:' '.join(i.replace(' ','') for i in x)+' ')*2
# combined_feats+=md['Keywords'].apply(lambda x:' '.join(i.replace(' ','') for i in x)+' ')*4

combined_vector = TfidfVectorizer(
    analyzer="word",
    dtype=np.float32,
).fit_transform(combined_feats)

combined_sim = cstk(combined_vector, top_k=21)


class model:
    indices = {
        title: [idx, poster]
        for title, idx, poster in zip(md["Name"], md.index, md["Poster"])
    }

    def get_recommendations(self, title, combined_sim=combined_sim):
        idx = self.indices[title][0]
        cs = combined_sim[idx]
        sorted_data = sorted(
            zip(cs.data, cs.indices), key=lambda x: x[0], reverse=True
        )[1:]
        ans_data = [i[1] for i in sorted_data]
        return md.loc[ans_data, ["Name", "Poster"]].itertuples(index=False, name=None)


genre_counts = Counter(
    [genre for genres_list in md["Genres"] for genre in genres_list if genre != ""]
)
genre_counts = {genre: count for genre, count in genre_counts.items() if count >= 100}

genredf = {}
# for genre in genre_counts.keys():
# md[md["Genres"].astype("str").str.contains(genre)]


def get_genre_movies(genre):
    if genre == "All":
        return tuple(
            md[["Name", "votewt"]].itertuples(
                index=False,
            )
        )
        # return md[["Name", "votewt"]].itertuples(index=False, name=None)
    # return tuple(
    #     md[md["Genres"].apply(lambda x: genre in x)][["Name", "votewt"]].iterrows()
    # )
    return tuple(
        md[md["Genres"].apply(lambda x: genre in x)][["Name", "votewt"]].itertuples(
            index=False
        )
    )


logics = {
    # "md": md,
    # 'combined_feats':combined_feats,
    "combined_vector": combined_vector,
    "combined_sim": combined_sim,
    "model": model(),
    "genre_counts": genre_counts,
    "get_genre_movies": get_genre_movies,
}

model_file = "model"
if not Path(model_file).exists():
    joblib.dump(logics, model_file, compress=0)
# joblib.dump(logics, model_file, compress=0)


# with open("data.pkl", "wb") as file:
#     pickle.dump(logics, file)
