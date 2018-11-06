import csv
import os

for f in os.listdir():
    if '.view.lkml' in f:
        with open(f, 'r', encoding='utf-8') as in_file:
            stripped = (line.strip('\n').strip('{').strip('}').strip('"') for line in in_file)
            lines = (line for line in stripped if line)

            pairs = []
            count = 0
            for l in lines:
                if 'dimension:' in l or 'measure:' in l or 'dimension_group:' in l:
                    pairs.append({'label': l.split(':')[1].strip(' ')})
                    count += 1
                elif 'description:' in l:
                    pairs[count-1].update({'value': l.replace('"','').split(':')[1].lstrip()})
                else:
                    pass
            newfilename = in_file.name.split('.',1)[0]+'.csv'
            with open(newfilename, 'w') as out_file:
                fieldnames = ['label','value']
                writer = csv.DictWriter(out_file, lineterminator='\n', fieldnames = fieldnames)
                writer.writeheader()
                writer.writerows(pairs)
                print('{} has been converted to {}.'.format(in_file.name, newfilename))
                out_file.close()
            in_file.close()
    else:
        pass