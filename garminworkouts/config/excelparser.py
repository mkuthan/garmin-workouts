import numpy as np
import pandas as pd


def excel_to_yaml(filename, seconds_block=10):  # noqa: C901
    df = pd.read_excel(filename)
    df = df[df.columns.tolist()[:3]]
    df.columns = ["start", "end", "duration"]
    df.reset_index(inplace=True, drop=True)

    def normalise(x):
        if str(x) == str(np.nan):
            return x
        elif "W" in str(x):
            x = str(x).replace("W", "").replace(" ", "").replace(",", ".")
            x = float(x)
            return x
        else:
            x = float(x)
            return x

    def check_power_type(x):
        if "W" in str(x):
            return "W"
        else:
            return ""

    df["power_type"] = df["start"].apply(lambda x: check_power_type(x))

    df["start"] = df["start"].apply(lambda x: normalise(x))
    df["end"] = df["end"].apply(lambda x: normalise(x))
    df["duration"] = df["duration"].astype(str)

    def check_n_steps(df, seconds_block=seconds_block):
        if str(df["end"]) == str(np.nan):
            return 1
        elif df["start"] == df["end"]:
            return 1
        elif df["start"] != df["end"]:
            duration = df["duration"]
            seconds = int(duration.split(":")[-1]) + int(duration.split(":")[-2]) * 60
            n_blocks = seconds / seconds_block
            n_blocks = round(n_blocks, 0)
            return n_blocks

    df["n_blocks"] = df.apply(check_n_steps, axis=1)

    total_steps = df["n_blocks"].sum()

    if total_steps > 50:
        one_steps = len(total_steps[total_steps["n_blocks"] == 1])
        more_than_one_step = total_steps - one_steps

        # one_steps + more_than_one_steps <= 50

        max_more_than_one = 50 - one_steps
        perc = max_more_than_one / more_than_one_step

        df["n_blocks"] = df["n_blocks"].apply(lambda x: int(x * perc))

    workout_name = filename.replace("_", " ").split(".xls")[0].split("/")[-1]
    workout_name = 'name: "{}"\n'.format(workout_name)

    def create_steps(i, df=df):
        start = df.loc[i, "start"]
        end = df.loc[i, "end"]
        duration = df.loc[i, "duration"]
        n_blocks = df.loc[i, "n_blocks"]
        power_type = df.loc[i, "power_type"]
        if n_blocks == 1:
            template = '  - {{ power: {power}{power_type}, duration: "{duration}" }}\n'
            return template.format(power=int(start), power_type=power_type, duration=duration)
        elif n_blocks > 1:
            seconds = int(duration.split(":")[-1]) + int(duration.split(":")[-2]) * 60
            # n_blocks=seconds/seconds_block
            seconds_block = int(seconds / n_blocks)
            minutes_ = int(seconds_block / 60)
            seconds_ = int((float(seconds_block / 60) - int(seconds_block / 60)) * 60)
            duration = "{minutes}:{seconds}".format(minutes=minutes_, seconds=seconds_)
            power_dif = abs(end - start)
            power_step = power_dif / n_blocks
            steps_text = ""
            total_time = 0
            while total_time <= seconds:
                text = '  - {{ power: {0}{1}, duration: "{2}" }}\n'.format(int(start), power_type, duration)
                steps_text = steps_text + text
                if start <= end:
                    start = start + power_step
                elif start >= end:
                    start = start - power_step
                total_time = total_time + seconds_block
            return steps_text

    steps = "steps:\n"
    for i in df.index.tolist():
        step = create_steps(i)
        steps = steps + step

    yaml_text = '{workout_name}\n{steps}'.format(workout_name=workout_name, steps=steps)

    filename = filename.split(".xls")[0] + ".yaml"
    with open(filename, "w") as fout:
        fout.write(yaml_text)
    return filename
