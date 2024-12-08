import os
import statistics

import cv2
import numpy as np
import pandas as pd
import rembg

input_dir = "input"
matte_dir = "matte"
csv_path = "data_out.csv"

# TODO toml?

data_in = pd.read_csv("data_in.csv", dtype={"name": str}, skipinitialspace=True)


def generate_mattes(df):
    print("\nGenerating mattes...")

    model_name = "birefnet-general"  # good quality, but slow
    session = rembg.new_session(model_name)

    # TODO spawn rembg session only when there are unprocessed images

    for index, row in df.iterrows():
        subject_name = row["name"]
        subdir = os.path.join(input_dir, subject_name)

        for img_name in os.listdir(subdir):

            out_subject_path = os.path.join(matte_dir, subject_name)
            if not os.path.exists(out_subject_path):
                os.makedirs(out_subject_path)
            out_img_path = os.path.join(out_subject_path, img_name)

            if os.path.isfile(out_img_path):
                continue

            input_path = os.path.join(subdir, img_name)
            img_in = cv2.imread(input_path)
            matte = rembg.remove(img_in, session=session, only_mask=True)
            cv2.imwrite(out_img_path, matte)
            print(f"{os.path.join(subject_name, img_name)}")

    print("All inputs processed.")


def generate_areas(df):
    print("\nCalculating areas...")

    for index, row in df.iterrows():
        subject_name = row["name"]
        subdir = os.path.join(matte_dir, subject_name)

        m2_to_px2_ratio = 1 / row["calib"] ** 2
        areas = []

        for img_name in os.listdir(subdir):
            matte_img_path = os.path.join(subdir, img_name)
            matte = cv2.imread(matte_img_path, cv2.IMREAD_UNCHANGED)
            px_count = np.sum(matte / 255)
            area_m = px_count * m2_to_px2_ratio
            areas.append(area_m)

        area = statistics.mean(areas)
        df.at[index, "area"] = area
        print(f"Subject {subject_name}: {area:.3f} m^2")

    df = df.drop(columns=['calib'])
    return df


generate_mattes(data_in)

data_out = generate_areas(data_in)

data_out.to_csv(csv_path, index=False, header=True)
print("\nData saved.\n")
