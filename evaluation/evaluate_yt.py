import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score

def print_precision_recall(truth: pd.Series, pred: pd.Series, title: str):
    text = (
        f"** {title}: "
        f"precision={precision_score(truth, pred, zero_division=0):.2f} "
        f"recall={recall_score(truth, pred, zero_division=0):.2f} "
        f"f1-score={f1_score(truth, pred, zero_division=0):.2f}"
    )

    print(text)

def get_border_data(truth_df: pd.DataFrame, pred_df: pd.DataFrame) -> pd.DataFrame:
    result = pd.DataFrame(
        columns=["truth", "predict"],
        dtype=np.int8,
    )

    df = pd.DataFrame(
        {
            "truth": truth_df["border"],
            "predict": pred_df["border"],
            "height": pred_df["height"],
        }
    )

    for _, row in df.iterrows():
        
        truth_borders = (
            sorted(int(border) for border in row["truth"].split("_"))
            if row["truth"]
            else []
        )
        pred_borders = (
            sorted(int(border) for border in row["predict"].split("_"))
            if row["predict"]
            else []
        )

        for border in pred_borders:
            match = [x for x in truth_borders if abs(x - border) / row["height"] < 0.05]

            if not match:
                new_df = pd.DataFrame({"truth": [0], "predict": [1]})
                result = pd.concat([result, new_df], ignore_index=True)
            else:
                new_df = pd.DataFrame({"truth": [1], "predict": [1]})
                result = pd.concat([result, new_df], ignore_index=True)
                truth_borders.remove(match[0])

        for _ in truth_borders:
            new_df = pd.DataFrame({"truth": [1], "predict": [0]})
            result = pd.concat([result, new_df], ignore_index=True)

    return result


def main() -> None:
    truth_df = pd.read_csv("./corrected.csv")
    truth_df[["image", "border", "code_id"]] = (
        truth_df[["image", "border", "code_id"]].replace(np.nan, "").astype(str)
    )
    pred_df = pd.read_csv("./prediction.csv")
    pred_df[["image", "border"]] = (
        pred_df[["image", "border"]].replace(np.nan, "").astype(str)
    )

    print(truth_df.shape)
    print(pred_df.shape)
    print(pred_df.tail())

    # Analyze 'media unit' 
    result = get_border_data(truth_df, pred_df)
    print_precision_recall(result["truth"], result["predict"], title="Border")

    # Analyze 'view comments'
    print_precision_recall(truth_df["comment"], pred_df["comment"], title="Comment")

    # Analyze 'video'
    print_precision_recall(truth_df["video"], pred_df["video"], title="Video")

    # Analyze 'shorts'
    print_precision_recall(truth_df["shorts"], pred_df["shorts"], title="Shorts")

    # Analyze 'action on video'
    print_precision_recall(
        truth_df["video_action"], pred_df["video_action"], title="Video Action"
    )


if __name__ == "__main__":
    main()
