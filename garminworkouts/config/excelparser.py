import pandas as pd
import numpy as np

def excel_to_yaml(filename,ftp):

    df=pd.read_excel(filename)
    df=df[df.columns.tolist()[:3]]
    df.columns=["start","end","duration"]
    df.reset_index(inplace=True, drop=True)

    def Normalise(x,ftp=ftp):
        if str(x) == str(np.nan):
            return x
        elif "%" in str(x):
            x=str(x).replace("%","").replace(" ","").replace(",",".")
            x=float(x)
            return x
        else:
            x=float(x)/float(ftp)*100
            x=float(x)
            return x

    df["start"]=df["start"].apply(lambda x: Normalise(x) )
    df["end"]=df["end"].apply(lambda x: Normalise(x) )
    df["duration"]=df["duration"].astype(str)

    workout_name=filename.replace("_"," ").split(".xls")[0].split("/")[-1]
    workout_name='name: "{}"\n'.format(workout_name)

    def create_steps(i,df=df,seconds_block=10):
        start=df.loc[i,"start"]
        end=df.loc[i,"end"]
        duration=df.loc[i,"duration"]
        if str(end) == str(np.nan):
            return '  - {{ power: {power}, duration: "{duration}" }}\n'.format(power=round(start,2), duration=duration)
        else:
            if start == end:
                return '  - {{ power: {power}, duration: "{duration}" }}\n'.format(power=round(start,2), duration=duration)
            elif start != end:
                seconds=int(duration.split(":")[-1])+int(duration.split(":")[-2])*60
                n_blocks=seconds/seconds_block
                power_dif=abs(end - start)
                power_step=power_dif/n_blocks            
                steps_text=""
                total_time=0
                while total_time <= seconds:
                    text='  - {{ power: {0}, duration: "00:10" }}\n'.format(round(start,2))
                    steps_text=steps_text+text
                    if start <= end:
                        start=start+power_step
                    elif start >= end:
                        start=start-power_step
                    total_time=total_time+10
                return steps_text
            
    steps="steps:\n"
    for i in df.index.tolist():
        step=create_steps(i)
        steps=steps+step

    yaml_text='{workout_name}\n{steps}'.format(workout_name=workout_name,steps=steps)

    filename=filename.split(".xls")[0]+".yaml"
    with open(filename,"w") as fout:
        fout.write(yaml_text)
    return filename
    