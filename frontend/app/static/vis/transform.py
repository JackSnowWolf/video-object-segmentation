import csv
import pandas as pd
def trans(txtfile,csvfile):
    with open(txtfile, 'r') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split(",") for line in stripped if line)
        with open(csvfile, 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerow(('x1','y1','x2','y2','x3','y3'))
            writer.writerows(lines)

def read_col(csv_file):
    df = pd.read_csv(csvfile)
    x1 = df['x1']
    x2 = df['x2']
    x3 = df['x3']
    y1 = df['y1']
    y2 = df['y2']
    y3 = df['y3']
    x1 = x1.values.tolist()
    x2 = x2.values.tolist()
    x3 = x3.values.tolist()
    y1 = y1.values.tolist()
    y2 = y2.values.tolist()
    y3 = y3.values.tolist()
    print(x1)
    print(y1)
    print(x2)
    print(y2)
    print(x3)
    print(y3)


txtfile='car-turn.txt'
csvfile='car-turn.csv'
#trans(txtfile,csvfile)
read_col(csvfile)